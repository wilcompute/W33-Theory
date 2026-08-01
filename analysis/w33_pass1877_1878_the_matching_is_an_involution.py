"""Passes 1877-1878 -- why the completing frames land on a perfect matching, and
whether a third resolution class exists.

1877  Pass 1872 found the candidate frames pile q-fold onto a perfect matching of
      the points.  The counts say what that matching is.  A spread has q^2+1
      lines of q+1 points each, and

          touched / spread lines = 20/10 = 2,  78/26 = 3,  200/50 = 4
                                 = (q+1)/2 in every case.

      So the matching is a perfect matching WITHIN EACH SPREAD LINE.  That is
      exactly the orbit structure of a fixed-point-free involution acting on each
      line -- which exists iff q+1 is EVEN, i.e. iff q is ODD.  If that is right
      it proves the 1/q law AND explains the q=2 exception in one stroke, since
      for even q a line has an odd number of points and no such involution
      exists.  Tested at q = 3, 5, 7 and 2.

1878  Pass 1873 localised the resolution failure between the second and third
      class.  Fix two disjoint exact covers and decide EXHAUSTIVELY whether a
      third exists among the remaining 420 frames.  A definitive no would be an
      obstruction; a yes moves the frontier to the fourth.

Run:  py -3 analysis/w33_pass1877_1878_the_matching_is_an_involution.py
"""

from __future__ import annotations

import json
import os
import random
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1877_1878_involution_and_third.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)
from w33_pass1872_1873_q7_and_the_resolution_by_mrv import gq, one_spread  # noqa: E402


def matching_structure(q):
    """Is the touched set a perfect matching WITHIN each spread line?"""
    P, B, lines = gq(q)
    n = len(P)
    S, _ = one_spread(lines, n)
    eidx, E = {}, []
    for L in lines:
        for a in range(len(L)):
            for b in range(a + 1, len(L)):
                e = (L[a], L[b])
                if e not in eidx:
                    eidx[e] = len(E)
                    E.append(e)
    own_by_line = {}
    own = set()
    for li in S:
        L = lines[li]
        s = set()
        for a in range(len(L)):
            for b in range(a + 1, len(L)):
                s.add(eidx[(L[a], L[b])])
        own_by_line[li] = s
        own |= s

    def match(a, b):
        out = []
        for p in lines[a]:
            c = [r for r in lines[b] if B[p, r] == 0]
            out.append(eidx[(min(p, c[0]), max(p, c[0]))])
        return out

    touched = set()
    ncand = 0
    for a in range(len(lines)):
        sa = set(lines[a])
        for b in range(a + 1, len(lines)):
            if sa & set(lines[b]):
                continue
            es = match(a, b)
            if all(e in own for e in es):
                ncand += 1
                touched |= set(es)
    per_line, perfect_per_line = [], True
    for li in S:
        t = touched & own_by_line[li]
        per_line.append(len(t))
        pts_used = [p for e in t for p in E[e]]
        if sorted(pts_used) != sorted(lines[li]):
            perfect_per_line = False
    return {"q": q, "points": n, "spread_lines": len(S),
            "line_size": q + 1, "candidates": ncand,
            "touched": len(touched),
            "touched_per_spread_line": sorted(set(per_line)),
            "predicted_(q+1)/2": (q + 1) / 2,
            "perfect_matching_within_each_line": perfect_per_line,
            "q_odd_so_line_size_even": (q + 1) % 2 == 0}


def main():
    res = {}
    print("[1877] is the matching a fixed-point-free involution on each "
          "spread line?\n")
    rows = {}
    for q in (2, 3, 5, 7):
        r = matching_structure(q)
        rows[q] = r
        print(f"  q={q}: lines of {r['line_size']} points, "
              f"{r['candidates']:3d} candidates, {r['touched']:3d} touched")
        print(f"       touched per spread line : {r['touched_per_spread_line']}"
              f"   predicted (q+1)/2 = {r['predicted_(q+1)/2']}")
        print(f"       perfect matching within each line : "
              f"{r['perfect_matching_within_each_line']}"
              f"   (line size even: {r['q_odd_so_line_size_even']})")
    res["pass1877"] = {str(k): v for k, v in rows.items()}
    odd = [v for k, v in rows.items() if k % 2]
    print(f"\n  for every ODD q tested, the touched edges are a perfect "
          f"matching of each\n  spread line, of size (q+1)/2: "
          f"{all(v['perfect_matching_within_each_line'] for v in odd)}")
    print(f"  q=2 (line size {rows[2]['line_size']}, ODD) has "
          f"{rows[2]['candidates']} candidates -- no fixed-point-free "
          f"involution exists")

    # ---------------- 1878: is there a third class?
    print("\n[1878] two disjoint covers exist. Does a THIRD?\n")
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    ES = [set(np.nonzero(M[i])[0].tolist()) for i in range(540)]
    byedge = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]

    def cover(rng, forbid=frozenset(), cap=8.0, count_all=False, hard=None):
        t0, out, nodes = time.time(), [], [0]

        def rec(cov, ch):
            if (out and not count_all) or time.time() - t0 > cap:
                return
            if len(cov) == 240:
                out.append(tuple(sorted(ch)))
                return
            nodes[0] += 1
            bl = None
            for e in range(240):
                if e in cov:
                    continue
                adm = [f for f in byedge[e]
                       if f not in forbid and not (ES[f] & cov)]
                if not adm:
                    return
                if bl is None or len(adm) < len(bl):
                    bl = adm
                if len(bl) == 1:
                    break
            bl = list(bl)
            if rng:
                rng.shuffle(bl)
            for f in bl:
                rec(cov | ES[f], ch + [f])
                if out and not count_all:
                    return

        rec(set(), [])
        return out, nodes[0], (time.time() - t0 > cap)

    rng = random.Random(1878)
    attempts, results = 0, []
    t0 = time.time()
    while time.time() - t0 < 300 and attempts < 12:
        c1, _, _ = cover(rng, cap=8.0)
        if not c1:
            continue
        used = set(c1[0])
        c2, _, _ = cover(rng, frozenset(used), cap=8.0)
        if not c2:
            continue
        used |= set(c2[0])
        attempts += 1
        # EXHAUSTIVE third-class search on the remaining 420 frames
        c3, nodes, to = cover(None, frozenset(used), cap=45.0, count_all=False)
        results.append({"third_found": bool(c3), "nodes": nodes,
                        "timed_out": to})
        print(f"  pair {attempts}: third class found = {bool(c3)}"
              f"   nodes {nodes}"
              f"{'   (TIMED OUT, so undecided)' if to else '   EXHAUSTIVE'}")
    nf = sum(1 for r in results if r["third_found"])
    ex = sum(1 for r in results if not r["timed_out"])
    print(f"\n  disjoint cover-pairs tested : {len(results)}")
    print(f"  a third class exists        : {nf}")
    print(f"  searches that ran to exhaustion (not capped) : {ex}")
    res["pass1878"] = {"pairs_tested": len(results), "third_found": nf,
                       "exhaustive": ex, "detail": results}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
