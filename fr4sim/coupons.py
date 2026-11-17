"""The two test coupons, written down as data.

A coupon is a test pattern etched on a panel.

Coupon A asks: does the dielectric constant change across the panel?
Coupon B asks: does the weave make two neighbouring traces differ?
"""

from dataclasses import dataclass

from .laminate import Laminate, Ply
from .materials import STYLE_2116
from .microstrip import Microstrip, solve, width_for_impedance
from .weave import TracePair


@dataclass(frozen=True)
class RingCoupon:
    """Coupon A: ring resonators spread over a thick two-layer panel."""

    laminate: Laminate
    ring_circumference_mm: float = 100.0  # measured along the middle of the trace
    target_impedance_ohm: float = 50.0
    sites: int = 9  # a 3 by 3 grid

    @property
    def trace_width_mm(self) -> float:
        board = self.laminate
        return width_for_impedance(
            self.target_impedance_ohm, board.thickness_mm, board.dk
        )

    def line_on(self, board: Laminate) -> Microstrip:
        """The coupon's trace, etched at its designed width, on some board.

        Pass a board with a different resin content to see what a drift
        across the panel would do.
        """
        return solve(self.trace_width_mm, board.thickness_mm, board.dk)


@dataclass(frozen=True)
class WeaveCoupon:
    """Coupon B: pairs of narrow traces on one thin ply, at several angles."""

    laminate: Laminate
    trace_width_mm: float = 0.22
    spacing_mm: float = 0.50
    length_mm: float = 50.0
    angles_deg: tuple[float, ...] = (0.0, 5.0, 10.0)

    def pair_at(self, angle_deg: float) -> TracePair:
        return TracePair(
            self.trace_width_mm, self.spacing_mm, angle_deg, self.length_mm
        )


COUPON_A = RingCoupon(Laminate(Ply(STYLE_2116, resin_weight_fraction=0.50), 5))
COUPON_B = WeaveCoupon(Laminate(Ply(STYLE_2116, resin_weight_fraction=0.55), 1))
