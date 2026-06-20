#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool(path: str):
    proc = subprocess.run([sys.executable, str(ROOT / path)], cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(proc.stdout)


def test_bt1393_ladder_consistency_audit_runs_true():
    out = run_tool("tools/bt1393_ladder_consistency_audit.py")
    assert out["bt"] == 1393
    assert out["verified"] is True
    assert out["first_crossing"] == 6


def test_bt1394_reduced_qutrit_demonstrator_runs_true():
    out = run_tool("tools/bt1394_reduced_qutrit_demonstrator.py")
    assert out["bt"] == 1394
    assert out["verified"] is True
    assert abs(out["V_F"] - 1/3) < 1e-12
    data = json.loads((ROOT / "data" / "bt1394_reduced_qutrit_demonstrator.json").read_text(encoding="utf-8"))
    assert data["checks"]["route_reduced_state_maximally_mixed"] is True


def test_bt1395_maxsat_bound_pathway_runs_true():
    out = run_tool("tools/bt1395_s3_maxsat_bound_pathway.py")
    assert out["bt"] == 1395
    assert out["verified"] is True
    assert out["optimality_status"] == "witness_only"
    data = json.loads((ROOT / "data" / "bt1395_s3_maxsat_bound_pathway.json").read_text(encoding="utf-8"))
    assert data["accepted_certificate_schema"] == "schema/bt1395_s3_maxsat_certificate.schema.json"
