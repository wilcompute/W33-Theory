#!/usr/bin/env python3
"""Local-search (hillclimb / simulated annealing) for improving W33->E8 bijection.

Strategy:
- Start from the canonical mapping in artifacts/explicit_bijection_decomposition.json
- Permute root assignments *within dot-pair classes* (i.e., swap two roots belonging to the same class)
  to preserve high-level decomposition counts.
- Score function: sum over adjacent edge pairs of abs(inner_product(root_a, root_b)). Maximize this score.

This is experimental: fast, pure-Python, and designed to run in CI with small iteration limits.
"""

from __future__ import annotations

import json
import math
import random
import time
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load_artifact(path: Path | None = None) -> Dict:
    if path is None:
        path = ROOT / "artifacts" / "explicit_bijection_decomposition.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_adjacency_list() -> Tuple[list, list]:
    # Reconstruct W33 edges and adjacency (share a vertex)
    from itertools import product

    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    n = len(edges)
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        a, b = edges[i]
        for j in range(i + 1, n):
            c, d = edges[j]
            if a == c or a == d or b == c or b == d:
                adj[i][j] = adj[j][i] = True
    return edges, adj


def dot_matrix(roots: list) -> np.ndarray:
    R = np.array(roots, dtype=int)
    return R @ R.T


def initial_score(
    mapping: list,
    adj: list,
    dotm: np.ndarray,
    triangles: list | None = None,
    triangle_weight: int = 0,
) -> int:
    n = len(mapping)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i][j]:
                total += abs(int(dotm[mapping[i], mapping[j]]))

    if triangle_weight and triangles:
        # reward A2 triangles where pairwise dot == -2
        tri_count = 0
        for a, b, c in triangles:
            if (
                int(dotm[mapping[a], mapping[b]]) == -2
                and int(dotm[mapping[a], mapping[c]]) == -2
                and int(dotm[mapping[b], mapping[c]]) == -2
            ):
                tri_count += 1
        total += triangle_weight * tri_count
    return total


def class_keys_for_roots(roots: list) -> Dict[Tuple[int, int], list]:
    u1 = (1, 1, 1, 1, 1, 1, 1, 1)
    u2 = (1, 1, 1, 1, 1, 1, -1, -1)
    classes = {}
    for i, r in enumerate(roots):
        d = (
            sum(int(r[j]) * u1[j] for j in range(8)),
            sum(int(r[j]) * u2[j] for j in range(8)),
        )
        classes.setdefault(d, []).append(i)
    return classes


def local_search(
    iterations: int = 20000,
    seed: int | None = None,
    time_limit: float | None = 10.0,
    triangle_weight: int = 0,
) -> Dict:
    data = load_artifact()
    mapping_dict = {int(k): v for k, v in data["edge_to_root_index"].items()}
    n = len(mapping_dict)
    mapping = [mapping_dict[i] for i in range(n)]
    roots = data["root_coords"]

    edges, adj = build_adjacency_list()
    dotm = dot_matrix(roots)

    classes = class_keys_for_roots(roots)
    root_to_class = {ri: k for k, vs in classes.items() for ri in vs}

    # Precompute adjacency lists for each edge
    adj_list = [[j for j in range(n) if adj[i][j]] for i in range(n)]

    # Precompute triangles (fully connected triples in the edge-adjacency graph)
    triangles = []
    for a in range(n):
        for b in range(a + 1, n):
            if not adj[a][b]:
                continue
            for c in range(b + 1, n):
                if adj[a][c] and adj[b][c]:
                    triangles.append((a, b, c))
    tri_per_edge = {i: [] for i in range(n)}
    for ti, (a, b, c) in enumerate(triangles):
        tri_per_edge[a].append(ti)
        tri_per_edge[b].append(ti)
        tri_per_edge[c].append(ti)

    baseline = initial_score(mapping, adj, dotm, triangles, 0)
    best = baseline
    best_mapping = mapping.copy()

    rng = random.Random(seed)
    start = time.time()
    T0 = 1.0
    for it in range(iterations):
        if time_limit is not None and (time.time() - start) > time_limit:
            break
        # pick two edges uniformly
        i, j = rng.randrange(n), rng.randrange(n)
        if i == j:
            continue
        ri, rj = mapping[i], mapping[j]
        # only swap roots that are in same class to preserve class distribution
        if root_to_class[ri] != root_to_class[rj]:
            continue

        # compute delta quickly: pairs involving i and j (adjacency contribution)
        delta = 0
        for k in adj_list[i]:
            if k == j:
                continue
            old = abs(int(dotm[ri, mapping[k]]))
            new = abs(int(dotm[rj, mapping[k]]))
            delta += new - old
        for k in adj_list[j]:
            if k == i:
                continue
            old = abs(int(dotm[rj, mapping[k]]))
            new = abs(int(dotm[ri, mapping[k]]))
            delta += new - old
        # include pair (i,j)
        if adj[i][j]:
            old = abs(int(dotm[ri, rj]))
            new = abs(int(dotm[rj, ri]))
            delta += new - old

        # triangle contribution: only triangles that include i or j are affected
        if triangle_weight and triangles:
            tri_delta = 0
            affected = set(tri_per_edge[i]) | set(tri_per_edge[j])
            for ti in affected:
                a, b, c = triangles[ti]
                # old membership
                old_a, old_b, old_c = mapping[a], mapping[b], mapping[c]
                old_ok = (
                    int(dotm[old_a, old_b]) == -2
                    and int(dotm[old_a, old_c]) == -2
                    and int(dotm[old_b, old_c]) == -2
                )

                # compute new roots after swap
                def root_after_swap(idx):
                    if idx == i:
                        return rj
                    if idx == j:
                        return ri
                    return mapping[idx]

                na, nb, nc = root_after_swap(a), root_after_swap(b), root_after_swap(c)
                new_ok = (
                    int(dotm[na, nb]) == -2
                    and int(dotm[na, nc]) == -2
                    and int(dotm[nb, nc]) == -2
                )
                tri_delta += (1 if new_ok else 0) - (1 if old_ok else 0)
            delta += triangle_weight * tri_delta

        # temperature schedule
        t = T0 * (1.0 - (it / float(iterations)))
        accept = False
        if delta > 0:
            accept = True
        else:
            if rng.random() < math.exp(delta / max(t, 1e-12)):
                accept = True
        if accept:
            mapping[i], mapping[j] = rj, ri
            baseline += delta
            if baseline > best:
                best = baseline
                best_mapping = mapping.copy()

    result = {
        "iterations": it + 1,
        "time_seconds": time.time() - start,
        "triangle_weight": triangle_weight,
        "baseline_score": initial_score(
            [mapping_dict[i] for i in range(n)], adj, dotm, triangles, triangle_weight
        ),
        "best_score": best,
        "mapping": best_mapping,
    }
    out = ROOT / "artifacts" / "equivariant_search_result.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Wrote", out)
    print(result)
    return result


if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("--iterations", type=int, default=20000)
    p.add_argument("--time-limit", type=float, default=10.0)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--triangle-weight", type=int, default=0)
    args = p.parse_args()
    local_search(
        iterations=args.iterations,
        seed=args.seed,
        time_limit=args.time_limit,
        triangle_weight=args.triangle_weight,
    )
