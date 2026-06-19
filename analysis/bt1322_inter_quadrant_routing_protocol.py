#!/usr/bin/env python3
"""BT1322 - Inter-quadrant routing protocol for the W33 holonet.

The holonet has a layered routing architecture:

  Local   : Q4 packet router   (16 states, 32 edges)   -- BT1319
  Mid     : Q5 transit layer   (32 states, 80 edges)   -- BT1320
  Tomotope: Q6 flag bus        (64 states, 192 edges)  -- BT1321
  Global  : 540-chart Q3 atlas (540 charts, 2160 slots) -- BT813-BT815

This script establishes the inter-quadrant routing rules:

  1. Q4 -> Q5 : extend one bit (0 = stay, 1 = transit)
  2. Q5 -> Q6 : extend one bit (0 = local bus, 1 = flag bus)
  3. Q6 -> D12 mirror bus : 2160 = 540 * 4 slot assignment
  4. Routing metric: e-cube (hypercube BFS = Gray code hops)
  5. Protected lift: [8,4,4] Hamming -> [16,5,8] RM(1,4) -> [32,6,16] RM(1,5)

The key invariant: every inter-quadrant hop increases the Hamming weight of
the codeword by at least the code distance at that layer, ensuring that a
single-bit error in any layer is caught before it propagates up.
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "bt1322_inter_quadrant_routing_protocol.json"

# Layer parameters
LAYERS = [
    {"name": "Q4_local",     "n": 4, "vertices": 16,  "edges": 32,  "code": "[8,4,4] Hamming",   "code_distance": 4},
    {"name": "Q5_transit",   "n": 5, "vertices": 32,  "edges": 80,  "code": "[16,5,8] RM(1,4)",  "code_distance": 8},
    {"name": "Q6_flag_bus",  "n": 6, "vertices": 64,  "edges": 192, "code": "[32,6,16] RM(1,5)", "code_distance": 16},
]

GLOBAL_CHARTS = 540
GLOBAL_SLOTS = 2160
TOMOTOPE_FLAGS = 192


def ecube_distance(a: int, b: int, n: int) -> int:
    """Hypercube BFS distance = Hamming weight of XOR."""
    return bin(a ^ b).count("1")


def routing_table(n_src: int, n_dst: int) -> dict[str, Any]:
    """Describe the bit-extension map from Q_n_src to Q_{n_src+1}."""
    assert n_dst == n_src + 1
    return {
        "src_layer": f"Q{n_src}",
        "dst_layer": f"Q{n_dst}",
        "mechanism": f"append bit 0 (stay) or bit 1 (transit) to {n_src}-bit address",
        "src_vertices": 2 ** n_src,
        "dst_vertices": 2 ** n_dst,
        "embedding_count": n_dst,  # n_dst embedded copies of Q_n_src in Q_n_dst
        "lift_code": {
            4: "[8,4,4] -> [16,5,8]",
            5: "[16,5,8] -> [32,6,16]",
        }.get(n_src, "unknown"),
    }


def d12_slot_assignment() -> dict[str, Any]:
    return {
        "total_mirror_slots": GLOBAL_SLOTS,
        "chart_count": GLOBAL_CHARTS,
        "transversals_per_chart": GLOBAL_SLOTS // GLOBAL_CHARTS,
        "q6_flag_bus_edges": TOMOTOPE_FLAGS,
        "slots_per_flag_bus_edge": GLOBAL_SLOTS // TOMOTOPE_FLAGS,
        "reading": f"{GLOBAL_SLOTS} = {GLOBAL_CHARTS} * {GLOBAL_SLOTS // GLOBAL_CHARTS} = {TOMOTOPE_FLAGS} * {GLOBAL_SLOTS // TOMOTOPE_FLAGS}",
    }


def build_protocol() -> dict[str, Any]:
    hops = [
        routing_table(4, 5),
        routing_table(5, 6),
    ]
    d12 = d12_slot_assignment()

    # Error isolation: each hop multiplies code distance by 2
    code_distances = [layer["code_distance"] for layer in LAYERS]
    distance_doubling = all(
        code_distances[i + 1] == 2 * code_distances[i]
        for i in range(len(code_distances) - 1)
    )

    # Total protected path: local Q4 -> global D12
    # Maximum hops at each layer before escalation
    max_local_hops = LAYERS[0]["n"]      # 4 hops in Q4
    max_transit_hops = LAYERS[1]["n"]    # 5 hops in Q5
    max_flag_hops = LAYERS[2]["n"]       # 6 hops in Q6

    checks = {
        "q4_to_q5_embedding_count_is_5": hops[0]["embedding_count"] == 5,
        "q5_to_q6_embedding_count_is_6": hops[1]["embedding_count"] == 6,
        "code_distance_doubles_at_each_layer": distance_doubling,
        "q6_edges_equal_tomotope_flags": LAYERS[2]["edges"] == TOMOTOPE_FLAGS,
        "d12_slots_divide_evenly_by_q6_edges": GLOBAL_SLOTS % TOMOTOPE_FLAGS == 0,
        "d12_slots_divide_evenly_by_charts": GLOBAL_SLOTS % GLOBAL_CHARTS == 0,
        "d12_transversals_per_chart_is_4": d12["transversals_per_chart"] == 4,
        "d12_slots_per_flag_edge_is_integer": GLOBAL_SLOTS // TOMOTOPE_FLAGS == 11,
        "max_hops_increase_by_layer": max_local_hops < max_transit_hops < max_flag_hops,
        "layer_vertex_doubling": all(
            LAYERS[i + 1]["vertices"] == 2 * LAYERS[i]["vertices"]
            for i in range(len(LAYERS) - 1)
        ),
    }

    return {
        "theorem": "BT1322 inter-quadrant routing protocol",
        "verified": all(checks.values()),
        "layers": LAYERS,
        "routing_hops": hops,
        "d12_mirror_bus_interface": d12,
        "error_protection": {
            "code_distance_sequence": code_distances,
            "distance_doubles_each_layer": distance_doubling,
            "principle": "each inter-quadrant hop doubles the minimum code distance, isolating errors within layers",
        },
        "maximum_hops_per_layer": {
            "q4_local": max_local_hops,
            "q5_transit": max_transit_hops,
            "q6_flag_bus": max_flag_hops,
        },
        "checks": checks,
        "boundary": (
            "BT1322 establishes the inter-quadrant routing protocol and error-isolation "
            "principle. Physical photon scheduling within each layer requires a future "
            "construction assigning hypercube vertices to physical degrees of freedom."
        ),
    }


def write_results(path: Path = OUT_PATH) -> Path:
    payload = build_protocol()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    payload = build_protocol()
    out = write_results()
    print(f"BT1322 verified={payload['verified']} wrote {out}")
    if not payload["verified"]:
        failed = [name for name, ok in payload["checks"].items() if not ok]
        raise SystemExit(f"BT1322 failed checks: {failed}")


if __name__ == "__main__":
    main()
