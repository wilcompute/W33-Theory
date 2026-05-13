#!/usr/bin/env python3
"""Part CCCCCXCIX: toroidal step-transport bridge into tomotope six slots.

Build an explicit transport model on the 7 toroidal modes (C1..C5,S1,S2):

1) oriented transports on the 7-cycle produce exactly 42 ordered mode pairs,
2) these decompose into six step classes (d = 1..6), each with 7 transports,
3) identify step classes with tomotope six-slot channels k1..k6,
4) weight each channel by its S4 edge-stabilizer size (4) to recover
   active packet weight 42*4 = 168, matching the dual toroidal flag shell.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
S4_BRIDGE_PATH = ROOT / "data" / "tomotope_six_kernel_s4_edge_bridge.json"
DUAL_PACKET_PATH = ROOT / "data" / "tomotope_toroidal_dual_packet_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_step_transport_bridge.json"


def _compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def _closure(generators: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    n = len(generators[0])
    identity = tuple(range(n))
    group: set[tuple[int, ...]] = {identity}
    frontier = [identity]
    while frontier:
        g = frontier.pop()
        for a in generators:
            h = _compose(a, g)
            if h not in group:
                group.add(h)
                frontier.append(h)
    return group


@dataclass(frozen=True)
class StepBridgeSummary:
    toroidal_mode_count: int
    oriented_transport_count: int
    unoriented_transport_count: int
    step_class_count: int
    per_step_transport_count: int
    slot_count: int
    slot_stabilizer_size: int
    weighted_active_transport: int
    active_packet_weight: int
    dual_toroidal_flag_weight: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    s4_bridge = json.loads(S4_BRIDGE_PATH.read_text(encoding="utf-8"))
    dual_packet = json.loads(DUAL_PACKET_PATH.read_text(encoding="utf-8"))

    modes = ["C1", "C2", "C3", "C4", "C5", "S1", "S2"]
    n = len(modes)

    oriented: list[dict[str, Any]] = []
    step_classes: dict[int, list[dict[str, Any]]] = {d: [] for d in range(1, n)}
    for i in range(n):
        for d in range(1, n):
            j = (i + d) % n
            row = {
                "from": modes[i],
                "to": modes[j],
                "from_index": i,
                "to_index": j,
                "step": d,
            }
            oriented.append(row)
            step_classes[d].append(row)

    # Unoriented transports are 7*6/2 = 21
    unoriented = {
        tuple(sorted((row["from_index"], row["to_index"])))
        for row in oriented
    }

    slot_labels = sorted(s4_bridge["canonical_bivector_slots"].keys())
    if len(slot_labels) != 6:
        raise ValueError("Expected six slot labels in S4 bridge payload")

    # Canonical step->slot identification: step classes d=1..6 map to k1..k6.
    step_to_slot = {d: slot_labels[d - 1] for d in range(1, n)}

    slot_transport_counts = {
        step_to_slot[d]: len(step_classes[d])
        for d in range(1, n)
    }

    slot_generators = {
        name: tuple(perm)
        for name, perm in s4_bridge["slot_generators"].items()
    }
    group = _closure(list(slot_generators.values()))
    slot_count = len(slot_labels)
    group_order = len(group)
    slot_stabilizer_size = group_order // slot_count

    oriented_transport_count = len(oriented)
    weighted_active_transport = oriented_transport_count * slot_stabilizer_size

    active_packet_weight = int(dual_packet["summary"]["active_packet_weight"])
    dual_toroidal_flag_weight = int(dual_packet["summary"]["dual_toroidal_flag_weight"])

    identities = {
        "oriented_count_is_42": oriented_transport_count == 42,
        "unoriented_count_is_21": len(unoriented) == 21,
        "six_step_classes": len(step_classes) == 6,
        "each_step_has_seven_transports": all(len(v) == 7 for v in step_classes.values()),
        "six_slots_present": slot_count == 6,
        "slot_stabilizer_is_4": slot_stabilizer_size == 4,
        "weighted_active_equals_168": weighted_active_transport == 168,
        "weighted_active_matches_active_packet_weight": (
            weighted_active_transport == active_packet_weight
        ),
        "active_packet_matches_dual_toroidal_flags": (
            active_packet_weight == dual_toroidal_flag_weight
        ),
    }

    summary = StepBridgeSummary(
        toroidal_mode_count=n,
        oriented_transport_count=oriented_transport_count,
        unoriented_transport_count=len(unoriented),
        step_class_count=len(step_classes),
        per_step_transport_count=7,
        slot_count=slot_count,
        slot_stabilizer_size=slot_stabilizer_size,
        weighted_active_transport=weighted_active_transport,
        active_packet_weight=active_packet_weight,
        dual_toroidal_flag_weight=dual_toroidal_flag_weight,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "mode_order": modes,
        "step_to_slot": step_to_slot,
        "slot_transport_counts": slot_transport_counts,
        "step_class_samples": {
            str(d): step_classes[d][:3] for d in range(1, n)
        },
        "identities": identities,
        "upstream": {
            "s4_bridge_path": str(S4_BRIDGE_PATH),
            "dual_packet_path": str(DUAL_PACKET_PATH),
            "slot_group_order": group_order,
        },
        "notes": (
            "Transport bridge: the toroidal 7-cycle has 42 oriented transports = 6*7. "
            "Identifying the six step classes with the six tomotope slots and weighting "
            "by the S4 edge-stabilizer (4) gives 42*4=168, matching the active dual-"
            "toroidal/tomotope packet weight exactly."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
