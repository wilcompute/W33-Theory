#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_threeway_576_provenance_closure.py"
OUT = ROOT / "data" / "w33_threeway_576_provenance_closure.json"


def test_threeway_576_provenance_closes_exactly() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(proc.stdout)
    assert summary["status"] == "PASS"
    assert summary["order"] == 576
    assert summary["GL4"] == [6, 11, 7, 14]

    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert data["psp_minimum"]["derived_chain"] == [576, 96, 32]
    assert data["psp_minimum"]["orders"] == {
        "1": 1,
        "2": 43,
        "3": 80,
        "4": 84,
        "6": 272,
        "12": 96,
    }
    assert data["wf4"]["index2_kernels"]["long_root_parity"]["orders"] == data["psp_minimum"]["orders"]
    assert data["wf4"]["index2_kernels"]["short_root_parity"]["orders"] == data["psp_minimum"]["orders"]
    rotation = data["wf4"]["index2_kernels"]["total_reflection_parity_rotations"]["orders"]
    assert rotation["8"] == 144
    assert rotation != data["psp_minimum"]["orders"]
    iso = data["explicit_isomorphism"]
    assert iso["characteristic_kernel"] == "second derived subgroup 2_+^{1+4} of order 32"
    assert iso["quotient_action_order"] == 18
    assert iso["GL4_conjugator_columns"] == [6, 11, 7, 14]
    assert iso["full_576_squared_homomorphism_check"] is True
    assert iso["bijection"] is True


if __name__ == "__main__":
    test_threeway_576_provenance_closes_exactly()
    print("three-way 576 provenance regression passed")
