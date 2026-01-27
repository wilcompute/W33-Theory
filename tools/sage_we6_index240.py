#!/usr/bin/env python3
"""Sage/GAP: find an index-240 subgroup of W(E6) and compare to edge action."""
from __future__ import annotations

from itertools import product
from pathlib import Path
import json

from sage.all import WeylGroup, PermutationGroup, Permutation, libgap

ROOT = Path(__file__).resolve().parents[1]


def build_w33_edges():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

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
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i+1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def normalize_proj(v):
    v = list(v)
    for i in range(4):
        if v[i] != 0:
            inv = 1 if v[i] == 1 else 2
            return tuple((x * inv) % 3 for x in v)
    return tuple(v)


def check_symplectic(M):
    Omega = [[0,0,1,0],[0,0,0,1],[2,0,0,0],[0,2,0,0]]
    def mat_mult(A, B):
        n, k, m = len(A), len(B), len(B[0])
        result = [[0]*m for _ in range(n)]
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
        perm.append(v_to_idx[v_new])
    return perm


def vertex_perm_to_edge_perm(vperm, edges):
    edge_to_idx = {frozenset(e): i for i, e in enumerate(edges)}
    perm = []
    for e in edges:
        i, j = e
        new_i, new_j = vperm[i], vperm[j]
        perm.append(edge_to_idx[frozenset([new_i, new_j])])
    return perm


def edge_group_generators(vertices, edges):
    gen_matrices = [
        [[1,0,1,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,0],[1,0,1,0],[0,0,0,1]],
        [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,1,0,1]],
        [[1,1,0,0],[0,1,0,0],[0,0,1,0],[0,0,2,1]],
        [[1,0,0,0],[1,1,0,0],[0,0,1,2],[0,0,0,1]],
        [[0,0,1,0],[0,1,0,0],[2,0,0,0],[0,0,0,1]],
        [[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,2,0,0]],
        [[2,0,0,0],[0,1,0,0],[0,0,2,0],[0,0,0,1]],
        [[1,0,0,0],[0,2,0,0],[0,0,1,0],[0,0,0,2]],
    ]
    gens = []
    for M in gen_matrices:
        if not check_symplectic(M):
            continue
        vperm = matrix_to_vertex_perm(M, vertices)
        eperm = vertex_perm_to_edge_perm(vperm, edges)
        gens.append(Permutation([x+1 for x in eperm]))
    return gens


def main():
    # Edge action group (PSp(4,3) on edges)
    vertices, edges = build_w33_edges()
    edge_gens = edge_group_generators(vertices, edges)
    G_edges = PermutationGroup(edge_gens)

    # Weyl group of E6
    G_we6 = WeylGroup(['E', 6], prefix="s")

    # Find subgroups of index 240 (size 216) via GAP low-index search on fp-group
    G_fp = G_we6.as_finitely_presented_group()
    G_gap = libgap(G_fp)
    subs = libgap.LowIndexSubgroupsFpGroup(G_gap, 240)
    print("Index-240 subgroups (low-index search):", subs.Length())

    results = {
        "edge_group_order": int(G_edges.order()),
        "we6_order": int(G_we6.order()),
        "index240_subgroup_count": int(subs.Length()),
        "isomorphism_found": False,
    }

    # Try each subgroup to see if coset action is isomorphic to edge action
    for idx in range(int(subs.Length())):
        H_gap = subs[idx]
        # convert GAP subgroup to Sage subgroup
        H = libgap(H_gap).sage(G_we6)
        # coset action permutation group
        P = G_we6.coset_action(H)
        if P.order() != G_edges.order():
            continue
        if P.is_isomorphic(G_edges):
            results["isomorphism_found"] = True
            results["subgroup_index"] = idx
            results["subgroup_order"] = int(H.order())
            break

    out_path = ROOT / "artifacts" / "we6_index240_search.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
