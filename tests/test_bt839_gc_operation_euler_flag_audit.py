#!/usr/bin/env python3
"""Focused direct test for BT839 GC operation Euler/flag audit."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    with (ROOT / relpath).open() as f:
        return json.load(f)


def test_bt839_gc_operation_euler_flag_audit():
    run_script("analysis/bt839_gc_operation_euler_flag_audit.py")
    data = load_json("data/bt839_gc_operation_euler_flag_audit.json")
    assert all(data["checks"].values())
    assert data["euler_charge"] == {
        "11_cell": [-11],
        "57_cell": [-57],
        "tomotope_partial_b": [-4],
    }
    bridge = data["regular_polychoron_bridge"]
    assert bridge["primary_pairing"]["11_cell_to_600_cell"]["score"] == 2
    assert bridge["primary_pairing"]["57_cell_to_120_cell"]["score"] == 3
    assert bridge["regular_polychoron_counts"]["24_cell"]["edges"] == 96
    assert data["flag_bridge"]["57_cell"]["petersen_home_plus_sentinel_sheet"] == 3420


if __name__ == "__main__":
    test_bt839_gc_operation_euler_flag_audit()
    print("BT839 GC operation Euler/flag audit test passed")
