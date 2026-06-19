#!/usr/bin/env python3
"""Focused regression for BT1304-BT1306 holonet runtime physicalization."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_script(relpath: str) -> None:
    subprocess.run([sys.executable, str(ROOT / relpath)], cwd=ROOT, check=True)


def load_json(relpath: str) -> dict:
    with (ROOT / relpath).open(encoding="utf-8") as handle:
        return json.load(handle)


def test_bt1304_bt1306_holonet_runtime_physicalization():
    run_script("analysis/w33_horizon_f3_parity_matrix.py")
    run_script("analysis/w33_universal_oscillator_stack.py")
    run_script("analysis/bt827_holonet_fractal_architecture.py")
    run_script("analysis/bt828_holonet_packet_compiler.py")
    run_script("analysis/bt838_tomotope_wythoff_runtime_ladder.py")
    run_script("analysis/bt1299_harmonic_microframe_runtime.py")
    run_script("analysis/bt1300_oscillator_instruction_isa.py")
    run_script("analysis/bt1301_full_chart_atlas_isa_compiler.py")
    run_script("analysis/bt1302_parity_epilogue_reroute_protocol.py")
    run_script("analysis/bt1303_holonet_stack_contract.py")
    run_script("analysis/bt1304_holonet_contention_model.py")
    run_script("analysis/bt1305_mirror_bus_queueing_law.py")
    run_script("analysis/bt1306_physical_timing_model.py")

    bt1304 = load_json("data/bt1304_holonet_contention_model.json")
    assert bt1304["verified"] is True
    assert all(bt1304["checks"].values())
    contention = bt1304["contention_summary"]
    assert contention["atlas_packets"] == 540
    assert contention["target_chart_count"] == 540
    assert contention["output_port_conflicts"] == 0
    assert contention["mirror_bus_slots"] == 2160
    assert contention["mirror_bus_utilization"] == "540/2160 = 1/4"
    assert contention["mirror_phase_histogram"] == {
        "0": 135,
        "1": 135,
        "2": 135,
        "3": 135,
    }
    assert contention["active_tick_histogram"] == {
        "4": 108,
        "5": 108,
        "6": 108,
        "7": 108,
        "8": 108,
    }
    assert contention["tick_load"] == {
        "0": 540,
        "1": 540,
        "2": 540,
        "3": 540,
        "4": 432,
        "5": 324,
        "6": 216,
        "7": 108,
    }

    bt1305 = load_json("data/bt1305_mirror_bus_queueing_law.json")
    assert bt1305["verified"] is True
    assert all(bt1305["checks"].values())
    by_mode = {row["packets_per_chart"]: row for row in bt1305["traffic_modes"]}
    assert by_mode[1]["utilization"] == "1/4"
    assert by_mode[3]["utilization"] == "3/4"
    assert by_mode[4]["utilization"] == "1/1"
    assert by_mode[4]["stable_without_queue"] is True
    assert by_mode[5]["backlog_after_one_epoch_per_chart"] == 1
    assert by_mode[8]["epochs_needed"] == 2
    assert by_mode[9]["epochs_needed"] == 3
    assert all(row["utilization"] == "1/4" for row in bt1305["recursive_scaling"])
    assert all(row["slack_per_instance"] == 1620 for row in bt1305["recursive_scaling"])

    bt1306 = load_json("data/bt1306_physical_timing_model.json")
    assert bt1306["verified"] is True
    assert all(bt1306["checks"].values())
    schedule = bt1306["tick_schedule"]
    assert len(schedule) == 8
    assert [row["hardware"] for row in schedule[:3]] == [
        "tritter/EOM phase-address pulse",
        "tritter/EOM phase-address pulse",
        "tritter/EOM phase-address pulse",
    ]
    assert all(row["hardware"] == "delay-line switch pulse" for row in schedule[3:])
    assert [row["lane"] for row in bt1306["parity_windows"]] == [
        66,
        67,
        68,
        69,
        70,
        71,
    ]
    assert bt1306["durations"]["word"]["tau_units"] == 8
    assert bt1306["durations"]["tomotope_body"]["tau_units"] == 48
    assert bt1306["durations"]["parity_epilogue"]["tau_units"] == 24
    assert bt1306["durations"]["microframe"]["tau_units"] == 72
    assert bt1306["durations"]["mirror_bus_epoch"]["tau_units"] == 2160
    assert bt1306["durations"]["clifford_supercycle"]["tau_units"] == 51840


if __name__ == "__main__":
    test_bt1304_bt1306_holonet_runtime_physicalization()
    print("BT1304-BT1306 holonet runtime physicalization test passed")
