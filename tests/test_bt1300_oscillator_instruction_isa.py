#!/usr/bin/env python3
"""Focused direct regression for BT1300 oscillator instruction ISA."""
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


def test_bt1300_oscillator_instruction_isa():
    run_script("analysis/w33_horizon_f3_parity_matrix.py")
    run_script("analysis/w33_universal_oscillator_stack.py")
    run_script("analysis/bt827_holonet_fractal_architecture.py")
    run_script("analysis/bt828_holonet_packet_compiler.py")
    run_script("analysis/bt838_tomotope_wythoff_runtime_ladder.py")
    run_script("analysis/bt1299_harmonic_microframe_runtime.py")
    run_script("analysis/bt1300_oscillator_instruction_isa.py")

    data = load_json("data/bt1300_oscillator_instruction_isa.json")
    assert data["verified"] is True
    assert all(data["checks"].values())

    header = data["isa_header"]
    assert header["frame_lanes"] == 72
    assert header["payload_lanes"] == 66
    assert header["parity_lanes"] == 6
    assert header["route_digits_per_frame"] == 9
    assert header["ticks_per_digit"] == 8
    assert header["frame_split"] == "72 = 48 + 18 + 6"
    assert header["body_split"] == "48 = q! * 2^q"
    assert header["epilogue_split"] == "24 = q * 2^q = 18 payload + 6 parity"
    assert header["micro_ops"] == [
        "q3_xor_axis_0",
        "q3_xor_axis_1",
        "q3_xor_axis_2",
        "apartment_hop_0",
        "apartment_hop_1",
        "apartment_hop_2",
        "apartment_hop_3",
        "apartment_hop_4",
    ]

    assert data["edge_class_counts"] == {
        "row_edge": 18,
        "column_edge": 12,
        "mixed_edge": 36,
        "parity_symbol": 6,
    }

    lanes = data["lane_layout"]
    assert len(lanes) == 72
    assert all(lane["frame_region"] == "tomotope_body" for lane in lanes[:48])
    assert all(lane["frame_region"] == "local_lift_epilogue" for lane in lanes[48:])
    assert all(lane["kind"] == "payload" for lane in lanes[:66])
    assert all(lane["kind"] == "parity" for lane in lanes[66:])
    assert [lane["digit"] for lane in lanes[0::8]] == list(range(9))
    assert [lane["tick"] for lane in lanes[:8]] == list(range(8))

    by_name = {program["program"]: program for program in data["compiled_programs"]}
    assert by_name["local_flip"]["isa_active_ticks"] == 4
    assert by_name["single_digit_far"]["isa_active_ticks"] == 7
    assert by_name["two_digit_cross"]["isa_active_ticks"] == 12
    assert by_name["three_digit_far"]["isa_active_ticks"] == 19

    stress = by_name["six_digit_stress"]
    assert stress["route_bound"] == 48
    assert stress["isa_active_ticks"] == 47
    assert stress["fits_tomotope_body"] is True
    assert stress["route_bound"] - stress["isa_active_ticks"] == 1
    assert max(stress["active_lanes"]) < 48

    assert all(
        program["active_ticks_match_bt828"] and program["fits_microframe"]
        for program in data["compiled_programs"]
    )


if __name__ == "__main__":
    test_bt1300_oscillator_instruction_isa()
    print("BT1300 oscillator instruction ISA test passed")
