#!/usr/bin/env python3
"""Test equivariance of the edge->root bijection under PSp(4,3) generators.

If the induced permutations on roots preserve the E8 bilinear form,
then the bijection is compatible with a Weyl-group action.
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path

from sage.all import RootSystem

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
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
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
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


def get_sp43_generators(vertices, edges):
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

    edge_perms = []
    for M in gen_matrices:
        if not check_symplectic(M):
            continue
        vperm = matrix_to_vertex_perm(M, vertices)
        eperm = vertex_perm_to_edge_perm(vperm, edges)
        edge_perms.append(eperm)
    return edge_perms


def main():
    vertices, edges = build_w33()

    # Load edge->root mapping
    edge_to_root = json.loads((ROOT / "artifacts" / "edge_to_e8_root.json").read_text())
    edge_map = {}
    for k, v in edge_to_root.items():
        i, j = k.strip("() ").split(",")
        e = tuple(sorted((int(i), int(j))))
        edge_map[e] = tuple(v)

    # Build root list and index
    roots = list(edge_map.values())
    root_index = {r: i for i, r in enumerate(roots)}

    # Gram matrix in simple-root basis (consistent with Sage ordering)
    R = RootSystem(["E", 8]).root_lattice()
    C = R.cartan_type().cartan_matrix()

    def ip(r, s):
        return int(sum(r[i] * C[i, j] * s[j] for i in range(8) for j in range(8)))

    # Precompute Gram matrix entries
    n = len(roots)
    Gram = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            Gram[i][j] = ip(roots[i], roots[j])

    # Edge index mapping
    edge_list = edges
    edge_idx = {e: i for i, e in enumerate(edge_list)}

    # Generators
    edge_perms = get_sp43_generators(vertices, edges)
    print(f"Generators: {len(edge_perms)}")

    # Test equivariance: each edge perm induces a root perm
    for g_idx, eperm in enumerate(edge_perms):
        # Build root permutation induced by edge permutation
        perm = [0] * n
        for e in edge_list:
            i = edge_idx[e]
            e2 = edge_list[eperm[i]]
            r = edge_map[e]
            r2 = edge_map[e2]
            perm[root_index[r]] = root_index[r2]

        # Check Gram invariance
        ok = True
        for i in range(n):
            pi = perm[i]
            row_i = Gram[i]
            row_pi = Gram[pi]
            for j in range(n):
                if row_i[j] != row_pi[perm[j]]:
                    ok = False
                    break
            if not ok:
                break
        print(f"Generator {g_idx}: Gram preserved = {ok}")


if __name__ == "__main__":
    main()
