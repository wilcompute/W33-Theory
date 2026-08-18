"""Pass 7114 -- large-neighbourhood search for a 52-point partial ovoid of W(3,9).

STATE OF PLAY, checked against the literature before running:

  * upper bound  q^2-q+1 = 73   Tallini, and BETTER than the 80.84 MILP dual bound this
                                repo currently records for q=9. That is a free improvement
                                and it is a theorem, not a computation.
  * lower bound  2q+1 = 19      the best PUBLISHED general construction for q = 3^h
                                (Ceria-De Beule-Pavese-Smaldore, arXiv:2203.04553, Table 1;
                                their stronger (q^{3/2}+3q-q^{1/2}+3)/3 needs p != 3, and
                                9 = 3^2, so q=9 is excluded from it).
  * this repo    51             a MILP incumbent from Pass 5658, with NO STORED WITNESS.
  * target       52             from interpolating alpha = q^2-q+1 - C(q-2,2) through the
                                three known odd values 7, 18, 33. Zero degrees of freedom,
                                so this is a prediction, not evidence.

WHY LNS AND NOT MORE LOCAL SEARCH. Pass 5784 reports three local-search classes all
plateauing at 51. Repeating them is not a plan. LNS destroys a random slice of the
incumbent and re-solves that slice EXACTLY by ILP, so it escapes plateaus a (1,2)-swap
neighbourhood cannot: the exact sub-solve can perform a coordinated k-way exchange that no
single swap sees.

Every witness found is written out with its points, so the repo gets something it can
re-verify -- which it currently cannot do even for 51.

    py -3 analysis/w33_pass7114_q9_lns.py [--target 52] [--seconds 2400]
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

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from w33_pass7107_q9_target_52 import build, check_field  # noqa: E402


def greedy(adj, n, rng, order=None):
    if order is None:
        order = list(range(n))
        rng.shuffle(order)
    cur, banned = [], set()
    for v in order:
        if v not in banned:
            cur.append(v)
            banned |= adj[v]
            banned.add(v)
    return cur


def swap_1_2(adj, n, cur, rng, rounds=20000):
    """Classic (1,2) improvement: drop one, add two."""
    S = set(cur)
    blocked = [0] * n
    for v in S:
        for u in adj[v]:
            blocked[u] += 1
    for _ in range(rounds):
        # free vertices: exactly one neighbour in S
        ones = [u for u in range(n) if u not in S and blocked[u] == 1]
        if not ones:
            break
        rng.shuffle(ones)
        done = False
        for u in ones:
            w = next(iter(adj[u] & S))
            partners = [x for x in ones
                        if x != u and x not in adj[u] and w in adj[x]]
            if partners:
                x = partners[0]
                S.discard(w)
                for t in adj[w]:
                    blocked[t] -= 1
                for add in (u, x):
                    S.add(add)
                    for t in adj[add]:
                        blocked[t] += 1
                done = True
                break
        if not done:
            break
    return sorted(S)


def lns_step(adj, n, cur, rng, free_size, timelimit):
    """Free a random slice, fix the rest, re-solve the slice exactly."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    S = set(cur)
    seed = rng.choice(sorted(S))
    # grow a connected-ish region around a seed so the freed slice is coherent
    region = {seed}
    frontier = list(adj[seed])
    rng.shuffle(frontier)
    while len(region) < free_size and frontier:
        v = frontier.pop()
        if v in region:
            continue
        region.add(v)
        nb = list(adj[v])
        rng.shuffle(nb)
        frontier.extend(nb[:6])
    region = sorted(region)

    kept = [v for v in S if v not in region]
    forbidden = set()
    for v in kept:
        forbidden |= adj[v]
    cand = [v for v in region if v not in forbidden and v not in kept]
    if len(cand) < 2:
        return cur
    idx = {v: i for i, v in enumerate(cand)}
    m = len(cand)
    edges = [(idx[a], idx[b]) for a in cand for b in adj[a] if b in idx and a < b]
    if not edges:
        return sorted(set(kept) | set(cand))
    r, c, val = [], [], []
    for e, (i, j) in enumerate(edges):
        r += [e, e]
        c += [i, j]
        val += [1.0, 1.0]
    A = coo_matrix((val, (r, c)), shape=(len(edges), m))
    res = milp(c=-np.ones(m), constraints=LinearConstraint(A, -np.inf, 1),
               integrality=np.ones(m), bounds=Bounds(0, 1),
               options={"mip_rel_gap": 0.0, "time_limit": timelimit, "presolve": True})
    if res.status != 0 or res.x is None:
        return cur
    new = sorted(set(kept) | {cand[i] for i in range(m) if res.x[i] > 0.5})
    return new if len(new) > len(cur) else cur


def verify(P, B, sel):
    return [(a, b) for a, b in itertools.combinations(sel, 2) if B(P[a], P[b]) == 0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=int, default=52)
    ap.add_argument("--seconds", type=float, default=2400.0)
    ap.add_argument("--free", type=int, default=170)
    args = ap.parse_args()

    print("=" * 78)
    print(f"Pass 7114 -- LNS hunt for a {args.target}-point partial ovoid of W(3,9)")
    print("=" * 78, flush=True)

    check_field()
    P, adj, B = build()
    n = len(P)
    print(f"\n  W(3,9): {n} points, degree {len(adj[0])}", flush=True)
    print(f"  published lower bound 19 | repo incumbent 51 | Tallini upper bound 73")
    print(f"  target {args.target}\n", flush=True)

    rng = random.Random(20260818)
    t0 = time.time()
    best, best_set = 0, []

    # phase 1: many greedy restarts + (1,2) improvement
    for it in range(60):
        cur = swap_1_2(adj, n, greedy(adj, n, rng), rng)
        if len(cur) > best:
            best, best_set = len(cur), cur
            print(f"    [{time.time() - t0:6.1f}s] greedy+swap -> {best}", flush=True)
    print(f"\n  phase 1 best: {best}", flush=True)

    # phase 2: LNS on the incumbent
    stall = 0
    while time.time() - t0 < args.seconds and best < args.target:
        cur = lns_step(adj, n, best_set, rng, args.free, 25.0)
        if len(cur) > best:
            bad = verify(P, B, cur)
            if bad:
                print(f"    LNS produced an INVALID set, discarding ({len(bad)} violations)")
                continue
            best, best_set, stall = len(cur), cur, 0
            print(f"    [{time.time() - t0:6.1f}s] LNS -> {best}", flush=True)
        else:
            stall += 1
            if stall % 25 == 0:
                print(f"    [{time.time() - t0:6.1f}s] stalled at {best} "
                      f"({stall} non-improving)", flush=True)
            if stall % 60 == 0:
                # restart the incumbent from a perturbed greedy to escape
                alt = swap_1_2(adj, n, greedy(adj, n, rng), rng)
                if len(alt) >= best - 2:
                    best_set = alt if len(alt) > len(best_set) else best_set

    bad = verify(P, B, best_set)
    print(f"\n  BEST FOUND: {len(best_set)}   violations: {len(bad)}  "
          f"{'VALID' if not bad else 'INVALID'}", flush=True)
    if not bad and best_set:
        out = ROOT / "data" / f"PART_W33_Q9_PARTIAL_OVOID_{len(best_set)}.json"
        out.write_text(json.dumps({
            "q": 9, "size": len(best_set),
            "points": [list(P[i]) for i in best_set],
            "encoding": "GF(9) element k = (k%3) + (k//3)*i with i^2 = -1 = 2",
            "form": "x0y1 - x1y0 + x2y3 - x3y2",
            "verified": "all pairs checked non-collinear at write time",
            "context": {
                "tallini_upper_bound": 73,
                "repo_dual_bound_previously_recorded": 80.84,
                "published_general_lower_bound_for_q_eq_3_pow_h": 19,
                "repo_incumbent_pass5658": 51,
                "interpolated_target": 52,
                "note": ("the repo's 51 was a MILP incumbent with no stored witness; this "
                         "file stores one that can be re-verified")},
        }, indent=2), encoding="utf-8")
        print(f"  wrote {out.relative_to(ROOT).as_posix()}")
    if best >= args.target:
        print(f"\n  *** TARGET {args.target} REACHED ***")
    else:
        print(f"\n  target {args.target} NOT reached -- no claim either way about "
              f"whether it exists")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
