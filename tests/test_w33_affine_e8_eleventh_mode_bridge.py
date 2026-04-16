from __future__ import annotations

from exploration.w33_affine_e8_eleventh_mode_bridge import build_summary


def test_affine_e8_eleventh_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_eleventh_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_eleventh_excited_coefficient_is_exactly_1020416"] is True
    assert theorem["the_eta_minus_8_eleventh_excited_coefficient_splits_exactly_as_496_times_sigma3_k_plus_26_times_tau_plus_40"] is True
    assert theorem["the_theta_e8_eleventh_coefficient_is_exactly_319680_equals_E_times_496_plus_336_plus_252_plus_168_plus_80"] is True
    assert theorem["the_affine_e8_eleventh_coefficient_is_exactly_1749556736"] is True
    assert theorem["the_q11_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_sparse_residue_496_sigma3_k_plus_26_tau_plus_40"] is True
    assert theorem["the_eleventh_mode_keeps_the_exact_hierarchy_alive_with_a_heterotic_sigma3_lift_corrected_by_the_26_packet_and_the_point_carrier"] is True

    assert packet["heterotic_packet_496"] == 496
    assert packet["full_heawood_shell_336"] == 336
    assert packet["tau_packet_252"] == 252
    assert packet["dual_pair_flags_168"] == 168
    assert packet["levi_carrier_80"] == 80
    assert packet["half_f4_packet_26"] == 26
    assert packet["point_carrier_40"] == 40
    assert packet["half_f4_times_tau_6552"] == 6552
