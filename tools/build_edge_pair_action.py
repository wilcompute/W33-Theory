#!/usr/bin/env python3
"""Build action of PSp(4,3) generators on 120 edge-pairs (complement edges on lines).

Each W33 edge lies on a unique line of 4 points; the opposite edge on that line
is the complementary pair. This defines an invariant involution pairing edges
into 120 pairs.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_projective_points():
    F3 = [0, 1, 2]
    proj_points = []
    seen = set()
    for v in product(F3, repeat=4):
        if all(x == 0 for x in v):
            continue
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)
    return proj_points


def omega_sym(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_edges(points):
    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega_sym(points[i], points[j]) == 0:
                edges.append((i, j))
    return edges


def build_adj(edges):
    adj = [[0] * 40 for _ in range(40)]
    for i, j in edges:
        adj[i][j] = adj[j][i] = 1
    return adj


def build_edge_pairs(edges, adj):
    # map edge -> opposite edge on its line
    edge_to_idx = {tuple(e): i for i, e in enumerate(edges)}
    # ensure sorted tuples
    edges_sorted = [tuple(sorted(e)) for e in edges]

    pair_map = {}
    for i, j in edges_sorted:
        common = [k for k in range(40) if adj[i][k] and adj[j][k]]
        if len(common) != 2:
            raise RuntimeError("Edge does not have 2 common neighbors")
        a, b = common
        opp = tuple(sorted((a, b)))
        pair_map[(i, j)] = opp

    # build pairs set
    pair_set = set()
    for e, opp in pair_map.items():
        pair = tuple(sorted([e, opp]))
        pair_set.add(pair)

    pairs = sorted(list(pair_set))
    pair_index = {pair: idx for idx, pair in enumerate(pairs)}

    # For each edge, map to pair index
    edge_to_pair = {}
    for pair, idx in pair_index.items():
        e1, e2 = pair
        edge_to_pair[e1] = idx
        edge_to_pair[e2] = idx

    return pairs, edge_to_pair


def normalize_proj(v):
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    return tuple(v)


def check_symplectic(M):
    Omega = [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]]

    def mat_mult(A, B):
        n, k, m = len(A), len(B), len(B[0])
        result = [[0] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for l in range(k):
                    result[i][j] = (result[i][j] + A[i][l] * B[l][j]) % 3
        return result

    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    result = mat_mult(mat_mult(MT, Omega), M)
    return result == Omega


def apply_matrix(M, v):
    result = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    return normalize_proj(result)


def matrix_to_vertex_perm(M, vertices):
    v_to_idx = {tuple(v): i for i, v in enumerate(vertices)}
    perm = []
    for v in vertices:
        v_new = apply_matrix(M, v)
        if v_new in v_to_idx:
            perm.append(v_to_idx[v_new])
        else:
            return None
    return perm


def vertex_perm_to_edge_perm(vperm, edges):
    edge_to_idx = {frozenset(e): i for i, e in enumerate(edges)}
    edge_perm = []
    for e in edges:
        i, j = e
        ni, nj = vperm[i], vperm[j]
        edge_perm.append(edge_to_idx[frozenset((ni, nj))])
    return edge_perm


def main():
    points = build_projective_points()
    edges = build_edges(points)
    adj = build_adj(edges)

    pairs, edge_to_pair = build_edge_pairs(edges, adj)

    gen_matrices = [
        [[1, 0, 1, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1]],
        [[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 2, 1]],
        [[1, 0, 0, 0], [1, 1, 0, 0], [0, 0, 1, 2], [0, 0, 0, 1]],
        [[0, 0, 1, 0], [0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0]],
        [[2, 0, 0, 0], [0, 1, 0, 0], [0, 0, 2, 0], [0, 0, 0, 1]],
        [[1, 0, 0, 0], [0, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 2]],
    ]

    pair_gens = []
    for M in gen_matrices:
        if check_symplectic(M):
            vperm = matrix_to_vertex_perm(M, points)
            if vperm:
                eperm = vertex_perm_to_edge_perm(vperm, edges)
                # induce on pairs
                pair_perm = []
                for pair in pairs:
                    e1, e2 = pair
                    e1i = edges.index(e1)
                    e2i = edges.index(e2)
                    ne1 = edges[eperm[e1i]]
                    ne2 = edges[eperm[e2i]]
                    ne1 = tuple(sorted(ne1))
                    ne2 = tuple(sorted(ne2))
                    pair_idx = edge_to_pair[ne1]
                    pair_perm.append(pair_idx)
                pair_gens.append(pair_perm)

    out = {
        "pairs": pairs,
        "edge_to_pair": {f"{a}-{b}": idx for (a, b), idx in edge_to_pair.items()},
        "pair_generators": pair_gens,
    }
    out_path = ROOT / "artifacts" / "sp43_edgepair_generators.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
