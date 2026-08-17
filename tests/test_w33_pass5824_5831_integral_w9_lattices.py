from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_pass5824_5831_integral_w9_lattices.py"
RESULT = ROOT / "data" / "PART_W33_PASS5824_5831_INTEGRAL_W9_LATTICES.json"
MANIFEST = ROOT / "analysis" / "W33_CURRENT_FRONTIER_MANIFEST.tex"


def test_pass5824_5831_byte_exact_replay() -> None:
    before = RESULT.read_bytes()
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "PASS5824-5831: PASS" in proc.stdout
    assert RESULT.read_bytes() == before


def test_pass5824_5831_frozen_theorems() -> None:
    d = json.loads(RESULT.read_text())
    assert d["status"] == "PASS"
    p = d["pass_5824_saturated_lattices"]
    assert p["point_W9"] == "A3^3"
    assert p["heavy_W9"] == "A3^3"
    assert p["line_W9"] == "A3 tensor A3 after explicit GL4(2) coordinate relabel"
    assert p["point_heavy_discriminant"] == 64
    assert p["line_discriminant"] == 4096
    q = d["pass_5827_saturated_radon_snf"]
    assert q["R_transpose_A3cubed_to_A3tensorA3"] == [1, 1, 1, 1, 1, 2, 2, 4, 4]
    assert q["D_A3cubed_to_A3tensorA3"] == [1, 1, 1, 1, 1, 2, 2, 4, 4]
    assert q["H_transpose_A3cubed_to_A3cubed"] == [1, 1, 2, 2, 2, 2, 2, 4, 4]
    assert d["pass_5829_characteristic_two_firewall"]["mod2_ranks"] == {
        "Bcross": 1,
        "CH": 1,
        "CR": 1,
        "D": 8,
        "H": 4,
        "K9": 3,
        "R": 8,
    }


def test_pass5824_5831_promoted_once() -> None:
    needle = r"\input{analysis/PASS5824_5831_integral_w9_lattices_insert}%"
    assert MANIFEST.read_text().count(needle) == 1
