#!/usr/bin/env python3
"""Local search to repair a perfect matching of edges->roots to satisfy triangle constraints.

Algorithm:
- Build perfect matching using Hopcroft-Karp on candidate lists.
- Compute number of triangle violations.
- Perform iterative local changes (reassign a single edge to an unused candidate, or swap two edges' roots) that reduce violation count.
- Use random restarts and a time budget.

Usage: python scripts/local_repair_matching.py --k 30 --time-limit 120 --seed-json checks/PART_CVII_e8_embedding_attempt_seed.json
"""
from __future__ import annotations

import argparse
import json
import random
import time
from collections import Counter, deque
from typing import List, Tuple

import numpy as np

# reuse candidate builder
try:
    # Prefer package-relative import when used as a module; fall back to
    # absolute import for direct script execution.
    from .check_triangle_coverage import (
        build_w33_graph,
        compute_embedding_matrix,
        generate_scaled_e8_roots,
    )
except Exception:  # pragma: no cover - fallback for direct script execution
    from scripts.check_triangle_coverage import (
        build_w33_graph,
        compute_embedding_matrix,
        generate_scaled_e8_roots,
    )


def hopcroft_karp(adj, n_left, n_right):
    pair_u = [-1] * n_left
    pair_v = [-1] * n_right
    dist = [0] * n_left
    INF = 10**9

    from collections import deque

    def bfs():
        queue = deque()
        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = INF
        found = False
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if pair_v[v] != -1 and dist[pair_v[v]] == INF:
                    dist[pair_v[v]] = dist[u] + 1
                    queue.append(pair_v[v])
                if pair_v[v] == -1:
                    found = True
        return found

    def dfs(u):
        for v in adj[u]:
            if pair_v[v] == -1 or (dist[pair_v[v]] == dist[u] + 1 and dfs(pair_v[v])):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = INF
        return False

    matching = 0
    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1 and dfs(u):
                matching += 1
    return matching, pair_u, pair_v


def build_candidates(k: int, seed_json: str = None):
    X, edges = compute_embedding_matrix()
    A_mat = np.vstack(
        [(X[i] - X[j]) / (np.linalg.norm(X[i] - X[j]) + 1e-12) for (i, j) in edges]
    )
    roots = generate_scaled_e8_roots()
    roots_arr = np.array(roots, dtype=int)
    roots_unit = roots_arr.astype(float) / np.linalg.norm(
        roots_arr.astype(float), axis=1, keepdims=True
    )
    cost = np.linalg.norm(A_mat[:, None, :] - roots_unit[None, :, :], axis=2)

    N_edges = len(A_mat)
    candidates: List[List[int]] = []
    for e in range(N_edges):
        idxs = np.argsort(cost[e])[:k]
        candidates.append([int(i) for i in idxs])

    seed_assign = {}
    if seed_json:
        try:
            s = json.load(open(seed_json))
            for sd in s.get("seed_edges", []):
                eidx = sd.get("edge_index")
                ridx = sd.get("root_index")
                if eidx is not None and ridx is not None:
                    seed_assign[int(eidx)] = int(ridx)
                    if ridx not in candidates[eidx]:
                        candidates[eidx].append(ridx)
        except Exception:
            pass
    return candidates, edges, roots, seed_assign


def triangles_from_edges(edges):
    n, vertices, adj, _ = build_w33_graph()
    tris = []
    edge_index = {edges[i]: i for i in range(len(edges))}
    edge_index.update({(j, i): idx for (i, j), idx in edge_index.items()})
    for a in range(n):
        for b in adj[a]:
            if b <= a:
                continue
            for c in adj[b]:
                if c <= b:
                    continue
                if a in adj[c]:
                    tri = tuple(sorted((a, b, c)))
                    e_ab = edge_index[(a, b)]
                    e_bc = edge_index[(b, c)]
                    e_ac = edge_index[(a, c)]
                    tris.append((e_ab, e_bc, e_ac))
    return tris


def count_violations(assign, tris, roots):
    cnt = 0
    bad = []
    for e1, e2, e3 in tris:
        r1 = roots[assign[e1]]
        r2 = roots[assign[e2]]
        r3 = roots[assign[e3]]
        # check r1 + r2 == r3
        ok = True
        for i in range(8):
            if r1[i] + r2[i] != r3[i]:
                ok = False
                break
        if not ok:
            cnt += 1
            bad.append((e1, e2, e3))
    return cnt, bad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=30)
    parser.add_argument("--time-limit", type=float, default=120)
    parser.add_argument("--seed-json", type=str, default=None)
    parser.add_argument("--tries", type=int, default=200000)
    parser.add_argument(
        "--post-tries",
        type=int,
        default=100000,
        help="additional tries to maximize consistent positions after reducing violations",
    )
    parser.add_argument(
        "--maximize-nodes",
        action="store_true",
        help="run post-optimization to maximize number of connected vertices in positions mapping",
    )
    args = parser.parse_args()

    candidates, edges, roots, seed_assign = build_candidates(
        args.k, seed_json=args.seed_json
    )
    print(
        f"Built candidates k={args.k} edges={len(edges)} roots={len(roots)} seed_edges={len(seed_assign)}"
    )

    # build bipartite adjacency for matching
    n_edges = len(candidates)
    n_roots = len(roots)
    adj = [list(set(candidates[e])) for e in range(n_edges)]

    match_size, pair_u, pair_v = hopcroft_karp(adj, n_edges, n_roots)
    print("Initial matching size:", match_size)
    if match_size < n_edges:
        print("No perfect matching available at this k; aborting")
        return

    # initial assignment from matching
    assign = [None] * n_edges
    for e in range(n_edges):
        if pair_u[e] != -1:
            assign[e] = pair_u[e]
        else:
            # fallback greedy
            for r in candidates[e]:
                if r not in pair_v or pair_v[r] == -1:
                    assign[e] = r
                    break

    # ensure uniqueness
    used = set(assign)
    if len(used) != n_edges:
        # if duplicates, do greedy unique assignment
        used = set()
        assign = [-1] * n_edges
        for e in range(n_edges):
            for r in candidates[e]:
                if r not in used:
                    assign[e] = r
                    used.add(r)
                    break

    tris = triangles_from_edges(edges)
    best_assign = list(assign)
    best_cnt, _ = count_violations(assign, tris, roots)
    print("Initial violations:", best_cnt)

    start = time.time()
    T = args.time_limit
    iters = 0

    while time.time() - start < T and iters < args.tries and best_cnt > 0:
        iters += 1
        # pick a triangle that is violated
        cnt, bad = count_violations(assign, tris, roots)
        if cnt == 0:
            best_cnt = 0
            best_assign = list(assign)
            break
        tri = random.choice(bad)
        # choose a random edge from the triangle to change
        e = random.choice(tri)
        cur_r = assign[e]
        # try alternative candidate for this edge not used
        choices = [r for r in candidates[e] if r != cur_r and r not in used]
        if not choices:
            # try random swap with another edge
            e2 = random.randrange(0, n_edges)
            if e2 == e:
                continue
            # swap if reduces violations
            assign[e], assign[e2] = assign[e2], assign[e]
            new_cnt, _ = count_violations(assign, tris, roots)
            if new_cnt <= best_cnt:
                best_cnt = new_cnt
                best_assign = list(assign)
            else:
                # revert
                assign[e], assign[e2] = assign[e2], assign[e]
            continue
        r_new = random.choice(choices)
        # evaluate delta only for triangles touching e
        affected_tris = [t for t in tris if e in t]
        prev = 0
        for t in affected_tris:
            r1 = roots[assign[t[0]]]
            r2 = roots[assign[t[1]]]
            r3 = roots[assign[t[2]]]
            if not (all(r1[i] + r2[i] == r3[i] for i in range(8))):
                prev += 1
        # temporarily apply
        assign[e] = r_new
        new = 0
        for t in affected_tris:
            r1 = roots[assign[t[0]]]
            r2 = roots[assign[t[1]]]
            r3 = roots[assign[t[2]]]
            if not (all(r1[i] + r2[i] == r3[i] for i in range(8))):
                new += 1
        if new <= prev:
            # accept
            used.remove(cur_r)
            used.add(r_new)
            total_cnt, _ = count_violations(assign, tris, roots)
            if total_cnt < best_cnt:
                best_cnt = total_cnt
                best_assign = list(assign)
                print(
                    f"Iter {iters} improved best_cnt to {best_cnt} time={time.time()-start:.2f}s"
                )
        else:
            # revert
            assign[e] = cur_r

    end = time.time()
    print(
        f"Finished local repair in {end-start:.2f}s iters={iters} best_cnt={best_cnt}"
    )

    # convert edge->root to vertex positions (pos) similar to backtrack output
    def assignment_to_positions_consistent(edges, assignment, roots):
        # BFS from vertex 0, only follow edges whose induced position doesn't conflict
        from collections import deque

        pos = {0: tuple([0] * 8)}
        # build adjacency set
        adj = [set() for _ in range(40)]
        for i, j in edges:
            adj[i].add(j)
            adj[j].add(i)

        edge_adj = {i: [] for i in range(40)}
        for ei, (i, j) in enumerate(edges):
            edge_adj[i].append((ei, j))
            edge_adj[j].append((ei, i))

        roots_set = set(tuple(r) for r in roots)

        q = deque([0])
        while q:
            u = q.popleft()
            for ei, v in edge_adj[u]:
                if ei not in assignment or assignment[ei] == -1:
                    continue
                r_idx = assignment[ei]
                rvec = roots[r_idx]
                # edge stored as (i,j) with i<j; orientation depends on endpoints
                i, j = edges[ei]
                if u == i:
                    candidate = tuple(p_u - r for p_u, r in zip(pos[u], rvec))
                else:
                    candidate = tuple(p_u + r for p_u, r in zip(pos[u], rvec))
                if v not in pos:
                    # ensure this candidate doesn't conflict with existing positions
                    conflict = False
                    for z, pz in pos.items():
                        if z == v:
                            continue
                        diff = tuple(a - b for a, b in zip(candidate, pz))
                        is_root = (
                            diff in roots_set or tuple(-d for d in diff) in roots_set
                        )
                        if z in adj[v]:
                            # if neighbors, diff must be a root
                            if not is_root:
                                conflict = True
                                break
                        else:
                            # if non-neighbors, diff must NOT be a root
                            if is_root:
                                conflict = True
                                break
                    if not conflict:
                        pos[v] = candidate
                        q.append(v)
        return pos

    # post-optimization: try to maximize number of vertices in positions mapping
    best_assign_post = list(best_assign)

    def compute_pos_nodes(assign_map):
        a_map = {i: r for i, r in enumerate(assign_map) if r != -1}
        pos = assignment_to_positions_consistent(edges, a_map, roots)
        return len(pos), pos

    # build edges list consistent with other scripts for use in compute_pos_nodes
    def build_w33_edges_internal():
        F = 3
        all_vectors = [
            (a, b, c, d)
            for a in range(F)
            for b in range(F)
            for c in range(F)
            for d in range(F)
            if (a, b, c, d) != (0, 0, 0, 0)
        ]

        def canonical_rep(v):
            for i in range(4):
                if v[i] % F != 0:
                    a = v[i] % F
                    inv = 1 if a == 1 else 2
                    return tuple(((x * inv) % F) for x in v)
            return None

        reps = set(canonical_rep(v) for v in all_vectors if canonical_rep(v))
        vertices = sorted(list(reps))

        def symp(x, y):
            return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

        n = len(vertices)
        edges_local = []
        for i in range(n):
            for j in range(i + 1, n):
                if symp(vertices[i], vertices[j]) == 0:
                    edges_local.append((i, j))
        return edges_local

    edges = build_w33_edges_internal()
    # compute initial nodes
    best_nodes, best_positions = compute_pos_nodes(best_assign_post)
    print(f"Initial BFS-consistent nodes from best assign: {best_nodes}")

    if args.maximize_nodes:
        post_tries = args.post_tries
        post_iters = 0
        while post_iters < post_tries:
            post_iters += 1
            # random modification: pick edge, try alternate candidate
            e = random.randrange(0, len(best_assign_post))
            cur = best_assign_post[e]
            choices = [r for r in candidates[e] if r != cur]
            if not choices:
                continue
            new_r = random.choice(choices)
            # apply
            old = best_assign_post[e]
            best_assign_post[e] = new_r
            nodes, pos = compute_pos_nodes(best_assign_post)
            # accept if nodes increased or equal with fewer violations
            assign_map = {i: r for i, r in enumerate(best_assign_post) if r != -1}
            total_cnt, _ = count_violations(best_assign_post, tris, roots)
            if nodes > best_nodes or (nodes == best_nodes and total_cnt < best_cnt):
                best_nodes = nodes
                best_positions = pos
                best_cnt = total_cnt
                print(
                    f"post iter {post_iters} improved nodes to {best_nodes} violations={best_cnt}"
                )
            else:
                # revert
                best_assign_post[e] = old

    # build edges list consistent with other scripts
    def build_w33_edges():
        F = 3
        all_vectors = [
            (a, b, c, d)
            for a in range(F)
            for b in range(F)
            for c in range(F)
            for d in range(F)
            if (a, b, c, d) != (0, 0, 0, 0)
        ]

        def canonical_rep(v):
            for i in range(4):
                if v[i] % F != 0:
                    a = v[i] % F
                    inv = 1 if a == 1 else 2
                    return tuple(((x * inv) % F) for x in v)
            return None

        reps = set(canonical_rep(v) for v in all_vectors if canonical_rep(v))
        vertices = sorted(list(reps))

        def symp(x, y):
            return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % F

        n = len(vertices)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if symp(vertices[i], vertices[j]) == 0:
                    edges.append((i, j))
        return edges

    # final output: prefer post-optimized assignment if available
    final_assign = best_assign_post if args.maximize_nodes else best_assign
    final_positions = (
        best_positions
        if args.maximize_nodes
        else assignment_to_positions_consistent(
            edges, {i: r for i, r in enumerate(best_assign) if r != -1}, roots
        )
    )

    out = {
        "best_violations": best_cnt,
        "time_seconds": end - start,
        "iters": iters,
        "edge_to_root": {str(i): int(r) for i, r in enumerate(final_assign)},
        "best_assignment_count": sum(1 for r in final_assign if r != -1),
        "best": {
            "pos": {str(k): list(v) for k, v in final_positions.items()},
            "max_assigned": sum(1 for r in final_assign if r != -1),
        },
        "best_assigned": sum(1 for r in final_assign if r != -1),
    }
    from utils.json_safe import dump_json

    dump_json(out, "checks/PART_CVII_e8_local_repair.json", indent=2)
    print("Wrote checks/PART_CVII_e8_local_repair.json (with positions & edge_to_root)")


if __name__ == "__main__":
    main()
