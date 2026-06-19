#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1338_q4_chain_check_extraction_runs_and_flags_quotient_need():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1338_extract_q4_chain_checks.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1338
    assert out["k_naive"] == 0
    data = json.loads((ROOT / "data" / "bt1338_q4_chain_check_matrices.json").read_text(encoding="utf-8"))
    assert data["ranks"]["rank_boundary_1"] == 15
    assert data["ranks"]["rank_boundary_2"] == 17
    assert data["needed_for_w33_32_4_4"]["target_k"] == 4


def test_bt1339_optical_budget_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1339_optical_loss_crosstalk_budget.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1339
    assert out["verified"] is True
    data = json.loads((ROOT / "data" / "bt1339_optical_loss_crosstalk_budget.json").read_text(encoding="utf-8"))
    assert data["scenarios"]["conservative"]["total_loss_db"] <= 3.0
    assert data["scenarios"]["conservative"]["aggregate_crosstalk_db"] <= -20.0


def test_bt1340_extended_release_runner_exists():
    text = (ROOT / "tools" / "bt1340_run_extended_release_lock.sh").read_text(encoding="utf-8")
    assert "bt1338_extract_q4_chain_checks.py" in text
    assert "bt1339_optical_loss_crosstalk_budget.py" in text
    assert "BT1340 extended release lock passed" in text
