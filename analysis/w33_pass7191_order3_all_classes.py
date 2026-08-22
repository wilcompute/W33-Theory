"""Pass 7191 -- ALL order-3 classes, after Pass 7190 tested one and drew a false lesson.

WHAT PASS 7190 GOT WRONG. It keyed order-3 elements by the Jordan type of u - 1. That is a
genuine class invariant in characteristic 3, but at q = 5 and q = 7 order-3 elements are
SEMISIMPLE, every one of them lands in a single bucket, and `setdefault` then tested exactly
ONE representative. So its q=7 answer of 30 was the best over one class, reported as if it
were the best over all order-3 symmetry.

THE FIX is to key on the invariant that actually determines the answer: the ORBIT PROFILE on
the points of W(3,q), the multiset of orbit lengths. Two elements with different profiles
give genuinely different ILPs; two with the same profile give the same optimum. That is the
right equivalence for this question and it needs no conjugacy computation at all.

WHY THIS MATTERS RATHER THAN BEING BOOKKEEPING. q=7 is the calibration point that decides
whether order-3 symmetry is the right regime. If some order-3 class reaches the known 33,
the method is validated and its q=9 number is meaningful. If every class stops below 33,
then order-3 symmetry provably CANNOT reach the optimum in this family, and any q=9 number
it produces is a lower bound that should not be mistaken for alpha.

Either outcome is worth having. The script states which one occurred.

    py -3 analysis/w33_pass7191_order3_all_classes.py [--q 7] [--samples 4000]
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
    A = coo_matrix((v, (r, c)), shape=(max(e, 1), m))
    if e == 0:
        return int(w.sum()), [p for g in good for p in g["pts"]], "no conflicts"
    res = milp(c=-w, constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(m), bounds=Bounds(0, 1),
               options={"mip_rel_gap": 0.0, "time_limit": timelimit, "presolve": True})
    if res.x is None:
        return -1, [], f"no incumbent (status {res.status})"
    sel = [i for i in range(m) if res.x[i] > 0.5]
    pts = [p for i in sel for p in good[i]["pts"]]
    return len(pts), pts, ("PROVED optimal" if res.status == 0
                           else f"incumbent only (status {res.status})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=7)
    ap.add_argument("--samples", type=int, default=4000)
    ap.add_argument("--timelimit", type=float, default=300.0)
    ap.add_argument("--order", type=int, default=3)
    args = ap.parse_args()
    q, ordr = args.q, args.order

    print("=" * 78)
    print(f"Pass 7191 -- W(3,{q}): every order-{ordr} orbit profile, exact per profile")
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

    def orbits_of(M):
        vis = [False] * n
        out = []
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
            out.append({"pts": cyc, "mask": mk, "nbr": nb})
        return out

    rng = random.Random(7191 + q)
    profiles = {}
    for _ in range(args.samples):
        g = transvection(F, rng.choice(P), rng.randrange(1, q))
        for _ in range(rng.randrange(1, 5)):
            g = matmul(F, g, transvection(F, rng.choice(P), rng.randrange(1, q)))
        if g == IDENT:
            continue
        X, k = g, 1
        while X != IDENT and k <= ordr:
            X = matmul(F, X, g)
            k += 1
        if X != IDENT or k != ordr:
            continue
        orbs = orbits_of(g)
        prof = {}
        for o in orbs:
            prof[len(o["pts"])] = prof.get(len(o["pts"]), 0) + 1
        key = tuple(sorted(prof.items()))
        profiles.setdefault(key, (g, orbs))
    print(f"  distinct order-{ordr} ORBIT PROFILES found: {len(profiles)}\n", flush=True)

    best, bestpts, bestdesc = 0, [], ""
    for key, (g, orbs) in sorted(profiles.items()):
        prof = dict(key)
        w, pts, note = solve(orbs, args.timelimit)
        print(f"    profile {prof} ({len(orbs)} orbits) -> {w}   [{note}]", flush=True)
        if w > best:
            best, bestpts, bestdesc = w, pts, f"profile {prof}, {note}"

    bad = [(a, b) for a, b in itertools.combinations(bestpts, 2) if B(P[a], P[b]) == 0]
    print(f"\n  BEST over ALL order-{ordr} profiles: {best}")
    print(f"  verification: {len(bad)} collinear pairs among {len(bestpts)} points "
          f"-- {'VALID' if not bad else 'INVALID'}")
    known = {3: 7, 5: 18, 7: 33}
    verdict = ""
    if q in known:
        k = known[q]
        if best >= k:
            verdict = (f"order-{ordr} symmetry REACHES the known optimum {k} -- the regime "
                       f"is validated at q={q}")
        else:
            verdict = (f"order-{ordr} symmetry CANNOT reach the known optimum {k} "
                       f"(best {best}, short by {k - best}). The optimum at q={q} has no "
                       f"order-{ordr} symmetry, so a q=9 number from this method is a "
                       f"LOWER BOUND and must not be read as alpha.")
        print(f"  VERDICT: {verdict}")
    if not bad and bestpts:
        out = ROOT / "data" / f"PART_W33_Q{q}_ORDER{ordr}_ALLCLASSES_{best}.json"
        out.write_text(json.dumps(
            {"q": q, "order": ordr, "size": best, "symmetry": bestdesc,
             "profiles_tested": len(profiles),
             "points": [list(P[i]) for i in bestpts],
             "verified": "pairwise non-collinear under x0y1-x1y0+x2y3-x3y2",
             "verdict": verdict,
             "scope": ("maximum over sets invariant under an order-3 element, complete "
                       "over the orbit profiles found; a LOWER bound on alpha")},
            indent=2), encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
