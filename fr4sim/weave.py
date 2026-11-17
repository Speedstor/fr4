"""The weave: why two neighbouring traces can see different material.

Glass has a higher dielectric constant than resin. A trace that runs
along a yarn sits over more glass than one that runs along a gap, so
its signal is slower. The difference in arrival time between the two
traces of a pair is the skew.

The model, in four steps:

1. Each yarn is a lens-shaped bundle of glass. Warp yarns run along x
   and fill yarns along y.
2. Plies are stacked with random sideways shifts against each other.
3. Under any point of a trace, glass and resin are stacked one above
   the other, so they mix by the series rule.
4. The trace averages what lies under its width. Its delay is the
   average along its length.

It leaves out the waviness of the yarns, voids, and the field that
spreads beyond the edges of the trace.
"""

from dataclasses import dataclass

import numpy as np

from .laminate import Laminate, mix_series
from .materials import MM_PER_INCH, GlassStyle
from .microstrip import C_MM_PER_NS, solve

POINTS_ALONG_TRACE = 600
POINTS_ACROSS_TRACE = 15


def yarn_profile(distance_mm: np.ndarray, pitch_mm: float, cover: float) -> np.ndarray:
    """Height of a lens-shaped yarn, from 0 at its edge to 1 at its centre.

    distance_mm is measured across the yarns. The pattern repeats every pitch.
    """
    half_width = cover * pitch_mm / 2
    from_centre = (distance_mm + pitch_mm / 2) % pitch_mm - pitch_mm / 2
    inside = np.abs(from_centre) < half_width
    lens = np.sqrt(np.clip(1 - (from_centre / half_width) ** 2, 0, 1))
    return np.where(inside, lens, 0.0)


def glass_thickness_mm(
    style: GlassStyle,
    ply_glass_mm: float,
    x_mm: np.ndarray,
    y_mm: np.ndarray,
    shift_xy_mm: tuple[float, float] = (0.0, 0.0),
) -> np.ndarray:
    """Thickness of glass in one ply at each point (x, y).

    The peak heights are chosen so that the average over the cloth equals
    ply_glass_mm: the model moves glass around, it never adds any.
    """
    lens_mean = style.yarn_cover * np.pi / 4  # mean of the profile over a pitch

    warp_glass = ply_glass_mm * style.warp_share_of_glass
    warp = (warp_glass / lens_mean) * yarn_profile(
        y_mm + shift_xy_mm[1], style.warp_pitch_mm, style.yarn_cover
    )

    fill_glass = ply_glass_mm - warp_glass
    fill = (fill_glass / lens_mean) * yarn_profile(
        x_mm + shift_xy_mm[0], style.fill_pitch_mm, style.yarn_cover
    )
    return warp + fill


def random_ply_shifts(
    laminate: Laminate, rng: np.random.Generator
) -> list[tuple[float, float]]:
    """One random sideways shift for each ply in the stack."""
    style = laminate.ply.style
    return [
        (rng.uniform(0, style.fill_pitch_mm), rng.uniform(0, style.warp_pitch_mm))
        for _ in range(laminate.ply_count)
    ]


def trace_delay_ps_per_inch(
    laminate: Laminate,
    width_mm: float,
    angle_deg: float,
    length_mm: float,
    lateral_offset_mm: float,
    ply_shifts_mm: list[tuple[float, float]],
) -> float:
    """Delay of one straight trace laid over the weave.

    angle_deg is the angle between the trace and the warp yarns.
    lateral_offset_mm slides the trace sideways.
    """
    ply = laminate.ply
    height = laminate.thickness_mm

    # A grid of points covering the trace: s along it, v across it.
    s, v = np.meshgrid(
        np.linspace(0, length_mm, POINTS_ALONG_TRACE),
        np.linspace(-width_mm / 2, width_mm / 2, POINTS_ACROSS_TRACE),
    )
    angle = np.radians(angle_deg)
    x = s * np.cos(angle) - (v + lateral_offset_mm) * np.sin(angle)
    y = s * np.sin(angle) + (v + lateral_offset_mm) * np.cos(angle)

    glass = np.zeros_like(x)
    for shift in ply_shifts_mm:
        glass += glass_thickness_mm(ply.style, ply.glass_thickness_mm, x, y, shift)
    glass = np.clip(glass, 0, 0.98 * height)  # yarns cannot outgrow the board

    # Glass and resin stacked under each point: series rule.
    dk_local = mix_series(ply.glass.dk, ply.resin.dk, glass / height)
    dk_under_trace = dk_local.mean(axis=0)  # average across the width

    # Share of the field in the board, taken from a uniform board of the
    # same make-up.
    filling = solve(width_mm, height, laminate.dk_lower).filling_factor
    eps_eff = 1 + filling * (dk_under_trace - 1)

    return float(np.sqrt(eps_eff).mean() * MM_PER_INCH / C_MM_PER_NS * 1000.0)


@dataclass(frozen=True)
class TracePair:
    """Two parallel traces, as in a differential pair."""

    width_mm: float
    spacing_mm: float  # centre to centre
    angle_deg: float = 0.0  # against the warp yarns
    length_mm: float = 50.0


@dataclass(frozen=True)
class SkewSummary:
    """Skew between the two traces, in picoseconds per inch of length."""

    median: float
    percentile_95: float
    worst: float


def skew_samples_ps_per_inch(
    laminate: Laminate,
    pair: TracePair,
    trials: int = 300,
    seed: int = 7,
) -> np.ndarray:
    """Skew of the pair, for many random placements on the weave.

    Each trial draws new ply shifts and a new position for the pair,
    because nobody controls where a trace lands on the cloth.
    """
    rng = np.random.default_rng(seed)
    style = laminate.ply.style
    samples = np.empty(trials)
    for i in range(trials):
        shifts = random_ply_shifts(laminate, rng)
        offset = rng.uniform(0, style.warp_pitch_mm)
        delays = [
            trace_delay_ps_per_inch(
                laminate, pair.width_mm, pair.angle_deg, pair.length_mm, o, shifts
            )
            for o in (offset, offset + pair.spacing_mm)
        ]
        samples[i] = abs(delays[0] - delays[1])
    return samples


def skew_summary(
    laminate: Laminate, pair: TracePair, trials: int = 300, seed: int = 7
) -> SkewSummary:
    samples = skew_samples_ps_per_inch(laminate, pair, trials, seed)
    return SkewSummary(
        median=float(np.median(samples)),
        percentile_95=float(np.percentile(samples, 95)),
        worst=float(samples.max()),
    )
