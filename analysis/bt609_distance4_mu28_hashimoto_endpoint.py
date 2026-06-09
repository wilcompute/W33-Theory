#!/usr/bin/env python3
"""BT609: distance-4 mu=28 Hashimoto endpoint theorem.

BT605 found that the canonical directed-edge/flag fold satisfies

    (T B^3 T^T)_{fg} = 28

for every ordered pair of Levi flags f,g at distance 4 in the Levi flag line
scheme.  BT609 isolates this as its own endpoint theorem and records the exact
support law.

The distance-4 shell has 12960 ordered pairs, exactly the same count as the
minimal logical support incidence count 160*81 = 1620*8.  The folded cubic
Hashimoto transfer contributes 28 to each such ordered pair, giving endpoint
mass 12960*28.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np


def norm_vec(v: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    v = tuple(x % 3 for x in v)
    if all(x == 0 for x in v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in v)
    raise AssertionError("unreachable")


def symp(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def build_geometry():
    pts = sorted({norm_vec(v) for v in product(range(3), repeat=4) if any(v)})
    pt_index = {p: i for i, p in enumerate(pts)}
    edges = [(i, j) for i, j in combinations(range(len(pts)), 2) if symp(pts[i], pts[j]) == 0]
    adj = [set() for _ in pts]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    lines = set()
    for i, j in edges:
        u, v = pts[i], pts[j]
        line = set()
        for a, b in product(range(3), repeat=2):
            if a == 0 and b == 0:
                continue
            w = norm_vec(tuple((a * u[t] + b * v[t]) % 3 for t in range(4)))
            line.add(pt_index[w])
        lines.add(tuple(sorted(line)))
    lines = sorted(lines)
    edge_line = {}
    for li, line in enumerate(lines):
        for a, b in combinations(line, 2):
            edge_line[tuple(sorted((a, b)))] = li

    flags = []
    flag_index = {}
    for li, line in enumerate(lines):
        for p in line:
            flag_index[(p, li)] = len(flags)
            flags.append((p, li))

    directed = []
    for i, j in edges:
        li = edge_line[(i, j)]
        directed.append((i, j, li))
        directed.append((j, i, li))
    directed_index = {(i, j): idx for idx, (i, j, _li) in enumerate(directed)}
    return pts, edges, adj, lines, edge_line, flags, flag_index, directed, directed_index


def flag_distance_matrix(flags):
    n = len(flags)
    A = np.zeros((n, n), dtype=int)
    for i, (p, l) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i != j and (p == q or l == m):
                A[i, j] = 1
    dist = np.full((n, n), 99, dtype=int)
    for s in range(n):
        dist[s, s] = 0
        queue = [s]
        for u in queue:
            for v in np.nonzero(A[u])[0]:
                if dist[s, v] == 99:
                    dist[s, v] = dist[s, u] + 1
                    queue.append(v)
    return A, dist


def main() -> int:
    pts, edges, adj, lines, edge_line, flags, flag_index, directed, directed_index = build_geometry()
    T = np.zeros((160, 480), dtype=int)
    for de, (tail, _head, li) in enumerate(directed):
        T[flag_index[(tail, li)], de] = 1

    B = np.zeros((480, 480), dtype=int)
    for a, (u, v, _li) in enumerate(directed):
        for w in adj[v]:
            if w != u:
                B[a, directed_index[(v, w)]] = 1

    _A_flag, dist = flag_distance_matrix(flags)
    F3 = T @ np.linalg.matrix_power(B, 3) @ T.T
    endpoint_values = Counter(map(int, F3[dist == 4]))
    shell_profiles = {str(d): {str(k): v for k, v in sorted(Counter(map(int, F3[dist == d])).items())} for d in range(5)}
    distance4_count = int((dist == 4).sum())
    endpoint_mass = int(F3[dist == 4].sum())
    mu = 40 - 12

    # Geometric flags at distance 4 are the terminal/opposite flags in the Levi line graph.
    per_flag_distance4 = sorted(set(int(np.sum(dist[i] == 4)) for i in range(160)))
    per_flag_endpoint_mass = sorted(set(int(F3[i][dist[i] == 4].sum()) for i in range(160)))

    checks = {
        "distance4_ordered_pairs_12960": distance4_count == 12960,
        "distance4_per_flag_81": per_flag_distance4 == [81],
        "endpoint_value_is_uniform_28": endpoint_values == Counter({28: 12960}),
        "mu_is_28": mu == 28,
        "endpoint_mass_is_12960_times_28": endpoint_mass == 12960 * 28,
        "per_flag_endpoint_mass_is_81_times_28": per_flag_endpoint_mass == [81 * 28],
        "folded_cubic_row_sum_is_3993": sorted(set(map(int, F3.sum(axis=1)))) == [3993],
        "3993_equals_3_times_11_cubed": 3993 == 3 * 11**3,
    }

    result = {
        "bt": 609,
        "title": "Distance-4 mu=28 Hashimoto endpoint theorem",
        "operator": "F3 = T B^3 T^T",
        "distance4_shell": {
            "ordered_pairs": distance4_count,
            "per_flag_size": per_flag_distance4[0],
            "uniform_value": 28,
            "endpoint_mass": endpoint_mass,
            "per_flag_endpoint_mass": per_flag_endpoint_mass[0],
        },
        "mu_identity": "28 = v-k = 40-12",
        "minimal_logical_count_identity": "12960 = 160*81 = 1620*8",
        "all_distance_shell_value_profiles_for_F3": shell_profiles,
        "interpretation": "The third folded Hashimoto transfer has a uniform terminal shell: every opposite Levi flag pair receives exactly mu=28 nonbacktracking folded walks. This is the endpoint certificate linking Hashimoto propagation to the protected distance-4/H1 shell.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    Path("data/PART_BT609_DISTANCE4_MU28_HASHIMOTO_ENDPOINT_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
