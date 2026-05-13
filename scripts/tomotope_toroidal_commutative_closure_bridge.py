#!/usr/bin/env python3
"""Part DCXII: commutative closure bridge.

This certificate checks that all recently-added views commute to the same
invariants:

  21 + 21 = 42,
  42 * 4 = 168,
  (8,14) <-> (4,7) with factor 2.

Inputs are the generated artifacts from DCVII, DCIX, DCVIII, and DCXI.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EDGE_PAIR_PATH = ROOT / "data" / "tomotope_toroidal_edge_pair_bridge.json"
DIRECTIONAL_PATH = ROOT / "data" / "tomotope_toroidal_directional_split_bridge.json"
FAMILY_ENERGY_PATH = ROOT / "data" / "tomotope_toroidal_family_energy_split_bridge.json"
DUALITY_PATH = ROOT / "data" / "tomotope_toroidal_horizon_duality_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_commutative_closure_bridge.json"


@dataclass(frozen=True)
class ClosureSummary:
    edge_pair_total: int
    directional_total: int
    family_total: int
    transport_total: int
    weighted_total: int
    half_split_value: int
    directional_half_horizon: int
    energy_half_horizon: int
    directional_packet_horizon: int
    energy_packet_horizon: int
    all_identities_hold: bool


def build_bridge() -> dict[str, Any]:
    edge_pair = json.loads(EDGE_PAIR_PATH.read_text(encoding="utf-8"))
    directional = json.loads(DIRECTIONAL_PATH.read_text(encoding="utf-8"))
    family = json.loads(FAMILY_ENERGY_PATH.read_text(encoding="utf-8"))
    duality = json.loads(DUALITY_PATH.read_text(encoding="utf-8"))

    edge_total = int(edge_pair["summary"]["combined_dual_edges"])
    dir_total = int(directional["summary"]["total_oriented_count"])
    fam_total = int(family["summary"]["oriented_edges_total"])
    transport_total = int(edge_pair["summary"]["oriented_transport_count"])
    weighted = int(edge_pair["summary"]["stabilizer_weighted_oriented"])

    cs_edges = int(edge_pair["summary"]["csaszar_edges"])
    sz_edges = int(edge_pair["summary"]["szilassi_edges"])
    forward = int(directional["summary"]["forward_oriented_count"])
    backward = int(directional["summary"]["backward_oriented_count"])

    d_half = int(duality["summary"]["directional_half_horizon"])
    e_half = int(duality["summary"]["energy_one_channel_horizon"])
    d_packet = int(duality["summary"]["directional_packet_horizon"])
    e_packet = int(duality["summary"]["energy_packet_horizon"])

    identities = {
        "upstream_edge_pair_ok": bool(edge_pair["summary"]["all_identities_hold"]),
        "upstream_directional_ok": bool(directional["summary"]["all_identities_hold"]),
        "upstream_family_ok": bool(family["summary"]["all_identities_hold"]),
        "upstream_duality_ok": bool(duality["summary"]["all_identities_hold"]),
        "all_totals_equal_42": edge_total == dir_total == fam_total == transport_total == 42,
        "all_halves_equal_21": cs_edges == sz_edges == forward == backward == 21,
        "weighted_total_is_168": weighted == 168,
        "duality_half_8_4": (d_half, e_half) == (8, 4),
        "duality_packet_14_7": (d_packet, e_packet) == (14, 7),
        "duality_factor_two": d_half == 2 * e_half and d_packet == 2 * e_packet,
    }

    summary = ClosureSummary(
        edge_pair_total=edge_total,
        directional_total=dir_total,
        family_total=fam_total,
        transport_total=transport_total,
        weighted_total=weighted,
        half_split_value=cs_edges,
        directional_half_horizon=d_half,
        energy_half_horizon=e_half,
        directional_packet_horizon=d_packet,
        energy_packet_horizon=e_packet,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCXII commutative closure: edge/family/directional/transport views all "
            "meet at 42 with identical 21+21 halves, weighted closure 168, and "
            "matched horizon duality (8,14)<->(4,7)."
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
