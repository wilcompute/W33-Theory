#!/usr/bin/env python3
"""Part CCCCCXCVIII: tomotope <-> dual toroidal packet bridge.

This module connects the two toroidal polyhedra families (Csaszar/Szilassi)
to the tomotope packet ladder using executable invariants:

  - dual toroidal carrier: 84 + 84 = 168,
  - tetrahedral packet scale: 24,
  - tomotope carrier: 192 = 8 * 24 = 168 + 24,
  - seven toroidal modes: 5 Csaszar + 2 Szilassi = 7 active packets.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VERTEX_LIFT_PATH = ROOT / "data" / "tomotope_six_kernel_vertex_lift.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_dual_packet_bridge.json"


@dataclass(frozen=True)
class BridgeSummary:
    csaszar_realizations: int
    szilassi_realizations: int
    toroidal_mode_count: int
    packet_size: int
    active_toroidal_packets: int
    ground_packets: int
    total_packets: int
    active_packet_weight: int
    ground_packet_weight: int
    tomotope_weight: int
    dual_toroidal_flag_weight: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    vertex_lift = json.loads(VERTEX_LIFT_PATH.read_text(encoding="utf-8"))
    packet_size = int(vertex_lift["summary"]["vertex_group_order"])

    # Two toroidal polyhedra families used in-repo.
    csaszar_realizations = 5
    szilassi_realizations = 2
    toroidal_mode_count = csaszar_realizations + szilassi_realizations

    active_toroidal_packets = toroidal_mode_count
    ground_packets = 1
    total_packets = active_toroidal_packets + ground_packets

    active_packet_weight = active_toroidal_packets * packet_size
    ground_packet_weight = ground_packets * packet_size
    tomotope_weight = total_packets * packet_size

    # Polyhedral flag-side exact dual shell.
    csaszar_edges = 21
    szilassi_edges = 21
    csaszar_flags = 4 * csaszar_edges
    szilassi_flags = 4 * szilassi_edges
    dual_toroidal_flag_weight = csaszar_flags + szilassi_flags

    identities = {
        "five_plus_two_equals_seven": toroidal_mode_count == 7,
        "seven_plus_one_equals_eight": total_packets == 8,
        "packet_size_is_24": packet_size == 24,
        "active_weight_is_168": active_packet_weight == 168,
        "ground_weight_is_24": ground_packet_weight == 24,
        "tomotope_weight_is_192": tomotope_weight == 192,
        "dual_toroidal_flags_are_168": dual_toroidal_flag_weight == 168,
        "active_weight_matches_dual_toroidal_flags": (
            active_packet_weight == dual_toroidal_flag_weight
        ),
        "tomotope_splits_as_168_plus_24": (
            tomotope_weight == active_packet_weight + ground_packet_weight
        ),
    }

    mode_packet_assignment = [
        {"mode": "C1", "family": "csaszar", "packet_weight": packet_size},
        {"mode": "C2", "family": "csaszar", "packet_weight": packet_size},
        {"mode": "C3", "family": "csaszar", "packet_weight": packet_size},
        {"mode": "C4", "family": "csaszar", "packet_weight": packet_size},
        {"mode": "C5", "family": "csaszar", "packet_weight": packet_size},
        {"mode": "S1", "family": "szilassi", "packet_weight": packet_size},
        {"mode": "S2", "family": "szilassi", "packet_weight": packet_size},
        {"mode": "G", "family": "ground", "packet_weight": packet_size},
    ]

    summary = BridgeSummary(
        csaszar_realizations=csaszar_realizations,
        szilassi_realizations=szilassi_realizations,
        toroidal_mode_count=toroidal_mode_count,
        packet_size=packet_size,
        active_toroidal_packets=active_toroidal_packets,
        ground_packets=ground_packets,
        total_packets=total_packets,
        active_packet_weight=active_packet_weight,
        ground_packet_weight=ground_packet_weight,
        tomotope_weight=tomotope_weight,
        dual_toroidal_flag_weight=dual_toroidal_flag_weight,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "polyhedra": {
            "csaszar": {
                "realization_count": csaszar_realizations,
                "vertices": 7,
                "edges": csaszar_edges,
                "faces": 14,
                "flags": csaszar_flags,
            },
            "szilassi": {
                "realization_count": szilassi_realizations,
                "vertices": 14,
                "edges": szilassi_edges,
                "faces": 7,
                "flags": szilassi_flags,
            },
        },
        "mode_packet_assignment": mode_packet_assignment,
        "identities": identities,
        "upstream_artifact": {
            "vertex_lift_path": str(VERTEX_LIFT_PATH),
            "vertex_group_order": packet_size,
        },
        "notes": (
            "Outside-the-box bridge: treat each toroidal realization mode as one "
            "S4-sized packet (24 states), giving an active 7*24=168 shell that "
            "matches the dual toroidal flag carrier exactly; adding one ground "
            "packet gives the tomotope 8*24=192 carrier."
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
