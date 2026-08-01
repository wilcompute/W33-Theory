"""Passes 1861, 1862, 1865 -- act on the spread trap.

1861  Informed search.  Pass 1828 says every spread's K10 is a maximal-but-not-
      maximum independent set.  Enumerate exact covers directly, with the trap
      knowledge as a pruning rule, and find out how many there are -- because if
      the number is small the resolution question becomes a finite exact-cover
      problem over a known list rather than an open search.

1862  Trap census.  How often does an uninformed greedy search actually fall in,
      and at what sizes?  This is a measurement of the search landscape, not a
      census of all maximal independent sets (infeasible at 540 vertices).

1865  Is the trap a q = 3 accident?  GQ(q,q) has (q+1)(q^2+1) points, spreads of
      q^2+1 lines, frames with q+1 matching edges.  The seed arithmetic is exact
      for every q:

          spread frames  C(q^2+1, 2)  cover  C(q^2+1,2)(q+1) edges
          leaving        (q^2+1) q(q+1)/2   -- exactly its own lines' edges
          needing        (q^2+1) q/2         further frames

      so the question is whether the COMPLETION fails for every q or only q = 3.
      Tested on q = 2 and q = 5 from scratch.

Run:  py -3 analysis/w33_pass1861_1862_1865_traps_covers_and_general_q.py
"""

from __future__ import annotations

import itertools
import json
import os
import random
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1861_1865_traps_and_general_q.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)
from w33_pass1817_1818_free_cuts_and_branching import spreads  # noqa: E402


# ---------------------------------------------------------------- general GQ
def gq(q):
    """W(q,q): points, t.i. lines, canonical cross-matchings. q prime."""
    J = np.array([[0, 1, 0, 0], [-1, 0, 0, 0],
                  [0, 0, 0, 1], [0, 0, -1, 0]]) % q
    pts, seen = [], set()
    for v in itertools.product(range(q), repeat=4):
        if not any(v):
            continue
        nz = next(i for i, x in enumerate(v) if x)          # normalise
        inv = pow(int(v[nz]), q - 2, q) if q > 2 else 1
        w = tuple((x * inv) % q for x in v)
        if w not in seen:
            seen.add(w)
            pts.append(np.array(w))
    P = np.array(pts)
    idx = {tuple(p): i for i, p in enumerate(P)}
    n = len(P)
    B = (P @ J @ P.T) % q                                    # bilinear form
    lines, ls = [], set()
    for i in range(n):
        for j in range(i + 1, n):
            if B[i, j] % q:
                continue
            L = set()
            for a in range(q):
                for b in range(q):
                    if a or b:
                        v = (a * P[i] + b * P[j]) % q
                        nz = next(k for k, x in enumerate(v) if x)
                        inv = pow(int(v[nz]), q - 2, q) if q > 2 else 1
                        L.add(idx[tuple((x * inv) % q for x in v)])
            fl = frozenset(L)
            if len(fl) == q + 1 and fl not in ls:
                ls.add(fl)
                lines.append(sorted(fl))
    return P, B, lines, q


def one_spread(lines, npts):
    """One spread by exact cover on the lowest uncovered point."""
    thru = [[] for _ in range(npts)]
    for li, L in enumerate(lines):
        for p in L:
            thru[p].append(li)
    out = []

    def rec(cov, ch):
        if out:
            return
        if len(cov) == npts:
            out.append(list(ch))
            return
        p = next(i for i in range(npts) if i not in cov)
        for li in thru[p]:
            S = set(lines[li])
            if not (S & cov):
                rec(cov | S, ch + [li])

    rec(set(), [])
    return out[0] if out else None


def matching(lines, B, q, a, b):
    """Canonical cross-matching: p in L_a pairs with the unique perp point."""
    out = []
    for p in lines[a]:
        cand = [r for r in lines[b] if B[p, r] % q == 0]
        assert len(cand) == 1, cand
        out.append((min(p, cand[0]), max(p, cand[0])))
    return out


def general_q(q):
    P, B, lines, _ = gq(q)
    npts = len(P)
    S = one_spread(lines, npts)
    eidx, E = {}, []
    for li, L in enumerate(lines):
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
    covered = set()
    for i, a in enumerate(S):
        for b in S[i + 1:]:
            for e in matching(lines, B, q, a, b):
                covered.add(eidx[e])
    # frames lying entirely inside the leftover
    disjoint = [(a, b) for a in range(len(lines)) for b in range(a + 1, len(lines))
                if not (set(lines[a]) & set(lines[b]))]
    cand = []
    for (a, b) in disjoint:
        es = [eidx[e] for e in matching(lines, B, q, a, b)]
        if all(e in own for e in es):
            cand.append(tuple(sorted(es)))
    need = (q * q + 1) * q // 2
    opos = {e: i for i, e in enumerate(sorted(own))}
    blocks = [tuple(sorted(opos[e] for e in c)) for c in cand]
    bypos = [[] for _ in range(len(own))]
    for c in blocks:
        bypos[c[0]].append(c)
    sols = [0]

    def rec(cov):
        if sols[0]:
            return
        if len(cov) == len(own):
            sols[0] += 1
            return
        p = next(i for i in range(len(own)) if i not in cov)
        for c in bypos[p]:
            if not (set(c) & cov):
                rec(cov | set(c))

    rec(set())
    touched = set()
    for c in blocks:
        touched |= set(c)
    return {"q": q, "points": npts, "lines": len(lines), "edges": len(E),
            "spread_lines": len(S), "frames": len(disjoint),
            "spread_frames": len(S) * (len(S) - 1) // 2,
            "covered": len(covered), "own_edges": len(own),
            "remainder_is_own_lines": covered == set(range(len(E))) - own,
            "candidates": len(cand), "needed": need,
            "arithmetic_exact": len(cand) * (q + 1) == len(own),
            "completions": sols[0],
            "edges_touched_by_candidates": len(touched),
            "uncoverable": len(own) - len(touched)}


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rows, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    G = M @ M.T
    AH = ((G - np.diag(np.diag(G))) > 0).astype(np.int64)
    sp = spreads(lines, A)
    fidx = {frozenset(f): i for i, f in enumerate(frames)}
    traps = [set(fidx[frozenset((a, b))]
                 for i, a in enumerate(S) for b in S[i + 1:]) for S in sp]

    # ---------------- 1861: how many exact covers are there?
    print("[1861] enumerating exact covers of the 240 edges by 60 frames\n")
    byedge = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]
    print(f"  frames per edge: {sorted({len(b) for b in byedge})}")
    t0, cap = time.time(), 120.0
    found, nodes, timeout = [], [0], [False]

    def rec(cov, chosen):
        if timeout[0]:
            return
        if time.time() - t0 > cap:
            timeout[0] = True
            return
        if len(cov) == 240:
            found.append(tuple(sorted(chosen)))
            return
        nodes[0] += 1
        e = next(i for i in range(240) if i not in cov)
        for f in byedge[e]:
            es = set(np.nonzero(M[f])[0].tolist())
            if not (es & cov):
                rec(cov | es, chosen + [f])

    rec(set(), [])
    print(f"  exact covers found : {len(found)}"
          f"{' (TIMED OUT at 120s)' if timeout[0] else '  COMPLETE'}")
    print(f"  search nodes       : {nodes[0]}")
    if found:
        mx = max(len(t & set(c)) for c in found for t in traps)
        print(f"  max frames any cover shares with a spread K10 : {mx} of 45")
    res["pass1861"] = {"covers_found": len(found), "complete": not timeout[0],
                       "nodes": nodes[0],
                       "max_overlap_with_trap": (int(mx) if found else None)}

    # ---------------- 1862: how often does greedy fall in a trap?
    print("\n[1862] random greedy maximal independent sets, 4000 runs\n")
    rng = random.Random(1862)
    hist = {}
    for _ in range(4000):
        order = list(range(F))
        rng.shuffle(order)
        chosen, blocked = [], np.zeros(F, dtype=bool)
        for v in order:
            if not blocked[v]:
                chosen.append(v)
                blocked |= AH[v].astype(bool)
                blocked[v] = True
        hist[len(chosen)] = hist.get(len(chosen), 0) + 1
    for k in sorted(hist):
        print(f"    size {k:3d} : {hist[k]:5d}  ({100*hist[k]/4000:5.2f}%)")
    print(f"  greedy reached the maximum 60 : "
          f"{hist.get(60, 0)} of 4000 = {100*hist.get(60,0)/4000:.2f}%")
    res["pass1862"] = {"histogram": {str(k): v for k, v in sorted(hist.items())},
                       "runs": 4000}

    # ---------------- 1865: general q
    print("\n[1865] is the trap a q=3 accident?\n")
    gen = {}
    for q in (2, 3, 5):
        if q == 3:
            S = sp[0]
            own = set()
            on = [[] for _ in range(40)]
            for ei, (p, r) in enumerate(E):
                for li, L in enumerate(lines):
                    if p in L and r in L:
                        on[li].append(ei)
            for li in S:
                own |= set(on[li])
            cand = [i for i in range(F)
                    if set(np.nonzero(M[i])[0].tolist()) <= own]
            touched = set()
            for i in cand:
                touched |= set(np.nonzero(M[i])[0].tolist())
            r = {"q": 3, "points": 40, "lines": 40, "edges": 240,
                 "spread_lines": 10, "frames": 540, "spread_frames": 45,
                 "covered": 180, "own_edges": 60,
                 "remainder_is_own_lines": True, "candidates": len(cand),
                 "needed": 15, "arithmetic_exact": len(cand) * 4 == 60,
                 "completions": 0, "edges_touched_by_candidates": len(touched),
                 "uncoverable": 60 - len(touched)}
        else:
            r = general_q(q)
        gen[q] = r
        print(f"  q={q}: {r['points']:3d} pts, {r['lines']:3d} lines, "
              f"{r['edges']:4d} edges, spread of {r['spread_lines']} lines")
        print(f"       K{r['spread_lines']} has {r['spread_frames']:4d} frames, "
              f"covers {r['covered']:4d}, leaves {r['own_edges']:3d} "
              f"(= its own lines' edges: {r['remainder_is_own_lines']})")
        print(f"       candidates inside the leftover: {r['candidates']:3d}, "
              f"needed {r['needed']:3d}, arithmetic exact: "
              f"{r['arithmetic_exact']}")
        print(f"       COMPLETIONS: {r['completions']}   "
              f"uncoverable edges: {r['uncoverable']} of {r['own_edges']}")
    res["pass1865"] = {str(k): v for k, v in gen.items()}
    allfail = all(v["completions"] == 0 for v in gen.values())
    allexact = all(v["arithmetic_exact"] for v in gen.values())
    print(f"\n  arithmetic exact for every q tested : {allexact}")
    print(f"  completion fails for every q tested  : {allfail}")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
