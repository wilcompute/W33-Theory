#!/usr/bin/env python3
"""BT1406: expand continuous Q6 paths into 48-tick edge pulse schedules.

BT1405 closed the waypoint boundary by stitching packet-edge addresses into a
continuous Q6 walk.  BT1406 closes the next ABI layer: each Q6 edge traversal is
expanded into the q=3 pulse microcycle

    LOAD_FLAG -> FLIP_Q6_AXIS -> LATCH_VERTEX.

For the six-digit stress route, BT1405 found 16 Q6 edge traversals.  Since
16 * 3 = 48, the full continuous route occupies the entire tomotope body with no
idle tick.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1406_tomotope_body_edge_pulse_scheduler.json"
BODY_TICKS = 48
PULSE_PHASES = (
    ("LOAD_FLAG", "load tomotope flag/block/transversal"),
    ("FLIP_Q6_AXIS", "perform the one-bit Q6 edge traversal"),
    ("LATCH_VERTEX", "latch the target Q6 vertex and ABI record"),
)


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def pulse_for_step(
    step: dict[str, Any], pulse_tick: int, phase_trit: int
) -> dict[str, Any]:
    op, meaning = PULSE_PHASES[phase_trit]
    return {
        "body_tick": pulse_tick,
        "phase_trit": phase_trit,
        "pulse_op": op,
        "meaning": meaning,
        "edge_step": int(step["body_tick"]),
        "edge_kind": step["kind"],
        "packet_depth": step["packet_depth"],
        "q6_edge_index": int(step["q6_edge_index"]),
        "q6_direction": int(step["q6_direction"]),
        "walk_bit_axis": int(step["walk_bit_axis"]),
        "source": step["source"],
        "target": step["target"],
        "tomotope_flag": int(step["tomotope_flag"]),
        "tomotope_block": int(step["tomotope_block"]),
        "transversal_index": int(step["transversal_index"]),
    }


def schedule_for_route(route: dict[str, Any]) -> dict[str, Any]:
    edge_pulses: list[dict[str, Any]] = []
    for step in route["steps"]:
        base_tick = 3 * int(step["body_tick"])
        for phase_trit in range(3):
            edge_pulses.append(pulse_for_step(step, base_tick + phase_trit, phase_trit))

    idle_start = len(edge_pulses)
    idle_pulses = [
        {
            "body_tick": tick,
            "phase_trit": tick % 3,
            "pulse_op": "IDLE",
            "meaning": "unused tomotope-body pulse slot",
            "edge_step": None,
            "edge_kind": "idle",
            "packet_depth": None,
            "q6_edge_index": None,
            "q6_direction": None,
            "walk_bit_axis": None,
            "source": None,
            "target": None,
            "tomotope_flag": None,
            "tomotope_block": None,
            "transversal_index": None,
        }
        for tick in range(idle_start, BODY_TICKS)
    ]
    pulses = edge_pulses + idle_pulses
    phase_hist = Counter(pulse["pulse_op"] for pulse in pulses)
    packet_load_ticks = [
        pulse["body_tick"]
        for pulse in pulses
        if pulse["edge_kind"] == "packet" and pulse["phase_trit"] == 0
    ]

    edge_groups: dict[int, list[dict[str, Any]]] = {}
    for pulse in edge_pulses:
        edge_groups.setdefault(int(pulse["edge_step"]), []).append(pulse)

    return {
        "program": route["program"],
        "q6_walk_steps": int(route["q6_walk_steps"]),
        "edge_pulse_ticks": len(edge_pulses),
        "idle_ticks": len(idle_pulses),
        "fills_48_tick_body": len(pulses) == BODY_TICKS and not idle_pulses,
        "packet_load_ticks": packet_load_ticks,
        "pulses": pulses,
        "pulse_op_histogram": {str(k): v for k, v in sorted(phase_hist.items())},
        "checks": {
            "pulses_cover_48_body_ticks": [pulse["body_tick"] for pulse in pulses]
            == list(range(BODY_TICKS)),
            "each_q6_step_expands_to_three_pulses": len(edge_pulses)
            == 3 * int(route["q6_walk_steps"]),
            "phase_trits_cycle_0_1_2": [
                pulse["phase_trit"]
                for pulse in edge_pulses[: min(12, len(edge_pulses))]
            ]
            == ([0, 1, 2] * 4)[: min(12, len(edge_pulses))],
            "pulse_groups_keep_one_edge_identity": all(
                len(group) == 3
                and {pulse["q6_edge_index"] for pulse in group}
                == {group[0]["q6_edge_index"]}
                and {pulse["tomotope_flag"] for pulse in group}
                == {group[0]["tomotope_flag"]}
                and [pulse["pulse_op"] for pulse in group]
                == ["LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX"]
                for group in edge_groups.values()
            ),
            "all_non_idle_pulses_reference_q6_edges": all(
                pulse["q6_edge_index"] is not None for pulse in edge_pulses
            ),
            "edge_pulses_fit_48_tick_body": len(edge_pulses) <= BODY_TICKS,
        },
    }


def build_result() -> dict[str, Any]:
    bt1405 = load_json("data/bt1405_continuous_q6_path_router.json")
    schedules = [schedule_for_route(route) for route in bt1405["routes"]]
    stress = next(
        schedule for schedule in schedules if schedule["program"] == "six_digit_stress"
    )

    checks = {
        "bt1405_verified": bt1405["verified"] is True,
        "qutrit_microcycle_has_three_phases": len(PULSE_PHASES) == 3,
        "all_current_routes_fit_48_tick_body_as_edge_pulses": all(
            schedule["checks"]["edge_pulses_fit_48_tick_body"] for schedule in schedules
        ),
        "all_schedules_cover_48_body_ticks": all(
            schedule["checks"]["pulses_cover_48_body_ticks"] for schedule in schedules
        ),
        "all_edge_pulses_keep_q6_identity": all(
            schedule["checks"]["pulse_groups_keep_one_edge_identity"]
            for schedule in schedules
        ),
        "stress_has_sixteen_q6_edges": stress["q6_walk_steps"] == 16,
        "stress_expands_to_48_edge_pulses": stress["edge_pulse_ticks"] == BODY_TICKS,
        "stress_has_no_idle_body_ticks": stress["idle_ticks"] == 0
        and stress["fills_48_tick_body"] is True,
        "stress_packet_load_ticks_are_ordered": stress["packet_load_ticks"]
        == [0, 6, 12, 21, 27, 45],
    }

    return {
        "bt": 1406,
        "title": "Tomotope-body edge pulse scheduler",
        "verified": all(checks.values()),
        "pulse_microcycle": [
            {"phase_trit": idx, "pulse_op": op, "meaning": meaning}
            for idx, (op, meaning) in enumerate(PULSE_PHASES)
        ],
        "body_ticks": BODY_TICKS,
        "breakthrough": (
            "BT1406 turns the BT1405 continuous Q6 stress path into a complete "
            "48-tick tomotope-body pulse schedule: 16 Q6 edge traversals times "
            "the q=3 pulse microcycle equals 48 body ticks."
        ),
        "schedules": schedules,
        "stress_summary": {
            "program": stress["program"],
            "q6_walk_steps": stress["q6_walk_steps"],
            "edge_pulse_ticks": stress["edge_pulse_ticks"],
            "idle_ticks": stress["idle_ticks"],
            "packet_load_ticks": stress["packet_load_ticks"],
            "pulse_op_histogram": stress["pulse_op_histogram"],
        },
        "boundary": (
            "This is a timing ABI schedule: it assigns the hypercube route to "
            "tomotope-body ticks.  It is not a claim about calibrated optical "
            "pulse widths, detector jitter, or waveguide loss."
        ),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=OUT)
    ns = parser.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "stress_edge_pulses": result["stress_summary"]["edge_pulse_ticks"],
                "stress_idle_ticks": result["stress_summary"]["idle_ticks"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
