#!/usr/bin/env python3
"""BT1698 - executable 72-tick Holonet packet state machine.

BT1697 promotes the Holonet packet as a typed ABI.  This verifier takes the
next step: it reads the existing BT1407 microframe rows and proves that the ABI
is a deterministic 72-tick state machine.

The result is intentionally finite.  It does not simulate calibrated optical
loss or detector response; it proves that the packet fields have a total,
typed, tick-by-tick transition schedule.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1698_holonet_packet_state_machine.json"

BODY_OPS = ["LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX"]
EPILOGUE_OPS = [
    "ERASE",
    "ROUTE",
    "PHASE",
    "X-CORR",
    "Z-CORR",
    "T-BIT",
    "RESTORE",
    "NEXT",
]


def load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def phase_state(row: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    phase = int(row["phase_trit"])
    source = row["source"]
    target = row["target"]
    if phase == 0:
        before = f"VERTEX:{source}"
        after = f"FLAG_LOADED:{row['tomotope_flag']}"
        delta = {
            "loaded_tomotope_flag": row["tomotope_flag"],
            "loaded_q6_edge": row["q6_edge_index"],
        }
    elif phase == 1:
        before = f"FLAG_LOADED:{row['tomotope_flag']}"
        after = f"AXIS_FLIPPED:{row['q6_direction']}"
        delta = {
            "flipped_q6_direction": row["q6_direction"],
            "edge_kind": row["edge_kind"],
        }
    else:
        before = f"AXIS_FLIPPED:{row['q6_direction']}"
        after = f"VERTEX:{target}"
        delta = {
            "committed_vertex": target,
            "edge_step_completed": row["edge_step"],
        }
    return before, after, delta


def epilogue_state(row: dict[str, Any]) -> tuple[str, str, dict[str, Any]]:
    word_tick = int(row["word_tick"])
    h = int(row["h"])
    phase = int(row["phase_trit"])
    before = f"HESSE_WORD:{h}:TICK:{word_tick}"
    after = (
        f"HESSE_WORD:{h}:TICK:{word_tick + 1}"
        if word_tick < 7
        else f"HESSE_WORD:{h}:DONE"
    )
    delta: dict[str, Any] = {
        "hesse_outcome": h,
        "route_trit": row["route_trit"],
        "phase_trit": phase,
        "pauli_correction": row["pauli_correction"],
        "word_value": row["value"],
    }
    if row["op"] == "ROUTE":
        delta["route_register"] = row["value"]
    elif row["op"] == "PHASE":
        delta["phase_register"] = row["value"]
    elif row["op"] == "X-CORR":
        delta["x_correction"] = row["value"]
    elif row["op"] == "Z-CORR":
        delta["z_correction"] = row["value"]
    elif row["op"] == "T-BIT":
        delta["time_frame_bit"] = row["value"]
    elif row["op"] == "RESTORE":
        delta["restore_target"] = row["value"]
    elif row["op"] == "NEXT":
        delta["next_word"] = row["value"]
    return before, after, delta


def build_trace(bt1407: dict[str, Any]) -> list[dict[str, Any]]:
    trace: list[dict[str, Any]] = []
    for row in sorted(bt1407["body_ticks"], key=lambda item: item["frame_tick"]):
        before, after, delta = phase_state(row)
        trace.append(
            {
                "tick": row["frame_tick"],
                "region": row["region"],
                "op": row["op"],
                "phase_trit": row["phase_trit"],
                "edge_step": row["edge_step"],
                "q6_edge_index": row["q6_edge_index"],
                "q6_direction": row["q6_direction"],
                "source": row["source"],
                "target": row["target"],
                "tomotope_block": row["tomotope_block"],
                "tomotope_flag": row["tomotope_flag"],
                "state_before": before,
                "state_after": after,
                "register_delta": delta,
                "next_tick": row["frame_tick"] + 1,
            }
        )
    for row in sorted(bt1407["epilogue_ticks"], key=lambda item: item["frame_tick"]):
        before, after, delta = epilogue_state(row)
        trace.append(
            {
                "tick": row["frame_tick"],
                "region": row["region"],
                "op": row["op"],
                "word_tick": row["word_tick"],
                "hesse_outcome": row["h"],
                "route_trit": row["route_trit"],
                "phase_trit": row["phase_trit"],
                "pauli_correction": row["pauli_correction"],
                "state_before": before,
                "state_after": after,
                "register_delta": delta,
                "next_tick": row["frame_tick"] + 1 if row["frame_tick"] < 71 else None,
            }
        )
    return sorted(trace, key=lambda item: item["tick"])


def build_certificate() -> dict[str, Any]:
    bt1697 = load_json("data/bt1697_holonet_typed_packet_abi.json")
    bt1407 = load_json("data/bt1407_microframe_transaction_composer.json")
    trace = build_trace(bt1407)
    body = [row for row in trace if row["region"] == "tomotope_body"]
    epilogue = [row for row in trace if row["region"] == "local_lift_hesse_epilogue"]

    body_groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in body:
        body_groups[int(row["edge_step"])].append(row)
    body_group_checks = []
    for step in sorted(body_groups):
        group = sorted(body_groups[step], key=lambda item: item["tick"])
        body_group_checks.append(
            {
                "edge_step": step,
                "ticks": [row["tick"] for row in group],
                "ops": [row["op"] for row in group],
                "phases": [row["phase_trit"] for row in group],
                "same_edge": len({row["q6_edge_index"] for row in group}) == 1,
                "same_source_target": len(
                    {(row["source"], row["target"]) for row in group}
                )
                == 1,
            }
        )

    edge_heads = [
        sorted(body_groups[step], key=lambda item: item["tick"])[0]
        for step in sorted(body_groups)
    ]
    edge_continuity = [
        edge_heads[index]["target"] == edge_heads[index + 1]["source"]
        for index in range(len(edge_heads) - 1)
    ]

    epilogue_groups: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in epilogue:
        epilogue_groups[int(row["hesse_outcome"])].append(row)
    epilogue_group_checks = []
    for h in sorted(epilogue_groups):
        group = sorted(epilogue_groups[h], key=lambda item: item["tick"])
        epilogue_group_checks.append(
            {
                "hesse_outcome": h,
                "ticks": [row["tick"] for row in group],
                "ops": [row["op"] for row in group],
                "word_ticks": [row["word_tick"] for row in group],
                "phase_trits": sorted({row["phase_trit"] for row in group}),
                "pauli_corrections": sorted({row["pauli_correction"] for row in group}),
            }
        )

    op_histogram = Counter(row["op"] for row in trace)
    region_histogram = Counter(row["region"] for row in trace)

    checks = {
        "bt1697_verified": bt1697["verified"] is True,
        "bt1407_verified": bt1407["verified"] is True,
        "trace_has_72_ticks": len(trace) == 72,
        "ticks_are_contiguous_0_to_71": [row["tick"] for row in trace]
        == list(range(72)),
        "next_tick_links_are_total": all(
            row["next_tick"] == row["tick"] + 1 for row in trace[:-1]
        )
        and trace[-1]["next_tick"] is None,
        "body_is_first_48_ticks": [row["tick"] for row in body] == list(range(48)),
        "epilogue_is_last_24_ticks": [row["tick"] for row in epilogue]
        == list(range(48, 72)),
        "body_has_16_three_phase_edges": len(body_group_checks) == 16
        and all(item["ops"] == BODY_OPS for item in body_group_checks)
        and all(item["phases"] == [0, 1, 2] for item in body_group_checks)
        and all(
            item["same_edge"] and item["same_source_target"]
            for item in body_group_checks
        ),
        "body_edges_chain_without_gap": all(edge_continuity),
        "epilogue_has_three_hesse_words": sorted(epilogue_groups) == [3, 4, 5],
        "epilogue_words_are_eight_tick_clifford_returns": all(
            item["ops"] == EPILOGUE_OPS and item["word_ticks"] == list(range(8))
            for item in epilogue_group_checks
        ),
        "epilogue_encodes_route_one_phase_sweep": all(
            sorted({row["route_trit"] for row in epilogue_groups[h]}) == [1]
            and sorted({row["phase_trit"] for row in epilogue_groups[h]}) == [h - 3]
            for h in epilogue_groups
        ),
        "final_body_vertex_feeds_epilogue_boundary": body[-1]["target"] == "010011"
        and epilogue[0]["tick"] == 48,
    }

    return {
        "theorem": "BT1698 Holonet Packet State Machine",
        "verified": all(checks.values()),
        "breakthrough": (
            "The BT1697 packet ABI is executable as one deterministic 72-tick "
            "state machine: 16 Q6/tomotope edges with LOAD/FLIP/LATCH phases, "
            "followed by three eight-tick Hesse/Clifford return words."
        ),
        "state_machine_identity": {
            "ticks": 72,
            "body": "16 edges * 3 phases = 48 ticks",
            "epilogue": "3 Hesse words * 8 Clifford-return ticks = 24 ticks",
            "body_ops": BODY_OPS,
            "epilogue_ops": EPILOGUE_OPS,
            "initial_vertex": body[0]["source"],
            "final_body_vertex": body[-1]["target"],
        },
        "histograms": {
            "region": dict(sorted(region_histogram.items())),
            "op": dict(sorted(op_histogram.items())),
        },
        "body_edge_checks": body_group_checks,
        "epilogue_word_checks": epilogue_group_checks,
        "trace": trace,
        "source_certificates": [
            "data/bt1697_holonet_typed_packet_abi.json",
            "data/bt1407_microframe_transaction_composer.json",
        ],
        "checks": checks,
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print(f"  ticks: {cert['state_machine_identity']['ticks']}")
    print(f"  body: {cert['state_machine_identity']['body']}")
    print(f"  epilogue: {cert['state_machine_identity']['epilogue']}")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
