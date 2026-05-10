"""Regression tests for PART CCCCXV dressed Q4 packet logical verifier."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXV_DRESSED_Q4_PACKET_LOGICAL_VERIFIER.py"
RESULTS_PATH = ROOT / "PART_CCCCXV_dressed_q4_packet_logical_verifier_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("dressed_q4_packet_logical_verifier_ccccxv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_dressed_verifier_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 12
    assert all(check["passed"] for check in results["checks"])


def test_column_center_dresses_three_columns_to_one():
    mod = load_module()
    dressed = mod.min_dressed_column_count([0, 1, 2])
    assert dressed["raw_column_count"] == 3
    assert dressed["center_span_size"] == 8
    assert dressed["is_nontrivial"] is True
    assert dressed["best_dressed_column_count"] == 1
    assert dressed["best_dressed_physical_weight"] == 4


def test_attachment_audit_records_raw_versus_dressed_weight():
    audit = build_results()["attachment_audit"]
    conclusion = build_results()["dressed_distance_conclusion"]
    assert audit["attachments"] == 81
    assert audit["raw_replacement_weight"] == 12
    assert audit["sample_columns"] == [0, 1, 2]
    assert conclusion["current_subsystem_packet_distance"] == 4
    assert conclusion["raw_replacement_target"] == 12
    assert conclusion["integrated_12_claim_status"] == "not_proved_by_current_subsystem_dressing"


def test_repair_options_keep_architecture_honest():
    results = build_results()
    options = results["repair_options"]
    assert any("column-lock" in option for option in options)
    assert any("three independent packets" in option for option in options)
    assert any("Steane/Phi6" in option for option in options)
    assert "[[1296,81,4]]" in results["theorem"]
    assert "not yet [[1296,81,>=12]]" in results["theorem"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXV"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["dressed_distance_conclusion"] == live["dressed_distance_conclusion"]


def test_docs_index_exposes_dressed_q4_boundary():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Dressed Q4 Packet Logical Verifier" in text
    assert "PART_CCCCXV_DRESSED_Q4_PACKET_LOGICAL_VERIFIER.md" in text
    assert "[[1296,81,4]]" in text
    assert "weight-<code>12</code>" in text
    assert "weight <code>4</code>" in text
