"""Pass 7195 -- q=9 by large-neighbourhood search with an EXACT repair operator.

WHY THIS TOOL, AND WHY ONLY NOW. Pass 7192 proved the maximum partial ovoid of W(3,7) is
invariant under no element of order 3 (and none of order 7 in two of three classes). The
extremal objects are ASYMMETRIC. That rules out orbit methods -- they search a space proved
not to contain the optimum -- and it points at local search, which is exactly what this repo
already tried, plateauing at 51 across three move classes at q=9.

WHAT IS DIFFERENT HERE. Plain (1,2)- and (1,3)-swaps explore a neighbourhood of fixed tiny
radius. This destroys k points of the incumbent at once (k ~ 8..20) and then solves the
resulting subproblem EXACTLY with an ILP: given the surviving points, take every point
non-collinear with all of them and compute a true maximum independent set among those. The
repair is optimal, so the move is far larger than any swap while still never producing an
invalid set.

Every incumbent is a genuine partial ovoid by construction -- the constraints are enforced,
not scored -- so any size reported here is a LOWER bound on alpha(W(3,9)) and a construction.
No upper bound is claimed or implied. The repo's standing interval is 51 <= alpha <= 73
(Tallini).

    py -3 analysis/w33_pass7195_q9_lns_exact_repair.py [--q 9] [--budget 3000] [--target 52]
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
from w33_pass7187_q9_orbit_attack import Field, geometry  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def exact_mis(cands, adj, timelimit=20.0):
    """True maximum independent set on the induced subgraph -- exact when it closes."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    m = len(cands)
    if m == 0:
        return []
    pos = {p: i for i, p in enumerate(cands)}
    r, c, v, e = [], [], [], 0
    for i, p in enumerate(cands):
        for qq in adj[p]:
            j = pos.get(qq)
            if j is not None and j > i:
                r += [e, e]
                c += [i, j]
                v += [1.0, 1.0]
                e += 1
    if e == 0:
        return list(cands)
    A = coo_matrix((v, (r, c)), shape=(e, m))
    res = milp(c=-np.ones(m), constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(m), bounds=Bounds(0, 1),
               options={"mip_rel_gap": 0.0, "time_limit": timelimit, "presolve": True})
    if res.x is None:
        return []
    return [cands[i] for i in range(m) if res.x[i] > 0.5]


def greedy(n, adj, rng, nbr):
    S, banned = [], 0
    order = list(range(n))
    rng.shuffle(order)
    for p in order:
        if not (banned >> p) & 1:
            S.append(p)
            banned |= nbr[p] | (1 << p)
    return S


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--budget", type=float, default=3000.0)
    ap.add_argument("--target", type=int, default=52)
    ap.add_argument("--seed", type=int, default=7195)
    args = ap.parse_args()
    q = args.q

    print("=" * 78)
    print(f"Pass 7195 -- W(3,{q}) large-neighbourhood search, exact ILP repair")
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

    rng = random.Random(args.seed)
    best = []
    for _ in range(400):
        S = greedy(n, adj, rng, nbr)
        if len(S) > len(best):
            best = S
    print(f"  greedy start: {len(best)}", flush=True)

    cur = list(best)
    t0 = time.time()
    it = improved = 0
    while time.time() - t0 < args.budget:
        it += 1
        k = rng.randint(6, min(22, max(7, len(cur) - 2)))
        keep = list(cur)
        rng.shuffle(keep)
        keep = keep[:len(keep) - k]
        blocked = 0
        for p in keep:
            blocked |= nbr[p] | (1 << p)
        cands = [p for p in range(n) if not (blocked >> p) & 1]
        add = exact_mis(cands, adj, timelimit=15.0)
        new = keep + add
        if len(new) >= len(cur):
            cur = new
        if len(cur) > len(best):
            best = list(cur)
            improved += 1
            el = time.time() - t0
            print(f"    [{el:6.0f}s it{it:5d}] NEW BEST {len(best)}", flush=True)
            if len(best) >= args.target:
                print(f"    *** TARGET {args.target} REACHED ***", flush=True)
                break
        if it % 60 == 0:
            cur = list(best)     # restart from incumbent

    bad = [(a, b) for a, b in itertools.combinations(best, 2) if B(P[a], P[b]) == 0]
    print(f"\n  iterations {it}, improvements {improved}")
    print(f"  BEST partial ovoid found: {len(best)}")
    print(f"  verification: {len(bad)} collinear pairs among {len(best)} points "
          f"-- {'VALID' if not bad else 'INVALID'}")
    known = {3: 7, 5: 18, 7: 33}
    if q in known:
        k = known[q]
        print(f"  known optimum {k}: "
              f"{'REACHES' if len(best) >= k else f'falls {k - len(best)} short'}")
    if not bad and best:
        out = ROOT / "data" / f"PART_W33_Q{q}_LNS_OVOID_{len(best)}.json"
        out.write_text(json.dumps(
            {"q": q, "size": len(best), "method": "LNS with exact ILP repair",
             "points": [list(P[i]) for i in sorted(best)],
             "encoding": ("GF(9) k=(k%3)+(k//3)*i, i^2=-1" if q == 9 else f"GF({q})"),
             "verified": "pairwise non-collinear under x0y1-x1y0+x2y3-x3y2",
             "scope": ("a CONSTRUCTION, hence a lower bound on alpha(W(3,q)); no upper "
                       "bound is claimed. Tallini's upper bound at q=9 is 73")},
            indent=2), encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
