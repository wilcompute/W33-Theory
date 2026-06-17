#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(rel: str):
    subprocess.run([sys.executable, str(ROOT / rel)], cwd=ROOT, check=True)


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def test_bt1274_batch_candidate_scores():
    run("tools/bt1274_batch_score_candidates.py")
    d = load("data/bt1274_batch_candidate_scores_summary.json")
    assert d["candidate_count"] == 4
    assert d["band_counts"] == {"fail": 2, "pass": 1, "review": 1}
    rows = {r["candidate_id"]: r for r in d["rows"]}
    assert rows["exact_polar_path"]["band"] == "pass"
    assert rows["wrong_full_order_diam12"]["band"] == "review"
    assert rows["full_closure_sparse"]["band"] == "fail"
    assert rows["not_full_order"]["score"] == 0


def test_bt1275_strict_certificate_fields():
    d = load("data/bt1275_strict_polar_path_recovery_certificate.json")
    assert d["target"] == "diam14_polar_path"
    assert d["closure"]["order"] == 51840
    assert d["word_metric"]["diameter"] == 14
    assert d["edge_geometry"]["polar_graph"] == "P4"
    assert d["edge_geometry"]["nonpolar_graph"] == "P4"
    assert d["labelled_geodesic"]["channel_spread"] == 172
    assert d["score_vector"]["values"] == [1, 1, 1, 1, 1]
    assert d["validator_result"]["band"] == "pass"


def test_bt1276_external_protocol_section():
    sec = ROOT / "paper" / "sections" / "sec_bt1276_external_candidate_protocol.tex"
    assert sec.exists()
    text = sec.read_text(encoding="utf-8")
    assert "External candidate protocol" in text
    assert "(C,D,P,E,L)" in text
    assert "exact polar path" in text
    assert "5/5" in text
