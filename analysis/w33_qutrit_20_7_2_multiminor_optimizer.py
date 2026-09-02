#!/usr/bin/env python3
"""Exact support/locality tournament across several rank-preserving minors.

The one-minor CP-SAT certificate proves exact support optimality only after one
20-column invertible minor of A is frozen.  This module deliberately broadens
that search without overstating it:

* construct several deterministic, genuinely distinct rank-20 minors of the
  original A;
* for each candidate minor, keep its 20 columns fixed so rank(A)=20 is a hard
  invariant;
* optimize every other A column lexicographically: minimum Hamming support,
  then minimum W33 line-graph distance to row anchors among support minima;
* for that A, optimize each B row lexicographically under A b_i^T=e_i;
* compare the exact per-class optima by total A+B support, anchor-locality,
  maximum row radius, and line-graph spanning-tree cost.

The resulting winner is exact inside every displayed fixed-minor class and is
best among the finite deterministic candidate set.  It is NOT a proof of the
global optimum over all C(240,20) possible minors, nor is line-graph compactness
an optical/noise threshold theorem.
"""
from __future__ import annotations

from collections import deque
from functools import lru_cache
import hashlib
import json
import random

import numpy as np
from ortools.sat.python import cp_model

import w33_qutrit_20_7_2_symplectic_embedding as base
import w33_qutrit_20_7_2_sparse_symplectic as sparse

DEFAULT_CANDIDATES = 3


def matrix_hash(a):
    return "sha256:" + hashlib.sha256(bytes(int(x) for x in np.asarray(a).flatten())).hexdigest()


def edge_graph(hx):
    endpoints = sparse.edge_endpoints(hx)
    incident = [[] for _ in range(hx.shape[0])]
    for e, (u, v) in enumerate(endpoints):
        incident[u].append(e)
        incident[v].append(e)
    adj = [set() for _ in range(len(endpoints))]
    for es in incident:
        for e in es:
            adj[e].update(x for x in es if x != e)
    adj = [tuple(sorted(x)) for x in adj]
    return endpoints, adj


def all_pairs_edge_dist(adj):
    n = len(adj)
    out = np.full((n, n), 255, dtype=np.uint8)
    for s in range(n):
        out[s, s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            nd = int(out[s, u]) + 1
            for v in adj[u]:
                if int(out[s, v]) == 255:
                    out[s, v] = nd
                    q.append(v)
    if np.any(out == 255):
        raise RuntimeError("W33 edge line graph is disconnected")
    return out


def greedy_minor(A, order):
    chosen = []
    r = 0
    for j in order:
        cand = chosen + [int(j)]
        nr = base.rank(A[:, cand])
        if nr > r:
            chosen = cand
            r = nr
        if r == A.shape[0]:
            break
    if r != A.shape[0]:
        raise RuntimeError("candidate order failed to expose a rank-20 minor")
    return tuple(chosen)


def candidate_minors(A0, count=DEFAULT_CANDIDATES):
    n = A0.shape[1]
    weights = [int(np.count_nonzero(A0[:, j])) for j in range(n)]
    orders = [
        list(range(n)),
        list(reversed(range(n))),
        sorted(range(n), key=lambda j: (weights[j], j)),
        sorted(range(n), key=lambda j: (-weights[j], j)),
    ]
    for seed in range(1, 40):
        order = list(range(n))
        random.Random(seed).shuffle(order)
        orders.append(order)
    out = []
    seen = set()
    for order in orders:
        minor = greedy_minor(A0, order)
        key = tuple(sorted(minor))
        if key not in seen:
            seen.add(key)
            out.append(minor)
        if len(out) >= count:
            break
    if len(out) < min(count, 2):
        raise RuntimeError("failed to construct alternative rank-20 minors")
    return out


def _build_mod3_model(M, target, tag, support_target=None, locality_costs=None):
    M = np.asarray(M, dtype=np.int64) % 3
    target = np.asarray(target, dtype=np.int64) % 3
    rows, cols = M.shape
    model = cp_model.CpModel()
    x = [model.NewIntVar(0, 2, f"{tag}_x_{i}") for i in range(cols)]
    nz = [model.NewBoolVar(f"{tag}_nz_{i}") for i in range(cols)]
    for i in range(cols):
        model.Add(x[i] == 0).OnlyEnforceIf(nz[i].Not())
        model.Add(x[i] >= 1).OnlyEnforceIf(nz[i])
    for r in range(rows):
        max_sum = int(sum(int(M[r, i]) * 2 for i in range(cols)))
        k = model.NewIntVar(-1, max_sum // 3 + 1, f"{tag}_k_{r}")
        model.Add(sum(int(M[r, i]) * x[i] for i in range(cols)) - 3 * k == int(target[r]))
    if support_target is not None:
        model.Add(sum(nz) == int(support_target))
    if locality_costs is None:
        model.Minimize(sum(nz))
    else:
        if len(locality_costs) != cols:
            raise ValueError("locality cost length mismatch")
        model.Minimize(sum(int(locality_costs[i]) * nz[i] for i in range(cols)))
    return model, x, nz


def _solve(model, x, target_status=cp_model.OPTIMAL):
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.cp_model_presolve = True
    status = solver.Solve(model)
    if status != target_status:
        raise RuntimeError(f"CP-SAT exact optimum not certified: {solver.StatusName(status)}")
    v = np.array([solver.Value(q) for q in x], dtype=np.int64) % 3
    return v, int(round(solver.ObjectiveValue())), int(solver.NumBranches())


def solve_lex_mod3(M, target, costs, tag):
    m1, x1, _ = _build_mod3_model(M, target, tag + "_support")
    v1, support, branches1 = _solve(m1, x1)
    m2, x2, _ = _build_mod3_model(
        M, target, tag + "_local", support_target=support, locality_costs=costs
    )
    v2, locality, branches2 = _solve(m2, x2)
    if int(np.count_nonzero(v2)) != support:
        raise RuntimeError("lexicographic support optimum changed in locality stage")
    if not np.array_equal((np.asarray(M, dtype=np.int64) @ v2) % 3, np.asarray(target, dtype=np.int64) % 3):
        raise RuntimeError("lexicographic witness violates GF(3) equations")
    return v2, support, locality, branches1 + branches2


def row_anchor(A0, fixed, row, dist):
    support = [j for j in fixed if int(A0[row, j]) % 3]
    if not support:
        raise RuntimeError("invertible fixed minor unexpectedly has an empty row")
    return min(support, key=lambda j: (sum(int(dist[j, k]) for k in support), j))


def mst_cost(support, dist):
    support = list(support)
    if len(support) <= 1:
        return 0
    used = {support[0]}
    left = set(support[1:])
    total = 0
    while left:
        w, v = min((int(dist[u, v]), v) for u in used for v in left)
        total += w
        used.add(v)
        left.remove(v)
    return int(total)


def candidate_optimum(hx, h, T, A0, fixed, dist, label):
    A = A0.copy() % 3
    fixed_set = set(fixed)
    anchors = [row_anchor(A0, fixed, r, dist) for r in range(20)]
    a_records = []
    for j in range(240):
        if j in fixed_set:
            a_records.append({"column": j, "fixed": True, "support": int(np.count_nonzero(A[:, j])), "locality": 0, "branches": 0})
            continue
        costs = [int(dist[anchors[r], j]) for r in range(20)]
        col, support, locality, branches = solve_lex_mod3(h, T[:, j], costs, f"{label}_A{j}")
        A[:, j] = col
        a_records.append({"column": j, "fixed": False, "support": support, "locality": locality, "branches": branches})
    if base.rank(A[:, list(fixed)]) != 20 or base.rank(A) != 20:
        raise RuntimeError("rank guarantee failed")
    if not np.array_equal((h @ A) % 3, T):
        raise RuntimeError("optimized A violates H A = T")

    B_rows = []
    b_records = []
    eye = np.eye(20, dtype=np.int64)
    for i in range(20):
        costs = [int(dist[anchors[i], j]) for j in range(240)]
        row, support, locality, branches = solve_lex_mod3(A, eye[:, i], costs, f"{label}_B{i}")
        B_rows.append(row)
        b_records.append({"row": i, "support": support, "locality": locality, "branches": branches})
    B = np.array(B_rows, dtype=np.int64) % 3
    if not np.array_equal((A @ B.T) % 3, eye):
        raise RuntimeError("optimized B lost A B^T = I")

    a_support = int(np.count_nonzero(A))
    b_support = int(np.count_nonzero(B))
    a_locality = sum(int(dist[anchors[r], j]) for r in range(20) for j in range(240) if int(A[r, j]) % 3)
    b_locality = sum(int(dist[anchors[r], j]) for r in range(20) for j in range(240) if int(B[r, j]) % 3)
    radii = []
    tree_cost = 0
    for M in (A, B):
        for r in range(20):
            supp = [j for j in range(240) if int(M[r, j]) % 3]
            radii.append(max((int(dist[anchors[r], j]) for j in supp), default=0))
            tree_cost += mst_cost(supp, dist)
    score = (a_support + b_support, a_locality + b_locality, max(radii), tree_cost)
    return {
        "label": label,
        "fixed_minor": list(map(int, fixed)),
        "anchors": list(map(int, anchors)),
        "A": A,
        "B": B,
        "a_records": a_records,
        "b_records": b_records,
        "metrics": {
            "A_support": a_support,
            "B_support": b_support,
            "total_support": a_support + b_support,
            "A_anchor_locality": int(a_locality),
            "B_anchor_locality": int(b_locality),
            "total_anchor_locality": int(a_locality + b_locality),
            "max_row_radius": int(max(radii)),
            "line_graph_tree_cost": int(tree_cost),
            "score": list(map(int, score)),
        },
    }


@lru_cache(maxsize=None)
def selected_witness(candidate_count=DEFAULT_CANDIDATES):
    hx, hz, h, T, A0 = sparse.build_base()
    _, adj = edge_graph(hx)
    dist = all_pairs_edge_dist(adj)
    minors = candidate_minors(A0, int(candidate_count))
    candidates = [candidate_optimum(hx, h, T, A0, minor, dist, f"M{i}") for i, minor in enumerate(minors)]
    winner = min(candidates, key=lambda c: (tuple(c["metrics"]["score"]), tuple(sorted(c["fixed_minor"]))))
    return hx, hz, h, T, A0, dist, candidates, winner


def verify(candidate_count=DEFAULT_CANDIDATES):
    hx, hz, h, T, A0, dist, candidates, winner = selected_witness(int(candidate_count))
    summaries = []
    for c in candidates:
        A, B = c["A"], c["B"]
        summaries.append({
            "label": c["label"],
            "fixed_minor_columns_0_indexed": c["fixed_minor"],
            "anchors_0_indexed": c["anchors"],
            "A_sha256": matrix_hash(A),
            "B_sha256": matrix_hash(B),
            **c["metrics"],
            "free_A_columns_exact": int(sum(not r["fixed"] for r in c["a_records"])),
            "B_rows_exact": int(len(c["b_records"])),
        })
    A, B = winner["A"], winner["B"]
    scores = [tuple(c["metrics"]["score"]) for c in candidates]
    checks = {
        "at_least_two_distinct_rank_minors": len(candidates) >= 2 and len({tuple(sorted(c["fixed_minor"])) for c in candidates}) == len(candidates),
        "all_candidates_rank_20": all(base.rank(c["A"]) == 20 for c in candidates),
        "all_candidates_preserve_HA": all(np.array_equal((h @ c["A"]) % 3, T) for c in candidates),
        "all_candidates_preserve_symplectic_duality": all(np.array_equal((c["A"] @ c["B"].T) % 3, np.eye(20, dtype=np.int64)) for c in candidates),
        "winner_is_best_reported_score": tuple(winner["metrics"]["score"]) == min(scores),
        "line_graph_connected": int(dist.max()) < 255,
    }
    checks = {k: bool(v) for k, v in checks.items()}
    return {
        "schema": "w33.qutrit-20-7-2-multiminor-locality-optimizer.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "candidate_count": len(candidates),
        "line_graph_diameter": int(dist.max()),
        "candidates": summaries,
        "winner": {
            "label": winner["label"],
            "fixed_minor_columns_0_indexed": winner["fixed_minor"],
            "anchors_0_indexed": winner["anchors"],
            "A_sha256": matrix_hash(A),
            "B_sha256": matrix_hash(B),
            **winner["metrics"],
        },
        "theorem": "For every displayed fixed rank-20 minor, each free A column is exact minimum-support and then exact minimum anchor-distance among support minima; each B row is optimized by the same lexicographic rule. The displayed winner is best under the stated finite cross-minor score.",
        "boundary": "This finite tournament does not enumerate all rank-20 minors. Anchor distance and line-graph tree cost are exact combinatorial locality metrics on the W33 edge-interaction graph, not calibrated optical depth or a fault-tolerance threshold.",
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
