from __future__ import annotations

from exploration.w33_affine_e8_cumulative_regime_bridge import build_summary


def test_affine_e8_cumulative_regime_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_cumulative_regime_theorem"]
    regime = summary["affine_e8_cumulative_regime_dictionary"]

    assert theorem["the_old_canonical_sparse_sigma3_k_tau_residual_closure_survives_exactly_at_q11_as_496_sigma3_k_plus_26_tau_plus_40"] is True
    assert theorem["the_old_canonical_sparse_sigma3_k_tau_residual_closure_fails_completely_at_q12"] is True
    assert theorem["the_old_canonical_sparse_sigma3_k_tau_residual_closure_fails_completely_at_q13"] is True
    assert theorem["the_old_canonical_sparse_sigma3_k_tau_residual_closure_fails_completely_at_q14"] is True
    assert theorem["the_theta_side_remains_exactly_local_at_q12_q13_q14"] is True
    assert theorem["the_first_four_oscillator_recurrence_channels_are_exactly_8_24_32_56"] is True
    assert theorem["the_first_four_recurrence_channels_contribute_more_than_nine_tenths_of_the_total_at_q12"] is True
    assert theorem["the_first_four_recurrence_channels_contribute_more_than_nine_tenths_of_the_total_at_q13"] is True
    assert theorem["the_first_four_recurrence_channels_contribute_more_than_nine_tenths_of_the_total_at_q14"] is True
    assert theorem["the_post_q11_oscillator_side_enters_a_genuine_cumulative_regime_driven_by_the_exact_8_24_32_56_packet_ladder"] is True

    assert regime["channel_weights"] == [8, 24, 32, 56]
    assert regime["sparse_sigma_tau_residual_solutions"][11] == [(496, 26, 40)]
    assert regime["sparse_sigma_tau_residual_solutions"][12] == []
    assert regime["sparse_sigma_tau_residual_solutions"][13] == []
    assert regime["sparse_sigma_tau_residual_solutions"][14] == []
