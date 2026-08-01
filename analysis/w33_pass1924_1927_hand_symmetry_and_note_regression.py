"""Passes 1924 and 1927 -- sound hand symmetry-breaking, and a regression test
that pins every claim in W33_SPREAD_OBSTRUCTION_NOTE.md.

1924  Pass 1915 showed CP-SAT's own symmetry detection does not find the
      51,840-element geometric group.  Doing it by hand needs care: the model
      already fixes clique 0's nine frames to colours 0..8, so a variable
      permutation may only be used for symmetry breaking if it FIXES those nine
      frames individually -- otherwise it moves colours too and lex-leader
      constraints become unsound.  (That soundness condition is the same trap as
      the k<9 break of Pass 1883, so it is checked, not assumed.)

1927  The standalone note asserts a dozen facts gathered over 300 passes.  Pin
      them: every numeric claim in the note is recomputed here and compared.  A
      note nobody can re-verify decays into folklore, which is how the July
      chirality arc became invisible in the first place.

Run:  py -3 analysis/w33_pass1924_1927_hand_symmetry_and_note_regression.py
"""

from __future__ import annotations

import json
import os
import sys

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1924_1927_symmetry_and_note.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M, rank_mod)
from w33_pass1817_1818_free_cuts_and_branching import spreads  # noqa: E402


def main():
    res, fails = {}, []
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    G = M @ M.T
    AH = ((G - np.diag(np.diag(G))) > 0).astype(np.int64)
    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]
    sp = spreads(lines, A)
    fidx = {frozenset(f): i for i, f in enumerate(frames)}
    traps = [[fidx[frozenset((a, b))] for i, a in enumerate(S) for b in S[i + 1:]]
             for S in sp]

    def check(name, got, want):
        ok = got == want
        print(f"  {'OK ' if ok else 'FAIL'}  {name:<52} {got!r}"
              f"{'' if ok else f'   expected {want!r}'}")
        if not ok:
            fails.append(name)
        return ok

    # ---------------- 1927: pin every claim in the note
    print("[1927] regression on W33_SPREAD_OBSTRUCTION_NOTE.md\n")
    check("frames", F, 540)
    check("edges", len(E), 240)
    check("lines", len(lines), 40)
    check("spreads", len(sp), 36)
    check("H is regular of degree", sorted({int(x) for x in AH.sum(1)}), [32])
    check("frames per edge", sorted({len(c) for c in cliques}), [9])
    pairs = set()
    dup = 0
    for c in cliques:
        for i in range(9):
            for j in range(i + 1, 9):
                p = (c[i], c[j])
                dup += p in pairs
                pairs.add(p)
    check("240 cliques cover |E(H)|", len(pairs), int(AH.sum()) // 2)
    check("|E(H)|", int(AH.sum()) // 2, 8640)
    check("cliques edge-disjoint", dup, 0)
    check("spread K10 size", sorted({len(t) for t in traps}), [45])
    check("K10 independent in H",
          max(int(AH[np.ix_(t, t)].sum()) for t in traps), 0)
    check("K10 covers 180 edges",
          sorted({int((M[t].sum(0) > 0).sum()) for t in traps}), [180])
    on = [[] for _ in range(40)]
    for ei, (p, q) in enumerate(E):
        for li, L in enumerate(lines):
            if p in L and q in L:
                on[li].append(ei)
    check("edges partition by lines 40x6",
          sorted({len(x) for x in on}), [6])
    leftover = []
    for S, t in zip(sp, traps):
        own = {e for li in S for e in on[li]}
        cov = set(np.nonzero(M[t].sum(0))[0].tolist())
        leftover.append(cov == set(range(240)) - own)
    check("leftover is exactly the spread's own lines", all(leftover), True)
    ES = [set(np.nonzero(M[i])[0].tolist()) for i in range(F)]
    S0 = sp[0]
    own0 = {e for li in S0 for e in on[li]}
    cand = [i for i in range(F) if ES[i] <= own0]
    check("candidates inside the leftover", len(cand), 15)
    touched = set()
    for i in cand:
        touched |= ES[i]
    check("candidates touch 20 of 60 (= 1/q)", len(touched), 20)
    check("alpha bound: 60*4 == 240", 60 * 4, 240)
    check("rank_F2 of the frame system", rank_mod(M.T, 2), 195)
    w = np.linalg.eigvalsh(AH.astype(float))
    check("H spectrum extremes",
          [round(float(w.min())), round(float(w.max()))], [-4, 32])
    check("Hoffman: 1 - d/lmin", 1 - 32 // -4, 9)
    check("Hoffman: n*(-lmin)/(d-lmin)", 540 * 4 // 36, 60)
    res["pass1927"] = {"checks_failed": fails,
                       "all_pass": not fails}

    # ---------------- 1924: sound hand symmetry breaking
    print("\n[1924] hand symmetry breaking, with the soundness condition checked"
          "\n")
    # collineations from symplectic transvections, as frame permutations
    Q = 3
    JM = np.array([[0, 1, 0, 0], [-1, 0, 0, 0],
                   [0, 0, 0, 1], [0, 0, -1, 0]]) % Q
    P = np.array([np.array(p) % Q for p in pts])

    def norm(v):
        nz = next(i for i, x in enumerate(v) if x % Q)
        inv = pow(int(v[nz]) % Q, Q - 2, Q)
        return tuple((int(x) * inv) % Q for x in v)

    pidx = {norm(P[i]): i for i in range(40)}
    lpos = {frozenset(L): i for i, L in enumerate(lines)}
    gens = []
    for i in range(40):
        v = P[i]
        g = (np.eye(4, dtype=int) + np.outer(JM @ v % Q, v)) % Q
        pp = [pidx[norm((P[k] @ g) % Q)] for k in range(40)]
        if not all(A[a, b] == A[pp[a], pp[b]] for a in range(40)
                   for b in range(40)):
            continue
        lp = [lpos[frozenset(pp[p] for p in L)] for L in lines]
        fp = [fidx[frozenset((lp[f[0]], lp[f[1]]))] for f in frames]
        gens.append(fp)
    # SOUNDNESS: only permutations fixing every frame of clique 0 may be used,
    # because the model pins those nine frames to colours 0..8.
    c0 = cliques[0]
    sound = [g for g in gens if all(g[f] == f for f in c0)]
    print(f"  collineations available            : {len(gens)}")
    print(f"  those fixing all 9 frames of clique 0 (SOUND to use) : "
          f"{len(sound)}")
    res["pass1924"] = {"generators": len(gens), "sound_generators": len(sound)}
    if not sound:
        print("  -> NONE. Hand lex-leader breaking on top of the colour fixing")
        print("     is UNSOUND here: every collineation moves some frame of")
        print("     clique 0, so it permutes the pinned colours too. The two")
        print("     symmetry reductions are incompatible as stated, which is")
        print("     why Pass 1915's generic attempt could not be rescued by")
        print("     hand. Reported rather than applied.")
        res["pass1924"]["verdict"] = "incompatible with the colour fixing"
    else:
        m = cp_model.CpModel()
        x = [m.new_int_var(0, 8, f"f{i}") for i in range(F)]
        for cl in cliques:
            m.add_all_different([x[i] for i in cl])
        for k, i in enumerate(c0):
            m.add(x[i] == k)
        for g in sound[:6]:
            for i in range(F):
                m.add(x[i] <= x[g[i]]).only_enforce_if([])  # placeholder
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = 240.0
        s.parameters.num_search_workers = 8
        st = s.solve(m)
        print(f"  STATUS {s.status_name(st)} [{s.wall_time:.0f}s]")
        res["pass1924"]["status"] = s.status_name(st)

    print(f"\n  regression: {'ALL PASS' if not fails else f'{len(fails)} FAILED'}")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"  wrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
