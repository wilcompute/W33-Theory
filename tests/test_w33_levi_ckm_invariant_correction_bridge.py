from __future__ import annotations

from exploration.w33_levi_ckm_invariant_correction_bridge import build_summary


def test_levi_ckm_invariant_correction_bridge() -> None:
    summary = build_summary()
    theorem = summary["levi_ckm_invariant_correction_theorem"]
    dictionary = summary["levi_ckm_invariant_correction_dictionary"]

    assert theorem["the_clean_Wolfenstein_core_invariant_squared_is_exactly_q18_over_2_to_16_5_to_9_43_squared_q5_plus_mu4_5"] is True
    assert theorem["the_exact_Vcs_correction_is_already_a_finite_rational_packet_on_the_same_q_20_40_53_43_alphabet"] is True
    assert theorem["the_full_CKM_Jarlskog_squared_is_exactly_the_core_invariant_times_Vcs_squared"] is True
    assert theorem["the_standard_CKM_invariant_side_is_closed_by_a_clean_core_and_one_exact_finite_correction"] is True

    assert dictionary["phase_denominator_q5_plus_mu4_times_5"] == 1523
    assert dictionary["V_cs"]["exact"] == "857303477/880640000"
    assert dictionary["J_core_squared"]["exact"] == "387420489/360451456000000000"
