"""Regression tests for PART CCCCXXX cyclic Cayley obstruction."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXX_CYCLIC_CAYLEY_OBSTRUCTION.py"
RESULTS_PATH = ROOT / "PART_CCCCXXX_cyclic_cayley_obstruction_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("cyclic_cayley_obstruction_ccccxxx", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_cyclic_cayley_obstruction_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 27
    assert all(check["passed"] for check in results["checks"])


def test_exhaustive_z40_search_has_no_w33_srg_hits():
    search = build_results()["cyclic_search"]
    assert search["pair_count"] == 19
    assert search["candidate_count"] == search["expected_candidate_count"] == 27132
    assert search["hit_count"] == 0
    assert search["hits"] == []


def test_false_draft_connection_set_is_falsified():
    draft = build_results()["draft_connection_set"]
    assert draft["set"] == [1, 3, 7, 9, 13, 19, 21, 27, 31, 33, 37, 39]
    assert draft["is_srg_40_12_2_4"] is False
    assert draft["adjacent_common_neighbor_counts"] == {"0": 12}
    assert draft["nonadjacent_common_neighbor_counts"] != {"4": 27}


def test_architecture_redirects_cycle_to_hashimoto_and_qec():
    redirect = build_results()["architecture_redirect"]
    assert redirect["false_shortcut"] == "global cyclic Cayley graph on Z40"
    assert redirect["positive_cycle"] == "directed Hashimoto/fusion carrier with 480 states"
    assert redirect["qec_loop"] == "QEC ouroboros preserving the H1=81 line-star tail"
    assert redirect["protected_code"] == "[[82320,81,>=81]]"
    assert redirect["local_routing_code"] == "[[1296,81,4]]"


def test_theorem_and_boundary_are_negative_but_bounded():
    results = build_results()
    assert "C(19,6)=27132" in results["theorem"]
    assert "zero hits" in results["theorem"]
    assert "480-state directed Hashimoto/fusion carrier" in results["theorem"]
    assert "preserves H1=81" in results["theorem"]
    assert "does not rule out every possible non-cyclic Cayley representation" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXX"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["cyclic_search"] == live["cyclic_search"]
    assert artifact["draft_connection_set"] == live["draft_connection_set"]
    assert artifact["architecture_redirect"] == live["architecture_redirect"]


def test_docs_index_exposes_cyclic_obstruction():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Cyclic Cayley Obstruction and Photonic Ouroboros Guard" in text
    assert "PART_CCCCXXX_CYCLIC_CAYLEY_OBSTRUCTION.md" in text
    assert "C(19,6)=27132" in text
    assert "zero cyclic <code>Z40</code> hits" in text
    assert "480-state Hashimoto/fusion carrier" in text
    assert "QEC ouroboros preserving <code>H1=81</code>" in text
