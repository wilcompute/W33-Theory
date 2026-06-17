#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(rel: str):
    out = subprocess.check_output([sys.executable, str(ROOT / "tools" / "bt1272_score_candidate.py"), str(ROOT / rel)], cwd=ROOT, text=True)
    return json.loads(out)


def test_bt1269_schema_file_fields():
    schema = json.loads((ROOT / "schema" / "bt1269_tomography_candidate.schema.json").read_text(encoding="utf-8"))
    assert schema["required"] == ["candidate_id", "closure_order", "word_diameter", "edge_split", "diameter_endpoint_first_set_histogram", "labelled_channel_spread"]
    assert schema["properties"]["edge_split"]["required"] == ["polar_graph", "nonpolar_graph"]
    assert schema["additionalProperties"] is False


def test_bt1272_exact_fixture_scores_pass():
    d = run_cli("examples/bt1269_exact_polar_path_candidate.json")
    assert d["candidate_id"] == "exact_polar_path"
    assert d["band"] == "pass"
    assert d["score"] == 5
    assert d["missing_gates"] == []


def test_bt1272_review_fixture_scores_review():
    d = run_cli("examples/bt1269_diam12_review_candidate.json")
    assert d["candidate_id"] == "wrong_full_order_diam12"
    assert d["band"] == "review"
    assert d["score"] == 2
    assert "diameter14" in d["missing_gates"]


def test_bt1272_sparse_fixture_scores_fail():
    d = run_cli("examples/bt1269_full_closure_sparse_candidate.json")
    assert d["candidate_id"] == "full_closure_sparse"
    assert d["band"] == "fail"
    assert d["score"] == 1


def test_bt1272_not_full_fixture_scores_fail():
    d = run_cli("examples/bt1269_not_full_order_candidate.json")
    assert d["candidate_id"] == "not_full_order"
    assert d["band"] == "fail"
    assert d["score"] == 0
