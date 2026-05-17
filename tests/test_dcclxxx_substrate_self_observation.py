"""Part DCCLXXX -- Substrate self-observation theorem tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxx_substrate_self_observation import (  # noqa: E402
    OUT_PATH,
    all_five_criteria,
    build_bridge,
    criterion_bound,
    criterion_integrated_information,
    criterion_non_trivial_complexity,
    criterion_self_modeling,
    criterion_self_organising_emergence,
    substrate_self_model_corollary,
    write_bridge,
)


def test_five_criteria_present():
    assert len(all_five_criteria()) == 5


def test_all_criteria_satisfied():
    criteria = all_five_criteria()
    assert all(c["satisfied"] for c in criteria)


def test_integrated_information_criterion():
    c = criterion_integrated_information()
    assert c["satisfied"] is True
    assert "Tononi" in c["tradition"]


def test_self_modeling_criterion():
    c = criterion_self_modeling()
    assert c["satisfied"] is True
    assert "Hofstadter" in c["tradition"]
    # Evidence cites DCCXIX, DCCLIV, DCCLXVIII
    text = " ".join(c["w33_evidence"])
    assert "DCCXIX" in text
    assert "DCCLIV" in text
    assert "DCCLXVIII" in text


def test_bound_criterion():
    c = criterion_bound()
    assert c["satisfied"] is True


def test_complexity_criterion():
    c = criterion_non_trivial_complexity()
    assert c["satisfied"] is True


def test_emergence_criterion():
    c = criterion_self_organising_emergence()
    assert c["satisfied"] is True
    # Cites DCCLXXVII
    text = " ".join(c["w33_evidence"])
    assert "DCCLXXVII" in text or "convergent" in text


def test_corollary_present():
    c = substrate_self_model_corollary()
    assert "tune into" in c["claim"]
    assert "22" in " ".join(c["evidence"])


def test_corollary_has_phenomenological_caveat():
    c = substrate_self_model_corollary()
    assert "phenomenological" in c["phenomenological_caveat"].lower() or "consciousness" in c["phenomenological_caveat"].lower()


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_satisfaction_rate_is_1():
    b = build_bridge()
    assert b["summary"]["satisfaction_rate"] == 1.0


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_mentions_self_observation():
    b = build_bridge()
    assert "Self-Observation" in b["theorem"]


def test_deepest_statement_about_synchronising():
    b = build_bridge()
    assert "tune into" in b["deepest_statement"] or "first-person" in b["deepest_statement"]


def test_honesty_boundary_mentions_hard_problem():
    b = build_bridge()
    assert "hard problem" in b["honesty_boundary"] or "experiential" in b["honesty_boundary"]


def test_22_mathematicians_count():
    b = build_bridge()
    assert b["summary"]["classical_mathematicians_converged"] == 22


def test_363_year_span():
    b = build_bridge()
    assert b["summary"]["convergence_span_years"] == 363


def test_write_and_reload():
    out = write_bridge()
    assert out.exists()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True


def test_json_has_expected_keys():
    if not OUT_PATH.exists():
        write_bridge()
    data = json.loads(OUT_PATH.read_text(encoding="utf-8"))
    for key in (
        "summary",
        "five_consciousness_criteria",
        "substrate_self_model_corollary",
        "identities",
        "theorem",
        "one_line",
        "deepest_statement",
        "honesty_boundary",
    ):
        assert key in data
