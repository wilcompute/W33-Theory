"""Pass 7188 -- the q=9 sweep the calibration pointed at: EVERY transvection subgroup.

Pass 7187 calibrated symmetric search against the two known odd optima and reached both:

    q=3  optimum 7  reached, by a subgroup of order 3
    q=5  optimum 18 reached, by a subgroup of order 3

Both winners have order THREE. W(3,9) lives in characteristic 3, where the order-3 elements
of Sp(4,q) include the symplectic transvections

    t_{v,lam}(x) = x + lam * B(x,v) * v

and t^3 = t_{v,3lam} = 1 exactly. Transvections are indexed by a projective point v, so
there are only 820 of them at q=9 -- the whole family is ENUMERABLE. This is not a random
search over subgroups; it is a complete sweep of one structurally motivated conjugacy class.

For each such H the orbit structure is forced: the 91 points of the tangent plane v^perp are
FIXED, and the other 729 fall into 243 orbits of size 3. So the 820-variable problem becomes
a 334-variable one, solved exactly by ILP per subgroup.

WHAT A RESULT WOULD MEAN. A hit at 52 is a construction and therefore a theorem. A miss is
only a statement about transvection-invariant sets -- it does not bound alpha(W(3,9)). The
script never reports a miss as a bound.

    py -3 analysis/w33_pass7188_q9_transvection_sweep.py [--q 9] [--limit 0]
"""

from __future__ import annotations

import argparse
import itertools
import json
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


def orbit_ilp(orbs, adjmask, sizes, target=None, timelimit=60.0):
    """Exact max-weight set of orbits, pairwise and internally non-collinear."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    good, gmask = [], []
    for o, mask in zip(orbs, adjmask):
        pts = o["mask"]
        if not (o["nbr"] & pts):          # internally non-collinear
            good.append(o)
            gmask.append(pts)
    m = len(good)
    if m == 0:
        return 0, []
    rows, cols, vals, e = [], [], [], 0
    for i in range(m):
        ni = good[i]["nbr"]
        for j in range(i + 1, m):
            if ni & gmask[j]:
                rows += [e, e]
                cols += [i, j]
                vals += [1.0, 1.0]
                e += 1
    if e == 0:
        return sum(len(g["pts"]) for g in good), [p for g in good for p in g["pts"]]
    A = coo_matrix((vals, (rows, cols)), shape=(e, m))
    w = np.array([len(g["pts"]) for g in good], float)
    res = milp(c=-w, constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(m), bounds=Bounds(0, 1),
               options={"mip_rel_gap": 0.0, "time_limit": timelimit, "presolve": True})
    if res.status != 0 or res.x is None:
        return -1, []
    sel = [i for i in range(m) if res.x[i] > 0.5]
    return int(round(sum(w[i] for i in sel))), [p for i in sel for p in good[i]["pts"]]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--limit", type=int, default=0, help="0 = all points v")
    ap.add_argument("--target", type=int, default=52)
    args = ap.parse_args()
    q = args.q

    print("=" * 78)
    print(f"Pass 7188 -- complete transvection sweep of W(3,{q}), target {args.target}")
    print("=" * 78)

    F = Field(q)
    P, idx, adj, B = geometry(F)
    n = len(P)
    print(f"\n  W(3,{q}): {n} points, degree {len(adj[0])}")
    nbrmask = [0] * n
    for i in range(n):
        mk = 0
        for j in adj[i]:
            mk |= 1 << j
        nbrmask[i] = mk

    lams = [l for l in range(1, q)]
    vs = P if not args.limit else P[:args.limit]
    print(f"  sweeping {len(vs)} transvection centres x {len(lams)} multipliers\n")

    best, bestpts, bestdesc = 0, [], ""
    seen_orbit_sig = set()
    tested = 0
    for vi, v in enumerate(vs):
        for lam in lams:
            M = transvection(F, v, lam)
            if M == IDENT:
                continue
            # order must be 3 in char 3
            if matmul(F, matmul(F, M, M), M) != IDENT:
                continue
            # orbits of <M>
            seen = [False] * n
            orbs = []
            for i in range(n):
                if seen[i]:
                    continue
                cyc, j = [], i
                while not seen[j]:
                    seen[j] = True
                    cyc.append(j)
                    j = idx[apply(F, M, P[j])]
                mk = 0
                nb = 0
                for p in cyc:
                    mk |= 1 << p
                    nb |= nbrmask[p]
                orbs.append({"pts": cyc, "mask": mk, "nbr": nb})
            sig = tuple(sorted(len(o["pts"]) for o in orbs))
            key = (sig, min(o["pts"][0] for o in orbs))
            if key in seen_orbit_sig:
                continue
            seen_orbit_sig.add(key)
            tested += 1
            w, pts = orbit_ilp(orbs, nbrmask, None)
            if w > best:
                best, bestpts = w, pts
                bestdesc = f"transvection centre {v}, lam={lam}, {len(orbs)} orbits"
                print(f"    v={v} lam={lam}: {len(orbs):4d} orbits -> "
                      f"invariant partial ovoid of size {w}")
                if w >= args.target:
                    print(f"    *** TARGET {args.target} REACHED ***")
        if vi % 100 == 0 and vi:
            print(f"    ... {vi}/{len(vs)} centres, {tested} distinct orbit types, "
                  f"best {best}", flush=True)

    print(f"\n  swept {tested} distinct transvection orbit-structures")
    print(f"  BEST transvection-invariant partial ovoid: {best}")
    bad = [(a, b) for a, b in itertools.combinations(bestpts, 2) if B(P[a], P[b]) == 0]
    print(f"  verification: {len(bad)} collinear pairs among the {len(bestpts)} points "
          f"-- {'VALID' if not bad else 'INVALID'}")
    if not bad and best >= args.target:
        out = ROOT / "data" / f"PART_W33_Q{q}_PARTIAL_OVOID_{best}.json"
        out.write_text(json.dumps(
            {"q": q, "size": best, "subgroup": bestdesc,
             "points": [list(P[i]) for i in bestpts],
             "encoding": "GF(9) k = (k%3) + (k//3)*i, i^2 = -1",
             "verified": "pairwise non-collinear under x0y1-x1y0+x2y3-x3y2"},
            indent=2), encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    print(f"""
  SCOPE. This sweep is COMPLETE over transvection-invariant sets and says nothing
  about sets with no transvection symmetry. A best of {best} is a lower bound on
  alpha(W(3,{q})) and NOT an upper bound of any kind.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
