from __future__ import annotations

from scripts.w33_publication_claim_reconciliation_audit import analyze


def test_publication_claim_tiers_are_reconciled_without_overpromotion() -> None:
    payload = analyze()

    assert payload["status"] == "ok"
    assert payload["boundary_record"] == {
        "name": "q3_full_physical_realization_theorem",
        "support_level": "boundary summary with promoted frontier response",
    }

    claims = payload["claim_tier_table"]
    assert len(claims) == 4
    assert {claim["name"] for claim in claims} == {
        "q3_full_physical_realization_theorem",
        "q3_smooth_realization_witness",
        "yukawa_nonlinear_d4_relation_certificate",
        "h4_s3_selector_holonomy_observable",
    }
    assert all(claim["executable_gate"] for claim in claims)

    theorem = payload["publication_claim_reconciliation_theorem"]
    assert theorem["boundary_tier_honest"] is True
    assert theorem["all_claim_gates_pass"] is True
    assert theorem["no_overpromotion_detected"] is True
    assert theorem["publication_claim_tiers_reconciled"] is True
