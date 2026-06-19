#!/usr/bin/env python3
"""Focused regression for BT1313-BT1315 holonet engineering closure."""
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


def test_bt1313_bt1315_holonet_optimality_stability_physical_budget():
    run_script("analysis/bt1313_entropy_router_optimality_certificate.py")
    run_script("analysis/bt1314_deterministic_traffic_stability.py")
    run_script("analysis/bt1315_parametric_photonic_loss_budget.py")

    bt1313 = load_json("data/bt1313_entropy_router_optimality_certificate.json")
    assert bt1313["verified"] is True
    assert all(bt1313["checks"].values())
    assert bt1313["bounds"]["one_epoch_capacity"] == 2160
    hot_540 = bt1313["one_hot_certificates"]["540"]
    assert hot_540["minimum_nonempty_charts"] == 135
    assert hot_540["minimum_max_cyclic_displacement"] == 134
    assert hot_540["minimum_mean_cyclic_displacement"] == "67/1"
    hot_full = bt1313["one_hot_certificates"]["2160"]
    assert hot_full["minimum_nonempty_charts"] == 540
    assert hot_full["minimum_max_cyclic_displacement"] == 539
    assert hot_full["minimum_mean_cyclic_displacement"] == "539/2"
    cases = bt1313["bt1310_case_comparison"]
    assert cases["all_to_one_collapse"]["nonempty_charts"] == 135
    assert cases["all_to_one_collapse"]["max_displacement"] == 134
    assert cases["over_capacity_five_per_chart"]["accepted"] == 2160
    assert cases["over_capacity_five_per_chart"]["rejected"] == 540

    bt1314 = load_json("data/bt1314_deterministic_traffic_stability.json")
    assert bt1314["verified"] is True
    assert all(bt1314["checks"].values())
    traffic = bt1314["cases"]
    raw_540 = traffic["one_packet_per_chart_randomized"]["raw"]
    assert raw_540["backlog_after_one_epoch_mean"] > 0
    assert raw_540["hot_charts_mean"] > 0
    raw_1620 = traffic["q_packets_per_chart_randomized"]["raw"]
    assert raw_1620["backlog_after_one_epoch_mean"] == 168.5
    raw_2160 = traffic["saturated_randomized"]["raw"]
    assert raw_2160["backlog_after_one_epoch_mean"] == 420.5
    for name in [
        "one_packet_per_chart_randomized",
        "q_packets_per_chart_randomized",
        "saturated_randomized",
    ]:
        routed = traffic[name]["routed"]
        assert routed["backlog_after_one_epoch_max"] == 0
        assert routed["rejected_max"] == 0
        assert routed["max_chart_load_max"] == 4
    overflow = traffic["overflow_randomized"]["routed"]
    assert overflow["accepted_min"] == 2160
    assert overflow["accepted_max"] == 2160
    assert overflow["rejected_min"] == 540
    assert overflow["rejected_max"] == 540

    bt1315 = load_json("data/bt1315_parametric_photonic_loss_budget.json")
    assert bt1315["verified"] is True
    assert all(bt1315["checks"].values())
    base = bt1315["level_rows"][0]
    assert base["detector_windows"] == 540
    assert base["mirror_slots"] == 2160
    assert (
        base["scenario_costs"]["equal_active_pulse_cost"]["total_first_order_cost"]
        == "3240/1"
    )
    assert (
        base["scenario_costs"]["delay_double_cost"]["total_first_order_cost"]
        == "4860/1"
    )
    assert (
        base["scenario_costs"]["equal_active_plus_idle_tenth"]["total_first_order_cost"]
        == "3348/1"
    )
    level6 = bt1315["level_rows"][-1]
    assert level6["w33_instances"] == 105025641
    assert level6["detector_windows"] == 56713846140
    assert level6["mirror_slots"] == 226855384560
    assert (
        level6["scenario_costs"]["equal_active_pulse_cost"]["total_first_order_cost"]
        == "340283076840/1"
    )


if __name__ == "__main__":
    test_bt1313_bt1315_holonet_optimality_stability_physical_budget()
    print("BT1313-BT1315 holonet optimality/stability/budget test passed")
