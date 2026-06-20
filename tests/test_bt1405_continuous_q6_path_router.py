#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_tool() -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "bt1405_continuous_q6_path_router.py")],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(proc.stdout)


def load_result() -> dict:
    return json.loads(
        (ROOT / "data" / "bt1405_continuous_q6_path_router.json").read_text(
            encoding="utf-8"
        )
    )


def test_bt1405_continuous_router_runs_true() -> None:
    out = run_tool()
    assert out == {
        "bt": 1405,
        "stress_q6_steps": 16,
        "stress_slack": 32,
        "verified": True,
    }

    data = load_result()
    assert data["bt"] == 1405
    assert data["verified"] is True
    assert all(data["checks"].values())
    assert "continuous Q6 walk" in data["breakthrough"]


def test_bt1405_stress_route_is_continuous_body_trace() -> None:
    data = load_result()
    stress = next(
        route for route in data["routes"] if route["program"] == "six_digit_stress"
    )

    assert stress["q6_walk_steps"] == 16
    assert stress["packet_edge_steps"] == 6
    assert stress["connector_steps"] == 10
    assert stress["body_slack_ticks"] == 32
    assert stress["route_bound"] == 48
    assert stress["start_vertex"] == "110111"
    assert stress["end_vertex"] == "010011"
    assert stress["packet_depth_to_body_tick"] == {
        "0": 0,
        "1": 2,
        "2": 4,
        "3": 7,
        "4": 9,
        "5": 15,
    }

    packet_edges = [
        step["q6_edge_index"] for step in stress["steps"] if step["kind"] == "packet"
    ]
    assert packet_edges == [175, 133, 56, 37, 142, 77]
    assert [step["body_tick"] for step in stress["steps"]] == list(range(16))
    assert (
        len(
            {
                tuple(sorted((step["source"], step["target"])))
                for step in stress["steps"]
            }
        )
        == 16
    )

    for step in stress["steps"]:
        assert sum(a != b for a, b in zip(step["source"], step["target"])) == 1
        assert step["walk_bit_axis"] == 5 - step["q6_direction"]
        assert step["tomotope_block"] == step["tomotope_flag"] // 4
        assert step["transversal_index"] == step["tomotope_flag"] % 4


def test_bt1405_all_existing_programs_fit_original_bounds() -> None:
    data = load_result()
    profile = {
        route["program"]: (route["q6_walk_steps"], route["route_bound"])
        for route in data["routes"]
    }
    assert profile == {
        "local_flip": (1, 8),
        "single_digit_far": (1, 8),
        "two_digit_cross": (3, 16),
        "three_digit_far": (9, 24),
        "six_digit_stress": (16, 48),
    }
    assert all(steps <= bound for steps, bound in profile.values())
    assert all(all(route["checks"].values()) for route in data["routes"])


def test_bt1405_publication_anchors() -> None:
    docs = " ".join((ROOT / "docs" / "index.html").read_text(encoding="utf-8").split())
    holonet = " ".join(
        (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8").split()
    )
    single = " ".join(
        (ROOT / "single_photon_universal_computation.tex")
        .read_text(encoding="utf-8")
        .split()
    )

    assert "BT1405: continuous Q6 path router" in docs
    assert "BT1405_continuous_q6_path_router.md" in docs
    assert "BT1405 continuous Q6 path router" in holonet
    assert "6 packet edges plus 10 connector edges" in holonet
    assert "BT1405 Continuous Q6 Router" in single


if __name__ == "__main__":
    test_bt1405_continuous_router_runs_true()
    test_bt1405_stress_route_is_continuous_body_trace()
    test_bt1405_all_existing_programs_fit_original_bounds()
    test_bt1405_publication_anchors()
    print("BT1405 focused tests passed")
