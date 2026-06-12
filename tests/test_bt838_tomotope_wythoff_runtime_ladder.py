#!/usr/bin/env python3
"""Focused direct test for BT838 tomotope Wythoff runtime ladder."""
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


def test_bt838_tomotope_wythoff_runtime_ladder():
    run_script("analysis/bt838_tomotope_wythoff_runtime_ladder.py")
    data = load_json("data/bt838_tomotope_wythoff_runtime_ladder.json")
    assert all(data["checks"].values())
    assert list(data["source_operation_vertices"].values()) == [4, 12, 24, 48, 96]
    assert data["source_operation_vertices"]["maximal_expanded_tomotope"] == 48
    assert data["source_operation_vertices"]["omnitruncated_tomotope"] == 96
    assert all(
        row["expanded_packet_slots"] == row["bt832_lifted_capacity"]
        for row in data["cover_scaled_ladder"]
    )
    assert all(
        row["full_flags"] == row["bt831_Wk_order"]
        for row in data["cover_scaled_ladder"]
    )


if __name__ == "__main__":
    test_bt838_tomotope_wythoff_runtime_ladder()
    print("BT838 tomotope Wythoff runtime ladder test passed")
