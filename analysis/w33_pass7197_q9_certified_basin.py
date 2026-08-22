"""Pass 7197 -- how far from a known 51-set any 52-set must lie, certified.

THE SITUATION. Three independent LNS runs with exact ILP repair -- a method that finds the
q=7 optimum of 33 in five seconds -- reach 51 at q=9 within seconds and then stall for
minutes. This repo's earlier local searches plateau at 51 too, across three move classes.
Against that stands only a zero-degrees-of-freedom quadratic through 7, 18, 33 predicting 52.

A PLATEAU IS NOT A THEOREM, so this turns it into one, locally. Given a known 51-point
partial ovoid S, ask directly:

    does ANY 52-point partial ovoid agree with S in at least 51 - d points?

That is a single ILP per d, not C(51,d) subproblems: constrain sum_{p in S} x_p >= 51-d,
constrain the total to >= 52, and keep the collinearity constraints. INFEASIBLE certifies
that every 52-set, if one exists, differs from S in more than d points.

WHAT THIS CAN AND CANNOT SETTLE. It cannot prove alpha(W(3,9)) = 51 -- a 52-set could live
far from S. It CAN replace "our searches kept returning 51" with a measured radius, which is
a statement with content. The script reports the largest d it certified and never converts
that into a bound on alpha.

    py -3 analysis/w33_pass7197_q9_certified_basin.py [--dmax 12] [--timelimit 300]
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import Field, geometry  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", type=int, default=9)
    ap.add_argument("--seedfile", default="")
    ap.add_argument("--dmax", type=int, default=12)
    ap.add_argument("--target", type=int, default=52)
    ap.add_argument("--timelimit", type=float, default=300.0)
    args = ap.parse_args()
    q = args.q

    print("=" * 78)
    print(f"Pass 7197 -- certified basin around a known 51-set in W(3,{q})")
    print("=" * 78)

    cand = ([Path(args.seedfile)] if args.seedfile else
            sorted(ROOT.glob(f"data/PART_W33_Q{q}_LNS_OVOID_*.json")) +
            sorted(ROOT.glob(f"data/PART_W33_Q{q}_*OVOID*.json")))
    src = next((c for c in cand if c.is_file()), None)
    if src is None:
        print("  no stored partial ovoid for this q -- run Pass 7195 first")
        return 1
    doc = json.loads(src.read_text(encoding="utf-8"))
    F = Field(q)
    P, idx, adj, B = geometry(F)
    n = len(P)
    S = sorted(idx[tuple(p)] for p in doc["points"])
    bad = [(a, b) for a, b in itertools.combinations(S, 2) if B(P[a], P[b]) == 0]
    print(f"\n  seed: {src.name}, |S| = {len(S)}, "
          f"{'VALID' if not bad else 'INVALID -- abort'}")
    if bad:
        return 1
    print(f"  W(3,{q}): {n} points, degree {len(adj[0])}\n", flush=True)

    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    edges = [(i, j) for i in range(n) for j in adj[i] if i < j]
    r, c, v = [], [], []
    for e, (i, j) in enumerate(edges):
        r += [e, e]
        c += [i, j]
        v += [1.0, 1.0]
    E = len(edges)
    Sset = set(S)
    # row E: total >= target ; row E+1: agreement with S >= |S| - d
    r += [E] * n + [E + 1] * len(S)
    c += list(range(n)) + list(S)
    v += [1.0] * n + [1.0] * len(S)
    A = coo_matrix((v, (r, c)), shape=(E + 2, n))

    certified = -1
    for d in range(0, args.dmax + 1):
        lo = np.full(E + 2, -np.inf)
        hi = np.ones(E + 2)
        lo[E] = args.target
        hi[E] = np.inf
        lo[E + 1] = len(S) - d
        hi[E + 1] = np.inf
        res = milp(c=np.zeros(n), constraints=LinearConstraint(A, lo, hi),
                   integrality=np.ones(n), bounds=Bounds(0, 1),
                   options={"mip_rel_gap": 0.0, "time_limit": args.timelimit,
                            "presolve": True})
        if res.status == 2:
            certified = d
            print(f"    d={d:2d}: INFEASIBLE -- no {args.target}-set agrees with S in "
                  f">= {len(S) - d} points", flush=True)
        elif res.status == 0 and res.x is not None:
            sel = [i for i in range(n) if res.x[i] > 0.5]
            vb = [(a, b) for a, b in itertools.combinations(sel, 2) if B(P[a], P[b]) == 0]
            print(f"    d={d:2d}: FEASIBLE -- found a {len(sel)}-point set, "
                  f"{len(vb)} violations", flush=True)
            if not vb:
                out = ROOT / "data" / f"PART_W33_Q{q}_PARTIAL_OVOID_{len(sel)}.json"
                out.write_text(json.dumps(
                    {"q": q, "size": len(sel),
                     "points": [list(P[i]) for i in sorted(sel)],
                     "found_by": f"basin search at radius d={d} from a {len(S)}-set",
                     "verified": "pairwise non-collinear"}, indent=2), encoding="utf-8")
                print(f"    *** {len(sel)} FOUND -- wrote "
                      f"{out.relative_to(ROOT).as_posix()} ***")
            break
        else:
            print(f"    d={d:2d}: did not resolve in {args.timelimit:.0f}s "
                  f"(status {res.status}) -- NO CONCLUSION, stopping", flush=True)
            break

    print(f"\n  CERTIFIED RADIUS: {certified}")
    if certified >= 0:
        print(f"""  Every {args.target}-point partial ovoid of W(3,{q}), if one exists, differs from
  this particular 51-set in MORE THAN {certified} points. That is a measured statement and
  it is NOT a bound on alpha(W(3,{q})): a {args.target}-set could exist far from S.""")
    out = ROOT / "data" / f"PART_W33_PASS7197_Q{q}_CERTIFIED_BASIN.json"
    out.write_text(json.dumps(
        {"boundary": (f"every {args.target}-set, if any exists, differs from this 51-set in "
                      f"more than {certified} points. NOT a bound on alpha(W(3,{q}))"),
         "q": q, "seed_size": len(S), "target": args.target,
         "certified_radius": certified, "seed_file": src.name}, indent=2), encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
