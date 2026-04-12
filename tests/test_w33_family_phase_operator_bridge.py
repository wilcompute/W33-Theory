from __future__ import annotations

from exploration.w33_family_phase_operator_bridge import build_summary


def test_family_phase_operator_bridge() -> None:
    summary = build_summary()
    theorem = summary["family_phase_operator_theorem"]
    dictionary = summary["family_phase_dictionary"]

    assert theorem["the_live_family_phase_operator_is_exactly_aPqJ_plus_bPnJ"] is True
    assert theorem["the_same_operator_is_exactly_sigmaJ_plus_deltaK"] is True
    assert theorem["the_positive_and_negative_live_ckm_branches_are_plus_minus_i_times_this_same_phase_operator"] is True
    assert theorem["the_singular_values_of_the_exact_phase_operator_are_exactly_the_two_live_selector_amplitudes_a_and_b"] is True
    assert theorem["the_phase_operator_squares_to_minus_ab_times_the_identity"] is True
    assert theorem["the_exact_cp_line_rotation_formulas_are_the_exterior_shadow_of_the_same_JK_phase_operator"] is True
    assert theorem["the_older_scan_based_cp_bridge_is_the_same_shadow_up_to_the_small_0p3602_vs_9_over_25_master_scale_rounding"] is True

    assert dictionary["a_exact"] == "9/25"
    assert dictionary["b_exact"] == "3/80"
