from __future__ import annotations

from exploration.w33_affine_e8_ninth_mode_bridge import build_summary


def test_affine_e8_ninth_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_ninth_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_ninth_excited_coefficient_is_exactly_164560"] is True
    assert theorem["the_eta_minus_8_ninth_excited_coefficient_splits_exactly_as_80_times_sigma3_k_plus_4_times_tau_plus_32"] is True
    assert theorem["the_theta_e8_ninth_coefficient_is_exactly_181680_equals_E_times_496_plus_252_plus_9"] is True
    assert theorem["the_affine_e8_ninth_coefficient_is_exactly_197230000"] is True
    assert theorem["the_q9_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_sparse_residue_80_sigma3_k_plus_4_tau_plus_32"] is True
    assert theorem["the_ninth_mode_keeps_the_exact_hierarchy_alive_with_the_levi_carrier_as_the_new_lifting_packet"] is True

    assert packet["heterotic_packet_496"] == 496
    assert packet["tau_packet_252"] == 252
    assert packet["q_squared_9"] == 9
    assert packet["levi_carrier_80"] == 80
    assert packet["sigma3_k_packet_2044"] == 2044
    assert packet["mu_times_tau_1008"] == 1008
    assert packet["spin32_packet_32"] == 32
