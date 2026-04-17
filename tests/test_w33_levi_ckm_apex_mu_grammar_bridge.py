from __future__ import annotations

from exploration.w33_levi_ckm_apex_mu_grammar_bridge import build_summary


def test_levi_ckm_apex_mu_grammar_bridge() -> None:
    summary = build_summary()
    theorem = summary["levi_ckm_apex_mu_grammar_theorem"]
    dictionary = summary["levi_ckm_apex_mu_grammar_dictionary"]

    assert theorem["the_exact_phase_denominator_is_q5_plus_mu4_times_5_equals_1523"] is True
    assert theorem["the_squared_real_apex_coordinate_is_exactly_q9_k2_over_25_53_squared_1523"] is True
    assert theorem["the_squared_imaginary_apex_coordinate_is_exactly_q4_k2_mu4_over_5_53_squared_1523"] is True
    assert theorem["the_apex_coordinate_ratio_eta2_over_rho2_is_exactly_mu4_5_over_q5"] is True
    assert theorem["the_apex_coordinates_and_the_gamma_phase_use_the_same_exact_phase_denominator"] is True
    assert theorem["the_CKM_apex_packet_is_generated_by_the_same_exact_finite_alphabet_q_mu_5_53_k"] is True

    assert dictionary["phase_denominator_q5_plus_mu4_times_5"] == 1523
    assert dictionary["rho_bar_squared"]["exact"] == "2834352/106952675"
    assert dictionary["eta_bar_squared"]["exact"] == "2985984/21390535"
    assert dictionary["eta2_over_rho2"]["exact"] == "1280/243"
