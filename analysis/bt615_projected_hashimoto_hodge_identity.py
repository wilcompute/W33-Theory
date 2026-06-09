#!/usr/bin/env python3
"""BT615: projected folded-Hashimoto/Hodge identity.

BT611--BT613 showed that the folded cubic Hashimoto transfer

    F3 = T B^3 T^T

has exact endpoint component 28 A4, with lower-shell orientation residuals.
BT615 asks what the protected Hodge/cycle sector actually sees.

Let

    E4 = (1/160) K,
    K = 81 A0 - 27 A1 + 9 A2 - 3 A3 + A4 = C C^T.

Then the exact identity is

    E4 F3 E4 = E4.

So after Hodge projection, the folded cubic Hashimoto operator acts as the
identity on the protected 81-dimensional Levi cycle sector.
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
    return dist


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

    dist = flag_distance_matrix(flags)
    A = [(dist == d).astype(int) for d in range(5)]
    K = 81 * A[0] - 27 * A[1] + 9 * A[2] - 3 * A[3] + A[4]
    F3 = T @ np.linalg.matrix_power(B, 3) @ T.T

    # Since E4=K/160, E4 F3 E4=E4 is equivalent to K F3 K = 160 K.
    kf3k = K @ F3 @ K
    radial_coeffs = {}
    for d in range(5):
        vals = [int(x) for x in F3[dist == d]]
        radial_coeffs[f"A{d}"] = str(Fraction(sum(vals), len(vals)))

    shell_value_profiles = {
        f"A{d}": {str(k): v for k, v in sorted(Counter(map(int, F3[dist == d])).items())}
        for d in range(5)
    }

    checks = {
        "K_idempotent_scale": np.array_equal(K @ K, 160 * K),
        "E4_rank_81": np.linalg.matrix_rank(K) == 81,
        "projected_identity": np.array_equal(kf3k, 160 * K),
        "trace_E4_F3_is_81": Fraction(int(np.trace(K @ F3)), 160) == 81,
        "endpoint_uniform_28": shell_value_profiles["A4"] == {"28": 12960},
        "radial_projection_coefficients": radial_coeffs == {"A0": "12", "A1": "11", "A2": "33/2", "A3": "25", "A4": "28"},
    }
    result = {
        "bt": 615,
        "title": "Projected folded-Hashimoto/Hodge identity",
        "identity": "E4 F3 E4 = E4",
        "integer_equivalent": "K F3 K = 160 K",
        "trace_E4_F3": str(Fraction(int(np.trace(K @ F3)), 160)),
        "rank_E4": int(np.linalg.matrix_rank(K)),
        "radial_projection": "12 A0 + 11 A1 + (33/2) A2 + 25 A3 + 28 A4",
        "radial_coefficients": radial_coeffs,
        "shell_value_profiles": shell_value_profiles,
        "interpretation": "Although F3 has lower-shell orientation residuals, the protected Hodge/cycle idempotent sees F3 as the identity. Thus Hodge projection converts folded cubic nonbacktracking propagation into identity transport on the 81-dimensional protected sector.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    Path("data/PART_BT615_PROJECTED_HASHIMOTO_HODGE_IDENTITY_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
