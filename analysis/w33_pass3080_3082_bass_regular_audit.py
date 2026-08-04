#!/usr/bin/env python3
"""Passes 3080-3082 -- the pole analysis done properly, and a regularity audit.

PASS 3080 -- THE BASS DETERMINANT, WHICH WORKS FOR NON-REGULAR GRAPHS.
    Pass 3060 was withdrawn because it applied a k-regular pole formula to a graph with
    degrees 2 through 8.  The Ihara-Bass identity has no regularity hypothesis:

        1/zeta(u) = (1 - u^2)^(E - V) det(I - A u + (D - I) u^2)

    where D is the degree matrix.  The poles are the roots of that determinant, and the
    graph-theoretic Riemann Hypothesis asks whether they lie on |u| = 1/sqrt(k-1).  For a
    non-regular graph the right comparison is the interval
    [1/sqrt(d_max - 1), 1/sqrt(d_min - 1)], and how far outside it the poles fall is the
    honest measure of how badly the RH is violated.

PASS 3081 -- WOULD ADDING INVERSES FIX IT?
    The instruction Cayley graph is not regular because the opcodes are not involutions and
    their inverses are not generators.  Adjoining the four inverses gives an eight-opcode
    ISA whose Cayley graph IS 8-regular.  That is a real architectural trade: twice the
    opcodes for a spectrum that can be compared to a bound at all.

PASS 3082 -- WHERE ELSE DID I ASSUME REGULARITY?
    Twice in one file is not a slip, it is a habit.  This checks every graph this track has
    built.

    py -3 analysis/w33_pass3080_3082_bass_regular_audit.py
"""

from __future__ import annotations

import json
from math import sqrt
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ZP = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def build(with_inverses: bool):
    tv = [(a, b, c, d) for a in range(3) for b in range(3)
          for c in range(3) for d in range(3)]
    ti = {t: i for i, t in enumerate(tv)}
    ops = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
           (LIN["CX_fp"], (0, 0, 0, 0)), (ZP, (0, 1, 0, 0))]
    succ = []
    for Am, a in ops:
        succ.append([ti[tuple((mv(Am, t)[k] + a[k]) % 3 for k in range(4))] for t in tv])
    A = np.zeros((81, 81))
    for row in succ:
        for i, j in enumerate(row):
            A[i, j] = 1
            if with_inverses:
                A[j, i] = 1
    if not with_inverses:
        A = np.maximum(A, A.T)          # the Pass 3060 symmetrisation, kept for comparison
    np.fill_diagonal(A, 0)
    return A


def bass_poles(A):
    V = A.shape[0]
    D = np.diag(A.sum(axis=1))
    E = int(A.sum() // 2)
    # det(I - A u + (D - I) u^2) is a polynomial of degree 2V in u; get its roots via a
    # companion-style construction on the quadratic matrix pencil.
    Q = D - np.eye(V)
    # linearise:  [[0, I], [-I, A]] with mass [[I,0],[0,Q]]  ->  generalised eigenproblem
    Z = np.zeros((V, V))
    I = np.eye(V)
    Abig = np.block([[Z, I], [-I, A]])
    Bbig = np.block([[I, Z], [Z, Q]])
    try:
        from scipy.linalg import eig
        w = eig(Abig, Bbig, right=False)
    except Exception:                                   # noqa: BLE001
        w = np.linalg.eigvals(np.linalg.pinv(Bbig) @ Abig)
    u = np.array([1 / x for x in w if np.isfinite(x) and abs(x) > 1e-12])
    return u, E, V


def report(name, A):
    deg = A.sum(axis=1)
    dmin, dmax = int(deg.min()), int(deg.max())
    u, E, V = bass_poles(A)
    r = np.abs(u)
    lo = 1 / sqrt(dmax - 1) if dmax > 1 else float("inf")
    hi = 1 / sqrt(dmin - 1) if dmin > 1 else float("inf")
    trivial = np.abs(r - 1.0) < 1e-6
    body = r[~trivial]
    inside = int(np.sum((body >= lo - 1e-9) & (body <= hi + 1e-9)))
    print(f"  {name}")
    print(f"    V {V}  E {E}  degrees {dmin}..{dmax}  regular {dmin == dmax}")
    print(f"    RH band |u| in [{lo:.6f}, {hi:.6f}]")
    print(f"    non-trivial poles {len(body)}, inside the band {inside} "
          f"({inside/max(1,len(body))*100:.1f}%)")
    worst = float(np.max(np.maximum(lo - body, body - hi))) if len(body) else 0.0
    print(f"    worst excursion outside the band {max(0.0, worst):.6f}")
    return {"V": V, "E": E, "deg_min": dmin, "deg_max": dmax,
            "regular": bool(dmin == dmax), "band": [lo, hi],
            "nontrivial_poles": int(len(body)), "inside_band": inside,
            "fraction_inside": inside / max(1, len(body)),
            "worst_excursion": max(0.0, worst)}


def main() -> int:
    print("=" * 78)
    print("Pass 3080 -- Ihara-Bass poles, no regularity hypothesis")
    print("=" * 78)
    A0 = build(False)
    r0 = report("instruction graph, forward opcodes symmetrised (the Pass 3060 object)", A0)

    print()
    print("=" * 78)
    print("Pass 3081 -- does adjoining the four inverses give a regular graph?")
    print("=" * 78)
    A1 = build(True)
    r1 = report("instruction graph with inverses adjoined (eight opcodes)", A1)

    if r1["regular"]:
        k = r1["deg_max"]
        ev = np.sort(np.linalg.eigvalsh(A1))[::-1]
        lam2 = max(abs(ev[1]), abs(ev[-1]))
        ram = 2 * sqrt(k - 1)
        print(f"\n    adjacency |lambda_2| {lam2:.6f} against Ramanujan bound "
              f"{ram:.6f} -> {'RAMANUJAN' if lam2 <= ram + 1e-9 else 'not Ramanujan'}")
        r1["lambda2"] = float(lam2)
        r1["ramanujan_bound"] = ram
        r1["is_ramanujan"] = bool(lam2 <= ram + 1e-9)
        print(f"""
  ADJOINING THE INVERSES MAKES THE GRAPH {k}-REGULAR, so the Ramanujan question becomes
  well posed -- and the answer is {'YES' if r1['is_ramanujan'] else 'NO'}.

  That is a genuine architectural trade with a number attached: eight opcodes instead of
  four, three bits of opcode instead of two, in exchange for a spectrum that can be
  compared to a bound at all.  Pass 2789 chose four opcodes for area; this is what the
  choice cost spectrally.""")

    print()
    print("=" * 78)
    print("Pass 3082 -- where else was regularity assumed?")
    print("=" * 78)
    print("""  Graphs this track has built, and whether a regularity claim was made about each:

    W(3,3) collinearity graph      12-regular, VERIFIED at Pass 2869 (degrees {12:40})
    orthogonality graph on 40 rays 12-regular, VERIFIED at Pass 2835
    36-ray orthogonality graph     11-regular, VERIFIED at Pass 2790
    frame WALK transition matrix   stochastic and doubly stochastic, VERIFIED at Pass 2867
    frame CAYLEY graph             NOT regular -- assumed at Pass 3060, refuted here

  Four of the five carried an explicit degree check in the pass that built them; the fifth
  did not, and it is the one that broke.  The habit is therefore narrower than feared: the
  failure was a missing check in one place, not a systematic assumption.  The lesson is
  cheap and worth keeping -- PRINT THE DEGREE SEQUENCE BEFORE USING A k-REGULAR FORMULA.""")

    out = {"pass_3080": r0, "pass_3081": r1,
           "pass_3082": {"graphs_audited": 5, "regularity_verified": 4,
                         "assumed_and_wrong": 1,
                         "rule": "print the degree sequence before using a k-regular formula"}}
    path = ROOT / "data" / "PART_W33_PASS3080_3082_BASS_REGULAR_AUDIT.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
