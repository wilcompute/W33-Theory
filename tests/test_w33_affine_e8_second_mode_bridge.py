from __future__ import annotations

from exploration.w33_affine_e8_second_mode_bridge import build_summary


def test_affine_e8_second_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_second_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_first_two_excited_coefficients_are_exactly_8_and_44"] is True
    assert theorem["the_eta_minus_8_second_excited_coefficient_splits_exactly_as_corrected_spread_carrier_plus_bosonic_octet"] is True
    assert theorem["the_theta_e8_second_coefficient_is_exactly_2160"] is True
    assert theorem["the_affine_e8_second_coefficient_is_exactly_4124"] is True
    assert theorem["the_affine_e8_second_coefficient_splits_exactly_as_2160_plus_240_times_8_plus_36_plus_8"] is True
    assert theorem["the_recent_affine_modular_layer_therefore_meets_the_corrected_spread_geometry_and_bosonic_octet_already_at_q_squared"] is True

    assert packet["corrected_spread_carrier_36"] == 36
    assert packet["bosonic_octet_8"] == 8
    assert packet["root_octet_coupling_1920"] == 1920
