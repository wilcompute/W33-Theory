"""Pass 7189 -- q=9 by LARGER subgroups, where the orbit ILP is actually tractable.

WHY THE TRANSVECTION SWEEP STALLED. A single transvection has 334 orbits on the 820 points
(91 fixed, 243 of size 3), and maximum-weight independent set over 334 orbits with ~40%
conflict density did not close. Small subgroups do not reduce the problem enough.

THE INVERSION. Orbit count is ~820/|H|, so LARGER subgroups give SMALLER ILPs. At |H| = 27
the problem is ~40 variables and solves instantly. Characteristic 3 is generous here: the
Sylow 3-subgroup of Sp(4,9) has order 3^8 = 6561, so subgroups of order 9, 27, 81 are
plentiful, and the extraspecial/Heisenberg group of order 27 sits naturally inside it.

WHAT IS BEING TESTED. For each subgroup H found, the exact maximum H-invariant partial ovoid.
This is complete for each H and says nothing about sets H does not stabilize -- a hit is a
construction and a theorem, a miss is not a bound. The script never reports a miss as a bound.

CALIBRATION. Run with --q 5 to check the sweep still reaches the known optimum 18 before
trusting anything it says at q=9.

    py -3 analysis/w33_pass7189_q9_heisenberg_sweep.py [--q 9] [--trials 3000]
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import (  # noqa: E402
    Field, geometry, transvection, apply, matmul, closure, IDENT,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def orbit_ilp(orbs, timelimit=90.0):
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    good = [o for o in orbs if not (o["nbr"] & o["mask"])]
    m = len(good)
    if m == 0:
        return 0, []
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
    if e == 0:
        return int(w.sum()), [p for g in good for p in g["pts"]]
    A = coo_matrix((v, (r, c)), shape=(e, m))
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
    ap.add_argument("--trials", type=int, default=3000)
    ap.add_argument("--minH", type=int, default=9)
    ap.add_argument("--maxH", type=int, default=400)
    ap.add_argument("--budget", type=float, default=5400.0)
    ap.add_argument("--target", type=int, default=52)
    args = ap.parse_args()
    q = args.q

    print("=" * 78)
    print(f"Pass 7189 -- W(3,{q}) by subgroups of order {args.minH}..{args.maxH}")
    print("=" * 78)

    F = Field(q)
    P, idx, adj, B = geometry(F)
    n = len(P)
    print(f"\n  W(3,{q}): {n} points, degree {len(adj[0])}", flush=True)
    nbr = [0] * n
    for i in range(n):
        m = 0
        for j in adj[i]:
            m |= 1 << j
        nbr[i] = m

    rng = random.Random(7189 + q)
    best, bestpts, bestdesc = 0, [], ""
    seen = set()
    t0 = time.time()
    hist = {}
    for t in range(args.trials):
        if time.time() - t0 > args.budget:
            print(f"    [budget {args.budget:.0f}s reached at trial {t}]", flush=True)
            break
        gens = []
        for _ in range(rng.choice([2, 2, 3])):
            g = transvection(F, rng.choice(P), rng.randrange(1, q))
            for _ in range(rng.randrange(0, 2)):
                g = matmul(F, g, transvection(F, rng.choice(P), rng.randrange(1, q)))
            gens.append(g)
        H = closure(F, gens, cap=args.maxH)
        if H is None or len(H) < args.minH:
            continue
        key = frozenset(H)
        if key in seen:
            continue
        seen.add(key)
        # orbits
        vis = [False] * n
        orbs = []
        for i in range(n):
            if vis[i]:
                continue
            o = set()
            stack = [i]
            vis[i] = True
            while stack:
                j = stack.pop()
                o.add(j)
                for M in H:
                    k = idx[apply(F, M, P[j])]
                    if not vis[k]:
                        vis[k] = True
                        stack.append(k)
            pts = sorted(o)
            mk = 0
            nb = 0
            for p in pts:
                mk |= 1 << p
                nb |= nbr[p]
            orbs.append({"pts": pts, "mask": mk, "nbr": nb})
        if len(orbs) > 160:      # ILP would not close; skip rather than lie
            continue
        w, pts = orbit_ilp(orbs)
        hist[len(H)] = max(hist.get(len(H), 0), w)
        if w > best:
            best, bestpts = w, pts
            bestdesc = f"|H|={len(H)}, {len(orbs)} orbits"
            print(f"    |H|={len(H):4d}  {len(orbs):4d} orbits -> {w}", flush=True)
            if w >= args.target:
                print(f"    *** TARGET {args.target} REACHED ***", flush=True)

    print(f"\n  distinct subgroups tested: {len(seen)}")
    print(f"  best by |H|: {dict(sorted(hist.items()))}")
    print(f"  BEST invariant partial ovoid: {best}   ({bestdesc})")
    bad = [(a, b) for a, b in itertools.combinations(bestpts, 2) if B(P[a], P[b]) == 0]
    print(f"  verification: {len(bad)} collinear pairs among {len(bestpts)} points "
          f"-- {'VALID' if not bad else 'INVALID'}")
    known = {3: 7, 5: 18, 7: 33}
    if q in known:
        print(f"  known optimum {known[q]}: symmetric search "
              f"{'REACHES it' if best >= known[q] else f'falls {known[q]-best} short'}")
    if not bad and bestpts:
        out = ROOT / "data" / f"PART_W33_Q{q}_INVARIANT_OVOID_{best}.json"
        out.write_text(json.dumps(
            {"q": q, "size": best, "subgroup": bestdesc,
             "points": [list(P[i]) for i in bestpts],
             "encoding": ("GF(9) k = (k%3)+(k//3)*i, i^2=-1" if q == 9 else f"GF({q})"),
             "verified": "pairwise non-collinear under x0y1-x1y0+x2y3-x3y2",
             "scope": ("maximum over H-invariant sets for the subgroups sampled; a LOWER "
                       "bound on alpha, never an upper bound")},
            indent=2), encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
