import pytest

from fr4sim.laminate import Laminate, Ply, mix_log, mix_parallel, mix_series
from fr4sim.materials import E_GLASS, EPOXY, STYLE_2116


def test_glass_thickness_comes_from_the_cloth_alone():
    thin = Ply(STYLE_2116, 0.40)
    fat = Ply(STYLE_2116, 0.65)
    assert thin.glass_thickness_mm == fat.glass_thickness_mm
    assert thin.glass_thickness_mm == pytest.approx(104.0 / 2.55 / 1000)


def test_half_resin_by_weight_gives_thicknesses_in_the_density_ratio():
    ply = Ply(STYLE_2116, 0.50)
    ratio = ply.resin_thickness_mm / ply.glass_thickness_mm
    assert ratio == pytest.approx(E_GLASS.density_g_cm3 / EPOXY.density_g_cm3)


def test_more_resin_means_thicker_and_lower_dk():
    lean = Laminate(Ply(STYLE_2116, 0.45), 5)
    rich = Laminate(Ply(STYLE_2116, 0.55), 5)
    assert rich.thickness_mm > lean.thickness_mm
    assert rich.dk < lean.dk


def test_mixing_rules_are_ordered_and_meet_at_the_ends():
    for share in (0.2, 0.5, 0.8):
        low = mix_series(6.4, 3.3, share)
        mid = mix_log(6.4, 3.3, share)
        high = mix_parallel(6.4, 3.3, share)
        assert low < mid < high
    for rule in (mix_series, mix_log, mix_parallel):
        assert rule(6.4, 3.3, 1.0) == pytest.approx(6.4)
        assert rule(6.4, 3.3, 0.0) == pytest.approx(3.3)


def test_laminate_dk_lies_between_resin_and_glass():
    board = Laminate(Ply(STYLE_2116, 0.50), 5)
    assert EPOXY.dk < board.dk_lower < board.dk < board.dk_upper < E_GLASS.dk
