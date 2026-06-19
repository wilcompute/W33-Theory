#!/usr/bin/env python3
"""Focused regression for BT1310-BT1312 holonet network-control laws."""
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


def test_bt1310_bt1312_holonet_entropy_admission_pulse_scaling():
    run_script("analysis/bt1310_entropy_preserving_router.py")
    run_script("analysis/bt1311_mirror_admission_control.py")
    run_script("analysis/bt1312_recursive_pulse_energy_scaling.py")

    bt1310 = load_json("data/bt1310_entropy_preserving_router.json")
    assert bt1310["verified"] is True
    assert all(bt1310["checks"].values())
    assert bt1310["router"]["capacity"] == 2160
    routed = bt1310["routed_cases"]
    assert routed["balanced_atlas"]["zero_displacement_packets"] == 540
    assert routed["balanced_atlas"]["max_chart_load"] == 1
    assert routed["q_per_chart"]["zero_displacement_packets"] == 1620
    assert routed["q_per_chart"]["max_chart_load"] == 3
    assert routed["saturated_q_plus_1"]["zero_displacement_packets"] == 2160
    assert routed["saturated_q_plus_1"]["max_chart_load"] == 4
    assert routed["single_hot_chart_boundary"]["epochs_needed"] == 1
    assert routed["single_hot_chart_boundary"]["rejected"] == 0
    assert routed["all_to_one_collapse"]["epochs_needed"] == 1
    assert routed["all_to_one_collapse"]["nonempty_charts"] == 135
    assert routed["over_capacity_five_per_chart"]["accepted"] == 2160
    assert routed["over_capacity_five_per_chart"]["rejected"] == 540

    bt1311 = load_json("data/bt1311_mirror_admission_control.json")
    assert bt1311["verified"] is True
    assert all(bt1311["checks"].values())
    cases = bt1311["admission_cases"]
    assert cases["balanced_atlas"]["first_epoch_utilization"] == "1/4"
    assert cases["q_per_chart"]["first_epoch_utilization"] == "3/4"
    assert cases["saturated"]["first_epoch_utilization"] == "1/1"
    assert cases["first_overflow"]["spill_after_epoch_0"] == 540
    assert cases["double_plus_one"]["epochs_needed"] == 3
    assert cases["double_plus_one"]["final_epoch_packets"] == 1
    serial = cases["level6_one_packet_per_chart_serialized"]
    assert serial["arrival_packets"] == 105025641 * 540
    assert serial["epochs_needed"] == 26256411
    parallel = bt1311["parallel_admission_cases"][
        "level6_one_packet_per_chart_parallel"
    ]
    assert parallel["parallel_capacity"] == 2160 * 105025641
    assert parallel["epochs_needed"] == 1
    assert parallel["first_epoch_utilization"] == "1/4"

    bt1312 = load_json("data/bt1312_recursive_pulse_energy_scaling.json")
    assert bt1312["verified"] is True
    assert all(bt1312["checks"].values())
    rows = bt1312["scaling_rows"]
    assert [row["w33_instances"] for row in rows] == [
        1,
        41,
        1641,
        65641,
        2625641,
        105025641,
    ]
    for row in rows:
        assert row["qutrit_axis_pulses"] == row["delay_hop_pulses"]
        assert row["active_total_pulses"] * 4 == row["reserved_windows"] * 3
        assert row["idle_windows"] * 4 == row["reserved_windows"]
        assert row["compute_utilization"] == "3/4"
        assert row["mirror_transport_utilization"] == "1/4"
    assert rows[-1]["qutrit_axis_pulses"] == 170141538420
    assert rows[-1]["delay_hop_pulses"] == 170141538420


if __name__ == "__main__":
    test_bt1310_bt1312_holonet_entropy_admission_pulse_scaling()
    print("BT1310-BT1312 holonet entropy/admission/pulse test passed")
