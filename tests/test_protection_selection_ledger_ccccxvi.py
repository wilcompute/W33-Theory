"""Regression tests for PART CCCCXVI protection / selection ledger."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXVI_PROTECTION_SELECTION_LEDGER.py"
RESULTS_PATH = ROOT / "PART_CCCCXVI_protection_selection_ledger_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("protection_selection_ledger_ccccxvi", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_ledger_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 15
    assert all(check["passed"] for check in results["checks"])


def test_ledger_assigns_distinct_mechanism_roles():
    ledger = {entry["mechanism"]: entry for entry in build_results()["ledger"]}
    assert ledger["heralded_photonic_assembly"]["status"] == "retry_before_logic"
    assert ledger["triangle_flat_cyclic_covers"]["status"] == "valid_but_rejected_as_distance_upgrade"
    assert ledger["line_star_matter_sector"]["status"] == "preserve_and_reencode"
    assert ledger["q4_bacon_shor_packet"]["status"] == "local_routing_not_final_distance_layer"
    assert ledger["steane_phi6_lift"]["status"] == "committed_quantum_protection"
    assert ledger["classical_selector_commit"]["status"] == "commit_after_protection"
    assert ledger["e8_z3_operation_gate"]["status"] == "bounded_operation_gate"


def test_active_architecture_keeps_steane_as_protection_layer():
    active = build_results()["active_architecture"]
    assert active["rejected_distance_upgrade"] == "triangle-flat cyclic covers L=2,3 remain d=3"
    assert active["local_routing_layer"] == "[[1296,81,4]] Q4/Bacon-Shor subsystem packets"
    assert active["active_protection_layer"] == "[[82320,81,>=81]] Steane/Phi6 lift"
    assert active["selector_layer"] == "40-trit classical selector in a 64-bit envelope"
    assert active["operation_layer"] == "H1=81 -> E8 Z3 gate with 8347 checked bracket terms"


def test_theorem_prevents_q4_distance_overclaim():
    results = build_results()
    assert "not a dressed [[1296,81,>=12]] proof" in results["theorem"]
    assert "[[82320,81,>=81]]" in results["theorem"]
    assert "40-trit selector is committed only after" in results["theorem"]
    assert "device calibration" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXVI"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["active_architecture"] == live["active_architecture"]


def test_docs_index_exposes_protection_selection_ledger():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Protection / Selection Ledger" in text
    assert "PART_CCCCXVI_PROTECTION_SELECTION_LEDGER.md" in text
    assert "Q4 packets remain local routing hardware" in text
    assert "[[82320,81,&ge;81]]" in text
    assert "selector commits only after protected acceptance" in text
