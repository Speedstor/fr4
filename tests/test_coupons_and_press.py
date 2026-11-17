import pytest

from fr4sim.coupons import COUPON_A, COUPON_B
from fr4sim.laminate import Laminate, Ply
from fr4sim.microstrip import ring_resonance_ghz
from fr4sim.press import press_force


def test_coupon_a_design_numbers():
    """The figures the trail page quotes. If these move, update the page."""
    board = COUPON_A.laminate
    assert board.thickness_mm == pytest.approx(0.637, abs=0.001)
    assert COUPON_A.trace_width_mm == pytest.approx(1.25, abs=0.01)
    line = COUPON_A.line_on(board)
    assert line.impedance_ohm == pytest.approx(50.0, abs=0.05)
    ring = ring_resonance_ghz(COUPON_A.ring_circumference_mm, line.eps_eff)
    assert ring == pytest.approx(1.710, abs=0.002)


def test_resin_drift_moves_impedance_and_ring_the_expected_way():
    style = COUPON_A.laminate.ply.style
    lean = COUPON_A.line_on(Laminate(Ply(style, 0.45), 5))
    rich = COUPON_A.line_on(Laminate(Ply(style, 0.55), 5))
    # More resin: thicker board and lower Dk, so higher impedance, faster wave.
    assert rich.impedance_ohm > lean.impedance_ohm
    assert rich.eps_eff < lean.eps_eff


def test_coupon_b_is_one_thin_ply():
    assert COUPON_B.laminate.ply_count == 1
    assert COUPON_B.laminate.thickness_mm < 0.2
    assert COUPON_B.pair_at(5.0).angle_deg == 5.0


def test_press_force():
    force = press_force(6, 6, 300)
    assert force.lbf == 10800
    assert force.short_tons == pytest.approx(5.4)
    assert force.kilonewton == pytest.approx(48.0, abs=0.1)
