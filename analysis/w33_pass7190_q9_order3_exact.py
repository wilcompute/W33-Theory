"""Pass 7190 -- q=9 restricted to order-3 symmetry, the regime calibration selected.

THE CALIBRATION THAT CHOSE THIS. Symmetric search was run at q=5 in two regimes against the
known optimum 18:

    subgroups of order >= 9   ->  best 11   (SEVEN short -- over-constrained)
    subgroups of order 3      ->  best 18   (reaches the optimum)

So extremal partial ovoids in this family have SMALL stabilizers. Large-subgroup sweeps at
q=9 would have produced a confident number that meant nothing. The regime is order 3.

In characteristic 3 every order-3 element of Sp(4,9) is unipotent, and the classes are
distinguished by the Jordan type of u - 1. Two occur and both are swept here:

    [2,1,1]  rank(u-1) = 1   the symplectic transvections
    [2,2]    rank(u-1) = 2, (u-1)^2 = 0

For each the 820 points break into orbits of size 3 and fixed points, and the maximum
invariant partial ovoid is an exact max-weight independent set over those orbits.

WHY AN UNPROVEN ILP STILL SETTLES IT. Any incumbent the solver returns is a genuine
H-invariant partial ovoid -- it satisfies every non-collinearity constraint. So a 52 is a
CONSTRUCTION and therefore a theorem, whether or not optimality is proved. Only the claim
"this is the maximum" needs the proof, and that claim is not made unless the solver closes.

    py -3 analysis/w33_pass7190_q9_order3_exact.py [--q 9] [--timelimit 2400]
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import (  # noqa: E402
    Field, geometry, transvection, apply, matmul, IDENT,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def jordan_type(F, g):
    N = tuple(tuple(F.add[g[i][j]][F.neg[1 if i == j else 0]] for j in range(4))
              for i in range(4))

    def rank(M):
        rows = [list(r) for r in M]
        r = 0
        for c in range(4):
            piv = next((i for i in range(r, 4) if rows[i][c]), None)
            if piv is None:
                continue
            rows[r], rows[piv] = rows[piv], rows[r]
            iv = F.inv[rows[r][c]]
            rows[r] = [F.mul[x][iv] for x in rows[r]]
            for i in range(4):
                if i != r and rows[i][c]:
                    f = rows[i][c]
                    rows[i] = [F.add[rows[i][j]][F.neg[F.mul[f][rows[r][j]]]]
                               for j in range(4)]
            r += 1
        return r

    r1 = rank(N)
    r2 = rank(matmul(F, N, N))
    if r1 == 1:
        return "[2,1,1] transvection"
    return "[2,2]" if r2 == 0 else "[3,1]"


def orbits_of_cyclic(F, M, P, idx, nbr, n):
    vis = [False] * n
    orbs = []
    for i in range(n):
        if vis[i]:
            continue
        cyc, j = [], i
        while not vis[j]:
            vis[j] = True
            cyc.append(j)
            j = idx[apply(F, M, P[j])]
        mk = nb = 0
        for p in cyc:
            mk |= 1 << p
            nb |= nbr[p]
        orbs.append({"pts": cyc, "mask": mk, "nbr": nb})
    return orbs


def solve(orbs, timelimit):
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    good = [o for o in orbs if not (o["nbr"] & o["mask"])]
    m = len(good)
    if m == 0:
        return 0, [], "no internally-valid orbit"
    r, c, v, e = [], [], [], 0
    for i in range(m):
        ni = good[i]["nbr"]
        for j in range(i + 1, m):
            if ni & good[j]["mask"]:
                r += [e, e]
                c += [i, j]
                v += [1.0, 1.0]
                e += 1
    w = np.array([len(g["pts"]) for g in good], float)
    A = coo_matrix((v, (r, c)), shape=(e, m))
    res = milp(c=-w, constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(m), bounds=Bounds(0, 1),
               options={"mip_rel_gap": 0.0, "time_limit": timelimit, "presolve": True})
    if res.x is None:
        return -1, [], f"no incumbent (status {res.status})"
    sel = [i for i in range(m) if res.x[i] > 0.5]
    pts = [p for i in sel for p in good[i]["pts"]]
    proved = res.status == 0
    return len(pts), pts, ("PROVED optimal" if proved else
                           f"incumbent only, not proved (status {res.status})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--timelimit", type=float, default=2400.0)
    ap.add_argument("--target", type=int, default=52)
    args = ap.parse_args()
    q = args.q

    print("=" * 78)
    print(f"Pass 7190 -- W(3,{q}), order-3 invariant partial ovoids (exact per class)")
    print("=" * 78)

    F = Field(q)
    P, idx, adj, B = geometry(F)
    n = len(P)
    print(f"\n  W(3,{q}): {n} points, degree {len(adj[0])}", flush=True)
    nbr = [0] * n
    for i in range(n):
        mk = 0
        for j in adj[i]:
            mk |= 1 << j
        nbr[i] = mk

    reps, rng = {}, random.Random(7190)
    for _ in range(200000):
        g = transvection(F, rng.choice(P), rng.randrange(1, q))
        for _ in range(rng.randrange(1, 4)):
            g = matmul(F, g, transvection(F, rng.choice(P), rng.randrange(1, q)))
        if g == IDENT or matmul(F, matmul(F, g, g), g) != IDENT:
            continue
        t = jordan_type(F, g)
        reps.setdefault(t, g)
        if len(reps) >= 3:
            break
    print(f"  order-3 classes found: {sorted(reps)}\n", flush=True)

    best, bestpts, bestdesc = 0, [], ""
    for t, g in sorted(reps.items()):
        orbs = orbits_of_cyclic(F, g, P, idx, nbr, n)
        prof = {}
        for o in orbs:
            prof[len(o["pts"])] = prof.get(len(o["pts"]), 0) + 1
        print(f"  class {t}: {len(orbs)} orbits, profile {prof}", flush=True)
        w, pts, note = solve(orbs, args.timelimit)
        print(f"    -> best invariant partial ovoid {w}   [{note}]", flush=True)
        if w > best:
            best, bestpts, bestdesc = w, pts, f"{t}, {note}"

    bad = [(a, b) for a, b in itertools.combinations(bestpts, 2) if B(P[a], P[b]) == 0]
    print(f"\n  BEST over all order-3 classes: {best}")
    print(f"  verification: {len(bad)} collinear pairs among {len(bestpts)} points "
          f"-- {'VALID' if not bad else 'INVALID'}")
    known = {3: 7, 5: 18, 7: 33}
    if q in known:
        k = known[q]
        print(f"  known optimum {k}: {'REACHES' if best >= k else f'falls {k-best} short'}")
    if not bad and bestpts:
        out = ROOT / "data" / f"PART_W33_Q{q}_ORDER3_OVOID_{best}.json"
        out.write_text(json.dumps(
            {"q": q, "size": best, "symmetry": bestdesc,
             "points": [list(P[i]) for i in bestpts],
             "encoding": ("GF(9) k=(k%3)+(k//3)*i, i^2=-1" if q == 9 else f"GF({q})"),
             "verified": "pairwise non-collinear under x0y1-x1y0+x2y3-x3y2",
             "scope": ("maximum over sets invariant under an order-3 element; a LOWER "
                       "bound on alpha(W(3,q)), never an upper bound")},
            indent=2), encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    print(f"""
  SCOPE. Complete over order-3-invariant sets only. {best} is a LOWER bound on
  alpha(W(3,{q})) and is not an upper bound of any kind.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
