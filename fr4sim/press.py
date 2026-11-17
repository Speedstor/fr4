"""How hard the press has to push."""

from dataclasses import dataclass

LBF_PER_SHORT_TON = 2000.0
NEWTON_PER_LBF = 4.4482216


@dataclass(frozen=True)
class PressForce:
    lbf: float

    @property
    def short_tons(self) -> float:
        return self.lbf / LBF_PER_SHORT_TON

    @property
    def kilonewton(self) -> float:
        return self.lbf * NEWTON_PER_LBF / 1000.0


def press_force(width_in: float, length_in: float, pressure_psi: float) -> PressForce:
    """Force needed to put a given pressure on a panel."""
    return PressForce(width_in * length_in * pressure_psi)
