"""Passes 1817-1818 -- which frame-subsets give FREE resolution cuts, and which
constrain hardest.

Pass 1613 proved: for any frame-subset T with chi_T orthogonal to E_(-4)(H),
every colour class of every resolution meets T in exactly |T|/9, with no search.
The 45 octet neighbourhoods (parallel track, Pass 1541) are one family.

Pass 1817 asks what ELSE is free.  Pass 1818 asks the opposite question -- which
subsets have the LARGEST (-4)-component, since those are the ones whose
intersection number is least determined and therefore the best branching
variables.

An honest correction is recorded here too.  The obvious reading of "export all
225 free directions" is vacuous: col(M) has rank 225 over Q and IS the span of
the 240 edge columns, so as *rational* linear constraints the 225 add nothing
whatever to the edge equations already in the encoding.  What is not vacuous is
finding more 0/1 vectors in that span -- those are combinatorial cardinality
cuts a solver can use directly, and each one is a counting theorem.

Run:  py -3 analysis/w33_pass1817_1818_free_cuts_and_branching.py
"""

from __future__ import annotations

import itertools
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data", "w33_pass1817_1818_free_cuts.json")

import sys
sys.path.insert(0, HERE)
from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M, grids)


def spreads(lines, A):
    """Spreads: 10 pairwise disjoint lines partitioning the 40 points."""
    through = [[] for _ in range(40)]
    for li, L in enumerate(lines):
        for p in L:
            through[p].append(li)
    out = []

    def rec(covered, chosen):
        if len(chosen) == 10:
            out.append(tuple(sorted(chosen)))
            return
        p = next(i for i in range(40) if i not in covered)   # lowest uncovered
        for li in through[p]:
            S = set(lines[li])
            if S & covered:
                continue
            rec(covered | S, chosen + [li])

    rec(set(), [])
    return out


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rows, M = frames_and_M(A, lines, eidx)
    F = len(frames)

    G = M @ M.T
    AH = ((G - np.diag(np.diag(G))) > 0).astype(np.int64)
    w_, V_ = np.linalg.eigh(AH.astype(float))
    P = V_[:, np.abs(w_ + 4) < 1e-6]              # 540 x 315 basis of E_(-4)
    print(f"frames {F}, dim E_(-4) = {P.shape[1]}")

    def proj(chi):
        """||P_(-4) chi|| -- zero means a FREE exact-cardinality cut."""
        return float(np.linalg.norm(P.T @ chi.astype(float)))

    # ---------------- the candidate families, each a G-orbit of subsets
    fam = {}

    oc = grids(A)
    K = np.zeros((len(oc), 240), dtype=np.int64)
    for o, (Q1, Q2) in enumerate(oc):
        for p in Q1:
            for q in Q2:
                K[o, eidx[(min(p, q), max(p, q))]] = 1
    inter = M @ K.T
    fam["octet nbhd (|f cap o|=2)"] = [(inter[:, o] == 2).astype(np.int64)
                                       for o in range(len(oc))]

    # frames whose matching contains a fixed edge  -- the basic edge equation
    fam["edge (f's matching ni e)"] = [M[:, e].copy() for e in range(240)]

    # frames one of whose two lines is a fixed line
    fam["line (L in the frame)"] = [
        np.array([1 if L in f else 0 for f in frames], dtype=np.int64)
        for L in range(40)]

    # frames one of whose lines passes through a fixed point
    thru = [{li for li, L in enumerate(lines) if p in L} for p in range(40)]
    fam["point (some line ni p)"] = [
        np.array([1 if (f[0] in thru[p] or f[1] in thru[p]) else 0
                  for f in frames], dtype=np.int64) for p in range(40)]

    sp = spreads(lines, A)
    print(f"spreads found : {len(sp)}")
    spset = [set(s) for s in sp]
    fam["spread (both lines in S)"] = [
        np.array([1 if (f[0] in S and f[1] in S) else 0 for f in frames],
                 dtype=np.int64) for S in spset]
    fam["spread (some line in S)"] = [
        np.array([1 if (f[0] in S or f[1] in S) else 0 for f in frames],
                 dtype=np.int64) for S in spset]

    # H-neighbourhood of a frame: frames sharing an edge with it
    fam["H-neighbourhood of a frame"] = [AH[i].copy() for i in range(0, F, 37)]

    print("\n[1817] FREE cuts: ||P_(-4) chi_T|| == 0 means |S cap T| = |T|/9 "
          "for every class\n")
    print(f"{'family':<30}{'n':>5}{'|T|':>6}{'|T|/9':>8}"
          f"{'max ||proj||':>14}  verdict")
    table = {}
    for name, vecs in fam.items():
        sizes = sorted({int(v.sum()) for v in vecs})
        pr = max(proj(v) for v in vecs)
        free = pr < 1e-9
        divisible = all(s % 9 == 0 for s in sizes)
        table[name] = {"count": len(vecs), "sizes": sizes,
                       "max_proj": pr, "free": free,
                       "size_div_9": divisible}
        sz = sizes[0] if len(sizes) == 1 else -1
        print(f"{name:<30}{len(vecs):>5}{sz:>6}"
              f"{(sz / 9 if sz > 0 else 0):>8.2f}{pr:>14.3e}  "
              f"{'FREE' if free else 'constrains'}")
    res["pass1817"] = table

    # honest note about the "225 directions"
    rq = int(np.linalg.matrix_rank(M.astype(float)))
    print(f"\n  col(M) rank over Q = {rq}; the 240 edge columns already span it,")
    print(f"  so the 225 'free directions' add NOTHING as rational constraints.")
    print(f"  Only new 0/1 members of that span are new combinatorial cuts.")
    res["pass1817"]["_rank_note"] = {
        "rank_Q_colM": rq,
        "edge_columns_span_it": True,
        "so_rational_export_is_vacuous": True,
    }

    # ---------------- Pass 1818: how constraining is each family
    print("\n[1818] branching value: relative (-4)-mass "
          "||P chi_T|| / ||chi_T - (|T|/540)1||\n")
    print(f"{'family':<30}{'rel. (-4) mass':>16}   interpretation")
    rank = {}
    for name, vecs in fam.items():
        vals = []
        for v in vecs:
            c = v.astype(float) - v.sum() / F
            n = np.linalg.norm(c)
            if n > 1e-12:
                vals.append(proj(v) / n)
        m = float(np.mean(vals)) if vals else 0.0
        rank[name] = m
    for name, m in sorted(rank.items(), key=lambda kv: -kv[1]):
        tag = ("FREE - no branching value" if m < 1e-9
               else "strong branching" if m > 0.5 else "weak")
        print(f"{name:<30}{m:>16.4f}   {tag}")
    res["pass1818"] = {"relative_minus4_mass": rank}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
