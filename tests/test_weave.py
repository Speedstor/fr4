import numpy as np
import pytest

from fr4sim.laminate import Laminate, Ply
from fr4sim.materials import STYLE_1080, STYLE_2116
from fr4sim.weave import (
    TracePair,
    glass_thickness_mm,
    skew_samples_ps_per_inch,
    skew_summary,
    yarn_profile,
)

ONE_PLY = Laminate(Ply(STYLE_1080, 0.62), 1)
FIVE_PLIES = Laminate(Ply(STYLE_2116, 0.50), 5)


def test_yarn_profile_is_one_at_the_centre_and_zero_in_the_gap():
    pitch, cover = 0.4, 0.5
    profile = yarn_profile(np.array([0.0, pitch / 2, pitch]), pitch, cover)
    assert profile == pytest.approx([1.0, 0.0, 1.0])


def test_the_weave_moves_glass_around_but_adds_none():
    style = STYLE_2116
    ply_glass = Ply(style, 0.5).glass_thickness_mm
    # A fine grid over a whole number of yarn pitches in both directions.
    x = np.linspace(0, 20 * style.fill_pitch_mm, 2000, endpoint=False)
    y = np.linspace(0, 20 * style.warp_pitch_mm, 2000, endpoint=False)
    glass = glass_thickness_mm(style, ply_glass, *np.meshgrid(x, y))
    assert glass.mean() == pytest.approx(ply_glass, rel=0.01)


def test_two_traces_in_the_same_place_have_no_skew():
    pair = TracePair(width_mm=0.13, spacing_mm=0.0)
    assert skew_samples_ps_per_inch(ONE_PLY, pair, trials=5).max() == 0.0


def test_turning_the_traces_removes_most_of_the_skew():
    along = skew_summary(ONE_PLY, TracePair(0.13, 0.5, angle_deg=0), trials=40)
    turned = skew_summary(ONE_PLY, TracePair(0.13, 0.5, angle_deg=10), trials=40)
    assert turned.worst < 0.1 * along.worst


def test_a_thick_board_with_a_wide_trace_hides_the_weave():
    thin = skew_summary(ONE_PLY, TracePair(0.13, 0.5), trials=40)
    thick = skew_summary(FIVE_PLIES, TracePair(1.2, 3.0), trials=40)
    assert thick.median < 0.2 * thin.median


def test_same_seed_gives_the_same_answer():
    pair = TracePair(0.13, 0.5)
    first = skew_samples_ps_per_inch(ONE_PLY, pair, trials=10, seed=1)
    again = skew_samples_ps_per_inch(ONE_PLY, pair, trials=10, seed=1)
    assert np.array_equal(first, again)
