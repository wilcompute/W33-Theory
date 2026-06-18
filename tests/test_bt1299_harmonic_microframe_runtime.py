#!/usr/bin/env python3
"""Focused direct regression for BT1299 harmonic microframe runtime."""
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


def test_bt1299_harmonic_microframe_runtime():
    run_script("analysis/w33_universal_oscillator_stack.py")
    run_script("analysis/bt827_holonet_fractal_architecture.py")
    run_script("analysis/bt828_holonet_packet_compiler.py")
    run_script("analysis/bt838_tomotope_wythoff_runtime_ladder.py")
    run_script("analysis/bt1299_harmonic_microframe_runtime.py")

    data = load_json("data/bt1299_harmonic_microframe_runtime.json")
    assert data["verified"] is True
    assert all(data["checks"].values())

    microframe = data["microframe"]
    assert microframe["route_tick"] == 8
    assert microframe["oscillator_horizon_total"] == 72
    assert microframe["oscillator_horizon_payload"] == 66
    assert microframe["oscillator_horizon_parity"] == 6
    assert microframe["route_digits_per_frame"] == 9
    assert microframe["first_full_route_frame_depth"] == 9

    mirror = data["mirror_bus"]
    assert mirror["identity"] == "2160 = 30*72"
    assert mirror["frames_per_mirror_bus"] == 30
    assert mirror["payload_slots"] == 1980
    assert mirror["parity_slots"] == 180

    runtime = data["runtime_supercycle"]
    assert runtime["old_factorization"] == "24*45*48"
    assert runtime["new_factorization"] == "24*30*72"
    assert runtime["frame_factorization"] == "720*72"
    assert runtime["runtime_order"] == 51840
    assert runtime["runtime_frames"] == 720
    assert runtime["s6_order"] == runtime["sp4_2_order"] == 720
    assert runtime["basis_change_ratio"] == "45/30 = 72/48 = q/lambda = 3/2"

    tomotope = data["tomotope_to_oscillator"]
    assert tomotope["total_completion"] == "48 + 24 = 72"
    assert tomotope["payload_completion"] == "48 + 18 = 66"
    assert tomotope["parity_completion"] == "72 - 66 = 6"

    commit = data["commit_clock"]["table"]
    assert [row["mod_horizon_frame"] for row in commit[:6]] == [24, 48, 0, 24, 48, 0]
    assert [row["level"] for row in commit if row["frame_locked"]] == [3, 6, 9, 12]
    assert commit[2]["oscillator_frames"] == 19

    rows = data["fractal_scaling"]["rows"]
    assert all(row["mirror_frame_identity_holds"] for row in rows)
    assert all(row["runtime_frame_identity_holds"] for row in rows)
    assert rows[0]["mirror_frames_total"] == 30
    assert rows[0]["runtime_frames_total"] == 720
    assert rows[-1]["route_bound_as_frame_fraction"] == "2/3"


if __name__ == "__main__":
    test_bt1299_harmonic_microframe_runtime()
    print("BT1299 harmonic microframe runtime test passed")
