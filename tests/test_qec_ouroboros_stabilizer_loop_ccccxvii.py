"""Regression tests for PART CCCCXVII QEC ouroboros stabilizer loop."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXVII_QEC_OUROBOROS_STABILIZER_LOOP.py"
RESULTS_PATH = ROOT / "PART_CCCCXVII_qec_ouroboros_stabilizer_loop_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("qec_ouroboros_stabilizer_loop_ccccxvii", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_qec_ouroboros_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 15
    assert all(check["passed"] for check in results["checks"])


def test_index_snake_phrase_is_qec_anchor():
    anchor = build_results()["index_anchor"]
    assert anchor["section"] == "The Self-Referential Loop"
    assert anchor["phrase"] == "The snake eats its tail."
    assert "stabilizer/logical tail" in anchor["interpretation"]


def test_ouroboros_map_preserves_tail_instead_of_stabilizing_it_away():
    loop_map = build_results()["qec_ouroboros_map"]
    assert loop_map["head"] == "W33 edge-qubit CSS carrier [[240,81,3]]"
    assert loop_map["tail"] == "line-star triples are the H1=81 logical/matter sector modulo vertex checks"
    assert loop_map["failed_shortcut"] == "adding the tail as stabilizers gives k=0"
    assert loop_map["protected_closure"] == "Steane/Phi6 lift protects the same 81-sector as [[82320,81,>=81]]"


def test_closure_numbers_match_active_qec_architecture():
    numbers = build_results()["closure_numbers"]
    assert numbers["physical_edge_qubits"] == 240
    assert numbers["logical_sector"] == 81
    assert numbers["base_css_code"] == "[[240,81,3]]"
    assert numbers["line_star_mod_vertex_rank"] == 81
    assert numbers["k_if_line_stars_are_stabilizers"] == 0
    assert numbers["q4_raw_target"] == 12
    assert numbers["q4_dressed_weight"] == 4
    assert numbers["active_protection_code"] == "[[82320,81,>=81]]"
    assert numbers["correctable_weight"] == 40


def test_theorem_states_the_snake_tail_qec_connection():
    results = build_results()
    assert "stabilizer/logical feedback loop" in results["theorem"]
    assert "line-star tail spans those 81 sectors" in results["theorem"]
    assert "collapses k to zero" in results["theorem"]
    assert "[[1296,81,4]]" in results["theorem"]
    assert "[[82320,81,>=81]]" in results["theorem"]
    assert "not a new proof" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXVII"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["closure_numbers"] == live["closure_numbers"]


def test_docs_index_exposes_qec_ouroboros_bridge():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "The snake eats its tail" in text
    assert "QEC Ouroboros Stabilizer Loop" in text
    assert "PART_CCCCXVII_QEC_OUROBOROS_STABILIZER_LOOP.md" in text
    assert "QEC feedback loop on the" in text
    assert "[[240,81,3]]" in text
    assert "<code>240</code>-edge complex" in text
    assert "line-star tail is the <code>H1=81</code> logical sector" in text
    assert "collapses <code>k</code> to" in text
    assert "[[1296,81,4]]" in text
    assert "[[82320,81,&ge;81]]" in text
