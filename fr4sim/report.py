"""Print every prediction the documentation quotes.

Run it with:  python -m fr4sim

Each function below prints one table. Read main() first.
"""

from dataclasses import dataclass

from .coupons import COUPON_A, COUPON_B
from .laminate import Laminate, Ply
from .materials import STYLE_1080, STYLE_2116, STYLE_7628
from .microstrip import ring_resonance_ghz, solve
from .press import press_force
from .weave import TracePair, skew_summary

# One maker's figures, to show how far off the model is.
MAKER_DK = 4.49  # at 1 GHz, for a board that is 56% resin
MAKER_DK_RESIN = 0.56
MAKER_PLY_MM = 0.119  # one pressed ply of 2116 that is 52% resin
MAKER_PLY_RESIN = 0.52


def main() -> None:
    print("FR4 coupon model. Predictions only: nothing here has been measured.")
    print_resin_content_table()
    print_model_against_maker()
    print_coupon_a_design()
    print_coupon_a_resin_drift()
    print_coupon_a_sensitivity()
    print_weave_skew()
    print_press_force()


def heading(text: str) -> None:
    print()
    print(text)
    print("-" * len(text))


# ---------------------------------------------------------------------------
# 1. Resin content
# ---------------------------------------------------------------------------


def print_resin_content_table() -> None:
    heading("1. Panel dielectric constant against resin content (2116 cloth)")
    print("resin wt%   glass vol%   ply mm   Dk upper   Dk log   Dk lower")
    for resin in (0.40, 0.45, 0.50, 0.55, 0.60, 0.65):
        board = Laminate(Ply(STYLE_2116, resin), ply_count=1)
        glass_percent = board.ply.glass_volume_fraction * 100
        print(
            f"{resin * 100:9.0f}   {glass_percent:10.1f}   {board.thickness_mm:6.3f}"
            f"   {board.dk_upper:8.2f}   {board.dk:6.2f}   {board.dk_lower:8.2f}"
        )


def print_model_against_maker() -> None:
    board = Laminate(Ply(STYLE_2116, MAKER_DK_RESIN), ply_count=1)
    print(
        f"Check: a maker gives Dk {MAKER_DK} at {MAKER_DK_RESIN:.0%} resin."
        f" The model gives {board.dk:.2f}, so it reads low."
    )
    board = Laminate(Ply(STYLE_2116, MAKER_PLY_RESIN), ply_count=1)
    print(
        f"Check: a maker gives {MAKER_PLY_MM} mm per ply at {MAKER_PLY_RESIN:.0%}"
        f" resin. The model gives {board.thickness_mm:.3f} mm, so it reads thick."
    )


# ---------------------------------------------------------------------------
# 2. Coupon A: ring resonators across a thick panel
# ---------------------------------------------------------------------------


def print_coupon_a_design() -> None:
    heading("2. Coupon A: nine ring resonators on a thick two-layer panel")
    board = COUPON_A.laminate
    line = COUPON_A.line_on(board)
    print(
        f"Design: {board.ply_count} plies of {board.ply.style.name},"
        f" {board.thickness_mm:.3f} mm thick, Dk {board.dk:.2f}."
    )
    print(
        f"A {COUPON_A.target_impedance_ohm:.0f} ohm trace is"
        f" {COUPON_A.trace_width_mm:.2f} mm wide. eps_eff {line.eps_eff:.3f}."
    )


def print_coupon_a_resin_drift() -> None:
    """What the coupon reads where the panel has more or less resin."""
    design = COUPON_A.laminate
    ring_mm = COUPON_A.ring_circumference_mm
    print()
    print("If the resin content drifts across the panel:")
    print("resin wt%   thickness mm     Dk   impedance ohm   ring mode 1 GHz")
    for resin in (0.45, 0.50, 0.55):
        board = Laminate(Ply(design.ply.style, resin), design.ply_count)
        line = COUPON_A.line_on(board)
        ring_ghz = ring_resonance_ghz(ring_mm, line.eps_eff)
        print(
            f"{resin * 100:9.0f}   {board.thickness_mm:12.3f}   {board.dk:4.2f}"
            f"   {line.impedance_ohm:13.1f}   {ring_ghz:15.3f}"
        )


def print_coupon_a_sensitivity() -> None:
    """How far a small change in Dk moves the ring's resonances."""
    board = COUPON_A.laminate
    width = COUPON_A.trace_width_mm
    ring_mm = COUPON_A.ring_circumference_mm

    as_designed = solve(width, board.thickness_mm, board.dk)
    one_percent_up = solve(width, board.thickness_mm, board.dk * 1.01)

    print()
    print("How far a 1% rise in Dk moves each ring resonance:")
    for mode in (1, 2, 3):
        before = ring_resonance_ghz(ring_mm, as_designed.eps_eff, mode)
        after = ring_resonance_ghz(ring_mm, one_percent_up.eps_eff, mode)
        shift_mhz = (after - before) * 1000
        print(f"  mode {mode}: {before:.3f} GHz, moves {shift_mhz:+.1f} MHz")

    with_maker_dk = solve(width, board.thickness_mm, MAKER_DK)
    ring_ghz = ring_resonance_ghz(ring_mm, with_maker_dk.eps_eff)
    print(f"With the maker's Dk of {MAKER_DK}, mode 1 would be {ring_ghz:.3f} GHz.")


# ---------------------------------------------------------------------------
# 3. The weave
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class WeaveCase:
    """One board and one pair of traces to try on it."""

    name: str
    board: Laminate
    trace_width_mm: float
    spacing_mm: float


WEAVE_CASES = (
    WeaveCase("Coupon A board, wide trace", COUPON_A.laminate, 1.20, 3.0),
    WeaveCase(
        "Coupon B board, 1 ply of 2116",
        COUPON_B.laminate,
        COUPON_B.trace_width_mm,
        COUPON_B.spacing_mm,
    ),
    WeaveCase("1 ply of 1080", Laminate(Ply(STYLE_1080, 0.62), 1), 0.13, 0.5),
    WeaveCase("2 plies of 1080", Laminate(Ply(STYLE_1080, 0.62), 2), 0.28, 0.5),
    WeaveCase("1 ply of 7628", Laminate(Ply(STYLE_7628, 0.45), 1), 0.38, 0.5),
)
WEAVE_ANGLES_DEG = (0, 5, 10, 45)


def print_weave_skew() -> None:
    heading("3. Weave skew between two parallel traces, ps per inch")
    for case in WEAVE_CASES:
        print(
            f"{case.name}: {case.board.thickness_mm:.3f} mm thick,"
            f" trace {case.trace_width_mm} mm, spacing {case.spacing_mm} mm"
        )
        for angle in WEAVE_ANGLES_DEG:
            pair = TracePair(case.trace_width_mm, case.spacing_mm, angle)
            skew = skew_summary(case.board, pair)
            print(
                f"   {angle:2d} deg to the warp: median {skew.median:.2f},"
                f" 95th {skew.percentile_95:.2f}, worst {skew.worst:.2f}"
            )


# ---------------------------------------------------------------------------
# 4. The press
# ---------------------------------------------------------------------------


def print_press_force() -> None:
    heading("4. Press force")
    for side_in in (4, 6):
        for psi in (100, 300):
            force = press_force(side_in, side_in, psi)
            print(
                f"  {side_in} x {side_in} inch at {psi} psi:"
                f" {force.short_tons:.1f} short tons, {force.kilonewton:.0f} kN"
            )


if __name__ == "__main__":
    main()
