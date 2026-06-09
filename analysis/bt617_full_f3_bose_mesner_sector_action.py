#!/usr/bin/env python3
"""BT617: full Bose--Mesner sector action of the folded cubic Hashimoto operator.

BT615 proved the protected identity

    E4 F3 E4 = E4.

BT617 computes the full primitive-idempotent block pattern of

    F3 = T B^3 T^T

on the W33 Levi flag association scheme.  The action is much sharper than a
single protected block:

  * E0 is scalar with eigenvalue 3993 = 3*11^3;
  * E4 is scalar with eigenvalue 1;
  * E1 and E3 are conjugate 24-dimensional sectors with diagonal scalars and
    nonzero off-diagonal conjugate mixing;
  * E2 is invariant but splits internally as 77^15 plus (-3)^15.

Thus the only inter-idempotent mixing is E1 <-> E3, while the Hodge sector E4
is an isolated identity block.
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


def flag_distance_matrices(flags):
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
    return dist, [(dist == d).astype(int) for d in range(5)], A1


def primitive_idempotents(A1: np.ndarray) -> list[np.ndarray]:
    vals = [6, 2 + math.sqrt(6), 2, 2 - math.sqrt(6), -2]
    eye = np.eye(A1.shape[0])
    A = A1.astype(float)
    out = []
    for i, theta in enumerate(vals):
        num = eye.copy()
        den = 1.0
        for j, phi in enumerate(vals):
            if i == j:
                continue
            num = num @ (A - phi * eye)
            den *= theta - phi
        out.append(num / den)
    return out


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

    _dist, A, A1 = flag_distance_matrices(flags)
    E = primitive_idempotents(A1)
    F3 = T @ np.linalg.matrix_power(B, 3) @ T.T
    K = 81 * A[0] - 27 * A[1] + 9 * A[2] - 3 * A[3] + A[4]

    rank_matrix = []
    trace_matrix = []
    hs_norm_sq_matrix = []
    support = []
    for i in range(5):
        rrow = []
        trow = []
        nrow = []
        for j in range(5):
            block = E[i] @ F3 @ E[j]
            rank = int(np.linalg.matrix_rank(block, tol=1e-7))
            trace = float(np.trace(block))
            norm_sq = float(np.trace(block @ block.T))
            rrow.append(rank)
            trow.append(round(trace, 12))
            nrow.append(round(norm_sq, 12))
            if rank:
                support.append([i, j])
        rank_matrix.append(rrow)
        trace_matrix.append(trow)
        hs_norm_sq_matrix.append(nrow)

    M22 = E[2] @ F3 @ E[2]
    P77 = (M22 + 3 * E[2]) / 80
    Pm3 = (77 * E[2] - M22) / 80
    M13 = E[1] @ F3 @ E[3]
    M31 = E[3] @ F3 @ E[1]

    checks = {
        "E4_matches_Hodge_kernel": np.max(np.abs(E[4] - K / 160)) < 1e-9,
        "E0_scalar_3993": np.max(np.abs(E[0] @ F3 @ E[0] - 3993 * E[0])) < 1e-8,
        "E1_scalar_minus_68_minus_31_sqrt6": np.max(np.abs(E[1] @ F3 @ E[1] - (-68 - 31 * math.sqrt(6)) * E[1])) < 1e-8,
        "E3_scalar_minus_68_plus_31_sqrt6": np.max(np.abs(E[3] @ F3 @ E[3] - (-68 + 31 * math.sqrt(6)) * E[3])) < 1e-8,
        "E4_identity": np.max(np.abs(E[4] @ F3 @ E[4] - E[4])) < 1e-9,
        "E2_internal_minimal_polynomial": np.max(np.abs((M22 - 77 * E[2]) @ (M22 + 3 * E[2]))) < 1e-8,
        "E2_split_ranks_15_15": int(np.linalg.matrix_rank(P77, tol=1e-7)) == 15 and int(np.linalg.matrix_rank(Pm3, tol=1e-7)) == 15,
        "E1_E3_mixing_product": np.max(np.abs(M13 @ M31 + 6455 * E[1])) < 1e-8 and np.max(np.abs(M31 @ M13 + 6455 * E[3])) < 1e-8,
        "support_pattern": support == [[0, 0], [1, 1], [1, 3], [2, 2], [3, 1], [3, 3], [4, 4]],
    }

    result = {
        "bt": 617,
        "title": "Full folded-cubic Bose--Mesner sector action",
        "operator": "F3 = T B^3 T^T",
        "primitive_idempotent_order": ["E0", "E1", "E2", "E3", "E4"],
        "block_support": support,
        "rank_matrix": rank_matrix,
        "trace_matrix_numeric": trace_matrix,
        "hilbert_schmidt_norm_sq_numeric": hs_norm_sq_matrix,
        "exact_block_laws": {
            "E0F3E0": "3993 E0 = 3*11^3 E0",
            "E1F3E1": "(-68 - 31*sqrt(6)) E1",
            "E3F3E3": "(-68 + 31*sqrt(6)) E3",
            "E4F3E4": "E4",
            "E2F3E2": "internal split 77^15 plus (-3)^15; equivalently (M22-77E2)(M22+3E2)=0",
            "E1E3_mixing": "M13 M31 = -6455 E1 and M31 M13 = -6455 E3",
        },
        "interpretation": "The folded cubic Hashimoto operator is block-supported only on E0, the conjugate E1/E3 pair, E2, and E4. The protected Hodge sector is isolated and sees identity transport; the only cross-idempotent mixing is the E1<->E3 conjugate 24-sector channel.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT617_FULL_F3_BOSE_MESNER_SECTOR_ACTION_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
