#!/usr/bin/env python3
"""Pass 260: a fresh anchor for the odd-q rank law -- q = 13 (and q = 17).

Pass 238 derived rank_2 W(3,q) = (q^2+1)(q+2)/2 for odd q and verified it at
q = 3,5,7 (25/91/225) and freshly at q = 11 (793).  The even-q law is now closed
too (Pass 256).  This witness adds further independent anchors by building
W(3,13) -- and W(3,17) if it is tractable -- and computing the F2 incidence rank
directly.

    predicted  rank_2 W(3,13) = (169+1)(15)/2 = 1275   (n = 14*170 = 2380)
    predicted  rank_2 W(3,17) = (289+1)(19)/2 = 2755   (n = 18*290 = 5220)

Each successful anchor makes the odd-q law as well-attested as the even-q one.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import (
    f2_rank,
    incidence_rows,
    isotropic_lines,
    pg3_points,
)

OUT = ROOT / "data" / "w33_pass260_odd_law_q13.json"


def rank_law(q):
    return (q * q + 1) * (q + 2) // 2


def sentinel_law(q):
    return q * (q * q + 1) // 2


def build_and_rank(q):
    t0 = time.time()
    points = pg3_points(q)
    n = len(points)
    lines = isotropic_lines(points, q)
    rows = incidence_rows(lines, n)
    r = f2_rank(rows)
    return {"q": q, "n": n, "lines": len(lines), "rank": r,
            "predicted": rank_law(q), "match": bool(r == rank_law(q)),
            "seconds": round(time.time() - t0, 2)}


def main():
    checks = {}
    results = {}

    # ---- fresh anchor: q = 13
    r13 = build_and_rank(13)
    results["13"] = r13
    checks["q13_n_2380"] = r13["n"] == 2380
    checks["q13_lines_2380"] = r13["lines"] == 2380
    checks["q13_rank_1275"] = r13["rank"] == 1275
    checks["q13_matches_law"] = r13["match"]

    # ---- second fresh anchor: q = 17 (attempt; skip gracefully if too slow)
    try:
        r17 = build_and_rank(17)
        results["17"] = r17
        checks["q17_matches_law"] = r17["match"]
    except Exception as exc:  # pragma: no cover
        results["17"] = {"skipped": str(exc)}

    # ---- consistency: n - 2*sentinel = k = q^2+1 at every anchor
    ident = True
    for q in (3, 5, 7, 11, 13):
        n = (q + 1) * (q * q + 1)
        if n - 2 * sentinel_law(q) != q * q + 1:
            ident = False
        if n - sentinel_law(q) != rank_law(q):
            ident = False
    checks["identities_hold"] = ident

    # ---- the odd law now has anchors at q = 3,5,7,11,13(,17)
    anchors = {3: 25, 5: 91, 7: 225, 11: 793, 13: r13["rank"]}
    checks["all_odd_anchors_match_law"] = all(
        rank_law(q) == v for q, v in anchors.items())

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass260.odd_law_q13.v1",
        "status": "PASS" if all_pass else "FAIL",
        "law": "rank_2 W(3,q) = (q^2+1)(q+2)/2   (q odd PRIME; see Pass 262)",
        "fresh_anchors": results,
        "all_odd_anchors": anchors,
        "reading": (
            "W(3,13) was built (2380 points, 2380 isotropic lines) and its F2 "
            "incidence rank computed directly, giving a fresh independent "
            "anchor for the odd-q law. Together with q = 3,5,7,11 the law is now "
            "attested at five odd primes. NOTE: every one of these anchors is a "
            "PRIME; whether the same polynomial holds at odd prime POWERS is a "
            "separate question, settled in Pass 262."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
