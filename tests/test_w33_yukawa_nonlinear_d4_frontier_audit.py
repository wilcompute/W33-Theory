from __future__ import annotations

from scripts.w33_yukawa_nonlinear_d4_frontier_audit import (
    analyze,
    build_nonlinear_d4_relation_certificate,
)


def test_nonlinear_d4_relation_certificate_gates_match_frontier_claim() -> None:
    payload = build_nonlinear_d4_relation_certificate()
    cert = payload["nonlinear_d4_relation_certificate"]

    assert cert["degree_gate"]["max_active_factor_degree"] >= 4
    assert cert["degree_gate"]["open_problem_max_active_factor_degree"] >= 4
    assert cert["degree_gate"]["native_mixed_seed_lift_reaches_11_to_12"] is True

    assert cert["d4_galois_gate"]["quartic_galois_labels"] == {
        "H_2:-+": "D4",
        "Hbar_2:+-": "D4",
    }
    assert cert["d4_galois_gate"]["quartic_galois_orders"] == {
        "H_2:-+": 8,
        "Hbar_2:+-": 8,
    }
    assert cert["d4_galois_gate"]["both_even_lifts_are_irreducible_d4_quartics"] is True

    assert cert["branch_stability_gate"][
        "mixed_product_ratio_branch_stable_irreducible_octics"
    ] is True
    assert cert["frontier_consistency_gate"][
        "open_problem_relation_above_two_linearly_disjoint_d4_splitting_fields"
    ] is True


def test_nonlinear_d4_relation_certificate_theorem_passes_and_is_reproducible() -> None:
    payload = analyze()
    theorem = payload["nonlinear_d4_relation_certificate_theorem"]
    frozen = payload["frozen_artifact"]

    assert theorem["degree_gate_passes"] is True
    assert theorem["d4_galois_gate_passes"] is True
    assert theorem["branch_stability_gate_passes"] is True
    assert theorem["frontier_consistency_gate_passes"] is True
    assert theorem["frozen_artifact_reproducibility_verified"] is True
    assert theorem["nonlinear_d4_relation_certificate_passes"] is True

    assert frozen["reproducibility_verified"] is True
    assert frozen["written_sha256"] == frozen["read_back_sha256"]
