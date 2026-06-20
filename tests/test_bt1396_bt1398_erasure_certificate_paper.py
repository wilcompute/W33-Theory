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


def test_bt1396_qutrit_erasure_readout_runs_true():
    out = run_tool("tools/bt1396_qutrit_quantum_erasure_readout.py")
    assert out["bt"] == 1396
    assert out["verified"] is True
    assert abs(out["p_eraser"] - 1/3) < 1e-12


def test_bt1397_example_optimality_certificate_runs_true_but_not_project_proof():
    out = run_tool("tools/bt1397_verify_example_optimality_certificate.py")
    assert out["bt"] == 1397
    assert out["verified"] is True
    assert out["project_optimality_status"] == "not_solver_certified"


def test_bt1398_paper_patch_manifest_and_content():
    manifest = json.loads((ROOT / "data" / "bt1398_claim_master_patch_manifest.json").read_text(encoding="utf-8"))
    tex = (ROOT / "paper" / "w33_q4_claim_stratified_master.tex").read_text(encoding="utf-8")
    assert manifest["verified"] is True
    assert "BT1393" in tex
    assert "BT1396" in tex
    assert "BT1397" in tex
    assert "quantum-erasure" in tex
    assert "not a solver-generated global optimality proof" in manifest["boundary"]
