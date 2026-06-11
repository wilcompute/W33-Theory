#!/usr/bin/env python3
"""Focused direct tests for BT828-BT831 holonet runtime architecture."""
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


def test_bt828_packet_compiler():
    run_script("analysis/bt828_holonet_packet_compiler.py")
    data = load_json("data/bt828_holonet_packet_compiler.json")
    assert data["compiler_contract"]["per_digit_bound"].endswith("reversible_moves <= 8")
    assert all(data["checks"].values())
    stress = data["compiled_programs"][-1]
    assert stress["program"] == "six_digit_stress"
    assert stress["level"] == 6
    assert stress["route_bound"] == 48
    assert stress["fits_bt827_bound"]


def test_bt829_fault_sentinel_monitor():
    run_script("analysis/bt828_holonet_packet_compiler.py")
    run_script("analysis/bt829_fault_sentinel_monitor.py")
    data = load_json("data/bt829_fault_sentinel_monitor.json")
    assert data["projector_profile"]["trace"] == "15"
    assert all(data["checks"].values())
    rows = {row["fault"]: row for row in data["fault_signatures"]}
    assert rows["context_line_K4"]["sentinel_energy"] == "0"
    assert rows["single_point_impulse"]["sentinel_energy"] == "3/8"
    assert rows["gauge_neighbor_shell_12"]["sentinel_fraction"] == "5/7"


def test_bt830_two_phase_commit_clock():
    run_script("analysis/bt828_holonet_packet_compiler.py")
    run_script("analysis/bt830_two_phase_commit_clock.py")
    data = load_json("data/bt830_two_phase_commit_clock.json")
    assert all(data["checks"].values())
    assert data["sync_levels_1_to_24"][:4] == [1, 2, 3, 4]
    assert data["desync_levels_1_to_24"][0] == 5
    assert all(row["prepare_fits_commit_phase"] for row in data["sample_program_commit_fit"])


def test_bt831_tomotope_minimal_cover_boundary():
    run_script("analysis/bt831_tomotope_minimal_cover_architecture.py")
    data = load_json("data/bt831_tomotope_minimal_cover_architecture.json")
    assert all(data["checks"].values())
    assert data["source_facts"]["monodromy_order"] == 18432
    assert data["architecture_interpretation"]["abi"].startswith("BT814 48-block")
    assert data["cover_indices_tested"][0]["MonQk_order"] == 36864 * 3**6


if __name__ == "__main__":
    test_bt828_packet_compiler()
    test_bt829_fault_sentinel_monitor()
    test_bt830_two_phase_commit_clock()
    test_bt831_tomotope_minimal_cover_boundary()
    print("BT828-BT831 holonet runtime tests passed")
