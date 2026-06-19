#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1341_q4_gauge_quotient_runs_3244():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1341_q4_gauge_quotient_3244.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1341
    assert out["verified"] is True
    assert out["k"] == 4
    assert out["dx"] == 4
    assert out["dz"] == 4


def test_bt1342_hashimoto_falsifier_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1342_hashimoto_falsifier_simulator.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1342
    assert out["verified"] is True
    assert out["v"] == 40
    assert out["edges"] == 240


def test_bt1343_claim_stratified_master_paper():
    tex = (ROOT / "paper" / "w33_q4_claim_stratified_master.tex").read_text(encoding="utf-8")
    manifest = json.loads((ROOT / "data" / "bt1343_claim_stratified_master_manifest.json").read_text(encoding="utf-8"))
    for label in ["EXACT", "CERT", "STRUCT", "SIM", "ENG", "SPEC"]:
        assert label in tex
        assert label in manifest["claim_classes"]
    assert "BT1341" in tex
    assert "BT1342" in tex
    assert manifest["tex"] == "paper/w33_q4_claim_stratified_master.tex"
