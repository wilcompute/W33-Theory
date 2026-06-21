#!/usr/bin/env python3
"""BT1407: compose the 48-tick body and 24-tick Hesse epilogue.

BT1406 fills the first 48 tomotope-body ticks with ternary Q6 edge pulses.  The
BT1300 frame still has a 24-tick local-lift epilogue.  BT1407 identifies that
epilogue as exactly one route branch's Hesse phase fanout:

    3 phase outcomes * 8 return-word ticks = 24 epilogue ticks.

For the six-digit stress route the final target digit is 4, so the selected
route branch is r = 4 mod 3 = 1 and the epilogue carries Hesse outcomes
h = 3, 4, 5.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1407_microframe_transaction_composer.json"
FRAME_TICKS = 72
BODY_TICKS = 48
EPILOGUE_TICKS = 24
WORD_TICKS = 8


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def stress_program(bt1374: dict[str, Any]) -> dict[str, Any]:
    return next(
        program
        for program in bt1374["compiled_programs"]
        if program["program"] == "six_digit_stress"
    )


def stress_schedule(bt1406: dict[str, Any]) -> dict[str, Any]:
    return next(
        schedule
        for schedule in bt1406["schedules"]
        if schedule["program"] == "six_digit_stress"
    )


def hesse_frames_by_outcome(bt1404: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(frame["h"]): frame for frame in bt1404["frames"]}


def build_body_ticks(schedule: dict[str, Any]) -> list[dict[str, Any]]:
    ticks = []
    for pulse in schedule["pulses"]:
        ticks.append(
            {
                "frame_tick": int(pulse["body_tick"]),
                "region": "tomotope_body",
                "op": pulse["pulse_op"],
                "edge_kind": pulse["edge_kind"],
                "edge_step": pulse["edge_step"],
                "q6_edge_index": pulse["q6_edge_index"],
                "q6_direction": pulse["q6_direction"],
                "source": pulse["source"],
                "target": pulse["target"],
                "tomotope_flag": pulse["tomotope_flag"],
                "tomotope_block": pulse["tomotope_block"],
                "phase_trit": pulse["phase_trit"],
            }
        )
    return ticks


def build_epilogue_ticks(
    *,
    route_branch: int,
    frames_by_h: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    ticks = []
    for phase_trit in range(3):
        h = 3 * route_branch + phase_trit
        frame = frames_by_h[h]
        for word_tick in frame["packet_word"]:
            ticks.append(
                {
                    "frame_tick": BODY_TICKS + 8 * phase_trit + int(word_tick["tick"]),
                    "region": "local_lift_hesse_epilogue",
                    "op": word_tick["lane"],
                    "h": h,
                    "route_trit": route_branch,
                    "phase_trit": phase_trit,
                    "branch": frame["branch"],
                    "pauli_correction": frame["pauli_correction"],
                    "t_frame_bit": frame["t_frame_bit"],
                    "value": word_tick["value"],
                    "word_tick": int(word_tick["tick"]),
                }
            )
    return ticks


def build_result() -> dict[str, Any]:
    bt1374 = load_json("data/bt1374_q6_tomotope_packet_route_compiler.json")
    bt1404 = load_json("data/bt1404_holonet_scope_microframe.json")
    bt1406 = load_json("data/bt1406_tomotope_body_edge_pulse_scheduler.json")
    bt1300 = load_json("data/bt1300_oscillator_instruction_isa.json")

    stress = stress_program(bt1374)
    schedule = stress_schedule(bt1406)
    final_target_digit = int(stress["target"][-1])
    selected_route_branch = final_target_digit % 3
    frames_by_h = hesse_frames_by_outcome(bt1404)
    body_ticks = build_body_ticks(schedule)
    epilogue_ticks = build_epilogue_ticks(
        route_branch=selected_route_branch,
        frames_by_h=frames_by_h,
    )
    frame_ticks = sorted(
        body_ticks + epilogue_ticks, key=lambda tick: tick["frame_tick"]
    )
    epilogue_outcomes = sorted({tick["h"] for tick in epilogue_ticks})
    epilogue_ops = [tick["op"] for tick in epilogue_ticks[:WORD_TICKS]]
    region_hist = Counter(tick["region"] for tick in frame_ticks)

    checks = {
        "bt1300_frame_contract_verified": bt1300["verified"] is True
        and bt1300["isa_header"]["frame_lanes"] == FRAME_TICKS
        and bt1300["isa_header"]["epilogue_split"]
        == "24 = q * 2^q = 18 payload + 6 parity",
        "bt1404_scope_verified": bt1404["verified"] is True,
        "bt1406_pulse_schedule_verified": bt1406["verified"] is True,
        "stress_body_fills_first_48_ticks": len(body_ticks) == BODY_TICKS
        and [tick["frame_tick"] for tick in body_ticks] == list(range(BODY_TICKS)),
        "epilogue_is_three_hesse_words": len(epilogue_ticks) == EPILOGUE_TICKS
        and epilogue_outcomes
        == [3 * selected_route_branch + phase for phase in range(3)],
        "epilogue_words_are_8_ticks_each": [
            sum(1 for tick in epilogue_ticks if tick["h"] == h)
            for h in epilogue_outcomes
        ]
        == [WORD_TICKS, WORD_TICKS, WORD_TICKS],
        "frame_ticks_are_contiguous_0_to_71": [
            tick["frame_tick"] for tick in frame_ticks
        ]
        == list(range(FRAME_TICKS)),
        "no_region_overlap": set(tick["frame_tick"] for tick in body_ticks).isdisjoint(
            tick["frame_tick"] for tick in epilogue_ticks
        ),
        "selected_branch_is_final_target_digit_mod_3": selected_route_branch
        == final_target_digit % 3
        == 1,
        "epilogue_reuses_bt1404_return_word_shape": epilogue_ops
        == ["ERASE", "ROUTE", "PHASE", "X-CORR", "Z-CORR", "T-BIT", "RESTORE", "NEXT"],
    }

    return {
        "bt": 1407,
        "title": "72-tick body/epilogue microframe transaction",
        "verified": all(checks.values()),
        "breakthrough": (
            "The full 72-tick oscillator frame is now a transaction: ticks 0-47 "
            "execute the BT1406 continuous Q6 body, and ticks 48-71 execute the "
            "Hesse phase fanout for the selected route branch.  For the stress "
            "route, final target digit 4 selects route branch r=1, so the "
            "epilogue carries h=3,4,5."
        ),
        "frame_identity": "48 Q6 body pulse ticks + 3 Hesse return words * 8 ticks = 72 ticks",
        "stress_selection": {
            "program": stress["program"],
            "final_target_digit": final_target_digit,
            "selected_route_branch": selected_route_branch,
            "epilogue_hesse_outcomes": epilogue_outcomes,
        },
        "region_histogram": {
            str(key): value for key, value in sorted(region_hist.items())
        },
        "body_ticks": body_ticks,
        "epilogue_ticks": epilogue_ticks,
        "frame_tick_summary": [
            {
                "frame_tick": tick["frame_tick"],
                "region": tick["region"],
                "op": tick["op"],
                "h": tick.get("h"),
                "q6_edge_index": tick.get("q6_edge_index"),
            }
            for tick in frame_ticks
        ],
        "boundary": (
            "BT1407 composes existing ABI schedules.  It does not certify the "
            "physical SIC optics, detector electronics, or calibrated optical "
            "pulse implementation of the Hesse port."
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
                "selected_route_branch": result["stress_selection"][
                    "selected_route_branch"
                ],
                "epilogue_hesse_outcomes": result["stress_selection"][
                    "epilogue_hesse_outcomes"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
