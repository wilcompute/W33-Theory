"""Pass 7107 -- is there a 52-point partial ovoid in W(3,9)?

THE TARGET COMES FROM AN INTERPOLATION, AND I SAY SO UP FRONT. The three known odd values

    alpha(W(3,3)) = 7    alpha(W(3,5)) = 18    alpha(W(3,7)) = 33

(q=3 computed here; q=5 and 7 are Cimrakova-Fack 2005, Table 1) are fitted exactly by
(q+4)(q-1)/2. Three points determine a quadratic, so the fit has ZERO degrees of freedom and
is not evidence of anything. It is a sharp prediction: 52 at q=9, where this repo's local
searches plateau at 51.

A 52 would beat the repo's best and test the formula. A proof that 51 is optimal would kill
the formula outright. Either is worth more than another search that returns 51.

GF(9) IS F_3[x]/(x^2+1), NOT Z/9. This has been got wrong twice in this repo.

    py -3 analysis/w33_pass7107_q9_target_52.py [--target 52] [--timelimit 3000]
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- GF(9) ----
# element k in 0..8 encodes a + b*i with a = k % 3, b = k // 3, and i^2 = -1 = 2.
MUL = [[0] * 9 for _ in range(9)]
ADD = [[0] * 9 for _ in range(9)]
for k in range(9):
    for m in range(9):
        a, b = k % 3, k // 3
        c, d = m % 3, m // 3
        ADD[k][m] = ((a + c) % 3) + 3 * ((b + d) % 3)
        MUL[k][m] = ((a * c - b * d) % 3) + 3 * ((a * d + b * c) % 3)
NEG = [(-(k % 3)) % 3 + 3 * ((-(k // 3)) % 3) for k in range(9)]
INV = {}
for k in range(1, 9):
    for m in range(1, 9):
        if MUL[k][m] == 1:
            INV[k] = m
            break


def check_field() -> None:
    assert len(INV) == 8, "GF(9) must have 8 invertible elements"
    for k in range(9):
        for m in range(9):
            for n in range(9):
                assert MUL[k][ADD[m][n]] == ADD[MUL[k][m]][MUL[k][n]]
    assert MUL[3][3] == 2, "i^2 must be -1 = 2, not 0 -- Z/9 would give 0 here"


def build(q_elems=9):
    pts = []
    for v in itertools.product(range(9), repeat=4):
        if not any(v):
            continue
        lead = next(c for c in v if c)
        inv = INV[lead]
        pts.append(tuple(MUL[c][inv] for c in v))
    P = sorted(set(pts))

    def B(u, v):
        t = ADD[MUL[u[0]][v[1]]][NEG[MUL[u[1]][v[0]]]]
        return ADD[t][ADD[MUL[u[2]][v[3]]][NEG[MUL[u[3]][v[2]]]]]

    n = len(P)
    adj = [set() for _ in range(n)]
    for i in range(n):
        Pi = P[i]
        for j in range(i + 1, n):
            if B(Pi, P[j]) == 0:
                adj[i].add(j)
                adj[j].add(i)
    return P, adj, B


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=52)
    ap.add_argument("--timelimit", type=float, default=3000.0)
    args = ap.parse_args()

    print("=" * 78)
    print(f"Pass 7107 -- hunting a {args.target}-point partial ovoid in W(3,9)")
    print("=" * 78)

    check_field()
    print("\n  GF(9) = F_3[x]/(x^2+1) verified: distributive, 8 units, i^2 = 2 (NOT Z/9)")

    P, adj, B = build()
    n = len(P)
    deg = len(adj[0])
    print(f"  W(3,9): {n} points, degree {deg}   expect SRG(820,90,8,10)")
    assert n == 820 and deg == 90, f"got ({n},{deg})"

    # The automorphism group is transitive on pairs of NON-collinear points
    # (Cimrakova-Fack sec. 2.1), so WLOG a maximum partial ovoid contains any
    # chosen non-collinear pair.  That is a legitimate, not heuristic, reduction.
    p0 = 0
    p1 = next(j for j in range(1, n) if j not in adj[p0])
    keep = [i for i in range(n)
            if i not in adj[p0] and i not in adj[p1] and i not in (p0, p1)]
    print(f"\n  WLOG fixing the non-collinear pair ({p0},{p1}) -- the group is transitive")
    print(f"  on such pairs, so this loses no generality.")
    print(f"    candidates remaining: {len(keep)} of {n}")
    print(f"    so the ILP seeks {args.target - 2} more among {len(keep)}")

    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    idx = {p: i for i, p in enumerate(keep)}
    m = len(keep)
    edges = [(idx[a], idx[b]) for a in keep for b in adj[a] if b in idx and a < b]
    r, c, v = [], [], []
    for e, (i, j) in enumerate(edges):
        r += [e, e]
        c += [i, j]
        v += [1.0, 1.0]
    r += [len(edges)] * m
    c += list(range(m))
    v += [1.0] * m
    A = coo_matrix((v, (r, c)), shape=(len(edges) + 1, m))
    lo = np.full(len(edges) + 1, -np.inf)
    hi = np.ones(len(edges) + 1)
    lo[-1] = args.target - 2
    hi[-1] = np.inf
    print(f"    {len(edges)} collinearity constraints\n")
    print(f"  solving feasibility (time limit {args.timelimit:.0f}s)...", flush=True)

    res = milp(c=np.zeros(m),
               constraints=LinearConstraint(A, lo, hi),
               integrality=np.ones(m), bounds=Bounds(0, 1),
               options={"mip_rel_gap": 0.0, "time_limit": args.timelimit,
                        "presolve": True, "disp": True})

    print(f"\n  status {res.status}: {res.message}")
    if res.status == 0 and res.x is not None:
        sel = [keep[i] for i in range(m) if res.x[i] > 0.5] + [p0, p1]
        bad = [(a, b) for a, b in itertools.combinations(sel, 2) if B(P[a], P[b]) == 0]
        print(f"\n  *** FOUND a partial ovoid of size {len(sel)} ***")
        print(f"      pairwise-collinear violations: {len(bad)}  "
              f"{'VALID' if not bad else 'INVALID -- discard'}")
        if not bad:
            out = ROOT / "data" / f"PART_W33_Q9_PARTIAL_OVOID_{len(sel)}.json"
            import json
            out.write_text(json.dumps(
                {"q": 9, "size": len(sel),
                 "points": [list(P[i]) for i in sel],
                 "encoding": "GF(9) element k = (k%3) + (k//3)*i, i^2 = -1",
                 "verified": "pairwise non-collinear under x0y1-x1y0+x2y3-x3y2",
                 "context": ("beats this repo's local-search plateau of 51; the target 52 "
                             "came from interpolating (q+4)(q-1)/2 through the three known "
                             "odd values 7, 18, 33")}, indent=2), encoding="utf-8")
            print(f"      wrote {out.relative_to(ROOT).as_posix()}")
    elif res.status == 2:
        print(f"\n  INFEASIBLE -- no partial ovoid of size {args.target} exists in W(3,9).")
        print(f"  That KILLS the interpolation (q+4)(q-1)/2 at its first real test.")
    else:
        print(f"\n  did not resolve within the limit -- NO CONCLUSION either way.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
