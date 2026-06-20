#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1378_runtime_contract_verifier_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1378_verify_runtime_contract.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1378
    assert out["verified"] is True


def test_bt1379_s3_gauge_max2csp_spec_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1379_verify_s3_gauge_max2csp_spec.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1379
    assert out["verified"] is True
    assert out["constraints"] == 540
    assert out["current_identity_score"] == 210


def test_bt1380_post_1377_bridge_index_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1380_verify_post_1377_bridge_index.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1380
    assert out["verified"] is True
    assert out["claim_count"] == 9
    index = json.loads((ROOT / "data" / "bt1380_post_1377_bridge_index.json").read_text(encoding="utf-8"))
    assert index["checks"]["non_clifford_boundary_preserved"] is True
    assert index["paper_insert"] == "tex/bt1380_post_1377_claim_table.tex"
