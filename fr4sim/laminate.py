"""A laminate: plies of glass cloth filled with resin.

The cloth fixes how much glass is in each ply. Whatever else is in the ply
is resin. So the resin content sets both the thickness and the dielectric
constant, and a thickness map of a panel is also a resin map.
"""

import math
from dataclasses import dataclass

from .materials import E_GLASS, EPOXY, Dielectric, GlassStyle


def mix_parallel(dk_a: float, dk_b: float, share_a: float) -> float:
    """Upper bound: the field runs along layers of the two materials."""
    return share_a * dk_a + (1 - share_a) * dk_b


def mix_series(dk_a: float, dk_b: float, share_a: float) -> float:
    """Lower bound: the field crosses the two materials one after the other."""
    return 1.0 / (share_a / dk_a + (1 - share_a) / dk_b)


def mix_log(dk_a: float, dk_b: float, share_a: float) -> float:
    """Lichtenecker's logarithmic rule. It sits between the two bounds."""
    return math.exp(share_a * math.log(dk_a) + (1 - share_a) * math.log(dk_b))


@dataclass(frozen=True)
class Ply:
    """One sheet of cloth with its resin, after pressing.

    resin_weight_fraction is the resin's share of the ply's weight,
    for example 0.50 for a ply that is half resin and half glass.
    """

    style: GlassStyle
    resin_weight_fraction: float
    glass: Dielectric = E_GLASS
    resin: Dielectric = EPOXY

    @property
    def glass_thickness_mm(self) -> float:
        """Thickness the glass would have as a solid sheet."""
        # g/m2 divided by g/cm3 gives micrometres.
        return self.style.areal_weight_g_m2 / self.glass.density_g_cm3 / 1000.0

    @property
    def resin_thickness_mm(self) -> float:
        """Thickness the resin would have as a solid sheet."""
        r = self.resin_weight_fraction
        resin_weight_g_m2 = self.style.areal_weight_g_m2 * r / (1 - r)
        return resin_weight_g_m2 / self.resin.density_g_cm3 / 1000.0

    @property
    def thickness_mm(self) -> float:
        return self.glass_thickness_mm + self.resin_thickness_mm

    @property
    def glass_volume_fraction(self) -> float:
        return self.glass_thickness_mm / self.thickness_mm


@dataclass(frozen=True)
class Laminate:
    """A stack of identical plies with no voids."""

    ply: Ply
    ply_count: int

    @property
    def thickness_mm(self) -> float:
        return self.ply_count * self.ply.thickness_mm

    @property
    def glass_thickness_mm(self) -> float:
        return self.ply_count * self.ply.glass_thickness_mm

    def _mix(self, rule) -> float:
        p = self.ply
        return rule(p.glass.dk, p.resin.dk, p.glass_volume_fraction)

    @property
    def dk(self) -> float:
        """Panel-average dielectric constant, by the logarithmic rule."""
        return self._mix(mix_log)

    @property
    def dk_upper(self) -> float:
        return self._mix(mix_parallel)

    @property
    def dk_lower(self) -> float:
        return self._mix(mix_series)
