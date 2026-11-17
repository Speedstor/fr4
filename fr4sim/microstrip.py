"""Microstrip: a trace on top of the board with a ground plane underneath.

Closed-form formulas of Hammerstad and Jensen (1980). They are static,
so they ignore how the values creep with frequency. For the comparisons
this package makes, that is good enough.

Part of the field is in the board and part is in the air above the trace.
The wave therefore sees an "effective" dielectric constant, eps_eff,
between 1 and the board's own value.
"""

import math
from dataclasses import dataclass

C_MM_PER_NS = 299.792458  # speed of light
ETA_0 = 376.730313668  # impedance of free space, ohm
STANDARD_COPPER_MM = 0.035  # "one ounce" copper


@dataclass(frozen=True)
class Microstrip:
    """The solved line."""

    width_mm: float
    height_mm: float
    dk: float
    eps_eff: float
    impedance_ohm: float

    @property
    def filling_factor(self) -> float:
        """Share of the field that is in the board: 0 is all air, 1 all board."""
        return (self.eps_eff - 1) / (self.dk - 1)

    def delay_ps(self, length_mm: float) -> float:
        return delay_ps(length_mm, self.eps_eff)

    def phase_deg(self, length_mm: float, freq_ghz: float) -> float:
        return phase_deg(length_mm, self.eps_eff, freq_ghz)


def _impedance_in_air(u: float) -> float:
    """Impedance of a thin trace over ground with air as the dielectric.

    u is trace width divided by height above ground.
    """
    f = 6 + (2 * math.pi - 6) * math.exp(-((30.666 / u) ** 0.7528))
    return ETA_0 / (2 * math.pi) * math.log(f / u + math.sqrt(1 + (2 / u) ** 2))


def _eps_eff_thin(u: float, dk: float) -> float:
    """Effective dielectric constant for a trace of zero thickness."""
    a = (
        1
        + math.log((u**4 + (u / 52) ** 2) / (u**4 + 0.432)) / 49
        + math.log(1 + (u / 18.1) ** 3) / 18.7
    )
    b = 0.564 * ((dk - 0.9) / (dk + 3)) ** 0.053
    return (dk + 1) / 2 + (dk - 1) / 2 * (1 + 10 / u) ** (-a * b)


def solve(
    width_mm: float,
    height_mm: float,
    dk: float,
    copper_mm: float = STANDARD_COPPER_MM,
) -> Microstrip:
    """Effective dielectric constant and impedance of a microstrip line."""
    u = width_mm / height_mm
    t = copper_mm / height_mm

    # Thick copper acts like a slightly wider trace. The widening is larger
    # in air (u_air) than with the board present (u_board).
    if t > 0:
        coth = 1 / math.tanh(math.sqrt(6.517 * u))
        widening_air = t / math.pi * math.log(1 + 4 * math.e / (t * coth**2))
        widening_board = 0.5 * (1 + 1 / math.cosh(math.sqrt(dk - 1))) * widening_air
    else:
        widening_air = widening_board = 0.0
    u_air = u + widening_air
    u_board = u + widening_board

    z_board = _impedance_in_air(u_board)
    eps_thin = _eps_eff_thin(u_board, dk)
    impedance = z_board / math.sqrt(eps_thin)
    eps_eff = eps_thin * (_impedance_in_air(u_air) / z_board) ** 2
    return Microstrip(width_mm, height_mm, dk, eps_eff, impedance)


def width_for_impedance(
    target_ohm: float,
    height_mm: float,
    dk: float,
    copper_mm: float = STANDARD_COPPER_MM,
) -> float:
    """Trace width that gives the wanted impedance. Found by bisection."""
    narrow, wide = 0.05 * height_mm, 10 * height_mm
    for _ in range(60):
        middle = 0.5 * (narrow + wide)
        if solve(middle, height_mm, dk, copper_mm).impedance_ohm > target_ohm:
            narrow = middle  # too narrow: impedance still too high
        else:
            wide = middle
    return 0.5 * (narrow + wide)


def delay_ps(length_mm: float, eps_eff: float) -> float:
    """Time for a signal to travel the length of the line."""
    return length_mm * math.sqrt(eps_eff) / C_MM_PER_NS * 1000.0


def phase_deg(length_mm: float, eps_eff: float, freq_ghz: float) -> float:
    """Phase a signal turns through along the line."""
    return 360.0 * freq_ghz * delay_ps(length_mm, eps_eff) / 1000.0


def eps_eff_from_two_lengths(
    phase_difference_deg: float, length_difference_mm: float, freq_ghz: float
) -> float:
    """Recover eps_eff from two lines that differ only in length.

    Subtracting the two phases cancels the connectors and launches.
    """
    delay_ns = phase_difference_deg / 360.0 / freq_ghz
    return (delay_ns * C_MM_PER_NS / length_difference_mm) ** 2


def ring_resonance_ghz(circumference_mm: float, eps_eff: float, mode: int = 1) -> float:
    """A ring resonates where a whole number of wavelengths fits round it."""
    return mode * C_MM_PER_NS / (circumference_mm * math.sqrt(eps_eff))


def eps_eff_from_ring(circumference_mm: float, freq_ghz: float, mode: int = 1) -> float:
    """Recover eps_eff from a measured ring resonance."""
    return (mode * C_MM_PER_NS / (circumference_mm * freq_ghz)) ** 2
