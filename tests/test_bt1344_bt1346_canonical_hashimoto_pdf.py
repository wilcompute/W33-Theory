#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1344_quotient_canonicalization_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1344_canonicalize_q4_quotient.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1344
    assert out["verified"] is True
    assert out["orbit_size"] == 384
    assert out["stabilizer_size"] == 1


def test_bt1345_hashimoto_matrix_falsifier_runs_and_records_correction():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1345_hashimoto_matrix_falsifier.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1345
    assert out["verified"] is True
    assert out["protocol_targets_match_standard_hashimoto"] is False
    data = json.loads((ROOT / "data" / "bt1345_hashimoto_matrix_summary.json").read_text(encoding="utf-8"))
    assert data["graph"]["directed_edges"] == 480
    assert data["hashimoto_phase_clusters_deg"]["72.452"] == 48
    assert data["hashimoto_phase_clusters_deg"]["127.087"] == 30


def test_bt1346_claim_stratified_pdf_workflow_and_manifest():
    wf = (ROOT / ".github" / "workflows" / "q4-claim-stratified-paper.yml").read_text(encoding="utf-8")
    manifest = json.loads((ROOT / "data" / "bt1346_pdf_manifest.json").read_text(encoding="utf-8"))
    assert "pdflatex" in wf
    assert "w33_q4_claim_stratified_master.tex" in wf
    assert "w33_q4_claim_stratified_master.pdf" in wf
    assert manifest["compiled"] is True
    assert manifest["pages"] == 4
    for label in ["EXACT", "CERT", "STRUCT", "SIM", "ENG", "SPEC"]:
        assert label in manifest["claim_classes"]
