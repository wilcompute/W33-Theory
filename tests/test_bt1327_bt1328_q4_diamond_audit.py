#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1327_q4_diamond_audit_flags_literal_lcm():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1327_q4_diamond_audit.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1327
    assert out["failed"] == ["epoch_lcm_10980"]
    data = json.loads((ROOT / "data" / "bt1327_q4_diamond_audit.json").read_text(encoding="utf-8"))
    assert data["values"]["literal_lcm_3660_1620"] == 98820
    assert data["values"]["claimed_epoch"] == 10980


def test_bt1328_epoch_repair_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1328_epoch_repair.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1328
    assert out["verified"] is True
    assert out["epoch"] == 10980
    data = json.loads((ROOT / "data" / "bt1328_epoch_repair.json").read_text(encoding="utf-8"))
    assert data["values"]["rolling_offset"] == 180
    assert data["values"]["phase_closure_steps"] == 3
    assert data["checks"]["literal_lcm_not_epoch"] is True


def test_bt1328_proof_note_states_correction():
    text = (ROOT / "proofs" / "BT1328_rolling_epoch_repair.md").read_text(encoding="utf-8")
    assert "3*3660 = 10980" in text
    assert "not lcm(3660,1620)" in text
