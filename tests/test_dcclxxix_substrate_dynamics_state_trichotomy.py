"""Part DCCLXXIX -- Substrate-Dynamics-State trichotomy tests."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxix_substrate_dynamics_state_trichotomy import (  # noqa: E402
    OUT_PATH,
    build_bridge,
    dynamics_layer,
    necessity_table,
    state_layer,
    substrate_layer,
    what_w33_answers,
    what_w33_does_NOT_answer,
    write_bridge,
)


def test_substrate_is_necessary():
    assert substrate_layer()["status"] == "necessary"


def test_dynamics_is_mixed():
    assert "partially" in dynamics_layer()["status"]


def test_state_is_fully_contingent():
    assert state_layer()["status"] == "fully contingent"


def test_substrate_layer_contains_W33():
    s = substrate_layer()
    assert any("W(3,3)" in c for c in s["contents"])


def test_substrate_layer_cites_DCCLXXVII():
    s = substrate_layer()
    assert "DCCLXXVII" in s["uniqueness"] or "convergent attractor" in s["uniqueness"]


def test_dynamics_necessary_contains_SM_gauge():
    d = dynamics_layer()
    assert any("SM gauge" in c for c in d["necessary_contents"])


def test_dynamics_contingent_contains_alpha_or_couplings():
    d = dynamics_layer()
    assert any("coupling" in c.lower() for c in d["contingent_contents"])


def test_state_layer_contains_initial_conditions():
    t = state_layer()
    assert any("initial conditions" in c.lower() for c in t["contents"])


def test_necessity_table_has_at_least_12_items():
    assert len(necessity_table()) >= 12


def test_necessity_table_has_both_statuses():
    table = necessity_table()
    necessary = [r for r in table if r["status"] == "necessary"]
    contingent = [r for r in table if r["status"] == "contingent"]
    assert len(necessary) >= 4
    assert len(contingent) >= 4


def test_w33_answers_at_least_15_questions():
    assert len(what_w33_answers()) >= 15


def test_w33_does_not_answer_at_least_8():
    assert len(what_w33_does_NOT_answer()) >= 8


def test_w33_answers_include_3D_space():
    answers = what_w33_answers()
    assert any("3 spatial dim" in a for a in answers)


def test_w33_answers_include_SM_gauge():
    answers = what_w33_answers()
    assert any("SM gauge" in a or "color" in a.lower() for a in answers)


def test_w33_does_not_answer_includes_alpha():
    non_answers = what_w33_does_NOT_answer()
    assert any("alpha" in a.lower() for a in non_answers)


def test_w33_does_not_answer_includes_initial_conditions():
    non_answers = what_w33_does_NOT_answer()
    assert any("initial conditions" in a.lower() for a in non_answers)


def test_summary_all_identities_hold():
    b = build_bridge()
    assert b["summary"]["all_identities_hold"] is True


def test_identities_all_pass():
    b = build_bridge()
    failed = [k for k, v in b["identities"].items() if not v]
    assert failed == []


def test_theorem_mentions_trichotomy():
    b = build_bridge()
    assert "Trichotomy" in b["theorem"]


def test_one_line_mentions_substrate_dynamics_state():
    b = build_bridge()
    assert "Substrate" in b["one_line"] or "necessary" in b["one_line"]


def test_final_breakthrough_statement_present():
    b = build_bridge()
    assert "complete form" in b["final_breakthrough_statement"]


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
        "substrate_layer",
        "dynamics_layer",
        "state_layer",
        "necessity_table",
        "what_w33_answers",
        "what_w33_does_not_answer",
        "identities",
        "theorem",
        "one_line",
        "final_breakthrough_statement",
        "honesty_boundary",
    ):
        assert key in data
