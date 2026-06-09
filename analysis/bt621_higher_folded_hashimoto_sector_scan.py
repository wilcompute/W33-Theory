#!/usr/bin/env python3
"""BT621: higher folded-Hashimoto sector scan.

BT617 computed the full primitive-idempotent action of

    F3 = T B^3 T^T.

BT621 extends the scan to F_n for n=1,...,6, where

    F_n = T B^n T^T

and T folds directed W33 collinearity edges to W33 point-line Levi flags.

Main empirical/exact pattern verified by the script:

  * every F_n has row sum 3*11^n;
  * the primitive block support is constant for n=1,...,6:
        E0, E2, E4 diagonal blocks plus the conjugate E1/E3 pair;
  * the protected Hodge block is scalar and alternates
        E4 F_n E4 = E4      for odd n,
        E4 F_n E4 = 3 E4    for even n.

Thus the physical sector does not inherit the raw 3*11^n growth.  It sees a
small parity clock 1,3,1,3,... after projection.
"""
from __future__ import annotations

from itertools import combinations, product
import json
import math
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


def flag_adjacency(flags) -> np.ndarray:
    n = len(flags)
    A1 = np.zeros((n, n), dtype=float)
    for i, (p, l) in enumerate(flags):
        for j, (q, m) in enumerate(flags):
            if i != j and (p == q or l == m):
                A1[i, j] = 1
    return A1


def primitive_idempotents(A1: np.ndarray) -> list[np.ndarray]:
    vals = [6, 2 + math.sqrt(6), 2, 2 - math.sqrt(6), -2]
    eye = np.eye(A1.shape[0])
    out = []
    for i, theta in enumerate(vals):
        num = eye.copy()
        den = 1.0
        for j, phi in enumerate(vals):
            if i == j:
                continue
            num = num @ (A1 - phi * eye)
            den *= theta - phi
        out.append(num / den)
    return out


def main() -> int:
    pts, edges, adj, lines, edge_line, flags, flag_index, directed, directed_index = build_geometry()
    T = np.zeros((160, 480), dtype=float)
    for de, (tail, _head, li) in enumerate(directed):
        T[flag_index[(tail, li)], de] = 1

    B = np.zeros((480, 480), dtype=float)
    for a, (u, v, _li) in enumerate(directed):
        for w in adj[v]:
            if w != u:
                B[a, directed_index[(v, w)]] = 1

    E = primitive_idempotents(flag_adjacency(flags))
    expected_support = [[0, 0], [1, 1], [1, 3], [2, 2], [3, 1], [3, 3], [4, 4]]
    scan = {}
    Bp = np.eye(480)
    all_checks = []
    for n in range(1, 7):
        Bp = Bp @ B
        Fn = T @ Bp @ T.T
        support = []
        rank_matrix = []
        trace_matrix = []
        for i in range(5):
            ranks = []
            traces = []
            for j in range(5):
                block = E[i] @ Fn @ E[j]
                rank = int(np.linalg.matrix_rank(block, tol=1e-7))
                ranks.append(rank)
                traces.append(round(float(np.trace(block)), 12))
                if rank:
                    support.append([i, j])
            rank_matrix.append(ranks)
            trace_matrix.append(traces)
        e4_scalar = float(np.trace(E[4] @ Fn @ E[4]) / 81)
        e4_expected = 1 if n % 2 else 3
        e4_error = float(np.max(np.abs(E[4] @ Fn @ E[4] - e4_expected * E[4])))
        row_sum = float(Fn.sum(axis=1)[0])
        checks = {
            "row_sum_is_3_11_power_n": abs(row_sum - 3 * 11**n) < 1e-7,
            "support_pattern_constant": support == expected_support,
            "E4_parity_scalar": abs(e4_scalar - e4_expected) < 1e-8,
            "E4_block_error_small": e4_error < 1e-7,
        }
        all_checks.extend(checks.values())
        scan[f"F{n}"] = {
            "row_sum": int(round(row_sum)),
            "expected_row_sum": int(3 * 11**n),
            "block_support": support,
            "rank_matrix": rank_matrix,
            "trace_matrix_numeric": trace_matrix,
            "E4_scalar": int(round(e4_scalar)),
            "E4_expected_scalar": e4_expected,
            "checks": checks,
        }

    result = {
        "bt": 621,
        "title": "Higher folded-Hashimoto sector scan",
        "operator_family": "F_n = T B^n T^T for n=1,...,6",
        "primitive_idempotent_order": ["E0", "E1", "E2", "E3", "E4"],
        "constant_block_support": expected_support,
        "protected_sector_law": "E4 F_n E4 = E4 for odd n and 3 E4 for even n, checked for 1<=n<=6",
        "raw_row_sum_law": "rowsum(F_n)=3*11^n",
        "scan": scan,
        "interpretation": "The raw folded nonbacktracking transfer grows with Ihara scale 3*11^n, but its Hodge-projected protected sector is governed by the small parity clock 1,3,1,3,... . The only persistent inter-idempotent mixing remains the conjugate E1/E3 channel.",
        "all_identities_hold": all(all_checks),
    }
    out = Path("data/PART_BT621_HIGHER_FOLDED_HASHIMOTO_SECTOR_SCAN_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
