#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1381_s3_gauge_solver_probe_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1381_s3_gauge_global_solver_probe.py"), "--restarts", "20"], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1381
    assert out["verified"] is True
    assert out["best_score"] <= 210


def test_bt1382_non_clifford_port_abi_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1382_non_clifford_port_abi.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1382
    assert out["verified"] is True
    assert out["ports"] == 2


def test_bt1383_runtime_frontier_integration_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1383_verify_runtime_frontier_integration.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1383
    assert out["verified"] is True
    data = json.loads((ROOT / "data" / "bt1383_runtime_frontier_integration.json").read_text(encoding="utf-8"))
    assert "tex/bt1381_bt1383_runtime_frontier_insert.tex" in data["paper_inserts"]
    assert "data/bt1382_non_clifford_port_abi.json" in data["release_frontier_artifacts"]
