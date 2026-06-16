#!/usr/bin/env python3
"""BT1199 -- test the 270-edge S3 projection from the 2160 codec.

The 2160 carrier projects cleanly to 270 x 8 by factoring the 48 half-fiber as
6 x 8.  Reading the factor 6 as S3 gives

    C2160 = 45 x 48 = 45 x 6 x 8 = 270 x 8.

The same carrier also equals 54 x 40, because 270 x 8 = 54 x 5 x 8.  This is the
new holonet-compatible interpretation: the 54-pocket S3 carrier can be read as
54 pockets each carrying a full 40-slot W33 shell (5 local edge choices times 8
support slots).  Thus the S3 route is not a direct 720-edge table; it is a
pocket/W33-shell projection of the common 2160 carrier.
"""

from __future__ import annotations

import itertools
import json

# fixed order of S3 permutations; sign is the honest S3 -> Z2 abelianization
S3 = list(itertools.permutations((0, 1, 2)))
def sign(p):
    inv = sum(1 for i in range(3) for j in range(i+1,3) if p[i] > p[j])
    return inv % 2

rows = []
for t in range(45):
    for h in range(48):
        s3_index = h // 8
        support8 = h % 8
        edge270 = 6 * t + s3_index
        pocket54 = edge270 // 5
        local5 = edge270 % 5
        w33_slot40 = 8 * local5 + support8
        rows.append({
            "triple45": t,
            "half48": h,
            "s3_index": s3_index,
            "s3_perm": S3[s3_index],
            "s3_parity": sign(S3[s3_index]),
            "edge270": edge270,
            "support8": support8,
            "pocket54": pocket54,
            "w33_slot40": w33_slot40,
        })

payload = {
    "bt": 1199,
    "title": "S3 projection from universal 2160 codec",
    "projection_270x8_bijective": len({(r["edge270"], r["support8"]) for r in rows}) == 2160,
    "projection_54x40_bijective": len({(r["pocket54"], r["w33_slot40"]) for r in rows}) == 2160,
    "s3_parity_distribution": {"even": sum(1 for r in rows if r["s3_parity"] == 0), "odd": sum(1 for r in rows if r["s3_parity"] == 1)},
    "interpretation": "S3 transport is a pocket/W33-shell projection: 2160=270*8=54*40; S3 parity exists, unlike bare C3->Z2",
    "checks": {
        "row_count_2160": len(rows) == 2160,
        "projection_270x8_bijective": len({(r["edge270"], r["support8"]) for r in rows}) == 2160,
        "projection_54x40_bijective": len({(r["pocket54"], r["w33_slot40"]) for r in rows}) == 2160,
        "s3_even_odd_balanced": sum(1 for r in rows if r["s3_parity"] == 0) == sum(1 for r in rows if r["s3_parity"] == 1) == 1080,
    },
}
payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
print(json.dumps(payload, indent=2, sort_keys=True))
