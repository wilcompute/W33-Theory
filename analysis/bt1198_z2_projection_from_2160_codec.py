#!/usr/bin/env python3
"""BT1198 -- test the 720-edge Z2 projection from the 2160 codec.

The projection C2160 -> 720 x C3 is bijective, but raw Z2 voltage is not a
function of the C3 label alone.  This is the crucial obstruction: C3 has no
nontrivial homomorphism to Z2, and in the explicit half-fiber codec the Z2 sheet
is h//24, which depends on the 16-slot edge residue as well as the C3 layer.
Therefore the raw Z2 voltage must come from the 2*24 half-fiber / 2T side or
from S3 parity, not from a bare C3 projection.
"""

from __future__ import annotations

import json
from collections import defaultdict

rows = []
for t in range(45):
    for h in range(48):
        rows.append({
            "edge720": 16 * t + (h % 16),
            "slot16": h % 16,
            "c3": h // 16,
            "z2": h // 24,
        })

z2_by_c3 = defaultdict(set)
z2_by_edge_c3 = defaultdict(set)
for r in rows:
    z2_by_c3[r["c3"]].add(r["z2"])
    z2_by_edge_c3[(r["edge720"], r["c3"])].add(r["z2"])

payload = {
    "bt": 1198,
    "title": "Z2 projection from C2160 codec",
    "projection_720xC3_bijective": len({(r["edge720"], r["c3"]) for r in rows}) == 2160,
    "z2_by_c3": {str(k): sorted(v) for k, v in sorted(z2_by_c3.items())},
    "z2_is_function_of_c3_alone": all(len(v) == 1 for v in z2_by_c3.values()),
    "z2_is_function_of_edge720_and_c3": all(len(v) == 1 for v in z2_by_edge_c3.values()),
    "homomorphism_obstruction": "C3 has no nontrivial group homomorphism to Z2",
    "interpretation": "raw Z2 cannot be recovered from the C3 sheet label alone; it needs half-fiber parity/2T or S3 parity data",
    "checks": {
        "projection_size_2160": len(rows) == 2160,
        "projection_720xC3_bijective": len({(r["edge720"], r["c3"]) for r in rows}) == 2160,
        "c3_not_enough": not all(len(v) == 1 for v in z2_by_c3.values()),
        "edge_c3_enough_as_codec": all(len(v) == 1 for v in z2_by_edge_c3.values()),
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
