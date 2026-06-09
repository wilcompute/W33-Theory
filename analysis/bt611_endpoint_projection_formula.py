#!/usr/bin/env python3
"""BT611: endpoint projection formula.

This refines BT608--BT609 by writing the folded cubic Hashimoto transfer

    F3 = T B^3 T^T

as its Bose-Mesner radial projection plus an orientation residual.

The endpoint component is exact:

    F3 ∘ A4 = 28 A4.

The full radial projection is

    R(F3) = 12 A0 + 11 A1 + (33/2) A2 + 25 A3 + 28 A4.

The residual has support only on A1,A2,A3 and has zero mean on every distance
shell; the protected endpoint A4 has zero residual.
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


def flag_distance_matrix(flags):
    n = len(flags)
    A1 = np.zeros((n, n), dtype=int)
    for i, (p, l) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i != j and (p == q or l == m):
                A1[i, j] = 1
    dist = np.full((n, n), 99, dtype=int)
    for s in range(n):
        dist[s, s] = 0
        queue = [s]
        for u in queue:
            for v in np.nonzero(A1[u])[0]:
                if dist[s, v] == 99:
                    dist[s, v] = dist[s, u] + 1
                    queue.append(v)
    A = {d: (dist == d).astype(int) for d in range(5)}
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

    A, dist = flag_distance_matrix(flags)
    F3 = T @ np.linalg.matrix_power(B, 3) @ T.T

    coeffs = {}
    residual_profiles = {}
    radial = np.zeros_like(F3, dtype=object)
    for d in range(5):
        vals = [int(x) for x in F3[dist == d]]
        avg = Fraction(sum(vals), len(vals))
        coeffs[f"A{d}"] = str(avg)
        for i in range(160):
            for j in range(160):
                if dist[i, j] == d:
                    radial[i, j] = avg
        residuals = [str(Fraction(v, 1) - avg) for v in vals]
        residual_profiles[f"A{d}"] = {k: v for k, v in sorted(Counter(residuals).items())}

    endpoint = F3 * A[4]
    checks = {
        "radial_projection_coefficients": coeffs == {"A0": "12", "A1": "11", "A2": "33/2", "A3": "25", "A4": "28"},
        "endpoint_component_is_28_A4": np.array_equal(endpoint, 28 * A[4]),
        "endpoint_residual_zero": residual_profiles["A4"] == {"0": 12960},
        "A0_residual_zero": residual_profiles["A0"] == {"0": 160},
        "residual_only_on_A1_A2_A3": all(residual_profiles[k] == {"0": (dist == int(k[1])).sum()} for k in ["A0", "A4"]),
        "row_sum_3993": sorted(set(map(int, F3.sum(axis=1)))) == [3993],
        "radial_projection_row_sum_3993": 12 + 11 * 6 + Fraction(33, 2) * 18 + 25 * 54 + 28 * 81 == 3993,
    }

    result = {
        "bt": 611,
        "title": "Endpoint projection formula",
        "operator": "F3 = T B^3 T^T",
        "radial_projection": "12 A0 + 11 A1 + (33/2) A2 + 25 A3 + 28 A4",
        "coefficients": coeffs,
        "endpoint_formula": "F3 ∘ A4 = 28 A4",
        "residual_profiles_by_distance_shell": residual_profiles,
        "interpretation": "The folded cubic Hashimoto transfer has an exact Bose-Mesner endpoint component 28A4. Nonradial orientation residuals occur only on lower shells A1,A2,A3 and vanish on the protected endpoint shell.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    Path("data/PART_BT611_ENDPOINT_PROJECTION_FORMULA_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
