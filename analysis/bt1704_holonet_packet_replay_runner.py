#!/usr/bin/env python3
"""BT1704 - deterministic Holonet packet replay runner.

BT1698 proves that the packet trace is a 72-tick transition system.  BT1704
replays that trace as an event log and verifies determinism by executing the
same log twice from the same initial state.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

from bt1698_holonet_packet_state_machine import build_certificate as build_state
from bt1699_holonet_abi_to_hardware_lowering import build_certificate as build_lowering

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1704_holonet_packet_replay_runner.json"


def initial_state(trace: list[dict[str, Any]]) -> dict[str, Any]:
    first = trace[0]
    return {
        "cursor": f"VERTEX:{first['source']}",
        "vertex": first["source"],
        "loaded_flag": None,
        "loaded_edge": None,
        "axis": None,
        "last_committed_edge_step": None,
        "hesse_word": None,
        "route_register": None,
        "phase_register": None,
        "x_correction": None,
        "z_correction": None,
        "time_frame_bit": None,
        "restore_target": None,
        "next_word": None,
        "tick": -1,
    }


def apply_event(state: dict[str, Any], event: dict[str, Any]) -> dict[str, Any]:
    next_state = deepcopy(state)
    op = event["op"]
    next_state["tick"] = event["tick"]
    if event["region"] == "tomotope_body":
        if op == "LOAD_FLAG":
            next_state["loaded_flag"] = event["tomotope_flag"]
            next_state["loaded_edge"] = event["q6_edge_index"]
            next_state["cursor"] = f"FLAG_LOADED:{event['tomotope_flag']}"
        elif op == "FLIP_Q6_AXIS":
            next_state["axis"] = event["q6_direction"]
            next_state["cursor"] = f"AXIS_FLIPPED:{event['q6_direction']}"
        elif op == "LATCH_VERTEX":
            next_state["vertex"] = event["target"]
            next_state["last_committed_edge_step"] = event["edge_step"]
            next_state["cursor"] = f"VERTEX:{event['target']}"
        else:
            raise ValueError(f"unknown body op {op}")
    else:
        h = event["hesse_outcome"]
        word_tick = event["word_tick"]
        next_state["hesse_word"] = h
        if op == "ROUTE":
            next_state["route_register"] = event["register_delta"]["route_register"]
        elif op == "PHASE":
            next_state["phase_register"] = event["register_delta"]["phase_register"]
        elif op == "X-CORR":
            next_state["x_correction"] = event["register_delta"]["x_correction"]
        elif op == "Z-CORR":
            next_state["z_correction"] = event["register_delta"]["z_correction"]
        elif op == "T-BIT":
            next_state["time_frame_bit"] = event["register_delta"]["time_frame_bit"]
        elif op == "RESTORE":
            next_state["restore_target"] = event["register_delta"]["restore_target"]
        elif op == "NEXT":
            next_state["next_word"] = event["register_delta"]["next_word"]
        elif op != "ERASE":
            raise ValueError(f"unknown epilogue op {op}")
        next_state["cursor"] = (
            f"HESSE_WORD:{h}:TICK:{word_tick + 1}"
            if word_tick < 7
            else f"HESSE_WORD:{h}:DONE"
        )
    return next_state


def replay(trace: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    state = initial_state(trace)
    event_log = []
    for event in trace:
        before = deepcopy(state)
        after = apply_event(state, event)
        event_log.append(
            {
                "tick": event["tick"],
                "op": event["op"],
                "region": event["region"],
                "cursor_before": before["cursor"],
                "cursor_after": after["cursor"],
                "vertex_after": after["vertex"],
                "registers_after": {
                    key: after[key]
                    for key in (
                        "loaded_flag",
                        "loaded_edge",
                        "axis",
                        "route_register",
                        "phase_register",
                        "x_correction",
                        "z_correction",
                        "time_frame_bit",
                        "restore_target",
                        "next_word",
                    )
                },
            }
        )
        state = after
    return event_log, state


def build_certificate() -> dict[str, Any]:
    state_cert = build_state()
    lowering = build_lowering()
    trace = state_cert["trace"]
    first_log, first_final = replay(trace)
    second_log, second_final = replay(trace)
    ticks = [row["tick"] for row in first_log]
    checks = {
        "bt1698_verified": state_cert["verified"] is True,
        "bt1699_verified": lowering["verified"] is True,
        "replay_has_72_events": len(first_log) == 72,
        "replay_ticks_are_0_to_71": ticks == list(range(72)),
        "replay_is_deterministic": first_log == second_log
        and first_final == second_final,
        "body_final_vertex_matches_bt1698": first_log[47]["vertex_after"]
        == state_cert["state_machine_identity"]["final_body_vertex"]
        == "010011",
        "final_hesse_word_done": first_final["cursor"] == "HESSE_WORD:5:DONE",
        "final_pauli_registers_match_last_epilogue_word": first_final["x_correction"]
        == "X^1"
        and first_final["z_correction"] == "Z^2"
        and first_final["time_frame_bit"] == "1",
        "hardware_stage_count_preserved": lowering["stage_histogram"]
        == {
            "analyzer_or_fuel_body": 16,
            "dark_reference": 8,
            "detector_or_hesse_handoff": 16,
            "program_delay": 24,
            "source_switch": 8,
        },
    }
    return {
        "theorem": "BT1704 Holonet Packet Replay Runner",
        "verified": all(checks.values()),
        "breakthrough": (
            "The 72-tick packet trace replays deterministically: two executions "
            "from the same initial vertex produce identical event logs, final "
            "cursor, and Pauli/Hesse registers."
        ),
        "initial_state": initial_state(trace),
        "final_state": first_final,
        "event_log": first_log,
        "source_certificates": [
            "data/bt1698_holonet_packet_state_machine.json",
            "data/bt1699_holonet_abi_to_hardware_lowering.json",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  events: {len(cert['event_log'])}")
    print(f"  final cursor: {cert['final_state']['cursor']}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
