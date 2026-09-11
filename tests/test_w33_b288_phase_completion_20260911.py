#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_b288_phase_completion_no_go.py"
OUT = ROOT / "data" / "w33_b288_phase_completion_no_go.json"


def test_b288_has_inequivalent_residual_c2_phase_lifts() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(proc.stdout)
    assert summary == {
        "clifford_residual_derived": 48,
        "common_projective": "SmallGroup(288,1025)",
        "status": "PASS",
        "w33_derived": 96,
    }

    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["common_projective_group"]["order"] == 288
    assert data["w33_C2_lift"]["element_orders"] == {
        "1": 1,
        "2": 43,
        "3": 80,
        "4": 84,
        "6": 272,
        "12": 96,
    }
    assert data["complex_residual_C2_quotient"]["element_orders"] == {
        "1": 1,
        "2": 31,
        "3": 80,
        "4": 96,
        "6": 176,
        "12": 192,
    }
    assert data["complex_residual_C2_quotient"]["derived_order"] == 48
    assert data["w33_C2_lift"]["derived_order"] == 96
    assert data["complex_Clifford_C4_lift_literature_input"]["full_GAP_id"] == "SmallGroup(1152,155473)"


if __name__ == "__main__":
    test_b288_has_inequivalent_residual_c2_phase_lifts()
    print("B288 phase-completion no-go regression passed")
