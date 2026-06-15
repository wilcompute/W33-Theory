#!/usr/bin/env python3
"""BT1081: W33 incidence ladder projected-rank harness.

Builds W(3,3), C1 with 240 edges, the triangle 2-complex, Delta_1, and then
computes ranks of projected C1 operators between nearest eigensectors.
"""
from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path
from collections import Counter

import numpy as np


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c*y) % 3 for y in v)
    raise ValueError


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    n = len(pts)

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    adj = np.zeros((n, n), dtype=bool)
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            adj[i, j] = adj[j, i] = True
    edges = [(i, j) for i, j in combinations(range(n), 2) if adj[i, j]]
    edge_index = {e: k for k, e in enumerate(edges)}
    triangles = [t for t in combinations(range(n), 3)
                 if adj[t[0], t[1]] and adj[t[0], t[2]] and adj[t[1], t[2]]]
    m, T = len(edges), len(triangles)

    d0 = np.zeros((m, n))
    for idx, (i, j) in enumerate(edges):
        d0[idx, i] = -1
        d0[idx, j] = 1
    d2 = np.zeros((m, T))
    for t_idx, (i, j, k) in enumerate(triangles):
        for (a, b), sgn in [((j, k), 1), ((i, k), -1), ((i, j), 1)]:
            e = tuple(sorted((a, b)))
            orient = 1 if a < b else -1
            d2[edge_index[e], t_idx] = sgn * orient

    L1 = d0 @ d0.T + d2 @ d2.T
    evals, V = np.linalg.eigh(L1)
    lambdas = [0, 4, 10, 16]
    spaces = {lam: V[:, np.where(np.abs(evals-lam) < 1e-6)[0]] for lam in lambdas}

    # C1 adjacency operators.
    edge_sets = [set(e) for e in edges]
    A_line = np.zeros((m, m))
    for a, b in combinations(range(m), 2):
        if edge_sets[a] & edge_sets[b]:
            A_line[a, b] = A_line[b, a] = 1
    A_tri = np.zeros((m, m))
    for tri in triangles:
        es = [edge_index[tuple(sorted(e))] for e in combinations(tri, 2)]
        for a, b in combinations(es, 2):
            A_tri[a, b] = A_tri[b, a] = 1

    def rank_between(B, lam, mu, tol=1e-7):
        M = spaces[mu].T @ B @ spaces[lam]
        return int((np.linalg.svd(M, compute_uv=False) > tol).sum())

    pairs = [(0, 4), (4, 10), (10, 16)]
    out = {
        "theorem": "BT1081 incidence ladder projected ranks",
        "counts": {"points": n, "edges": m, "triangles": T},
        "spectrum": {str(k): int(v) for k, v in Counter(round(x) for x in evals).items()},
        "operators": {
            "line_edge_adjacency": {f"{a}->{b}": rank_between(A_line, a, b) for a, b in pairs},
            "triangle_edge_adjacency": {f"{a}->{b}": rank_between(A_tri, a, b) for a, b in pairs},
            "exact_part_d0d0T": {f"{a}->{b}": rank_between(d0 @ d0.T, a, b) for a, b in pairs},
            "coexact_part_d2d2T": {f"{a}->{b}": rank_between(d2 @ d2.T, a, b) for a, b in pairs}
        },
        "boundary": "line/triangle edge-adjacency operators give nonzero incidence ladders; d0d0T and d2d2T commute with Delta_1 and give zero off-sector ranks"
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1081_incidence_ladder_rank_script.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
