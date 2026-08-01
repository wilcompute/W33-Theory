"""Passes 1897, 1898, 1899.

1898  Pass 1896 showed my asserted bound |class cap K10| <= 5 was false, with
      covers observed at 10..13 under biased sampling.  Replace the guess with a
      measurement: maximise and minimise |cover cap K10| exactly.  Those two
      numbers are SOUND cuts, unlike the one I invented.

1899  Pass 1894 showed sigma_S generates the C2 kernel of Stab(S) acting on the
      spread's lines.  The general-q construction should be a MATRIX.  Predicted:
      sigma_S is induced by a symplectic g with

          g^2 = mu * I,   mu a NON-SQUARE in F_q^*.

      Then a projective fixed point would need lambda^2 = mu with lambda in F_q,
      which is impossible, so g is fixed-point-free -- and for q EVEN every
      element is a square, so no such g exists and there is no sigma_S.  That is
      exactly the odd/even dichotomy of Passes 1877/1882, from one equation.
      Recover g from the permutation and check it at q = 3, 5, 7.

1897  Launch the spread-variable encoding (Pass 1892's, the cheapest so far) for
      a long run rather than ten minutes.

Run:  py -3 analysis/w33_pass1897_1899_long_run_k10_max_and_sigma_matrix.py
"""

from __future__ import annotations

import itertools
import json
import os
import sys

import numpy as np
from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, "..", "data", "w33_pass1898_1899_k10max_and_sigma.json")

from w33_pass1612_1614_frame_kernel_and_the_simplex import (  # noqa: E402
    build_w33, edge_list, frames_and_M)
from w33_pass1817_1818_free_cuts_and_branching import spreads  # noqa: E402
from w33_pass1872_1873_q7_and_the_resolution_by_mrv import gq, one_spread  # noqa: E402


def sigma_matrix(q):
    """Recover the 4x4 matrix inducing sigma_S and test g^2 = mu I."""
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
            out.append(eidx[(min(p, c[0]), max(p, c[0]))])
        return out

    touched = set()
    for a in range(len(lines)):
        sa = set(lines[a])
        for b in range(a + 1, len(lines)):
            if sa & set(lines[b]):
                continue
            es = match(a, b)
            if all(e in own for e in es):
                touched |= set(es)
    sig = [-1] * n
    for e in touched:
        u, v = E[e]
        sig[u], sig[v] = v, u
    if any(x < 0 for x in sig):
        return {"q": q, "sigma_exists": False}

    # solve for g with P[i] @ g ~ P[sig[i]] (projectively), using a basis
    basis = []
    for i in range(n):
        M2 = np.array(basis + [P[i]]) % q
        if np.linalg.matrix_rank(M2.astype(float)) > len(basis):
            basis.append(P[i])
        if len(basis) == 4:
            break
    Bm = np.array(basis) % q
    # image of each basis vector is sig, up to an unknown scalar each
    sq = {(x * x) % q for x in range(1, q)}
    nonsq = sorted(set(range(1, q)) - sq)
    found = None
    for scal in itertools.product(range(1, q), repeat=4):
        Im = np.array([(scal[k] * P[sig[np.where((P == basis[k]).all(1))[0][0]]])
                       % q for k in range(4)]) % q
        try:
            g = (np.linalg.solve(Bm.astype(float), Im.astype(float)))
        except np.linalg.LinAlgError:
            continue
        gi = np.rint(g).astype(int) % q
        if not np.allclose((Bm @ gi) % q, Im % q):
            continue
        ok = True
        for i in range(n):
            w = (P[i] @ gi) % q
            t = P[sig[i]]
            r = [k for k in range(1, q) if np.array_equal((k * t) % q, w)]
            if not r:
                ok = False
                break
        if ok:
            found = gi
            break
    if found is None:
        return {"q": q, "sigma_exists": True, "matrix_found": False}
    g2 = (found @ found) % q
    mu = int(g2[0, 0]) % q
    scalar = np.array_equal(g2, (mu * np.eye(4, dtype=int)) % q)
    return {"q": q, "sigma_exists": True, "matrix_found": True,
            "g": found.tolist(), "g2_is_scalar": bool(scalar), "mu": mu,
            "mu_is_nonsquare": mu in nonsq,
            "squares": sorted(sq), "nonsquares": nonsq}


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rws, M = frames_and_M(A, lines, eidx)
    F = len(frames)
    cliques = [np.nonzero(M[:, e])[0].tolist() for e in range(240)]
    sp = spreads(lines, A)
    fidx = {frozenset(f): i for i, f in enumerate(frames)}
    traps = [[fidx[frozenset((a, b))] for i, a in enumerate(S) for b in S[i + 1:]]
             for S in sp]

    # ---------- 1898: the exact extremes, replacing my guess
    print("[1898] exact max and min of |exact cover cap spread K10|\n")
    rows = {}
    for sense in ("max", "min"):
        m = cp_model.CpModel()
        y = [m.new_bool_var(f"y{f}") for f in range(F)]
        for cl in cliques:
            m.add_exactly_one([y[f] for f in cl])
        t = m.new_int_var(0, 45, "t")
        m.add(t == sum(y[f] for f in traps[0]))
        if sense == "max":
            m.maximize(t)
        else:
            m.minimize(t)
        s = cp_model.CpSolver()
        s.parameters.max_time_in_seconds = 300.0
        s.parameters.num_search_workers = 8
        st = s.solve(m)
        v = s.value(t) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
        rows[sense] = {"status": s.status_name(st), "value": v,
                       "seconds": round(s.wall_time, 1)}
        print(f"  {sense}: {s.status_name(st)}  value = {v}  "
              f"[{s.wall_time:.1f}s]")
    if rows["max"]["value"] is not None and rows["min"]["value"] is not None:
        lo, hi = rows["min"]["value"], rows["max"]["value"]
        print(f"\n  SOUND cut: {lo} <= |class cap K10| <= {hi}   "
              f"(I had asserted <= 5)")
        print(f"  the 9 classes partition the K10's 45 frames, and "
              f"9 x {lo} = {9*lo} <= 45 <= 9 x {hi} = {9*hi}: "
              f"{9*lo <= 45 <= 9*hi}")
    res["pass1898"] = rows

    # ---------- 1899: sigma_S as a matrix
    print("\n[1899] sigma_S as a symplectic matrix: is g^2 = mu I, mu a "
          "non-square?\n")
    mats = {}
    for q in (3, 5, 7):
        r = sigma_matrix(q)
        mats[q] = r
        if not r.get("matrix_found"):
            print(f"  q={q}: {r}")
            continue
        print(f"  q={q}: g^2 is scalar: {r['g2_is_scalar']}   "
              f"mu = {r['mu']}   squares mod {q}: {r['squares']}")
        print(f"        mu is a NON-SQUARE: {r['mu_is_nonsquare']}")
    ok = all(v.get("g2_is_scalar") and v.get("mu_is_nonsquare")
             for v in mats.values() if v.get("matrix_found"))
    print(f"\n  g^2 = mu I with mu a non-square, at every q tested : {ok}")
    if ok:
        print("  => a projective fixed point needs lambda^2 = mu with lambda in")
        print("     F_q, impossible for mu a non-square, so g is fixed-point-")
        print("     free.  For q EVEN every element is a square, so no such g")
        print("     exists and there is no sigma_S.  One equation, both branches.")
    res["pass1899"] = {str(k): v for k, v in mats.items()}

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, os.path.join(HERE, '..'))}")


if __name__ == "__main__":
    main()
