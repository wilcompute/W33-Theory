#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1327_q4_diamond_audit_runs_and_flags_epoch():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1327_q4_diamond_audit.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1327
    assert out["all_exact_checks_pass"] is False
    assert out["failed"] == ["epoch_lcm_10980"]
    data = json.loads((ROOT / "data" / "bt1327_q4_diamond_audit.json").read_text(encoding="utf-8"))
    assert data["values"]["literal_lcm_3660_1620"] == 98820
    assert data["values"]["claimed_epoch"] == 10980
    for key, ok in data["checks"].items():
        if key != "epoch_lcm_10980":
            assert ok is True


def test_bt1327_proof_note_records_lcm_issue():
    text = (ROOT / "proofs" / "BT1327_q4_diamond_audit.md").read_text(encoding="utf-8")
    assert "lcm(3660,1620) = 98820" in text
    assert "10,980 master epoch" in text
