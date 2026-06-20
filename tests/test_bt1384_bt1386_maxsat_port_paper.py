#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1384_maxsat_export_manifest_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1384_export_s3_gauge_maxsat.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1384
    assert out["verified"] is True
    assert out["variables"] == 780
    assert out["clauses"] == 20626


def test_bt1385_hesse_sic_t_port_abi_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1385_hesse_sic_t_port_abi.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1385
    assert out["verified"] is True
    assert out["sic_outcomes"] == 9


def test_bt1386_paper_splice_and_pdf_manifest():
    tex = (ROOT / "paper" / "w33_q4_claim_stratified_master.tex").read_text(encoding="utf-8")
    manifest = json.loads((ROOT / "data" / "bt1386_claim_master_pdf_manifest.json").read_text(encoding="utf-8"))
    assert "tex/bt1380_post_1377_claim_table.tex" in tex
    assert "tex/bt1381_bt1383_runtime_frontier_insert.tex" in tex
    assert "Hesse-SIC/T Non-Clifford Port" in tex
    assert manifest["compiled_locally"] is True
    assert manifest["pages"] == 5
    assert manifest["render_verified"] is True
