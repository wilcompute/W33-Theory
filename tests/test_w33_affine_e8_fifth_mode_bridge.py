from __future__ import annotations

from exploration.w33_affine_e8_fifth_mode_bridge import build_summary


def test_affine_e8_fifth_mode_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_fifth_mode_theorem"]
    packet = summary["w33_packet_dictionary"]

    assert theorem["the_eta_minus_8_first_five_excited_coefficients_are_exactly_8_44_192_726_and_2464"] is True
    assert theorem["the_eta_minus_8_fifth_excited_coefficient_splits_exactly_as_sigma3_k_plus_dual_pair_flags_plus_tau"] is True
    assert theorem["the_theta_e8_fifth_coefficient_is_exactly_30240_equals_E_times_tau_over_2"] is True
    assert theorem["the_affine_e8_fifth_coefficient_is_exactly_1057504"] is True
    assert theorem["the_affine_e8_fifth_coefficient_splits_exactly_as_30240_plus_140160_plus_241920_plus_53760_plus_414720_plus_172800_plus_1440_plus_2044_plus_168_plus_252"] is True
    assert theorem["the_fifth_mode_still_closes_on_existing_exact_w33_packets_but_now_requires_the_composite_sigma3_k_plus_dual_pair_plus_tau_oscillator_lift"] is True

    assert packet["ramanujan_half_shell_30240"] == 30240
    assert packet["sigma3_k_packet_2044"] == 2044
    assert packet["dual_pair_flags_168"] == 168
    assert packet["tau_packet_252"] == 252
    assert packet["gosset_spread_coupling_241920"] == 241920
    assert packet["transport_tomotope_coupling_414720"] == 414720
    assert packet["root_triple_root_coupling_172800"] == 172800
    assert packet["root_shared_six_coupling_1440"] == 1440
