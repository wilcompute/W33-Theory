#!/usr/bin/env python3
"""Refine explicit edge->root bijection by enforcing E8 automorphism constraints.

Given an initial bijection (edges -> roots), compute induced root permutations
from W33 edge generators and try to reduce mismatches of the E8 inner-product
matrix under those permutations by swapping assignments inside fixed classes
(27-classes, 72-class, 6-class).
"""
from __future__ import annotations

import json
import random
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# ---------------- W33 construction ----------------

def construct_w33_points():
    F3 = [0, 1, 2]
    points = []
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
            points.append(v)
    return points


def omega(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def construct_w33_edges(points):
    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(points[i], points[j]) == 0:
                edges.append((i, j))
    return edges


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
                s = 0
                for l in range(k):
                    s = (s + A[i][l] * B[l][j]) % 3
                result[i][j] = s
        return result
    MT = [[M[j][i] for j in range(4)] for i in range(4)]
    return mat_mult(mat_mult(MT, Omega), M) == Omega


def apply_matrix(M, v):
    result = [sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4)]
    return normalize_proj(result)


def matrix_to_vertex_perm(M, points):
    p_to_idx = {tuple(p): i for i, p in enumerate(points)}
    perm = []
    for p in points:
        p2 = apply_matrix(M, p)
        if p2 not in p_to_idx:
            return None
        perm.append(p_to_idx[p2])
    return perm


def vertex_perm_to_edge_perm(vperm, edges):
    edge_to_idx = {frozenset(e): i for i, e in enumerate(edges)}
    perm = []
    for e in edges:
        i, j = e
        i2, j2 = vperm[i], vperm[j]
        perm.append(edge_to_idx[frozenset([i2, j2])])
    return perm


def get_w33_edge_generators(points, edges):
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
    edge_gens = []
    for M in gen_matrices:
        if not check_symplectic(M):
            continue
        vperm = matrix_to_vertex_perm(M, points)
        if vperm is None:
            continue
        eperm = vertex_perm_to_edge_perm(vperm, edges)
        if eperm and eperm != list(range(len(edges))):
            edge_gens.append(np.array(eperm, dtype=int))
    return edge_gens

# ---------------- E8 roots ----------------

def build_e8_roots_scaled():
    roots = []
    # type 1
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in (2, -2):
                for s2 in (2, -2):
                    r = [0] * 8
                    r[i] = s1
                    r[j] = s2
                    roots.append(r)
    # type 2
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(signs)
    return np.array(roots, dtype=int)


def dot_matrix(roots):
    return roots @ roots.T


def load_mapping(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    edge_to_root = data["edge_to_root_index"]
    # edge_to_root keys are strings; convert to int
    mapping = [0] * 240
    for k, v in edge_to_root.items():
        mapping[int(k)] = int(v)
    return np.array(mapping, dtype=int), data


def induced_root_perm(edge_perm, mapping):
    # mapping: edge -> root
    # induced perm on roots: r -> r' where r = mapping[e], r' = mapping[edge_perm[e]]
    # We need inverse map root->edge
    inv = np.zeros_like(mapping)
    for e, r in enumerate(mapping):
        inv[r] = e
    # perm on roots
    perm = np.zeros(240, dtype=int)
    for r in range(240):
        e = inv[r]
        e2 = edge_perm[e]
        perm[r] = mapping[e2]
    return perm


def perm_preserves_dot(dot, perm):
    # check dot == dot[perm][:,perm]
    return np.array_equal(dot, dot[np.ix_(perm, perm)])


def mismatch_count(dot, perm):
    # count mismatches in dot matrix under perm
    d2 = dot[np.ix_(perm, perm)]
    return int(np.sum(dot != d2))


def main():
    roots = build_e8_roots_scaled()
    dot = dot_matrix(roots)

    points = construct_w33_points()
    edges = construct_w33_edges(points)
    edge_gens = get_w33_edge_generators(points, edges)

    mapping, data = load_mapping(ROOT / "artifacts" / "explicit_bijection_decomposition.json")

    # compute initial mismatches
    mismatches = []
    for g in edge_gens:
        perm = induced_root_perm(g, mapping)
        mismatches.append(mismatch_count(dot, perm))
    print("Initial mismatches per generator:", mismatches)
    print("Total mismatch:", sum(mismatches))

    # determine classes to allow swaps (27-classes + 72 + 6)
    class27_keys = data["class27_keys"]
    class1_keys = data["class1_keys"]
    class72_key = data["class72_key"]

    # build root classes
    # recompute dot-pair classes
    u1 = np.array([1,1,1,1,1,1,1,1])
    u2 = np.array([1,1,1,1,1,1,-1,-1])
    pairs = {}
    for idx, r in enumerate(roots):
        d = (int(r @ u1), int(r @ u2))
        pairs.setdefault(d, []).append(idx)

    class27 = [pairs[tuple(k)] for k in class27_keys]
    class1 = [pairs[tuple(k)][0] for k in class1_keys]
    class72 = pairs[tuple(class72_key)]

    # build edge classes aligned with mapping classes
    # reverse map: root -> edge
    edge_of_root = np.zeros(240, dtype=int)
    for e, r in enumerate(mapping):
        edge_of_root[r] = e

    edge_classes = []
    for cls in class27:
        edge_classes.append([edge_of_root[r] for r in cls])
    edge_classes.append([edge_of_root[r] for r in class72])
    edge_classes.append([edge_of_root[r] for r in class1])

    # Simulated swap search within classes
    random.seed(0)
    best_mapping = mapping.copy()
    best_score = sum(mismatches)

    for step in range(500):
        # pick a class and swap two edges
        cls = random.choice(edge_classes)
        if len(cls) < 2:
            continue
        e1, e2 = random.sample(cls, 2)
        # swap root assignments
        mapping[e1], mapping[e2] = mapping[e2], mapping[e1]

        # recompute mismatch score (full)
        score = 0
        for g in edge_gens:
            perm = induced_root_perm(g, mapping)
            score += mismatch_count(dot, perm)

        if score < best_score:
            best_score = score
            best_mapping = mapping.copy()
            print(f"Step {step}: improved score {best_score}")
        else:
            # revert with high probability
            if random.random() < 0.9:
                mapping[e1], mapping[e2] = mapping[e2], mapping[e1]

    # write refined mapping
    out = {
        "edge_to_root_index": {i: int(best_mapping[i]) for i in range(240)},
        "best_score": best_score,
    }
    out_path = ROOT / "artifacts" / "explicit_bijection_refined.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
