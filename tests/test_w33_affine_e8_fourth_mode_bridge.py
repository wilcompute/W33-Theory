from __future__ import annotations

from exploration.w33_affine_e8_fourth_mode_bridge import build_summary


def test_affine_e8_fourth_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_fourth_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_first_four_excited_coefficients_are_exactly_8_44_192_and_726"] is True
    assert theorem["the_eta_minus_8_fourth_excited_coefficient_splits_exactly_as_q_times_the_root_packet_plus_the_shared_six_channel"] is True
    assert theorem["the_theta_e8_fourth_coefficient_is_exactly_17520_equals_E_times_Phi12"] is True
    assert theorem["the_affine_e8_fourth_coefficient_is_exactly_213126"] is True
    assert theorem["the_affine_e8_fourth_coefficient_splits_exactly_as_17520_plus_53760_plus_77760_plus_17280_plus_46080_plus_720_plus_6"] is True
    assert theorem["the_fourth_mode_is_the_first_affine_mode_that_needs_a_secondary_oscillator_lift_but_it_still_closes_on_existing_exact_w33_packets"] is True

    assert packet["dodecagonal_shell_17520"] == 17520
    assert packet["gosset_edge_packet_6720"] == 6720
    assert packet["triple_root_packet_720"] == 720
    assert packet["shared_six_channel_6"] == 6
    assert packet["gosset_octet_coupling_53760"] == 53760
    assert packet["norm4_spread_coupling_77760"] == 77760
    assert packet["root_tomotope_coupling_46080"] == 46080
