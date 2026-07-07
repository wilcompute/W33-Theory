#!/usr/bin/env python3
"""
One law, two proofs: the constant nine-point page bill is the safe-zone overlap and the TD(4,3) churn,
and they are the same object. Pass 65 derived the relocation page bill from safe-zone overlap
(|Gamma(p) cap Gamma(q)| = 18 for every ordered pair, so the bill is 27 - 18 = 9). The parallel track's
BT1809/BT1816 derived the same nine independently from the TD(4,3) transversal design, with survival
histograms {3:6, 0:3} for edge moves and {2:9} for non-edge moves. This witness runs BOTH derivations
on the committed geometry and proves they are one theorem, then explains the edge/non-edge split with
Pass 66's rebuilt-line rule:

  THE SAME NINE. For all 1560 ordered moves p -> q, BT1816's retained count (survival summed over the
  destination triads against the source safe zone) equals the safe-zone overlap |safe(p) cap safe(q)|
  computed independently -- always 18 -- so both give the identical nine-point churn. The TD(4,3)
  bill and the overlap bill are literally the same set difference.

  THE EDGE SPLIT IS THE REBUILT LINE. For an edge move p -> q, BT1816's three fully-churned (survival-0)
  destination triads are EXACTLY the three phase rows whose center quad contains p -- the AG(2,3) line
  indexed by the departing center (Pass 66). So their observation that edge moves "preserve phase
  structure" (churn = three whole phase blocks) is explained: the churn is a line of the destination's
  phase plane, and by Pass 66 its three quads meet in exactly {p}. Edge re-keying is not just
  phase-coherent, it is ADDRESSED.

  THE NON-EDGE SPLIT IS TRANSVERSAL. For a non-edge move the nine churned points are one per
  destination triad (histogram {2:9}): the churn is a transversal of the phase plane, not a line --
  which is why non-edge moves scramble phase structure while edge moves preserve it. The two histograms
  {3:6,0:3} and {2:9} are the line/transversal dichotomy of the AG(2,3) directory.

Honest scope: exact finite computation over all 1560 ordered moves, using the parallel track's
committed BT1816 move_profile and bt1807 geometry alongside an independent safe-zone computation from
w33_master_audit. The result unifies two committed derivations into one theorem with two proofs and
supplies the geometric reason for the edge/non-edge dichotomy; no new numeric bill is introduced.
"""

from __future__ import annotations

import json
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bt1807_defect_phase_plane_transversal_design as td43  # noqa: E402
import bt1816_page_cache_churn_simulator as bt1816  # noqa: E402
import w33_master_audit as audit  # noqa: E402


def main():
    print(
        "== one law, two proofs: safe-zone overlap = TD(4,3) churn = the nine-point bill ==\n"
    )
    checks = []

    def chk(name, ok):
        checks.append((name, bool(ok)))
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}")

    # geometries (same indexing): their td43 and my master_audit
    pts_t, adj_t, _ = td43.build_w33()
    pts, A, lines, B = audit._build(3)
    n = len(pts)
    my_safe = [
        frozenset(x for x in range(n) if x != p and not A[p][x]) for p in range(n)
    ]

    # A. the same nine, over all 1560 ordered moves
    same = True
    bills = set()
    for p in range(n):
        for q in range(n):
            if p == q:
                continue
            prof = bt1816.move_profile(p, q, pts_t, adj_t)
            retained_td = sum(k * v for k, v in prof.items())
            overlap_me = len(my_safe[p] & my_safe[q])
            if retained_td != overlap_me:
                same = False
            bills.add(27 - retained_td)
    chk(
        "SAME NINE: BT1816 TD(4,3) retained-count == independent safe-zone overlap for all 1560 moves",
        same,
    )
    chk(
        f"both give a constant {sorted(bills)} churn = the nine-point page bill",
        bills == {9},
    )

    # B. the edge split is the rebuilt line (Pass 66)
    edge_ok = True
    for p in range(n):
        for q in (x for x in range(n) if A[p][x]):
            rows_q, _, _ = td43.vector_table(q, pts_t, adj_t)
            safe_p = {x for r in rows_q for x in r["triad"]} & my_safe[
                p
            ]  # noqa: F841 (structural)
            survived0 = [
                r for r in rows_q if not any(x in my_safe[p] for x in r["triad"])
            ]
            rebuilt_line = [r for r in rows_q if p in r["quad"]]
            # the 3 fully-churned triads == the 3 rows whose quad contains p (the AG-line of old center)
            if not (
                len(survived0) == 3
                and {r["triad"] for r in survived0}
                == {r["triad"] for r in rebuilt_line}
            ):
                edge_ok = False
    chk(
        "EDGE SPLIT = REBUILT LINE: the 3 fully-churned triads are exactly the rows whose quad contains "
        "the old center (the AG-line indexed by p, Pass 66)",
        edge_ok,
    )
    # and their 3 quads meet in exactly {p} (addressed re-keying)
    addressed = True
    for p in range(n):
        for q in (x for x in range(n) if A[p][x]):
            rows_q, _, _ = td43.vector_table(q, pts_t, adj_t)
            quads = [set(r["quad"]) for r in rows_q if p in r["quad"]]
            if set.intersection(*quads) != {p}:
                addressed = False
    chk(
        "edge re-keying is ADDRESSED: those 3 quads meet in exactly {old center} => phase-coherent AND "
        "origin-decodable",
        addressed,
    )

    # C. the non-edge split is a transversal
    nonedge_ok = True
    for p in range(n):
        for q in (x for x in range(n) if not A[p][x] and x != p):
            prof = bt1816.move_profile(p, q, pts_t, adj_t)
            if dict(prof) != {2: 9}:
                nonedge_ok = False
    chk(
        "NON-EDGE SPLIT = TRANSVERSAL: every non-edge move has histogram {2:9} -- churn is one point per "
        "triad, a transversal (not a line) of the phase plane",
        nonedge_ok,
    )

    all_ok = all(ok for _, ok in checks)
    print(
        "\nUNIFIED (move 3): the nine-point page bill is one theorem with two proofs -- safe-zone overlap"
        "\n(Pass 65) and TD(4,3) churn (BT1809/BT1816) compute the identical set difference. The {3:6,0:3}"
        "\nvs {2:9} dichotomy is the line-vs-transversal split of the AG(2,3) directory: edge moves churn a"
        "\nrebuilt LINE (addressed, phase-coherent), non-edge moves churn a TRANSVERSAL (phase-scrambling)."
    )
    print(f"\n{'ALL PASS' if all_ok else 'FAILURES present.'}")

    out = {
        "same_nine": {
            "moves": 1560,
            "td43_equals_overlap": same,
            "bill": sorted(bills),
        },
        "edge_split": {
            "profile": {"3": 6, "0": 3},
            "fully_churned_triads": "the AG-line indexed by the old center (Pass 66 rebuilt-line rule)",
            "addressed": "the 3 rebuilt quads meet in exactly {old center}",
        },
        "nonedge_split": {
            "profile": {"2": 9},
            "structure": "a transversal of the phase plane (one point per triad)",
        },
        "all_pass": bool(all_ok),
        "summary": (
            "one law, two proofs. The constant nine-point relocation page bill is derived two ways -- the "
            "safe-zone overlap of Pass 65 (|safe(p) cap safe(q)| = 18 => bill 9) and the TD(4,3) churn of "
            "the parallel track's BT1809/BT1816 -- and this witness proves they are the SAME set "
            "difference for all 1560 ordered moves (BT1816's retained count == the independent overlap, "
            "always 18). It then explains the edge/non-edge histogram dichotomy with Pass 66's "
            "rebuilt-line rule: for an edge move p->q the three fully-churned destination triads (profile "
            "{3:6,0:3}) are exactly the rows whose center quad contains p -- the AG(2,3) line indexed by "
            "the departing center, whose three quads meet in exactly {p}, so edge re-keying is "
            "phase-coherent AND origin-addressed; for a non-edge move the churn is a transversal (profile "
            "{2:9}, one point per triad), which scrambles phase structure. The two committed derivations "
            "collapse into one theorem with two proofs and a geometric reason for the line/transversal "
            "split. HONEST: exact over all 1560 moves on committed BT1816/bt1807 geometry plus an "
            "independent safe-zone computation; no new bill introduced."
        ),
        "sources": [
            "w33_ground_affine_plane / w33_defect_aware_placement (Pass 65); w33_kernel_dynamics (Pass 66)",
            "bt1809_page_loader_td43_fusion / bt1816_page_cache_churn_simulator / bt1807 (committed, parallel track)",
        ],
    }
    with open("data/w33_page_bill_unification.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_page_bill_unification.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
