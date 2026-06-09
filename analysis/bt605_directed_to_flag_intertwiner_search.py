#!/usr/bin/env python3
"""BT605: directed-to-flag intertwiner search.

This constructs the canonical fold from the 480 directed collinearity edges of
W(3,3) to the 160 point-line Levi flags.

A directed W33 edge (p -> q) determines the unique GQ line ell(p,q), hence the
Levi flag (p, ell(p,q)).  This gives a 160 x 480 matrix T with column sum 1
and row sum 3.  The script then folds the directed Hashimoto operator B by
T B^n T^T and records exact transfer statistics on the Levi flag scheme.

The main discovery is that the first fold has total row sum 33 = 3(k-1), so the
Ihara nonbacktracking outdegree 11 appears after the 3-to-1 directed-edge/flag
fold.  The third fold has full support and already sees the protected distance-4
shell value 28 = mu on every opposite flag shell.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product
import json
from pathlib import Path

import numpy as np


def norm_vec(v: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
    v = tuple(x % 3 for x in v)
    if all(x == 0 for x in v):
        return None
    for x in v:
        if x != 0:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % 3 for y in v)
    raise AssertionError("unreachable")


def symp(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return (u[0] * v[2] - u[2] * v[0] + u[1] * v[3] - u[3] * v[1]) % 3


def build_w33():
    pts = sorted({norm_vec(v) for v in product(range(3), repeat=4) if any(v)})
    pt_index = {p: i for i, p in enumerate(pts)}
    edges = []
    for i, j in combinations(range(len(pts)), 2):
        if symp(pts[i], pts[j]) == 0:
            edges.append((i, j))

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
    return pts, edges, lines, edge_line


def all_pairs_shortest_paths(A: np.ndarray) -> list[list[int]]:
    n = A.shape[0]
    dist = [[999 for _ in range(n)] for __ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        frontier = [i]
        while frontier:
            u = frontier.pop(0)
            for v in np.nonzero(A[u])[0]:
                if dist[i][v] == 999:
                    dist[i][v] = dist[i][u] + 1
                    frontier.append(v)
    return dist


def main() -> int:
    pts, edges, lines, edge_line = build_w33()
    flags = []
    flag_index = {}
    for li, line in enumerate(lines):
        for p in line:
            flag_index[(p, li)] = len(flags)
            flags.append((p, li))

    directed = []
    for i, j in edges:
        li = edge_line[tuple(sorted((i, j)))]
        directed.append((i, j, li))
        directed.append((j, i, li))
    directed_index = {(i, j): idx for idx, (i, j, _li) in enumerate(directed)}

    T = np.zeros((len(flags), len(directed)), dtype=int)
    for de, (tail, _head, li) in enumerate(directed):
        T[flag_index[(tail, li)], de] = 1

    B = np.zeros((len(directed), len(directed)), dtype=int)
    for a, (u, v, _li) in enumerate(directed):
        for w in range(len(pts)):
            if w == u:
                continue
            if tuple(sorted((v, w))) in edge_line:
                B[a, directed_index[(v, w)]] = 1

    # Levi flag graph X=L(E(L)): flags adjacent when they share point or line.
    A_flag = np.zeros((len(flags), len(flags)), dtype=int)
    for i, (p, l) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i != j and (p == q or l == m):
                A_flag[i, j] = 1
    dist = all_pairs_shortest_paths(A_flag)

    folded = {}
    for power in range(1, 5):
        M = T @ np.linalg.matrix_power(B, power) @ T.T
        by_distance = {}
        for d in range(5):
            vals = []
            for i in range(len(flags)):
                for j in range(len(flags)):
                    if dist[i][j] == d:
                        vals.append(int(M[i, j]))
            by_distance[str(d)] = {str(k): v for k, v in sorted(Counter(vals).items())}
        folded[str(power)] = {
            "row_sum": int(M.sum(axis=1)[0]),
            "global_values": {str(k): v for k, v in sorted(Counter(map(int, M.flatten())).items())},
            "by_flag_distance": by_distance,
        }

    checks = {
        "points_40": len(pts) == 40,
        "collinearity_edges_240": len(edges) == 240,
        "lines_40": len(lines) == 40,
        "flags_160": len(flags) == 160,
        "directed_edges_480": len(directed) == 480,
        "T_row_sum_3": set(map(int, T.sum(axis=1))) == {3},
        "T_col_sum_1": set(map(int, T.sum(axis=0))) == {1},
        "hashimoto_outdegree_11": set(map(int, B.sum(axis=1))) == {11},
        "flag_graph_degree_6": set(map(int, A_flag.sum(axis=1))) == {6},
        "first_fold_row_sum_33": folded["1"]["row_sum"] == 33,
        "third_fold_distance4_is_28": folded["3"]["by_flag_distance"]["4"] == {"28": 12960},
    }

    result = {
        "bt": 605,
        "title": "Directed-to-flag intertwiner search",
        "canonical_fold": "directed edge (p -> q) maps to Levi flag (p, ell(p,q))",
        "dimensions": {
            "w33_points": len(pts),
            "w33_edges": len(edges),
            "gq_lines": len(lines),
            "levi_flags": len(flags),
            "directed_edges": len(directed),
        },
        "fold_matrix": {
            "shape": [int(x) for x in T.shape],
            "row_sum": 3,
            "column_sum": 1,
            "TTt": "3I_160",
        },
        "hashimoto": {
            "shape": [int(x) for x in B.shape],
            "outdegree": 11,
            "first_fold_row_sum": folded["1"]["row_sum"],
            "interpretation": "T B T^T has row sum 33 = 3*(k-1), exposing the Ihara outdegree after the 3-to-1 directed-edge/flag fold.",
        },
        "folded_powers": folded,
        "interpretation": "The map T is the natural candidate directed-edge to Levi-flag intertwiner. It is not a perfect adjacency intertwiner, but it is an exact finite transfer: T T^T=3I, B has outdegree 11, TBT^T has row sum 33, and T B^3 T^T reaches the distance-4 protected shell uniformly with value 28=mu.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    Path("data/PART_BT605_DIRECTED_TO_FLAG_INTERTWINER_SEARCH_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
