"""Passes 1827-1828 -- do the 36 spreads SEED exact covers, and is any family
other than the octets useful mod 2?

Pass 1828 (the seed).  A spread is 10 pairwise disjoint lines partitioning the
40 points, so all C(10,2) = 45 of its line-pairs are frames.  Two such frames
cannot share a matching edge -- their endpoint sets are disjoint or meet in one
line whose partner lines are disjoint -- so:

    each spread's 45 frames are an INDEPENDENT SET of H, of size 45,

three quarters of the maximum 60.  Better, the 240 edges of W(3,3) are
partitioned by the 40 lines (6 edges each), so a spread's 45 matchings ought to
cover exactly the 180 edges lying OFF the spread's own lines, leaving the
10 x 6 = 60 edges lying ON them.  Completing a spread to an exact cover is then
a 15-frame exact-cover problem on 60 edges, not a 60-frame problem on 240.

That is the smallest handle on the resolution this project has had.  This script
tests every step of it and runs the completion search on all 36 spreads.

Pass 1827 (the sweep).  Pass 1817 tested seven hand-picked frame-subset
families and found the 45 octets the only one adding F_2 rank.  Here the sweep
is systematic: every relation-family {f : rel(f, x) = v} over every base object
class (points, lines, edges, octets, spreads, frames) and every attained value.

Run:  py -3 analysis/w33_pass1827_1828_spread_seeds_and_the_mod2_sweep.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1827_1828_spread_seeds.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M, grids, rank_mod)
from w33_pass1817_1818_free_cuts_and_branching import spreads  # noqa: E402


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rows, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    sp = spreads(lines, A)
    print(f"frames {F}, edges {len(E)}, spreads {len(sp)}")

    # the 240 edges are partitioned by the 40 lines, 6 each
    on_line = [[] for _ in range(40)]
    for ei, (p, q) in enumerate(E):
        for li, L in enumerate(lines):
            if p in L and q in L:
                on_line[li].append(ei)
    assert all(len(x) == 6 for x in on_line), "edges are NOT 6-per-line"
    print("edge partition by lines : 40 x 6 = 240  CONFIRMED")

    G = M @ M.T
    AH = ((G - np.diag(np.diag(G))) > 0).astype(np.int64)

    # ---------------- Pass 1828: the spread seed
    print("\n[1828] does a spread's 45 frames form an independent set of H?\n")
    fidx = {frozenset(f): i for i, f in enumerate(frames)}
    seed_rows = []
    for s, S in enumerate(sp):
        ids = [fidx[frozenset((a, b))]
               for i, a in enumerate(S) for b in S[i + 1:]]
        assert len(ids) == 45
        indep = int(AH[np.ix_(ids, ids)].sum()) == 0
        cov = M[ids].sum(axis=0)
        assert cov.max() <= 1
        covered = set(np.nonzero(cov)[0].tolist())
        own = set()
        for li in S:
            own |= set(on_line[li])
        seed_rows.append({"spread": s, "independent": indep,
                          "covered": len(covered), "own_line_edges": len(own),
                          "remainder_is_own_lines": covered == (
                              set(range(240)) - own)})
        if s < 2 or not indep:
            print(f"  spread {s:2d}: independent={indep}  covers "
                  f"{len(covered)} edges; the {240 - len(covered)} left over "
                  f"are exactly its own lines' edges: "
                  f"{covered == set(range(240)) - own}")
    allind = all(r["independent"] for r in seed_rows)
    allrem = all(r["remainder_is_own_lines"] for r in seed_rows)
    print(f"  all 36 spreads independent in H        : {allind}")
    print(f"  all 36 leave exactly their own 60 edges: {allrem}")

    # completion search: 15 frames partitioning the 60 leftover edges
    print("\n[1828] completing a spread to an exact cover "
          "(15 frames on 60 edges)\n")
    comp = []
    for s, S in enumerate(sp):
        own = sorted({e for li in S for e in on_line[li]})
        opos = {e: i for i, e in enumerate(own)}
        cand = []
        for i in range(F):
            es = np.nonzero(M[i])[0]
            if all(int(e) in opos for e in es):
                cand.append(tuple(sorted(opos[int(e)] for e in es)))
        # exact cover of 60 slots by 4-element candidate blocks
        bypos = [[] for _ in range(60)]
        for c in cand:
            bypos[c[0]].append(c)
        sols = [0]

        def rec(covered, depth):
            if sols[0] > 0:
                return
            if len(covered) == 60:
                sols[0] += 1
                return
            p = next(i for i in range(60) if i not in covered)
            for c in bypos[p]:
                if not (set(c) & covered):
                    rec(covered | set(c), depth + 1)

        rec(set(), 0)
        comp.append({"spread": s, "candidate_frames": len(cand),
                     "completions_found": sols[0]})
        if s < 3:
            print(f"  spread {s:2d}: {len(cand):3d} frames lie entirely inside "
                  f"the 60 leftover edges; completions found: {sols[0]}")
    ncand = sorted({c["candidate_frames"] for c in comp})
    nsol = sorted({c["completions_found"] for c in comp})
    print(f"  over all 36 spreads: candidate counts {ncand}, "
          f"completions {nsol}")
    if max(nsol) == 0:
        print("  -> NO spread extends to an exact cover: the K10 seed is a "
              "maximal-but-not-maximum independent set.")
    res["pass1828"] = {"seeds": seed_rows, "completions": comp,
                       "all_independent": allind,
                       "remainder_is_own_lines": allrem}

    # ---------------- Pass 1827: systematic mod-2 sweep
    print("\n[1827] systematic relation-family sweep for F_2 rank\n")
    base = rank_mod(M.T, 2)
    print(f"  baseline rank_F2(M^T) = {base}")

    oc = grids(A)
    K = np.zeros((len(oc), 240), dtype=np.int64)
    for o, (P, Q) in enumerate(oc):
        for p in P:
            for q in Q:
                K[o, eidx[(min(p, q), max(p, q))]] = 1

    thru = [{li for li, L in enumerate(lines) if p in L} for p in range(40)]
    rels = {
        "octet": (M @ K.T),
        "edge": M,
        "point": np.array([[int(f[0] in thru[p]) + int(f[1] in thru[p])
                            for p in range(40)] for f in frames]),
        "line": np.array([[int(L in f) for L in range(40)] for f in frames]),
        "spread": np.array([[int(f[0] in set(S)) + int(f[1] in set(S))
                             for S in sp] for f in frames]),
        "frame(H-dist)": AH,
    }
    sweep = {}
    for name, R in rels.items():
        vals = sorted(set(np.unique(R).tolist()))
        best, hits = base, []
        for v in vals:
            X = (R == v).astype(np.int64).T
            r = rank_mod(np.vstack([M.T, X]), 2)
            if r > base:
                hits.append({"value": int(v), "rank": int(r),
                             "gain": int(r - base)})
            best = max(best, r)
        sweep[name] = {"values": [int(v) for v in vals],
                       "best_rank": int(best), "gain": int(best - base),
                       "hits": hits}
        tag = f"GAIN +{best - base}" if best > base else "no gain"
        print(f"  {name:<16} values {str(vals):<14} best rank {best:>4}   {tag}")
    res["pass1827"] = {"baseline_rank_F2": int(base), "sweep": sweep}
    winners = [k for k, v in sweep.items() if v["gain"] > 0]
    print(f"\n  families that add F_2 rank: {winners}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
