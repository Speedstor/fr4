"""Materials and glass cloth styles.

Every number the model assumes lives in this file, so there is one place
to read them and one place to change them.

Units used across the package: millimetres, gigahertz, picoseconds.
"""

from dataclasses import dataclass

MM_PER_INCH = 25.4


@dataclass(frozen=True)
class Dielectric:
    """An insulating material, described by the two numbers the model needs."""

    name: str
    dk: float  # dielectric constant (relative permittivity)
    density_g_cm3: float


# ASSUMED. The middle of the ranges found in the literature:
# glass about 6.2 to 6.6, epoxy resin about 3.0 to 3.6.
E_GLASS = Dielectric("E-glass", dk=6.4, density_g_cm3=2.55)
EPOXY = Dielectric("cured epoxy, no bromine", dk=3.3, density_g_cm3=1.20)


@dataclass(frozen=True)
class GlassStyle:
    """A plain-weave glass cloth.

    Warp yarns run along the length of the roll and fill yarns across it.
    Each of the styles below uses the same yarn in both directions.
    """

    name: str
    warp_ends_per_inch: float
    fill_ends_per_inch: float
    areal_weight_g_m2: float
    # GUESS. Width of a yarn divided by the distance between yarn centres.
    # 1.0 would be a closed cloth with no windows. Not from a data sheet.
    yarn_cover: float

    @property
    def warp_pitch_mm(self) -> float:
        """Distance between the centres of neighbouring warp yarns."""
        return MM_PER_INCH / self.warp_ends_per_inch

    @property
    def fill_pitch_mm(self) -> float:
        """Distance between the centres of neighbouring fill yarns."""
        return MM_PER_INCH / self.fill_ends_per_inch

    @property
    def warp_share_of_glass(self) -> float:
        """Share of the glass that is in the warp yarns."""
        return self.warp_ends_per_inch / (
            self.warp_ends_per_inch + self.fill_ends_per_inch
        )


# Thread counts and weights are from makers' tables.
# The weight of 106 and the fill count of 2116 are from memory.
STYLE_106 = GlassStyle("106", 56, 56, 24.4, yarn_cover=0.40)
STYLE_1080 = GlassStyle("1080", 60, 47, 48.0, yarn_cover=0.50)
STYLE_2116 = GlassStyle("2116", 60, 58, 104.0, yarn_cover=0.70)
STYLE_7628 = GlassStyle("7628", 44, 31, 204.0, yarn_cover=0.80)

STYLES = {s.name: s for s in (STYLE_106, STYLE_1080, STYLE_2116, STYLE_7628)}
