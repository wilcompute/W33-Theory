#!/usr/bin/env python3
"""Focused regression for BT1307-BT1309 holonet runtime refinements."""
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


def test_bt1307_bt1309_holonet_latency_collision_pulse_budget():
    run_script("analysis/w33_holonet_physical_stack.py")
    run_script("analysis/bt1307_holonet_latency_classes.py")
    run_script("analysis/bt1308_adversarial_collision_stress.py")
    run_script("analysis/bt1309_photonic_pulse_budget.py")

    bt1307 = load_json("data/bt1307_holonet_latency_classes.json")
    assert bt1307["verified"] is True
    assert all(bt1307["checks"].values())
    assert [row["completion_tick_tau"] for row in bt1307["latency_classes"]] == [
        4,
        5,
        6,
        7,
        8,
    ]
    assert all(row["route_count"] == 108 for row in bt1307["latency_classes"])
    summary = bt1307["latency_summary"]
    assert summary["mean_completion_tau"] == 6
    assert summary["compute_utilization"] == "3/4"
    assert summary["instruction_slack"] == "1/4"
    assert summary["dual_utilization_identity"] == "3/4 compute + 1/4 mirror = 1"

    bt1308 = load_json("data/bt1308_adversarial_collision_stress.json")
    assert bt1308["verified"] is True
    assert all(bt1308["checks"].values())
    by_case = {row["case"]: row for row in bt1308["stress_cases"]}
    assert by_case["balanced_atlas"]["global_utilization"] == "1/4"
    assert by_case["balanced_atlas"]["epochs_needed"] == 1
    assert by_case["q_per_chart"]["global_utilization"] == "3/4"
    assert by_case["q_per_chart"]["stable_after_one_epoch"] is True
    assert by_case["saturated_q_plus_1"]["global_utilization"] == "1/1"
    assert by_case["saturated_q_plus_1"]["stable_after_one_epoch"] is True
    assert by_case["first_global_overflow"]["backlog_after_one_epoch"] == 540
    assert by_case["single_hot_chart_boundary"]["global_utilization"] == "34/135"
    assert by_case["single_hot_chart_boundary"]["backlog_after_one_epoch"] == 1
    assert by_case["all_to_one_collapse"]["global_utilization"] == "1/4"
    assert by_case["all_to_one_collapse"]["epochs_needed"] == 135

    bt1309 = load_json("data/bt1309_photonic_pulse_budget.json")
    assert bt1309["verified"] is True
    assert all(bt1309["checks"].values())
    word = bt1309["scheduled_window_hierarchy"]["word"]
    assert word["qutrit_axis_windows"] == 3
    assert word["delay_hop_windows"] == 5
    assert word["total_windows"] == 8
    frame = bt1309["scheduled_window_hierarchy"]["microframe"]
    assert frame["qutrit_axis_windows"] == 27
    assert frame["delay_hop_windows"] == 45
    assert frame["total_windows"] == 72
    active = bt1309["full_atlas_active_budget"]
    assert active["active_qutrit_axis_pulses"] == 1620
    assert active["active_delay_hop_pulses"] == 1620
    assert active["active_family_ratio"] == "1620:1620 = 1:1"
    assert active["idle_windows"] == 1080


if __name__ == "__main__":
    test_bt1307_bt1309_holonet_latency_collision_pulse_budget()
    print("BT1307-BT1309 holonet latency/collision/pulse test passed")
