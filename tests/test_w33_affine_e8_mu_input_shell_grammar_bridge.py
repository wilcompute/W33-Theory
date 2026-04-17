from __future__ import annotations

from exploration.w33_affine_e8_mu_input_shell_grammar_bridge import build_summary


def test_affine_e8_mu_input_shell_grammar_bridge() -> None:
    summary = build_summary()
    theorem = summary["affine_e8_mu_input_shell_grammar_theorem"]
    rows = summary["affine_e8_mu_input_shell_grammar_dictionary"]["grammar_rows"]

    assert theorem["the_canonical_E8_shell_generator_index_is_exactly_mu_times_mu"] is True
    assert theorem["the_canonical_Heawood_shell_generator_index_is_exactly_mu_times_mu_plus_1"] is True
    assert theorem["the_canonical_480_shell_generator_index_is_exactly_mu_times_2q"] is True
    assert theorem["the_canonical_A26_shell_generator_index_is_exactly_mu_times_q_squared"] is True
    assert theorem["the_canonical_qE_shell_generator_index_is_exactly_mu_times_Theta"] is True
    assert theorem["the_canonical_promoted_affine_shell_generators_form_the_exact_input_grammar_mu_times_mu_mu_plus_1_2q_q_squared_Theta"] is True

    assert rows["mu"]["mu_times_input"] == 16
    assert rows["mu_plus_1"]["mu_times_input"] == 20
    assert rows["2q"]["mu_times_input"] == 24
    assert rows["q_squared"]["mu_times_input"] == 36
    assert rows["Theta"]["mu_times_input"] == 40
