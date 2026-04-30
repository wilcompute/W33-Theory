from __future__ import annotations

from pathlib import Path

from scripts.w33_q8_claim_ledger import q8_claim_ledger


def test_q8_claim_ledger_has_required_tiers_and_counts() -> None:
    ledger = q8_claim_ledger()

    assert ledger["version"] == 1
    assert ledger["source"] == "scripts/w33_q8_spectral_action_master_audit.py"
    assert len(ledger["exact_finite_theorem"]) >= 4
    assert len(ledger["near_exact_phenomenology"]) >= 1
    assert len(ledger["frontier_conjecture"]) >= 1
    assert ledger["conflict_count"] == len(ledger["conflict"]) == 5


def test_q8_claim_ledger_promotes_pmns_and_alpha_integer_part() -> None:
    ledger = q8_claim_ledger()

    exact_ids = {entry["id"] for entry in ledger["exact_finite_theorem"]}
    assert "alpha_integer_part_gaussian_norm" in exact_ids
    assert "pmns_projective_incidence_packet" in exact_ids

    pmns_entry = next(
        entry
        for entry in ledger["exact_finite_theorem"]
        if entry["id"] == "pmns_projective_incidence_packet"
    )
    assert pmns_entry["sin2_theta12"] == "4/13"
    assert pmns_entry["sin2_theta23"] == "7/13"
    assert pmns_entry["sin2_theta13"] == "2/91"


def test_paper_and_docs_use_normalized_claim_surface() -> None:
    paper = Path("w33_paper.tex").read_text(encoding="utf-8")
    docs = Path("docs/index.html").read_text(encoding="utf-8")

    # Paper normalized surfaces.
    assert "669969/4889" in paper
    assert "\\sin^2\\theta_{12}^{\\rm PMNS}=\\tfrac{\\mu}{\\Phi_3}=\\tfrac{4}{13}" in paper

    # Docs normalized surfaces.
    assert "669969/4889 ≈ 137.035999182" in docs
    assert "4/13" in docs
    assert "Legacy sin&sup2;&theta;<sub>12</sub>=3/10 remains a boundary conflict in the Q8 claim" in docs


def test_legacy_formula_mentions_are_explicitly_boundary_tagged() -> None:
    paper = Path("w33_paper.tex").read_text(encoding="utf-8")
    docs = Path("docs/index.html").read_text(encoding="utf-8")

    # Paper must not present 3/10 PMNS as unqualified primary theorem text.
    assert "\\sin^2\\theta_{12}^{\\rm PMNS} & $q/(k-\\lambda)$ & $3/10$" not in paper
    assert "legacy $q/(k-\\lambda)=3/10$ boundary packet" in paper

    # Docs high-visibility prediction cards must boundary-tag legacy alpha shorthand.
    assert "legacy/boundary\n                &alpha;<sup>&minus;1</sup>&asymp;137.036" in docs


def test_docs_authoritative_sections_block_unqualified_legacy_drift() -> None:
    docs = Path("docs/index.html").read_text(encoding="utf-8")

    # Guard the canonical prediction table surface.
    predictions_start = docs.find('<section id="predictions">')
    assert predictions_start != -1
    predictions_end = docs.find("</section>", predictions_start)
    assert predictions_end != -1
    predictions = docs[predictions_start:predictions_end]

    assert "669969/4889" in predictions
    assert "sin²θ<sub>12</sub> (solar)" in predictions
    assert "4/13 = 0.3077" in predictions
    assert "152247/1111" not in predictions
    assert "137.036004" not in predictions

    # Guard the high-visibility master-predictions spotlight card.
    card_anchor = docs.find("Master Predictions Table")
    assert card_anchor != -1
    card_start = docs.rfind('<div class="card"', 0, card_anchor)
    assert card_start != -1
    card = docs[card_start : min(len(docs), card_start + 1400)]

    assert "legacy/boundary" in card
    assert "sin&sup2;&theta;<sub>12</sub>=4/13" in card
    assert "Legacy sin&sup2;&theta;<sub>12</sub>=3/10" in card
