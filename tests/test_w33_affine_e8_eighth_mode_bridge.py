from __future__ import annotations

from exploration.w33_affine_e8_eighth_mode_bridge import build_summary


def test_affine_e8_eighth_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_eighth_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_eighth_excited_coefficient_is_exactly_62337"] is True
    assert theorem["the_eta_minus_8_eighth_excited_coefficient_splits_exactly_as_30_times_sigma3_k_plus_4_times_tau_plus_q_squared"] is True
    assert theorem["the_theta_e8_eighth_coefficient_is_exactly_140400_equals_E_times_496_plus_84_plus_5"] is True
    assert theorem["the_affine_e8_eighth_coefficient_is_exactly_60655377"] is True
    assert theorem["the_q8_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_sparse_residue_30_sigma3_k_plus_4_tau_plus_9"] is True
    assert theorem["the_eighth_mode_keeps_the_exact_hierarchy_alive_but_only_in_a_sparse_mixed_shell_language"] is True

    assert packet["heterotic_packet_496"] == 496
    assert packet["single_surface_flags_84"] == 84
    assert packet["bosonic_4_plus_1_packet_5"] == 5
    assert packet["neutral_packet_30"] == 30
    assert packet["sigma3_k_packet_2044"] == 2044
    assert packet["mu_times_tau_1008"] == 1008
