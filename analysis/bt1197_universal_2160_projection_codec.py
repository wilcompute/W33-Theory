#!/usr/bin/env python3
"""BT1197 -- explicit universal 2160 projection codec.

After reading photonic_holonet.tex end to end, the right carrier is not a direct
720->270 collapse.  It is the common refinement

    C_2160 = {0..44} x {0..47}.

The 45-coordinate is simultaneously the triple-45 object and the D4-coset index
[Sp(4,3):Aut(D4)].  The 48-coordinate is the BT748 half-fiber coordinate.  Its
internal factorizations explain all blocked projections:

    48 = 16*3 = 6*8 = 2*24.

Therefore
    2160 = (45*16)*3 = (45*6)*8 = (45*2)*24 = 45*48.

This script gives the exact row codec.  It is a carrier/projection theorem, not
an incidence-isomorphism theorem: objectwise edge labels still need the older
transport data.
"""

from __future__ import annotations

import json

N45 = 45
H48 = 48


def row(t: int, h: int) -> dict:
    return {
        "triple45": t,
        "d4_coset": t,
        "half_fiber48": h,
        "edge720": 16 * t + (h % 16),
        "c3_label": h // 16,
        "edge270": 6 * t + (h // 8),
        "support8": h % 8,
        "cover90_vertex": 2 * t + (h // 24),
        "twoT24": h % 24,
        "z2_sheet": h // 24,
    }


def main():
    rows = [row(t, h) for t in range(N45) for h in range(H48)]
    payload = {
        "bt": 1197,
        "title": "universal 2160 projection codec",
        "carrier": "C2160 = 45 x 48",
        "factorizations": {
            "45_times_48": N45 * H48,
            "720_times_3": 720 * 3,
            "270_times_8": 270 * 8,
            "90_times_24": 90 * 24,
        },
        "projection_rules": {
            "to_720xC3": "edge720=16*t+(h mod 16), c3=floor(h/16)",
            "to_270x8": "edge270=6*t+floor(h/8), support8=h mod 8",
            "to_90x2T": "cover90=2*t+floor(h/24), twoT=h mod 24",
            "to_45x48": "triple45=t, half_fiber=h",
        },
        "sample_rows": [rows[i] for i in [0, 1, 15, 16, 23, 24, 47, 48, 2159]],
        "checks": {
            "row_count_2160": len(rows) == 2160,
            "unique_720_c3_pairs": len({(r["edge720"], r["c3_label"]) for r in rows}) == 2160,
            "unique_270_support_pairs": len({(r["edge270"], r["support8"]) for r in rows}) == 2160,
            "unique_90_2T_pairs": len({(r["cover90_vertex"], r["twoT24"]) for r in rows}) == 2160,
            "unique_45_48_pairs": len({(r["triple45"], r["half_fiber48"]) for r in rows}) == 2160,
        },
    }
    payload["checks"]["all_checks_pass"] = all(payload["checks"].values())
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
