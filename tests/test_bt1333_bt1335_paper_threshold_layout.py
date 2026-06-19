#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1333_repo_native_paper_and_workflow():
    tex = (ROOT / "paper" / "w33_q4_diamond_machine_audited_synthesis.tex").read_text(encoding="utf-8")
    wf = (ROOT / ".github" / "workflows" / "q4-diamond-paper.yml").read_text(encoding="utf-8")
    assert "Machine-Audited Master Synthesis" in tex
    assert "rolling chart-phase closure" in tex
    assert "q4-diamond-paper" in wf
    assert "pdflatex" in wf


def test_bt1334_threshold_capacity_gate_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1334_gk_threshold_capacity_gate.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1334
    assert out["verified"] is True
    data = json.loads((ROOT / "data" / "bt1334_gk_threshold_capacity_gate.json").read_text(encoding="utf-8"))
    assert data["checks"]["capacity_zero_at_50"] is True
    assert data["checks"]["capacity_zero_above_50"] is True
    assert "cannot push" in data["verdict"]


def test_bt1335_foundry_gate_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1335_foundry_layout_feasibility_gate.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1335
    assert out["verified"] is True
    assert out["base_channels"] == 4320
    data = json.loads((ROOT / "data" / "bt1335_foundry_layout_feasibility_gate.json").read_text(encoding="utf-8"))
    assert data["checks"]["base_channel_count_4320"] is True
    assert data["scenarios"]["conservative_cell"]["area_fits"] is True
    assert "70.8M" in data["interpretation"]
