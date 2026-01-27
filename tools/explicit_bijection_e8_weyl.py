#!/usr/bin/env python3
"""Explicit W33 edge -> E8 root bijection via W(E8) reflections.

We use the canonical BFS words for edges under 10 symplectic generators
and map those words into a selected 10-generator subgroup of W(E8)
(built from simple reflections and their products) to obtain 240 distinct
roots.
"""
from __future__ import annotations

import json
import random
from collections import deque
from itertools import product
from pathlib import Path

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
            edge_gens.append(eperm)
    return edge_gens


def bfs_edge_labels(gens, n_edges, base=0):
    labels = {base: ()}
    q = deque([base])
    while q:
        cur = q.popleft()
        word = labels[cur]
        for gi, g in enumerate(gens):
            nxt = g[cur]
            if nxt not in labels:
                labels[nxt] = word + (gi,)
                q.append(nxt)
    return labels

# ---------------- E8 reflections ----------------

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
                    roots.append(tuple(r))
    # type 2
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(signs))
    return roots


def dot(a, b):
    return sum(a[i] * b[i] for i in range(8))


def pick_generic_rho(roots, seed=2):
    random.seed(seed)
    while True:
        rho = [random.random() for _ in range(8)]
        if all(abs(dot(r, rho)) > 1e-9 for r in roots):
            return rho


def simple_roots_from_positive(roots):
    rho = pick_generic_rho(roots)
    pos = [r for r in roots if dot(r, rho) > 0]
    pos_set = set(pos)
    simples = []
    for r in pos:
        is_simple = True
        for s in pos:
            if s == r:
                continue
            t = tuple(r[i] - s[i] for i in range(8))
            if t in pos_set:
                is_simple = False
                break
        if is_simple:
            simples.append(r)
    return simples


def reflect(R, A):
    k = dot(R, A) // 4
    return tuple(R[i] - k * A[i] for i in range(8))


def build_reflection_perms(roots, simples):
    idx = {r: i for i, r in enumerate(roots)}
    perms = []
    for A in simples:
        perm = [0] * len(roots)
        for i, R in enumerate(roots):
            perm[i] = idx[reflect(R, A)]
        perms.append(perm)
    return perms


def compose(p, q):
    return [p[i] for i in q]


def apply_word(root_idx, gens, word):
    cur = root_idx
    for w in word:
        cur = gens[w][cur]
    return cur


def main():
    points = construct_w33_points()
    edges = construct_w33_edges(points)
    edge_gens = get_w33_edge_generators(points, edges)
    if len(edge_gens) < 6:
        print("Not enough W33 generators")
        return

    edge_words = bfs_edge_labels(edge_gens, len(edges), base=0)
    if len(edge_words) != 240:
        print("Edge BFS did not reach all edges:", len(edge_words))
        return

    # E8 simple reflections
    roots = build_e8_roots_scaled()
    simples = simple_roots_from_positive(roots)
    if len(simples) != 8:
        print("E8 simples found:", len(simples))
        return

    refls = build_reflection_perms(roots, simples)

    # Build candidate pool: 8 reflections + 8 adjacent products
    pool = list(refls)
    for i in range(8):
        pool.append(compose(refls[i], refls[(i+1)%8]))

    # Random search for a 10-generator set giving unique images
    words = [edge_words[i] for i in range(240)]
    root_base = 0

    best = None
    for trial in range(400):
        gens = random.sample(pool, 10)
        # quick check for distinctness
        images = [apply_word(root_base, gens, w) for w in words]
        if len(set(images)) == 240:
            best = gens
            print("Found generator set at trial", trial)
            break

    if best is None:
        print("No bijection found in 400 trials.")
        best = pool[:10]

    images = [apply_word(root_base, best, w) for w in words]
    edge_to_root = {i: images[i] for i in range(240)}

    out = {
        "edge_to_root_index": edge_to_root,
        "root_coords": [list(r) for r in roots],
    }

    out_path = ROOT / "artifacts" / "explicit_bijection_e8_weyl.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
