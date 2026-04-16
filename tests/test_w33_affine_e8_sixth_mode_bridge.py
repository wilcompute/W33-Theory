from __future__ import annotations

from exploration.w33_affine_e8_sixth_mode_bridge import build_summary


def test_affine_e8_sixth_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_sixth_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_first_six_excited_coefficients_are_exactly_8_44_192_726_2464_and_7704"] is True
    assert theorem["the_eta_minus_8_sixth_excited_coefficient_splits_exactly_as_gosset_plus_qE_plus_dual_pair_plus_surface_flags_plus_gauge_dimension"] is True
    assert theorem["the_theta_e8_sixth_coefficient_is_exactly_60480_equals_E_times_tau"] is True
    assert theorem["the_affine_e8_sixth_coefficient_is_exactly_4530744"] is True
    assert theorem["the_affine_e8_sixth_coefficient_splits_exactly_as_the_full_ramanujan_gosset_transport_root_ladder_plus_the_7704_residue"] is True
    assert theorem["the_sixth_mode_still_closes_on_existing_exact_w33_packets_but_only_as_a_full_packet_ladder_from_12_up_to_60480"] is True

    assert packet["ramanujan_shell_60480"] == 60480
    assert packet["single_surface_flags_84"] == 84
    assert packet["gauge_dimension_12"] == 12
    assert packet["gosset_tomotope_coupling_1290240"] == 1290240
    assert packet["transport_triple_root_coupling_1555200"] == 1555200
    assert packet["root_sigma3k_coupling_490560"] == 490560
