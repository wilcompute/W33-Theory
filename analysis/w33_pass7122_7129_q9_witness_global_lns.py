#!/usr/bin/env python3
"""Passes 7122--7129: recover the missing q=9 witness and strengthen the search neighbourhood.

The previous q=9 lower bound 51 was stored as an integer without its 51 points.  This
producer freezes an independently rediscovered witness and verifies it directly in
W(3,9).  It also replaces the earlier region-only LNS neighbourhood with a global-compatible
replacement neighbourhood: after keeping a core of the incumbent, *every* point of W(3,9)
compatible with that core is eligible for the exact residual MILP.

Default mode verifies the frozen witness and writes a compact certificate.  --search runs
seeded global-compatible replacement trials against target 52.  Failure to reach 52 is not
an upper bound and is never written as one.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7107_q9_target_52 import build, check_field  # noqa: E402

WITNESS = ROOT / "data" / "PART_W33_Q9_PARTIAL_OVOID_51.json"
OUT = ROOT / "data" / "PART_W33_PASS7122_7129_Q9_WITNESS_GLOBAL_LNS.json"


def verify_independent(adj, S):
    S = set(S)
    return [(u, v) for u in S for v in adj[u] if u < v and v in S]


def blocker_data(adj, S, n):
    S = set(S)
    outside = [v for v in range(n) if v not in S]
    blockers = {v: frozenset(adj[v] & S) for v in outside}
    hist = Counter(map(len, blockers.values()))
    return outside, blockers, hist


def exchange_stable_through(adj, S, n, max_removed=7):
    """Exact small-augmentation test.

    An improving exchange selecting t outside vertices must remove the union of their
    blockers.  Gain >=1 means |union blockers| < t.  Search every independent outside set
    with t<=max_removed+1 and that blocker-union bound.  This is exhaustive for this radius.
    """
    S = set(S)
    outside, blockers, _ = blocker_data(adj, S, n)
    checked = {}
    for t in range(1, max_removed + 2):
        cands = [v for v in outside if len(blockers[v]) <= t - 1]
        cands.sort(key=lambda v: (len(blockers[v]), v))
        nodes = 0
        found = None

        def rec(start, chosen, bunion):
            nonlocal nodes, found
            nodes += 1
            if len(chosen) == t:
                if len(bunion) < t:
                    found = (tuple(chosen), tuple(sorted(bunion)))
                    return True
                return False
            need = t - len(chosen)
            if len(cands) - start < need:
                return False
            for ii in range(start, len(cands)):
                v = cands[ii]
                nb = bunion | blockers[v]
                if len(nb) >= t:
                    continue
                if any(v in adj[u] for u in chosen):
                    continue
                if rec(ii + 1, chosen + [v], nb):
                    return True
            return False

        rec(0, [], frozenset())
        checked[str(t)] = {"candidate_vertices": len(cands), "dfs_nodes": nodes,
                           "augmenting_set": found}
        if found is not None:
            return False, checked
    return True, checked


def global_replace_step(adj, S, n, drop, rng, seconds=1.0, target=None):
    """Exact global-compatible residual solve after dropping `drop` incumbent points."""
    import numpy as np
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import coo_matrix

    S = set(S)
    removed = set(rng.sample(sorted(S), min(drop, len(S))))
    kept = S - removed
    forbidden = set()
    for v in kept:
        forbidden |= adj[v]
    cand = [v for v in range(n) if v not in kept and v not in forbidden]
    idx = {v: i for i, v in enumerate(cand)}
    edges = []
    for a in cand:
        ia = idx[a]
        for b in adj[a]:
            ib = idx.get(b)
            if ib is not None and ia < ib:
                edges.append((ia, ib))
    m = len(cand)
    rr, cc, vv = [], [], []
    for e, (i, j) in enumerate(edges):
        rr += [e, e]; cc += [i, j]; vv += [1.0, 1.0]
    A = coo_matrix((vv, (rr, cc)), shape=(len(edges), m))
    cons = [LinearConstraint(A, -np.inf, 1)]
    if target is None:
        objective = -np.ones(m)
    else:
        objective = np.zeros(m)
        need = target - len(kept)
        cons.append(LinearConstraint(np.ones((1, m)), need, np.inf))
    res = milp(c=objective, constraints=cons, integrality=np.ones(m), bounds=Bounds(0, 1),
               options={"time_limit": seconds, "mip_rel_gap": 0.0, "presolve": True})
    if res.x is None:
        return sorted(S), {"status": int(res.status), "candidates": m, "edges": len(edges)}
    chosen = {cand[i] for i, x in enumerate(res.x) if x > 0.5}
    new = sorted(kept | chosen)
    return new, {"status": int(res.status), "candidates": m, "edges": len(edges),
                 "kept": len(kept), "chosen": len(chosen)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--search", action="store_true")
    ap.add_argument("--trials", type=int, default=300)
    ap.add_argument("--seconds-per-trial", type=float, default=0.7)
    args = ap.parse_args()

    check_field()
    P, adj, B = build()
    assert len(P) == 820
    assert {len(x) for x in adj} == {90}

    w = json.loads(WITNESS.read_text(encoding="utf-8"))
    S = list(w["point_indices"])
    assert len(S) == 51 and len(set(S)) == 51
    assert [list(P[i]) for i in S] == w["points"]
    assert not verify_independent(adj, S)
    assert all(B(P[a], P[b]) != 0 for a, b in itertools.combinations(S, 2))

    outside, blockers, hist = blocker_data(adj, S, len(P))
    expected_hist = {1: 1, 2: 22, 3: 50, 4: 102, 5: 156,
                     6: 120, 7: 142, 8: 107, 9: 53, 10: 16}
    assert dict(sorted(hist.items())) == expected_hist
    assert hist.get(0, 0) == 0
    assert sum(j * c for j, c in hist.items()) == 51 * 90 == 4590
    assert sum((j * (j - 1) // 2) * c for j, c in hist.items()) == 1275 * 10 == 12750
    ones = [(v, tuple(blockers[v])) for v in outside if len(blockers[v]) == 1]
    assert ones == [(40, (80,))]

    stable, exchange = exchange_stable_through(adj, S, len(P), max_removed=7)
    assert stable

    search = {"attempted": False, "target": 52, "reached": False}
    if args.search:
        search["attempted"] = True
        rng = random.Random(20260818_7122)
        best = S[:]
        t0 = time.time()
        for it in range(args.trials):
            drop = rng.choice([18, 20, 22, 24, 26, 28, 30, 32, 34])
            new, meta = global_replace_step(adj, best, len(P), drop, rng,
                                            args.seconds_per_trial, target=52)
            if len(new) >= 52 and not verify_independent(adj, new):
                best = new
                search.update({"reached": True, "trial": it, "size": len(best),
                               "drop": drop, "meta": meta})
                break
        search["elapsed_seconds"] = round(time.time() - t0, 3)
        search["best_size"] = len(best)

    out = {
        "schema": "w33.pass7122_7129.q9_witness_global_lns.v1",
        "status": "PASS",
        "pass_7122_missing_witness_recovered": {
            "q": 9, "size": 51, "point_count": 820, "degree": 90,
            "witness_file": str(WITNESS.relative_to(ROOT)),
            "pairwise_collinearity_violations": 0,
            "claim": "alpha(W(3,9)) >= 51 now has a stored re-verifiable witness"
        },
        "pass_7123_blocker_moments": {
            "histogram": {str(k): v for k, v in sorted(hist.items())},
            "sum_b": 4590, "sum_choose_b_2": 12750,
            "identities": ["sum b = |S| k = 51*90", "sum C(b,2)=C(51,2) mu=1275*10"]
        },
        "pass_7124_maximality": {
            "zero_blockers": 0,
            "therefore_inclusion_maximal": True,
            "one_blockers": 1,
            "unique_one_for_one_exchange": {"remove": 80, "add": 40}
        },
        "pass_7125_exchange_rigidity": {
            "stable_through_removed_points": 7,
            "meaning": "no gain-one exchange removing <=7 incumbent points",
            "exact_search": exchange
        },
        "pass_7126_global_compatible_lns": {
            "difference_from_previous_region_lns": "replacement candidates range over every W(3,9) point compatible with the kept core, not only vertices inside the freed region",
            "private_recovery": "this neighbourhood independently rediscovered size 51 from a smaller incumbent before the witness was frozen",
            "search_52_this_run": search
        },
        "pass_7127_scope": {
            "lower_bound": 51, "published_upper_bound": 73,
            "not_proved": ["alpha(W(3,9)) = 51", "nonexistence of a 52-set", "the quadratic interpolation"],
            "novelty": "not claimed; literature search found published general bounds, not an exact q=9 classification"
        },
        "boundary": "Finite symplectic geometry/search certificate only. A 51 witness is proved; optimality is open."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
