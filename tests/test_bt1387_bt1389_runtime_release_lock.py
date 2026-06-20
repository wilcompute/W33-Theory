#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1387_maxsat_solver_harness_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1387_s3_maxsat_solver_harness.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1387
    assert out["verified"] is True
    assert out["optimality_status"] in {"unresolved", "solver_output_captured_requires_parse"}


def test_bt1388_hesse_sic_t_factory_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1388_hesse_sic_t_factory_model.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1388
    assert out["verified"] is True
    assert out["baseline_success"] > 0.87


def test_bt1389_runtime_release_lock_index():
    data = json.loads((ROOT / "data" / "bt1389_runtime_release_lock_index.json").read_text(encoding="utf-8"))
    runner = (ROOT / "tools" / "bt1389_run_runtime_frontier_release_lock.sh").read_text(encoding="utf-8")
    assert data["ready"] is True
    assert data["runner"] == "tools/bt1389_run_runtime_frontier_release_lock.sh"
    assert "tools/bt1384_export_s3_gauge_maxsat.py" in data["frontier_tools"]
    assert "tools/bt1388_hesse_sic_t_factory_model.py" in data["frontier_tools"]
    assert "BT1389 runtime frontier release lock passed" in runner
