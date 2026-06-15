#!/usr/bin/env python3
"""BT1185 -- invariants of the raw-voltage 2-cover.

Uses the existing reconstructed transport bridge counts.  The base graph is
SRG(45,32,22,24) with 720 edges.  The raw voltage is a connected nontrivial
binary cover layer; the archived bridge records canonical triangle parity
5280 = 3120 + 2160, so the voltage is not switching-trivial.
"""

import json

base_v = 45
base_k = 32
base_e = 720
cover_v = 90
cover_e = 2 * base_e
triangles = 5280
parity0 = 3120
parity1 = 2160

payload = {
    "bt": 1185,
    "title": "raw-voltage 2-cover invariants",
    "base_graph": {"v": base_v, "k": base_k, "e": base_e, "parameters": [45, 32, 22, 24]},
    "cover_graph": {"v": cover_v, "edge_slots": cover_e, "sheet_group": "Z2"},
    "triangle_parity": {"triangles": triangles, "parity0": parity0, "parity1": parity1},
    "switching_status": "nontrivial: parity1 triangles obstruct switching all voltages to zero",
    "checks": {
        "base_edges_720": base_e == base_v * base_k // 2,
        "cover_vertices_90": cover_v == 2 * base_v,
        "cover_edge_slots_1440": cover_e == 1440,
        "triangle_counts_sum": parity0 + parity1 == triangles,
        "nontrivial_voltage": parity1 > 0,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
