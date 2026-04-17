from __future__ import annotations

from exploration.w33_levi_ckm_mu_grammar_bridge import build_summary


def test_levi_ckm_mu_grammar_bridge() -> None:
    summary = build_summary()
    theorem = summary["levi_ckm_mu_grammar_theorem"]
    dictionary = summary["levi_ckm_mu_grammar_dictionary"]

    assert theorem["the_standard_branch_filtered_Cabibbo_parameter_is_exactly_q_squared_over_40"] is True
    assert theorem["the_standard_Wolfenstein_A_squared_parameter_is_exactly_20_squared_times_53_over_q_six_times_43"] is True
    assert theorem["the_standard_unitarity_triangle_radius_Ru_is_exactly_q_squared_k_over_5_times_53"] is True
    assert theorem["the_standard_CKM_phase_tangent_squared_is_exactly_mu_to_4_times_5_over_q_to_5"] is True
    assert theorem["the_standard_gamma_phase_squares_are_exactly_the_split_q5_over_q5_plus_mu4_5_and_mu4_5_over_q5_plus_mu4_5"] is True
    assert theorem["the_standard_Vcb_scale_is_exactly_q_squared_53_over_mu4_5_squared_43"] is True
    assert theorem["the_standard_Vub_scale_is_exactly_q10_k_squared_over_mu4_40_squared_5_to_4_53_43"] is True
    assert theorem["the_standard_CKM_packet_is_generated_by_the_exact_finite_alphabet_q_mu_5_20_40_53_43_k"] is True

    assert dictionary["mu_fourth_power"] == 256
    assert dictionary["gamma_denominator_q5_plus_mu4_times_5"] == 1523
    assert dictionary["lambda"]["exact"] == "9/40"
    assert dictionary["tan2_gamma"]["exact"] == "1280/243"
