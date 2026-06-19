#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1295_readiness_badge_and_doc():
    badge = ROOT / "data" / "bt1295_v1_release_readiness_badge.json"
    doc = ROOT / "docs" / "v1_release_readiness.md"
    assert badge.exists()
    assert doc.exists()
    data = json.loads(badge.read_text(encoding="utf-8"))
    assert data["ready"] is True
    assert data["release_target"] == "v1.0.0"
    assert data["strict_target"] == "diam14_polar_path"
    assert data["expected_outputs"]["strict_score_out_of_5"] == 5
    text = doc.read_text(encoding="utf-8")
    assert "ready = true" in text
    assert "v1.0.0" in text
    assert "diam14_polar_path" in text


def test_bt1296_readiness_badge_verifier_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1296_verify_release_readiness_badge.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1296
    assert out["verified"] is True
