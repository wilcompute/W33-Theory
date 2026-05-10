"""Regression tests for PART CCCCXXV theta/U(5) stabilizer completion."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "exploration" / "PART_CCCCXXV_THETA_U5_STABILIZER_COMPLETION.py"
RESULTS_PATH = ROOT / "PART_CCCCXXV_theta_u5_stabilizer_completion_results.json"


@lru_cache(maxsize=1)
def load_module():
    spec = importlib.util.spec_from_file_location("theta_u5_stabilizer_completion_ccccxxv", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def build_results():
    return load_module().build_results()


def test_all_theta_u5_completion_checks_pass():
    results = build_results()
    assert results["verified"] is True
    assert results["checks_passed"] == results["checks_total"] == 29
    assert all(check["passed"] for check in results["checks"])


def test_rank_completion_closes_the_w33_css_carrier():
    rank = build_results()["rank_completion"]
    assert rank["local_csaszar_check_rank"] == 95
    assert rank["u5_input_completion_rank"] == 25
    assert rank["w33_triangle_rank"] == 120
    assert rank["w33_vertex_rank"] == 39
    assert rank["full_stabilizer_rank"] == 159
    assert rank["h1_logical_rank"] == 81
    assert rank["completion_rank_25_plus_39"] == 64
    assert rank["identity"] == "95 + 25 + 39 + 81 = 240"
    assert 95 + 25 == rank["w33_triangle_rank"]
    assert 120 + 39 == rank["full_stabilizer_rank"]
    assert 159 + 81 == 240


def test_physical_split_is_theta_edges_plus_transport_bundle():
    split = build_results()["physical_split"]
    assert split["theta_edges"] == 105
    assert split["transport_edges"] == 135
    assert split["total_edges"] == 240
    assert split["theta_share"] == "7/16"
    assert split["transport_share"] == "9/16"
    assert split["transport_read"] == "135 = 45*3 transport bundle complement"
    assert split["theta_edges"] + split["transport_edges"] == split["total_edges"]


def test_protected_split_preserves_theta_transport_partition():
    protected = build_results()["protected_split"]
    assert protected["steane_block"] == 343
    assert protected["theta_protected_n"] == 36015
    assert protected["transport_protected_n"] == 46305
    assert protected["global_protected_n"] == 82320
    assert protected["active_protection_code"] == "[[82320,81,>=81]]"
    assert protected["distance_lower_bound"] == 81
    assert protected["correctable_weight"] == 40
    assert protected["theta_protected_n"] + protected["transport_protected_n"] == protected["global_protected_n"]


def test_completion_layers_are_ordered_and_honest():
    results = build_results()
    assert [layer["name"] for layer in results["completion_layers"]] == [
        "local_csaszar_toric_checks",
        "u5_input_mode_completion",
        "w33_vertex_star_completion",
        "h1_logical_tail",
    ]
    assert [layer["rank"] for layer in results["completion_layers"]] == [95, 25, 39, 81]
    assert "95+25=120" in results["theorem"]
    assert "159+H1=159+81=240" in results["theorem"]
    assert "7/16 plus 9/16" in results["theorem"]
    assert "not assert that the U(5) rank completion is a canonical W33 triangle operator isomorphism" in results["honesty_boundary"]
    assert "does not replace the existing Steane/Phi6 protection" in results["honesty_boundary"]


def test_result_artifact_is_present_and_current():
    artifact = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    live = build_results()
    assert artifact["part"] == "CCCCXXV"
    assert artifact["verified"] is True
    assert artifact["checks_passed"] == artifact["checks_total"] == live["checks_total"]
    assert artifact["rank_completion"] == live["rank_completion"]
    assert artifact["physical_split"] == live["physical_split"]
    assert artifact["protected_split"] == live["protected_split"]


def test_docs_index_exposes_theta_u5_stabilizer_completion():
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Theta / U(5) Stabilizer Completion" in text
    assert "PART_CCCCXXV_THETA_U5_STABILIZER_COMPLETION.md" in text
    assert "95+25=120" in text
    assert "120+39=159" in text
    assert "95+25+39+81=240" in text
    assert "105+135=240" in text
    assert "7/16" in text
    assert "9/16" in text
    assert "[[82320,81,&ge;81]]" in text
