#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_binary_tetrahedral_split_swap_completion.py"
OUT = ROOT / "data" / "w33_binary_tetrahedral_split_swap_completion.json"


def test_w33_576_is_split_binary_tetrahedral_factor_swap_completion() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(proc.stdout)
    assert summary == {
        "GL4": [5, 10, 7, 9],
        "order": 576,
        "oriented_exact": True,
        "status": "PASS",
        "swap_exact": True,
    }

    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["common_interior"]["order"] == 288
    assert data["outer_swap"]["order"] == 2
    assert data["W33_completion"]["structure"] == "K_288 : C2 with honest factor swap"
    assert data["W33_completion"]["element_orders"] == {
        "1": 1,
        "2": 43,
        "3": 80,
        "4": 84,
        "6": 272,
        "12": 96,
    }
    assert data["explicit_isomorphism"]["GL4_conjugator_columns"] == [5, 10, 7, 9]
    assert data["explicit_isomorphism"]["full_576_squared_homomorphism_check"] is True


if __name__ == "__main__":
    test_w33_576_is_split_binary_tetrahedral_factor_swap_completion()
    print("binary-tetrahedral split-swap regression passed")
