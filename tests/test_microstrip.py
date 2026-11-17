import pytest

from fr4sim.microstrip import (
    delay_ps,
    eps_eff_from_ring,
    eps_eff_from_two_lengths,
    phase_deg,
    ring_resonance_ghz,
    solve,
    width_for_impedance,
)


def test_a_familiar_board_gives_about_fifty_ohms():
    # A 3 mm trace on 1.6 mm board of Dk 4.4 is the textbook 50 ohm line.
    line = solve(width_mm=3.0, height_mm=1.6, dk=4.4)
    assert 48 < line.impedance_ohm < 52
    assert 3.2 < line.eps_eff < 3.5


def test_eps_eff_lies_between_air_and_board():
    line = solve(1.0, 0.6, 4.1)
    assert 1 < line.eps_eff < 4.1
    assert 0 < line.filling_factor < 1


def test_wider_trace_has_lower_impedance():
    narrow = solve(0.5, 0.6, 4.1)
    wide = solve(2.0, 0.6, 4.1)
    assert wide.impedance_ohm < narrow.impedance_ohm


def test_width_for_impedance_round_trip():
    width = width_for_impedance(50, height_mm=0.6, dk=4.1)
    assert solve(width, 0.6, 4.1).impedance_ohm == pytest.approx(50, abs=0.01)


def test_two_length_method_recovers_eps_eff():
    eps_eff, freq = 3.1, 2.0
    difference = phase_deg(150, eps_eff, freq) - phase_deg(50, eps_eff, freq)
    assert eps_eff_from_two_lengths(difference, 100, freq) == pytest.approx(eps_eff)


def test_ring_round_trip_and_harmonics():
    first = ring_resonance_ghz(100, 3.1, mode=1)
    assert ring_resonance_ghz(100, 3.1, mode=3) == pytest.approx(3 * first)
    assert eps_eff_from_ring(100, first) == pytest.approx(3.1)


def test_delay_in_air_is_the_speed_of_light():
    assert delay_ps(299.792458, eps_eff=1.0) == pytest.approx(1000.0)
