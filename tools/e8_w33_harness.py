#!/usr/bin/env python3
"""NumPy-based harness for checking mapped E8 root invariants for W33 edges.

Provides fast linear-algebra helpers and adjacency-based diagnostics used by tests.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def build_w33_points_and_edges() -> (
    Tuple[List[Tuple[int, int, int, int]], List[Tuple[int, int]]]
):
    F3 = [0, 1, 2]
    vectors = [
        v
        for v in __import__("itertools").product(F3, repeat=4)
        if any(x != 0 for x in v)
    ]

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

    return proj_points, edges


def mapped_root_matrix(data: Dict) -> np.ndarray:
    """Return (240,8) numpy array of roots mapped to edges in canonical edge index order."""
    _, edges = build_w33_points_and_edges()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}
    mapping = data["edge_to_root_index"]
    # mapping stored as edge_idx -> root_idx
    roots = np.array(data["root_coords"], dtype=int)
    mat = np.zeros((len(edges), roots.shape[1]), dtype=int)
    for e, idx in mapping.items():
        eidx = int(e)
        mat[eidx, :] = roots[idx]
    return mat


def edge_adjacency_matrix() -> np.ndarray:
    """Return (240,240) boolean adjacency matrix between edges (share a vertex)."""
    _, edges = build_w33_points_and_edges()
    n = len(edges)
    adj = np.zeros((n, n), dtype=bool)
    for i in range(n):
        a, b = edges[i]
        for j in range(i + 1, n):
            c, d = edges[j]
            if a == c or a == d or b == c or b == d:
                adj[i, j] = adj[j, i] = True
    return adj


def ip_distributions(data: Dict) -> Tuple[Dict[int, int], Dict[int, int]]:
    """Compute inner-product counts for adjacent vs non-adjacent edge pairs.

    Returns two dicts: (ip_counts_adj, ip_counts_nonadj)
    mapping ip_value (int) -> count
    """
    mat = mapped_root_matrix(data)
    # compute Gram matrix
    G = mat @ mat.T
    # Note: diagonal is norm 8
    adj = edge_adjacency_matrix()

    n = G.shape[0]
    ip_adj = {}
    ip_non = {}
    for i in range(n):
        for j in range(i + 1, n):
            v = int(G[i, j])
            if adj[i, j]:
                ip_adj[v] = ip_adj.get(v, 0) + 1
            else:
                ip_non[v] = ip_non.get(v, 0) + 1
    return ip_adj, ip_non


def save_ip_distributions(data: Dict, out_path: Path | None = None):
    if out_path is None:
        out_path = ROOT / "artifacts" / "ip_distributions.json"
    ip_adj, ip_non = ip_distributions(data)
    out = {"adjacent": ip_adj, "nonadjacent": ip_non}
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out
