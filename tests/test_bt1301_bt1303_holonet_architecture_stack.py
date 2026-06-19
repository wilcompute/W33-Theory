#!/usr/bin/env python3
"""Focused regression for BT1301-BT1303 holonet architecture stack."""
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


def test_bt1301_bt1303_holonet_architecture_stack():
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

    bt1301 = load_json("data/bt1301_full_chart_atlas_isa_compiler.json")
    assert bt1301["verified"] is True
    assert all(bt1301["checks"].values())
    assert bt1301["contract"]["chart_routes"] == 540
    assert bt1301["contract"]["ticks_per_word"] == 8
    assert bt1301["contract"]["candidate_digits"] == [7, 15, 23, 31, 39]
    assert bt1301["contract"]["active_tick_histogram"] == {
        "4": 108,
        "5": 108,
        "6": 108,
        "7": 108,
        "8": 108,
    }
    assert bt1301["contract"]["apartment_hop_histogram"] == {
        "1": 108,
        "2": 108,
        "3": 108,
        "4": 108,
        "5": 108,
    }
    assert len(bt1301["atlas_routes"]) == 540
    assert sorted(route["target_chart"] for route in bt1301["atlas_routes"]) == list(
        range(540)
    )
    assert all(route["xor_axes"] == [0, 1, 2] for route in bt1301["atlas_routes"])

    bt1302 = load_json("data/bt1302_parity_epilogue_reroute_protocol.json")
    assert bt1302["verified"] is True
    assert all(bt1302["checks"].values())
    assert bt1302["protocol"]["recovery_actions"] == 3240
    assert bt1302["protocol"]["changed_actions"] == 540
    assert bt1302["protocol"]["max_recovery_active_ticks"] == 8
    assert [lane["lane"] for lane in bt1302["protocol"]["parity_lanes"]] == [
        66,
        67,
        68,
        69,
        70,
        71,
    ]
    assert len(bt1302["recovery_table"]) == 540 * 6
    assert all(row["avoids_failed_pair"] for row in bt1302["recovery_table"])

    bt1303 = load_json("data/bt1303_holonet_stack_contract.json")
    assert bt1303["verified"] is True
    assert all(bt1303["checks"].values())
    handoffs = bt1303["exact_handoffs"]
    assert handoffs["route_word"] == "8 = 2^q ticks"
    assert handoffs["tomotope_body"] == "48 = q! * 2^q = 6 route words"
    assert (
        handoffs["parity_epilogue"]
        == "24 = q * 2^q = 3 route words = 18 payload + 6 parity"
    )
    assert handoffs["microframe"] == "72 = q^2 * 2^q = 48 + 24"
    assert handoffs["mirror_bus"] == "2160 = 30 * 72 = 540 * 4"
    assert handoffs["supercycle"] == "51840 = 24 * 2160 = 720 * 72"
    assert bt1303["fractal_route_table"][5]["route_ticks"] == 48
    assert bt1303["fractal_route_table"][8]["route_ticks"] == 72
    assert [layer["layer"] for layer in bt1303["stack_layers"]] == list(range(9))


if __name__ == "__main__":
    test_bt1301_bt1303_holonet_architecture_stack()
    print("BT1301-BT1303 holonet architecture stack test passed")
