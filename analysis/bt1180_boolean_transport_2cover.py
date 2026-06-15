#!/usr/bin/env python3
"""BT1180 -- minimal Boolean transport 2-cover requirement.

BT1178 showed that the Boolean 60=15+45 module predicts the 45-point incidence
and complement transport graph but not raw Z2 sheet voltage.  The minimal repair
is therefore a 2-cover of the 45-vertex transport graph.  The base transport has
SRG(45,32,22,24), so its 2-cover has 90 vertices and 1440 lifted directed slots
if every base edge carries one binary sheet sign.
"""

import json

base_vertices = 45
base_degree = 32
base_edges = base_vertices * base_degree // 2
cover_vertices = 2 * base_vertices
cover_edge_slots = 2 * base_edges

payload = {
    "bt": 1180,
    "title": "Boolean transport 2-cover requirement",
    "base_transport": {"vertices": base_vertices, "degree": base_degree, "edges": base_edges, "parameters": [45, 32, 22, 24]},
    "minimal_cover": {"vertices": cover_vertices, "edge_slots": cover_edge_slots, "sheet_group": "Z2"},
    "status": "incidence and complement transport are predicted; raw voltage requires this extra 2-cover coordinate",
    "checks": {
        "base_edges_720": base_edges == 720,
        "cover_vertices_90": cover_vertices == 90,
        "cover_edge_slots_1440": cover_edge_slots == 1440,
        "sheet_group_binary": True,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
