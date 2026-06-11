#!/usr/bin/env python3
"""Focused direct tests for BT832-BT834 holonet runtime extensions."""
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


def test_bt832_cover_indexed_durable_storage():
    run_script("analysis/bt832_cover_indexed_durable_storage.py")
    data = load_json("data/bt832_cover_indexed_durable_storage.json")
    assert all(data["checks"].values())
    first = data["cover_lifts"][0]
    assert first["cover_index"] == 3
    assert first["cover_counts"]["lifted_packet_slots"] == 48 * 3**3
    assert first["cover_counts"]["kernel_order_to_Q1"] == 3**6


def test_bt833_sentinel_aware_packet_rerouter():
    run_script("analysis/bt828_holonet_packet_compiler.py")
    run_script("analysis/bt833_sentinel_aware_packet_rerouter.py")
    data = load_json("data/bt833_sentinel_aware_packet_rerouter.json")
    assert all(data["checks"].values())
    assert any(
        len(route["waypoints"]) == 2
        for program in data["rerouted_programs"]
        for route in program["digit_routes"]
    )
    stress = data["rerouted_programs"][-1]
    assert stress["program"] == "six_digit_stress"
    assert stress["fits_commit_phase"]
    assert stress["sentinel_energy_reduction"] != "0"


def test_bt834_desync_guard_band_arithmetic():
    run_script("analysis/bt834_desync_guard_band_arithmetic.py")
    data = load_json("data/bt834_desync_guard_band_arithmetic.json")
    assert all(data["checks"].values())
    assert data["desync_levels_1_to_60"][0] == 5
    first = data["levels_1_to_60"][4]
    assert first["remainder"] == 24
    assert first["blockers"][0]["prime"] == 5
    assert first["blockers"][0]["order_of_7"] == 4


if __name__ == "__main__":
    test_bt832_cover_indexed_durable_storage()
    test_bt833_sentinel_aware_packet_rerouter()
    test_bt834_desync_guard_band_arithmetic()
    print("BT832-BT834 holonet runtime extension tests passed")
