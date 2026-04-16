from __future__ import annotations

from exploration.w33_affine_e8_tenth_mode_bridge import build_summary


def test_affine_e8_tenth_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_tenth_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_tenth_excited_coefficient_is_exactly_417140"] is True
    assert theorem["the_eta_minus_8_tenth_excited_coefficient_splits_exactly_as_204_times_sigma3_k_plus_80_plus_84"] is True
    assert theorem["the_theta_e8_tenth_coefficient_is_exactly_272160_equals_E_times_78_plus_336_plus_720"] is True
    assert theorem["the_affine_e8_tenth_coefficient_is_exactly_603096260"] is True
    assert theorem["the_q10_affine_mode_is_still_on_the_exact_w33_spine_but_the_new_information_is_concentrated_in_the_dual_spread_sigma3_residue"] is True
    assert theorem["the_tenth_mode_keeps_the_exact_hierarchy_alive_with_a_dual_spread_lift_of_sigma3_k_and_a_levi_plus_surface_remainder"] is True

    assert packet["e6_adjoint_packet_78"] == 78
    assert packet["full_heawood_shell_336"] == 336
    assert packet["qE_packet_720"] == 720
    assert packet["dual_spread_packet_204"] == 204
    assert packet["sigma3_k_packet_2044"] == 2044
    assert packet["levi_carrier_80"] == 80
    assert packet["single_surface_flags_84"] == 84
