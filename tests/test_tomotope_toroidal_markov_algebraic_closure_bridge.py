from scripts.tomotope_toroidal_markov_algebraic_closure_bridge import build_bridge


def test_algebraic_closure_summary_values():
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["polynomial_degree"] == 3
    assert summary["distinct_nontrivial_roots"] == 3
    assert summary["nontrivial_multiplicity_per_root"] == 2
    assert (summary["weighted_sum_num"], summary["weighted_sum_den"]) == (0, 1)
    assert (summary["weighted_square_sum_num"], summary["weighted_square_sum_den"]) == (21, 16)


def test_algebraic_closure_core_identities_hold():
    payload = build_bridge()
    identities = payload["identities"]

    assert identities["all_six_modes_annihilate_cubic"] is True
    assert identities["nontrivial_weighted_sum_is_zero"] is True
    assert identities["nontrivial_weighted_square_sum_is_21_over_16"] is True
    assert identities["three_distinct_real_roots"] is True
    assert payload["summary"]["all_identities_hold"] is True
