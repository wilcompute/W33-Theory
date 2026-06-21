#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool() -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "bt1406_tomotope_body_edge_pulse_scheduler.py"),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (ROOT / "data" / "bt1406_tomotope_body_edge_pulse_scheduler.json").read_text(
            encoding="utf-8"
        )
    )


def stress_schedule(data: dict) -> dict:
    return next(
        schedule
        for schedule in data["schedules"]
        if schedule["program"] == "six_digit_stress"
    )


def test_bt1406_pulse_scheduler_runs_true() -> None:
    out = run_tool()
    assert out == {
        "bt": 1406,
        "stress_edge_pulses": 48,
        "stress_idle_ticks": 0,
        "verified": True,
    }

    data = load_result()
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert data["body_ticks"] == 48
    assert [phase["pulse_op"] for phase in data["pulse_microcycle"]] == [
        "LOAD_FLAG",
        "FLIP_Q6_AXIS",
        "LATCH_VERTEX",
    ]


def test_bt1406_stress_route_fills_body_exactly() -> None:
    data = load_result()
    stress = stress_schedule(data)

    assert stress["q6_walk_steps"] == 16
    assert stress["edge_pulse_ticks"] == 48
    assert stress["idle_ticks"] == 0
    assert stress["fills_48_tick_body"] is True
    assert stress["packet_load_ticks"] == [0, 6, 12, 21, 27, 45]
    assert stress["pulse_op_histogram"] == {
        "FLIP_Q6_AXIS": 16,
        "LATCH_VERTEX": 16,
        "LOAD_FLAG": 16,
    }

    pulses = stress["pulses"]
    assert [pulse["body_tick"] for pulse in pulses] == list(range(48))
    assert [pulse["phase_trit"] for pulse in pulses] == [0, 1, 2] * 16
    assert [pulse["pulse_op"] for pulse in pulses[:3]] == [
        "LOAD_FLAG",
        "FLIP_Q6_AXIS",
        "LATCH_VERTEX",
    ]
    assert [pulse["pulse_op"] for pulse in pulses[-3:]] == [
        "LOAD_FLAG",
        "FLIP_Q6_AXIS",
        "LATCH_VERTEX",
    ]
    assert pulses[-3]["q6_edge_index"] == 77
    assert pulses[-3]["tomotope_flag"] == 180
    assert pulses[-3]["tomotope_block"] == 45
    assert pulses[-2]["source"] == "010111"
    assert pulses[-2]["target"] == "010011"
    assert pulses[-1]["target"] == "010011"


def test_bt1406_all_current_routes_have_valid_pulse_shells() -> None:
    data = load_result()
    profile = {
        schedule["program"]: (schedule["edge_pulse_ticks"], schedule["idle_ticks"])
        for schedule in data["schedules"]
    }
    assert profile == {
        "local_flip": (3, 45),
        "single_digit_far": (3, 45),
        "two_digit_cross": (9, 39),
        "three_digit_far": (27, 21),
        "six_digit_stress": (48, 0),
    }
    assert all(all(schedule["checks"].values()) for schedule in data["schedules"])


def test_bt1406_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    single = " ".join(
        (ROOT / "single_photon_universal_computation.tex")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "BT1406: tomotope-body edge pulse scheduler" in docs
    assert "BT1406_tomotope_body_edge_pulse_scheduler.md" in docs
    assert "BT1406 tomotope-body edge pulse scheduler" in holonet
    assert "16 Q6 edge traversals times 3 pulse phases equals 48 body ticks" in holonet
    assert "BT1406 Tomotope-Body Pulse Scheduler" in single


if __name__ == "__main__":
    test_bt1406_pulse_scheduler_runs_true()
    test_bt1406_stress_route_fills_body_exactly()
    test_bt1406_all_current_routes_have_valid_pulse_shells()
    test_bt1406_publication_anchors()
    print("BT1406 focused tests passed")
