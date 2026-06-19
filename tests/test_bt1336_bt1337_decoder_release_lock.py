#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_bt1336_erasure_distance_benchmark_runs_true():
    proc = subprocess.run([sys.executable, str(ROOT / "tools" / "bt1336_erasure_distance_benchmark.py")], cwd=ROOT, check=True, capture_output=True, text=True)
    out = json.loads(proc.stdout)
    assert out["bt"] == 1336
    assert out["verified"] is True
    data = json.loads((ROOT / "data" / "bt1336_erasure_distance_benchmark.json").read_text(encoding="utf-8"))
    assert data["n"] == 32
    assert data["k"] == 4
    assert data["d"] == 4
    assert "not a full ML" in data["boundary"]


def test_bt1337_release_index_includes_q4_paper_and_gates():
    data = json.loads((ROOT / "data" / "bt1303_v1_release_source_of_truth_index.json").read_text(encoding="utf-8"))
    assert ".github/workflows/q4-diamond-paper.yml" in data["workflows"]
    assert data["q4_diamond_paper"]["source"] == "paper/w33_q4_diamond_machine_audited_synthesis.tex"
    assert "data/bt1334_gk_threshold_capacity_gate.json" in data["machine_entrypoints"]
    assert "data/bt1335_foundry_layout_feasibility_gate.json" in data["machine_entrypoints"]
    assert "data/bt1336_erasure_distance_benchmark.json" in data["machine_entrypoints"]
    assert data["expected_outputs"]["q4_diamond_paper_compiled"] is True
