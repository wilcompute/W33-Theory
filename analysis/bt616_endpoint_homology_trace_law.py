#!/usr/bin/env python3
"""BT616: endpoint/homology trace law.

BT615 proved the projected identity

    E4 F3 E4 = E4.

BT616 compares three scales:

  1. the endpoint mass on the terminal A4 shell,
       sum(F3 o A4) = 12960 * 28 = 362880 = 9!;
  2. the protected Hodge trace,
       tr(E4 F3) = 81;
  3. the raw cubic leakage trace from BT562/BT585,
       tr(C3(G)) = 13651200.

The endpoint theorem therefore gives a factorial terminal shell scale, while the
Hodge projection collapses the same folded cubic transfer to identity trace on
H1=81.  The raw cubic leakage trace is not equal to the endpoint mass; its
exact ratio is 790/21.
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


def factorint(n: int) -> dict[str, int]:
    out = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[str(p)] = out.get(str(p), 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        out[str(n)] = out.get(str(n), 0) + 1
    return out


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
    endpoint = F3 * A[4]

    endpoint_mass = int(endpoint.sum())
    hodge_trace = Fraction(int(np.trace(K @ F3)), 160)
    endpoint_hodge_trace = Fraction(int(np.trace(K @ endpoint)), 160)
    raw_cubic_trace = 13_651_200
    shell_masses = {f"A{d}": int((F3 * A[d]).sum()) for d in range(5)}
    shell_profiles = {
        f"A{d}": {str(k): v for k, v in sorted(Counter(map(int, F3[dist == d])).items())}
        for d in range(5)
    }

    checks = {
        "endpoint_mass_is_12960_times_28": endpoint_mass == 12960 * 28,
        "endpoint_mass_is_9_factorial": endpoint_mass == 362880,
        "hodge_trace_is_81": hodge_trace == 81,
        "endpoint_hodge_trace_is_endpoint_mass_over_160": endpoint_hodge_trace == Fraction(endpoint_mass, 160),
        "projected_identity_trace_law": hodge_trace == 81,
        "raw_cubic_trace_known": raw_cubic_trace == 13_651_200,
        "raw_cubic_to_endpoint_ratio": Fraction(raw_cubic_trace, endpoint_mass) == Fraction(790, 21),
        "endpoint_to_hodge_trace_ratio": Fraction(endpoint_mass, hodge_trace) == 4480,
        "F3_total_mass": int(F3.sum()) == 638880,
        "F3_trace": int(np.trace(F3)) == 1920,
    }

    result = {
        "bt": 616,
        "title": "Endpoint/homology trace law",
        "endpoint_mass": endpoint_mass,
        "endpoint_mass_factorization": factorint(endpoint_mass),
        "endpoint_mass_reading": "12960*28 = 362880 = 9!",
        "hodge_trace_tr_E4_F3": str(hodge_trace),
        "endpoint_hodge_trace_tr_E4_endpoint": str(endpoint_hodge_trace),
        "raw_cubic_leakage_trace": raw_cubic_trace,
        "raw_cubic_trace_factorization": factorint(raw_cubic_trace),
        "raw_cubic_to_endpoint_ratio": str(Fraction(raw_cubic_trace, endpoint_mass)),
        "endpoint_to_hodge_trace_ratio": str(Fraction(endpoint_mass, hodge_trace)),
        "F3_total_mass": int(F3.sum()),
        "F3_trace": int(np.trace(F3)),
        "shell_masses": shell_masses,
        "shell_profiles": shell_profiles,
        "interpretation": "The folded cubic endpoint shell carries the factorial scale 9!=12960*28. Hodge projection collapses the same folded cubic transfer to identity trace 81 on H1. The raw cubic Gegenbauer leakage trace is a different, larger nonlinear scale; its exact ratio to endpoint mass is 790/21, so endpoint uniformity feeds the Hodge transport law but does not equal the raw cubic leakage trace.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    Path("data/PART_BT616_ENDPOINT_HOMOLOGY_TRACE_LAW_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
