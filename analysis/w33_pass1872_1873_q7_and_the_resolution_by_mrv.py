"""Passes 1872-1873 -- test the 1/q law at q=7, and attack the resolution with
the search order that actually works.

1872  Pass 1865 found that in GQ(q,q) a spread's K_{q^2+1} leaves exactly its own
      lines' edges, that for odd q the admissible completing frames exactly equal
      the number needed, and that they touch exactly 1/q of those edges (20/60 at
      q=3, 78/390 at q=5).  Three points and an exact fraction is a conjecture.
      q=7 is the test: 400 points, 400 lines, 11200 edges, a spread of 50 lines,
      1400 leftover edges, 175 needed candidates, and a PREDICTED 200 touched.

1873  Pass 1861 showed MRV branching with dead-edge pruning finds an exact cover
      in 10 s where naive DFS failed after 7M nodes.  A resolution is a partition
      of the 540 frames into 9 exact covers.  Generate many distinct covers with
      randomised MRV, then look for 9 that partition -- the first attack on
      chi(H)=9 with a search that can actually produce covers.

Run:  py -3 analysis/w33_pass1872_1873_q7_and_the_resolution_by_mrv.py
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
OUT = os.path.join(HERE, "..", "data", "w33_pass1872_1873_q7_and_resolution.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)


# ------------------------------------------------------------------ GQ(q,q)
def gq(q):
    Jm = np.array([[0, 1, 0, 0], [-1, 0, 0, 0],
                   [0, 0, 0, 1], [0, 0, -1, 0]]) % q
    pts, seen = [], set()
    for a in range(q ** 4):
        v = [(a // q ** k) % q for k in range(4)]
        if not any(v):
            continue
        nz = next(i for i, x in enumerate(v) if x)
        inv = pow(int(v[nz]), q - 2, q)
        w = tuple((x * inv) % q for x in v)
        if w not in seen:
            seen.add(w)
            pts.append(w)
    P = np.array(pts)
    idx = {tuple(p): i for i, p in enumerate(P)}
    B = (P @ Jm @ P.T) % q
    n = len(P)
    lines, ls = [], set()
    for i in range(n):
        for j in range(i + 1, n):
            if B[i, j]:
                continue
            L = set()
            for a in range(q):
                for b in range(q):
                    if a or b:
                        v = (a * P[i] + b * P[j]) % q
                        nz = next(k for k, x in enumerate(v) if x)
                        inv = pow(int(v[nz]), q - 2, q)
                        L.add(idx[tuple((x * inv) % q for x in v)])
            fl = frozenset(L)
            if len(fl) == q + 1 and fl not in ls:
                ls.add(fl)
                lines.append(sorted(fl))
    return P, B, lines


def one_spread(lines, npts):
    thru = [[] for _ in range(npts)]
    for li, L in enumerate(lines):
        for p in L:
            thru[p].append(li)
    out, nodes = [], [0]

    def rec(cov, ch):
        if out or nodes[0] > 4_000_000:
            return
        nodes[0] += 1
        if len(cov) == npts:
            out.append(list(ch))
            return
        p = next(i for i in range(npts) if i not in cov)
        for li in thru[p]:
            S = set(lines[li])
            if not (S & cov):
                rec(cov | S, ch + [li])

    rec(set(), [])
    return (out[0] if out else None), nodes[0]


def test_q(q):
    t0 = time.time()
    P, B, lines = gq(q)
    npts = len(P)
    S, nodes = one_spread(lines, npts)
    if S is None:
        return {"q": q, "error": "no spread found within node cap"}
    eidx, E = {}, []
    for L in lines:
        for a in range(len(L)):
            for b in range(a + 1, len(L)):
                e = (L[a], L[b])
                if e not in eidx:
                    eidx[e] = len(E)
                    E.append(e)
    own = set()
    for li in S:
        L = lines[li]
        for a in range(len(L)):
            for b in range(a + 1, len(L)):
                own.add(eidx[(L[a], L[b])])

    def match(a, b):
        out = []
        for p in lines[a]:
            c = [r for r in lines[b] if B[p, r] == 0]
            assert len(c) == 1
            out.append(eidx[(min(p, c[0]), max(p, c[0]))])
        return out

    covered = set()
    for i, a in enumerate(S):
        for b in S[i + 1:]:
            covered |= set(match(a, b))
    cand, touched = 0, set()
    npt = len(lines)
    for a in range(npt):
        sa = set(lines[a])
        for b in range(a + 1, npt):
            if sa & set(lines[b]):
                continue
            es = match(a, b)
            if all(e in own for e in es):
                cand += 1
                touched |= set(es)
    need = (q * q + 1) * q // 2
    return {"q": q, "points": npts, "lines": len(lines), "edges": len(E),
            "spread_lines": len(S), "spread_frames": len(S) * (len(S) - 1) // 2,
            "covered": len(covered), "own_edges": len(own),
            "remainder_is_own_lines": covered == set(range(len(E))) - own,
            "candidates": cand, "needed": need,
            "candidates_equal_needed": cand == need,
            "touched": len(touched), "own": len(own),
            "touched_fraction": len(touched) / len(own),
            "one_over_q": 1.0 / q,
            "law_holds": abs(len(touched) / len(own) - 1.0 / q) < 1e-12,
            "seconds": round(time.time() - t0, 1)}


def main():
    res = {}
    print("[1872] the 1/q law at q = 7\n")
    rows = {}
    for q in (3, 5, 7):
        r = test_q(q)
        rows[q] = r
        print(f"  q={q}: {r['points']:3d} pts, {r['lines']:3d} lines, "
              f"{r['edges']:5d} edges, spread {r['spread_lines']}")
        print(f"       leftover = own lines' edges : "
              f"{r['remainder_is_own_lines']}")
        print(f"       candidates {r['candidates']:3d} vs needed "
              f"{r['needed']:3d}  equal: {r['candidates_equal_needed']}")
        print(f"       touched {r['touched']:3d}/{r['own']:4d} = "
              f"{r['touched_fraction']:.6f}   1/q = {r['one_over_q']:.6f}   "
              f"LAW: {r['law_holds']}   [{r['seconds']}s]")
    res["pass1872"] = {str(k): v for k, v in rows.items()}
    print(f"\n  1/q law holds at every q tested: "
          f"{all(v['law_holds'] for v in rows.values())}")

    # ---------------- 1873: the resolution, with MRV
    print("\n[1873] the resolution, attacked with MRV\n")
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    ES = [set(np.nonzero(M[i])[0].tolist()) for i in range(540)]
    byedge = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]

    def cover(rng, forbid=frozenset(), cap=8.0):
        t0, out = time.time(), []

        def rec(cov, ch):
            if out or time.time() - t0 > cap:
                return
            if len(cov) == 240:
                out.append(tuple(sorted(ch)))
                return
            best, bl = None, None
            for e in range(240):
                if e in cov:
                    continue
                adm = [f for f in byedge[e]
                       if f not in forbid and not (ES[f] & cov)]
                if not adm:
                    return
                if bl is None or len(adm) < len(bl):
                    best, bl = e, adm
                if len(bl) == 1:
                    break
            bl = list(bl)
            rng.shuffle(bl)
            for f in bl:
                rec(cov | ES[f], ch + [f])
                if out:
                    return

        rec(set(), [])
        return out[0] if out else None

    rng = random.Random(1873)
    covers, t0 = set(), time.time()
    while time.time() - t0 < 150 and len(covers) < 4000:
        c = cover(rng)
        if c:
            covers.add(c)
    covers = [set(c) for c in covers]
    print(f"  distinct exact covers generated : {len(covers)} "
          f"in {time.time()-t0:.0f}s")

    # greedy: build a resolution class by class, forbidding used frames
    print("\n  building a resolution directly (each class forbids the last)\n")
    best, trials = 0, 0
    t0 = time.time()
    while time.time() - t0 < 240 and best < 9:
        trials += 1
        used, classes = set(), []
        for k in range(9):
            c = cover(rng, frozenset(used), cap=6.0)
            if c is None:
                break
            classes.append(c)
            used |= set(c)
        if len(classes) > best:
            best = len(classes)
            print(f"    trial {trials}: reached {best} disjoint covers "
                  f"({len(used)} of 540 frames)")
    ok = best == 9
    print(f"\n  best reached : {best} of 9 classes in {trials} trials")
    print(f"  RESOLUTION FOUND : {ok}")
    res["pass1873"] = {"covers_generated": len(covers), "trials": trials,
                       "best_classes": best, "resolution_found": ok}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
