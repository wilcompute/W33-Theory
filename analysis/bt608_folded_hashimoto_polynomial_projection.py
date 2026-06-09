#!/usr/bin/env python3
"""BT608: folded Hashimoto polynomial projection.

BT605 constructed the canonical fold

    T : directed W33 edge (p -> q) |-> Levi flag (p, ell(p,q)).

BT608 studies the folded powers

    F_n = T B^n T^T

against the 4-class Levi flag association scheme.  The honest result is not
that every F_n is already radial.  Rather:

  * F_n has constant row sum 3*11^n;
  * the Bose-Mesner/radial projection is obtained by averaging over flag
    distance shells A_0,...,A_4;
  * the terminal distance-4 shell is exact/uniform for n=2,3,4,5;
  * in particular F_3 has value 28=mu on every distance-4 ordered flag pair.

This separates the exact endpoint theorem from the lower-shell orientation
splitting.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
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


def flag_distances(flags):
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


def frac_avg(values: np.ndarray) -> str:
    return str(Fraction(int(values.sum()), int(values.size)))


def main() -> int:
    pts, edges, adj, lines, edge_line, flags, flag_index, directed, directed_index = build_geometry()
    T = np.zeros((len(flags), len(directed)), dtype=int)
    for de, (tail, _head, li) in enumerate(directed):
        T[flag_index[(tail, li)], de] = 1

    B = np.zeros((len(directed), len(directed)), dtype=int)
    for a, (u, v, _li) in enumerate(directed):
        for w in adj[v]:
            if w != u:
                B[a, directed_index[(v, w)]] = 1

    A_flag, dist = flag_distances(flags)
    shell_sizes = {str(d): int((dist == d).sum()) for d in range(5)}
    folded = {}
    for n in range(1, 6):
        M = T @ np.linalg.matrix_power(B, n) @ T.T
        radial_projection = {}
        exact_radial_by_shell = {}
        value_splits = {}
        max_abs_residual = 0
        for d in range(5):
            mask = dist == d
            vals = M[mask].astype(int)
            avg = Fraction(int(vals.sum()), int(vals.size))
            radial_projection[str(d)] = str(avg)
            counter = Counter(map(int, vals))
            value_splits[str(d)] = {str(k): v for k, v in sorted(counter.items())}
            exact_radial_by_shell[str(d)] = len(counter) == 1
            for val in vals:
                residual = abs(Fraction(int(val), 1) - avg)
                if residual > max_abs_residual:
                    max_abs_residual = residual
        folded[str(n)] = {
            "row_sum": int(M.sum(axis=1)[0]),
            "radial_projection_coefficients_on_A0_to_A4": radial_projection,
            "exact_radial_by_distance_shell": exact_radial_by_shell,
            "value_splits_by_distance_shell": value_splits,
            "max_abs_residual_from_radial_projection": str(max_abs_residual),
        }

    checks = {
        "fold_shape_160_by_480": list(T.shape) == [160, 480],
        "TTt_is_3I": np.array_equal(T @ T.T, 3 * np.eye(160, dtype=int)),
        "hashimoto_outdegree_11": set(map(int, B.sum(axis=1))) == {11},
        "flag_scheme_shell_sizes": shell_sizes == {"0": 160, "1": 960, "2": 2880, "3": 8640, "4": 12960},
        "folded_row_sums_are_3_times_11_power_n": all(folded[str(n)]["row_sum"] == 3 * (11 ** n) for n in range(1, 6)),
        "F3_distance4_is_exact_mu_28": folded["3"]["value_splits_by_distance_shell"]["4"] == {"28": 12960},
        "distance4_exact_for_n_2_through_5": all(folded[str(n)]["exact_radial_by_distance_shell"]["4"] for n in range(2, 6)),
        "lower_shells_not_all_radial": not all(folded["3"]["exact_radial_by_distance_shell"].values()),
    }

    result = {
        "bt": 608,
        "title": "Folded Hashimoto polynomial projection",
        "dimensions": {
            "points": len(pts),
            "w33_edges": len(edges),
            "lines": len(lines),
            "flags": len(flags),
            "directed_edges": len(directed),
        },
        "shell_sizes_ordered_pairs": shell_sizes,
        "folded_hashimoto_powers": folded,
        "interpretation": "The folded powers F_n=T B^n T^T have exact row sums 3*11^n and a canonical Bose-Mesner radial projection by distance shells. They are not fully radial on lower shells, but the terminal distance-4 shell is exact for n=2..5; at n=3 it is uniformly 28=mu.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    Path("data/PART_BT608_FOLDED_HASHIMOTO_POLYNOMIAL_PROJECTION_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
