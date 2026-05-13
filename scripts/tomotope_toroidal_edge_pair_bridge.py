#!/usr/bin/env python3
"""Part DCVII: dual-edge pair bridge for oriented transport.

This certificate locks the user's key observation as an exact finite identity:

  oriented_transport_count = Csaszar_edges + Szilassi_edges = 21 + 21 = 42.

It also verifies the companion identities:
  - unoriented_transport_count = 21 = each single-edge shell,
  - stabilizer-weighted oriented count 42*4 = 168 (active packet weight).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STEP_PATH = ROOT / "data" / "tomotope_toroidal_step_transport_bridge.json"
DUAL_PATH = ROOT / "data" / "tomotope_toroidal_dual_packet_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_edge_pair_bridge.json"


@dataclass(frozen=True)
class EdgePairSummary:
    csaszar_edges: int
    szilassi_edges: int
    combined_dual_edges: int
    unoriented_transport_count: int
    oriented_transport_count: int
    slot_stabilizer_size: int
    stabilizer_weighted_oriented: int
    active_packet_weight: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    step = json.loads(STEP_PATH.read_text(encoding="utf-8"))
    dual = json.loads(DUAL_PATH.read_text(encoding="utf-8"))

    cs_edges = int(dual["polyhedra"]["csaszar"]["edges"])
    sz_edges = int(dual["polyhedra"]["szilassi"]["edges"])
    combined_edges = cs_edges + sz_edges

    unoriented = int(step["summary"]["unoriented_transport_count"])
    oriented = int(step["summary"]["oriented_transport_count"])
    stabilizer = int(step["summary"]["slot_stabilizer_size"])
    weighted = oriented * stabilizer
    active_packet = int(step["summary"]["active_packet_weight"])

    identities = {
        "csaszar_edges_21": cs_edges == 21,
        "szilassi_edges_21": sz_edges == 21,
        "combined_edges_42": combined_edges == 42,
        "unoriented_transport_21": unoriented == 21,
        "oriented_transport_42": oriented == 42,
        "unoriented_equals_each_single_edge_shell": (unoriented == cs_edges == sz_edges),
        "oriented_equals_combined_dual_edges": oriented == combined_edges,
        "oriented_equals_two_times_unoriented": oriented == 2 * unoriented,
        "weighted_oriented_equals_168": weighted == 168,
        "weighted_oriented_matches_active_packet": weighted == active_packet,
    }

    summary = EdgePairSummary(
        csaszar_edges=cs_edges,
        szilassi_edges=sz_edges,
        combined_dual_edges=combined_edges,
        unoriented_transport_count=unoriented,
        oriented_transport_count=oriented,
        slot_stabilizer_size=stabilizer,
        stabilizer_weighted_oriented=weighted,
        active_packet_weight=active_packet,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCVII certificate: oriented transport 42 is exactly the combined dual-edge "
            "shell 21+21 from Csaszar and Szilassi. With slot stabilizer 4 this closes "
            "to the active packet weight 168."
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
