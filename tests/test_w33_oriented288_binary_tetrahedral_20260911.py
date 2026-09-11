#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis" / "w33_oriented288_binary_tetrahedral_bridge.py"
OUT = ROOT / "data" / "w33_oriented288_binary_tetrahedral_bridge.json"


def test_oriented_288_is_binary_tetrahedral_local_clifford() -> None:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(proc.stdout)
    assert summary == {
        "GL4": [2, 9, 1, 4],
        "full_check": True,
        "order": 288,
        "status": "PASS",
    }

    data = json.loads(OUT.read_text(encoding="utf-8"))
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["W33_oriented_288"]["structure"] == "2_+^{1+4} : (C3 x C3)"
    assert data["binary_tetrahedral_local_Clifford"]["literature_GAP_id"] == "SmallGroup(288,860)"
    assert data["W33_oriented_288"]["element_orders"] == {
        "1": 1,
        "2": 19,
        "3": 80,
        "4": 12,
        "6": 80,
        "12": 96,
    }
    assert data["W33_oriented_288"]["element_orders"] == data["binary_tetrahedral_local_Clifford"]["element_orders"]
    assert data["explicit_isomorphism"]["GL4_conjugator_columns"] == [2, 9, 1, 4]
    assert data["explicit_isomorphism"]["full_288_squared_homomorphism_check"] is True


if __name__ == "__main__":
    test_oriented_288_is_binary_tetrahedral_local_clifford()
    print("oriented-288 binary-tetrahedral regression passed")
