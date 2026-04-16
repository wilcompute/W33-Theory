from __future__ import annotations

from exploration.w33_affine_e8_third_mode_bridge import build_summary


def test_affine_e8_third_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_third_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_first_three_excited_coefficients_are_exactly_8_44_and_192"] is True
    assert theorem["the_eta_minus_8_third_excited_coefficient_is_exactly_the_tomotope_flag_packet"] is True
    assert theorem["the_theta_e8_third_coefficient_is_exactly_6720"] is True
    assert theorem["the_theta_e8_third_coefficient_is_exactly_the_gosset_edge_packet"] is True
    assert theorem["the_affine_e8_third_coefficient_is_exactly_34752"] is True
    assert theorem["the_affine_e8_third_coefficient_splits_exactly_as_6720_plus_17280_plus_8640_plus_1920_plus_192"] is True
    assert theorem["the_recent_affine_modular_layer_therefore_meets_the_corrected_tomotope_flag_packet_already_at_q_cubed"] is True

    assert packet["bosonic_octet_8"] == 8
    assert packet["corrected_spread_carrier_36"] == 36
    assert packet["tomotope_flag_packet_192"] == 192
    assert packet["gosset_edge_packet_6720"] == 6720
    assert packet["norm4_shell_octet_coupling_17280"] == 17280
    assert packet["root_spread_coupling_8640"] == 8640
