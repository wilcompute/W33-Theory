from verify_dclxiii_arxiv_claim_ledger import build_claim_ledger


def test_summary_exact_values_and_counts():
    payload = build_claim_ledger()
    summary = payload["summary"]

    assert summary["visible_vertices"] == 40
    assert summary["visible_degree"] == 12
    assert summary["hierarchy_exponent"] == 39
    assert summary["ihara_tree_exponent"] == 200
    assert (summary["sin2_theta_w_num"], summary["sin2_theta_w_den"]) == (3, 13)
    assert (summary["alpha_s_num"], summary["alpha_s_den"]) == (20, 169)
    assert (summary["omega_lambda_num"], summary["omega_lambda_den"]) == (9, 13)
    assert (summary["w0_num"], summary["w0_den"]) == (-19, 27)
    assert (summary["wa_num"], summary["wa_den"]) == (-1, 180)
    assert summary["falsifier_count"] == 39


def test_spectra_and_ihara_factorization_are_closed():
    payload = build_claim_ledger()
    spectra = payload["spectra"]
    ihara = payload["ihara_factorization"]

    assert spectra["visible_adjacency"] == [(12, 1), (2, 24), (-4, 15)]
    assert spectra["visible_laplacian"] == [(10, 24), (16, 15)]
    assert spectra["dark_laplacian"] == [(30, 24), (24, 15)]
    assert ihara["tree_exponent"] == 200
    assert ihara["regular_degree_shift"] == 11
    assert ihara["factors"] == [
        {"factor": "1-12u+11u^2", "multiplicity": 1},
        {"factor": "1-2u+11u^2", "multiplicity": 24},
        {"factor": "1+4u+11u^2", "multiplicity": 15},
    ]


def test_abstract_contract_and_identities_hold():
    payload = build_claim_ledger()

    assert payload["falsifier_numbers"] == list(range(1, 40))
    assert all(payload["abstract_markers"].values())
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True