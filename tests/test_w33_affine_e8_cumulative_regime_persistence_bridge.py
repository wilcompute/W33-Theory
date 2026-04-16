from __future__ import annotations

from exploration.w33_affine_e8_cumulative_regime_persistence_bridge import build_summary


def test_affine_e8_cumulative_regime_persistence_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_cumulative_regime_persistence_theorem"]
    regime = summary["affine_e8_cumulative_regime_persistence_dictionary"]

    assert theorem["the_sparse_sigma3_k_tau_residual_law_stays_dead_from_q12_through_q18"] is True
    assert theorem["the_first_four_recurrence_channels_contribute_more_than_six_sevenths_of_the_total_from_q12_through_q18"] is True
    assert theorem["the_first_eight_recurrence_channels_contribute_more_than_ninety_nine_percent_of_the_total_from_q12_through_q18"] is True
    assert theorem["the_first_eight_channel_weights_are_exactly_8_24_32_56_48_96_64_120"] is True
    assert theorem["the_top4_share_decreases_strictly_from_q12_through_q18"] is True
    assert theorem["the_top8_share_decreases_strictly_from_q12_through_q18"] is True
    assert theorem["the_post_q11_oscillator_side_is_a_persistent_cumulative_regime_not_a_single_mode_exception"] is True

    assert regime["channel_weights_m1_to_m8"] == [8, 24, 32, 56, 48, 96, 64, 120]
    for n in range(12, 19):
        assert regime["samples_q12_to_q18"][str(n)]["sparse_sigma_tau_residual_solutions"] == []
