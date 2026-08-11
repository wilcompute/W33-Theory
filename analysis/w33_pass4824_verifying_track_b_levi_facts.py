#!/usr/bin/env python3
"""Pass 4824 -- independently verify Track B's Levi-graph facts, because their object is
one this lane already builds.

Track B reports that their [2025,64,96]_2 code is Rep_12 of H_1(Levi(GQ(4,2)); F_2), with
the Levi graph having 72 vertices, 135 edges, cycle dimension 64, girth 8, edge-connectivity
3, and exactly 1,080 eight-cycles -- which give the 1,080 minimum words of weight 12x8 = 96.
Their open item 3 asks whether the design's automorphism group is exactly PGSp(4,3).

GQ(4,2) IS H(3,4), which this lane constructed at Pass 4562 over GF(4) and measured at
Passes 4799 and 4812.  So every one of those numbers is checkable here in seconds, from a
completely independent construction, and a cross-track number that both lanes compute
separately is worth more than one either lane asserts.

CLAUDE.md's protocol asks exactly this: cite across the boundary rather than re-derive.
The citation is only worth anything if the numbers agree.

    py -3 analysis/w33_pass4824_verifying_track_b_levi_facts.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


P62 = _load("p62", "w33_pass4562_second_dual_pair_and_a_correction.py")

# Track B's reported values, quoted from their packet
CLAIMED = {
    "levi_vertices": 72,
    "levi_edges": 135,
    "cycle_dimension": 64,
    "girth": 8,
    "edge_connectivity": 3,
    "eight_cycles": 1080,
}


def main() -> int:
    print("=" * 78)
    print("Pass 4824 -- Track B's Levi facts, checked against this lane's H(3,4)")
    print("=" * 78)

    pts, lines = P62.build_h34()
    n, L = len(pts), len(lines)
    B = igraph.Graph(n=n + L)
    B.add_edges([(p, n + j) for j, Ln in enumerate(lines) for p in Ln])

    got = {
        "levi_vertices": B.vcount(),
        "levi_edges": B.ecount(),
        "cycle_dimension": B.ecount() - B.vcount() + len(B.components()),
        "girth": int(B.girth()),
        "edge_connectivity": B.edge_connectivity(),
    }

    # count 8-cycles exactly: a girth-8 bipartite graph's 8-cycles are its shortest
    # cycles, so count closed non-backtracking 8-walks and divide by 2*8
    A = B.get_adjacency()
    import numpy as np
    M = np.array(A.data, dtype=object)
    # exact count via the standard cycle-counting identity is delicate; enumerate instead,
    # which is affordable at 72 vertices and girth 8
    adj = [set(B.neighbors(v)) for v in range(B.vcount())]
    eight = 0
    for start in range(B.vcount()):
        # paths of length 8 returning to start, all interior vertices > start, no repeats
        stack = [(start, [start])]
        while stack:
            v, path = stack.pop()
            if len(path) == 8:
                if start in adj[v]:
                    eight += 1
                continue
            for w in adj[v]:
                if w == start or (w > start and w not in path):
                    if w == start:
                        continue
                    stack.append((w, path + [w]))
    # DIVIDE BY 2, ONCE. Interior vertices are constrained to exceed `start`, so each cycle
    # is discovered exactly once from its least vertex -- and twice from there, once per
    # direction of travel. The first version divided by 2 and then by 2 again, reporting
    # 540 against Track B's 1,080 and making a correct cross-track number look like a
    # disagreement. Their figure was right; the checker was wrong.
    got["eight_cycles"] = eight // 2

    print(f"\n  {'quantity':22s} {'Track B':>10s} {'this lane':>10s} {'agree':>7s}")
    rows = []
    for k in CLAIMED:
        a, b = CLAIMED[k], got.get(k)
        ok = a == b
        rows.append({"quantity": k, "track_b": a, "this_lane": b, "agree": bool(ok)})
        print(f"  {k:22s} {a:>10,d} {str(b):>10s} {str(ok):>7s}")

    agree = all(r["agree"] for r in rows)
    print(f"""
    {'EVERY NUMBER AGREES.' if agree else 'AT LEAST ONE NUMBER DISAGREES -- READ THE ROWS.'}

    The two constructions share nothing: Track B reaches this graph through a binary code
    and its homology, this lane builds H(3,4) as a Hermitian quadrangle over GF(4) and takes
    its incidence graph. That the invariants match is worth more than either lane asserting
    them, and it is what CLAUDE.md's cross-boundary citation rule is for.

    ONE THING I CAN ADD TO THEIR OPEN ITEM 3. They ask whether the design's automorphism
    group is exactly PGSp(4,3) of order 51,840. This lane computed at Pass 4727 that
    |Aut(H(3,4))| = 51,840 -- and, more usefully, WHY: the exceptional isomorphism
    PSU(4,2) = PSp(4,3). H(3,4) is Hermitian over GF(4) with a unitary group; W(3,3) is
    symplectic over GF(3); the two simple groups coincide at order 25,920. So a
    coding-theoretic reconstruction landing on PGSp(4,3) would not be evidence of contact
    with W(3,3) specifically -- both geometries genuinely have that group, and Pass 4735
    found 56% of this corpus's 51,840 sightings do not say which one they mean.""")

    out = {
        "boundary": ("H(3,4) is built here over GF(4) from the Hermitian form; Track B's "
                     "numbers are quoted from their packet and their CODE is not "
                     "reconstructed. Agreement of graph invariants does not verify their "
                     "code-theoretic claims -- only that the graph they describe is the one "
                     "this lane builds"),
        "claimed_by_track_b": CLAIMED,
        "computed_here": got,
        "comparison": rows,
        "all_agree": bool(agree),
        "contribution_to_their_item_3": (
            "|Aut(H(3,4))| = 51,840 was computed at Pass 4727, and the reason is the "
            "exceptional isomorphism PSU(4,2) = PSp(4,3). A coding-theoretic "
            "reconstruction landing on that order is therefore NOT evidence of contact "
            "with W(3,3) specifically; both geometries have the group independently"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4824_TRACK_B_LEVI_VERIFICATION.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
