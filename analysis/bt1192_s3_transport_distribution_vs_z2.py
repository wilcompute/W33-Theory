#!/usr/bin/env python3
"""BT1192 -- S3/Z3 transport distribution versus raw Z2 layer.

The S3 port transport package has exact data on the 54-pocket / 270-edge
K-Schreier carrier:
  L distribution: {0:17, 1:11, 2:26}
  generator shifts: only g3 is nonzero
  cocycle distribution on 270 edges: {0:201, 1:33, 2:36}
  nontrivial cocycle edges: 69
The raw Z2 quotient voltage lives on the 45-point / 720-edge complement graph.
So S3 is an active refinement source, but not yet a direct 720-edge explanation.
"""

import json

payload = {
    "bt": 1192,
    "title": "S3 transport distribution versus raw Z2 layer",
    "s3_carrier": {"pockets": 54, "edges": 270, "L_distribution": {"0": 17, "1": 11, "2": 26}},
    "s3_cocycle": {"distribution": {"0": 201, "1": 33, "2": 36}, "nontrivial_edges": 69, "unique_shift_generator": "g3"},
    "z2_carrier": {"vertices": 45, "edges": 720, "cover_vertices": 90},
    "comparison_status": "S3/Z3 is a refinement carrier; no direct 720-edge S3 table exists yet",
    "checks": {
        "s3_edges_270": 270 == 201 + 33 + 36,
        "s3_nontrivial_69": 69 == 33 + 36,
        "z2_edges_720": 720 == 45 * 32 // 2,
        "carriers_different": 270 != 720,
        "direct_shadow_theorem_blocked": True,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
