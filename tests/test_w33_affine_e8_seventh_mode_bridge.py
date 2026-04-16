from __future__ import annotations

from exploration.w33_affine_e8_seventh_mode_bridge import build_summary


def test_affine_e8_seventh_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_seventh_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_seventh_excited_coefficient_is_exactly_22528"] is True
    assert theorem["the_eta_minus_8_seventh_excited_coefficient_splits_exactly_as_k_minus_1_times_sigma3_k_plus_44"] is True
    assert theorem["the_theta_e8_seventh_coefficient_is_exactly_82560_equals_E_times_336_plus_8"] is True
    assert theorem["the_affine_e8_seventh_coefficient_is_exactly_17333248"] is True
    assert theorem["the_q7_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_residue_22528"] is True
    assert theorem["the_seventh_mode_is_the_first_one_where_the_clean_residue_is_best_read_as_a_shell_index_lift_of_sigma3_k_rather_than_as_a_preexisting_single_packet"] is True

    assert packet["full_heawood_shell_336"] == 336
    assert packet["bosonic_octet_8"] == 8
    assert packet["corrected_spread_carrier_36"] == 36
    assert packet["sigma3_k_packet_2044"] == 2044
    assert packet["k_minus_1"] == 11
    assert packet["spread_plus_octet_44"] == 44
    assert packet["shell_index_lift_22484"] == 22484
