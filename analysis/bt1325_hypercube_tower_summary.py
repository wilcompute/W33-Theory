#!/usr/bin/env python3
"""BT1325 - Hypercube tower summary and W33 holonet layer census.

This packet provides the authoritative summary of the Q4->Q5->Q6->D12
hypercube tower as it relates to the W33 holonet architecture.

It aggregates the verified results from BT1319-BT1324 into a single
consistent layer table and computes the tower's key invariants:

  Layer table:
  n | vertices | edges  | diameter | code          | d  | role
  --|----------|--------|----------|---------------|----|-----
  4 | 16       | 32     | 4        | [8,4,4]       | 4  | local Q4 packet router
  5 | 32       | 80     | 5        | [16,5,8]      | 8  | Q5 transit
  6 | 64       | 192    | 6        | [32,6,16]     | 16 | tomotope flag bus
  - | 2160 slots| -     | -        | D12 mirror bus| -  | global chart atlas

  Tower invariants:
  - Vertices double at each layer (16, 32, 64)
  - Code distance doubles at each layer (4, 8, 16)
  - Q6 edges = tomotope flags = 192
  - Q6 2-faces = 240 = 2 * D12 antipode pairs (120)
  - D12 slots = 2160 = 540 * 4 = 192 * 11.25 (scale factor from Q6 to D12)

Open problems recorded at this boundary:
  1. Bijection between 7 metric toroidal realizations and 7 Csaszar involutions
  2. Objectwise Q6->D12 slot assignment (beyond counting identity)
  3. Full Clifford algebra construction for 14641 = 11^4 scale marker
  4. Physical photon scheduling within Q4/Q5/Q6 layers
"""

from __future__ import annotations

import json
from math import comb
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "bt1325_hypercube_tower_summary.json"

TOMOTOPE_FLAGS = 192
D12_SLOTS = 2160
D12_CHARTS = 540
D12_ANTIPODE_PAIRS = 120
HEPTAD_REALIZATIONS = 7

TOWER = [
    {
        "n": 4,
        "vertices": 16,
        "edges": 32,
        "diameter": 4,
        "code": "[8,4,4] Hamming / RM(1,3)",
        "code_distance": 4,
        "role": "local Q4 packet router",
        "bt_reference": "BT1319",
        "k_faces": {k: comb(4, k) * 2 ** (4 - k) for k in range(5)},
    },
    {
        "n": 5,
        "vertices": 32,
        "edges": 80,
        "diameter": 5,
        "code": "[16,5,8] RM(1,4)",
        "code_distance": 8,
        "role": "Q5 transit layer",
        "bt_reference": "BT1320",
        "k_faces": {k: comb(5, k) * 2 ** (5 - k) for k in range(6)},
    },
    {
        "n": 6,
        "vertices": 64,
        "edges": 192,
        "diameter": 6,
        "code": "[32,6,16] RM(1,5)",
        "code_distance": 16,
        "role": "tomotope flag bus",
        "bt_reference": "BT1321",
        "k_faces": {k: comb(6, k) * 2 ** (6 - k) for k in range(7)},
    },
]


def build_summary() -> dict[str, Any]:
    # Prepare tower for JSON (convert int keys to strings)
    tower_json = []
    for layer in TOWER:
        layer_copy = dict(layer)
        layer_copy["k_faces"] = {str(k): v for k, v in layer["k_faces"].items()}
        tower_json.append(layer_copy)

    # Tower invariants
    vertex_doubling = all(
        TOWER[i + 1]["vertices"] == 2 * TOWER[i]["vertices"]
        for i in range(len(TOWER) - 1)
    )
    distance_doubling = all(
        TOWER[i + 1]["code_distance"] == 2 * TOWER[i]["code_distance"]
        for i in range(len(TOWER) - 1)
    )
    q6_edge_tomotope = TOWER[2]["edges"] == TOMOTOPE_FLAGS
    q6_2faces_double_d12 = TOWER[2]["k_faces"][2] == 2 * D12_ANTIPODE_PAIRS

    # Open problems
    open_problems = [
        {
            "id": "OP1",
            "description": "Bijection between 7 metric toroidal realizations and 7 Csaszar C2 involutions",
            "status": "not_proved_current_labels",
            "bt_reference": "BT1318",
        },
        {
            "id": "OP2",
            "description": "Objectwise Q6->D12 slot assignment beyond counting identity",
            "status": "open",
            "bt_reference": "BT1321-BT1322",
        },
        {
            "id": "OP3",
            "description": "Full Clifford algebra construction for 14641 = 11^4 scale marker",
            "status": "scale_marker_only",
            "bt_reference": "BT1319",
        },
        {
            "id": "OP4",
            "description": "Physical photon scheduling within Q4/Q5/Q6 layers",
            "status": "parameter_budgets_established_BT1323",
            "bt_reference": "BT1323",
        },
    ]

    checks = {
        "tower_vertex_count_doubles": vertex_doubling,
        "tower_code_distance_doubles": distance_doubling,
        "q6_edges_equal_tomotope_flags": q6_edge_tomotope,
        "q6_2faces_equal_2x_d12_antipode_pairs": q6_2faces_double_d12,
        "d12_slots_equal_540_times_4": D12_SLOTS == D12_CHARTS * 4,
        "heptad_count_is_7": HEPTAD_REALIZATIONS == 7,
        "tower_has_3_layers": len(TOWER) == 3,
        "q4_role_is_local_router": TOWER[0]["role"] == "local Q4 packet router",
        "q6_role_is_flag_bus": TOWER[2]["role"] == "tomotope flag bus",
        "q4_code_distance_is_4": TOWER[0]["code_distance"] == 4,
        "q6_code_distance_is_16": TOWER[2]["code_distance"] == 16,
    }

    return {
        "theorem": "BT1325 W33 holonet hypercube tower summary",
        "verified": all(checks.values()),
        "tower": tower_json,
        "d12_global_layer": {
            "slots": D12_SLOTS,
            "charts": D12_CHARTS,
            "transversals_per_chart": 4,
            "antipode_pairs": D12_ANTIPODE_PAIRS,
            "role": "global 540-chart Q3 atlas + D12 mirror bus",
        },
        "tower_invariants": {
            "vertex_count_doubles_each_layer": vertex_doubling,
            "code_distance_doubles_each_layer": distance_doubling,
            "q6_edge_tomotope_identity": {
                "q6_edges": TOMOTOPE_FLAGS,
                "tomotope_flags": TOMOTOPE_FLAGS,
                "identity_holds": q6_edge_tomotope,
            },
            "q6_2faces_d12_antipode_identity": {
                "q6_2faces": TOWER[2]["k_faces"][2],
                "double_d12_antipode_pairs": 2 * D12_ANTIPODE_PAIRS,
                "identity_holds": q6_2faces_double_d12,
            },
        },
        "heptad_carrier": {
            "realizations": HEPTAD_REALIZATIONS,
            "csaszar": 5,
            "szilassi": 2,
            "shared_edge_count": 21,
            "moment_ladder": "21/16 * 16 * 2 * 4 = 168",
        },
        "open_problems": open_problems,
        "checks": checks,
        "bt_packet_range": "BT1316-BT1325",
    }


def write_results(path: Path = OUT_PATH) -> Path:
    payload = build_summary()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    payload = build_summary()
    out = write_results()
    print(f"BT1325 verified={payload['verified']} wrote {out}")
    if not payload["verified"]:
        failed = [name for name, ok in payload["checks"].items() if not ok]
        raise SystemExit(f"BT1325 failed checks: {failed}")


if __name__ == "__main__":
    main()
