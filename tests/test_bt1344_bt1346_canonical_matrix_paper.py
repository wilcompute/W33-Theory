#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1344_q4_quotient_canonicalization_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1344_canonicalize_q4_quotient.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1344
    assert out["verified"] is True
    assert out["orbit_size"] == 384
    assert out["stabilizer_size"] == 1


def test_bt1345_hashimoto_matrix_summary():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1345_hashimoto_matrix_falsifier.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1345
    assert out["verified"] is True
    assert out["protocol_targets_match_standard_hashimoto"] is False
    data = json.loads((ROOT / "data" / "bt1345_hashimoto_matrix_summary.json").read_text(encoding="utf-8"))
    assert data["hashimoto_phase_clusters_deg"]["72.452"] == 48
    assert data["hashimoto_phase_clusters_deg"]["127.087"] == 30


def test_bt1346_claim_stratified_pdf_manifest_and_tex():
    manifest = json.loads((ROOT / "data" / "bt1346_claim_stratified_pdf_manifest.json").read_text(encoding="utf-8"))
    tex = (ROOT / "paper" / "w33_q4_claim_stratified_master.tex").read_text(encoding="utf-8")
    assert manifest["compiled_locally"] is True
    assert manifest["pages"] == 4
    assert manifest["render_verified"] is True
    assert "BT1344" in tex
    assert "BT1345" in tex
    assert "72.452" in tex
    assert "127.087" in tex
