#!/usr/bin/env python3
"""Construct an explicit W33-edge -> E8-root bijection via even W(E6).

We build:
- W33 edge generator permutations (from symplectic matrices)
- E6 simple reflections on the E8 roots (scaled by 2 for integer arithmetic)
- Even Weyl generators as products of E6 reflections

We then try to map the W33 generator words to the even Weyl generators by
searching for a permutation of generators that yields a bijection.
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
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


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
    Omega = [[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]]

    def mat_mult(A, B):
        n, k, m = len(A), len(B), len(B[0])
        result = [[0] * m for _ in range(n)]
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
    labels = {base: (0, ())}
    q = deque([base])
    while q:
        cur = q.popleft()
        dist, word = labels[cur]
        for gi, g in enumerate(gens):
            nxt = g[cur]
            if nxt not in labels:
                labels[nxt] = (dist + 1, word + (gi,))
                q.append(nxt)
            # inverse
            # build inverse on the fly
            if dist < 6:
                # only use inverse if needed
                pass
    return labels


# ---------------- E8 / E6 / even Weyl ----------------


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


def e6_subset(roots):
    u1 = (1, 1, 1, 1, 1, 1, 1, 1)
    u2 = (1, 1, 1, 1, 1, 1, -1, -1)
    return [r for r in roots if dot(r, u1) == 0 and dot(r, u2) == 0]


def pick_generic_rho(roots, seed=7):
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
    # A·A = 8 for scaled roots
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
    # p ∘ q
    return [p[i] for i in q]


def orbit_size(gens, start=0):
    seen = {start}
    q = deque([start])
    while q:
        x = q.popleft()
        for g in gens:
            y = g[x]
            if y not in seen:
                seen.add(y)
                q.append(y)
    return len(seen)


def apply_word(root_idx, gens, word):
    cur = root_idx
    for w in word:
        if w >= 0:
            cur = gens[w][cur]
        else:
            gi = -w - 1
            # compute inverse on the fly
            g = gens[gi]
            inv = [0] * len(g)
            for i, j in enumerate(g):
                inv[j] = i
            cur = inv[cur]
    return cur


def main():
    # W33 edge labels
    points = construct_w33_points()
    edges = construct_w33_edges(points)
    edge_gens = get_w33_edge_generators(points, edges)
    if len(edge_gens) < 6:
        print("Not enough W33 generators")
        return

    edge_labels = bfs_edge_labels(edge_gens, len(edges), base=0)
    if len(edge_labels) != 240:
        print("Edge BFS did not reach all edges:", len(edge_labels))
        return

    # E8/E6 setup
    roots = build_e8_roots_scaled()
    e6 = e6_subset(roots)
    simples = simple_roots_from_positive(e6)
    if len(simples) != 6:
        print("E6 simple roots found:", len(simples))
        return

    refls = build_reflection_perms(roots, simples)

    # Build even Weyl generators as products of adjacent reflections
    # (We will build 10 generators to match W33)
    even_gens = []
    for i in range(5):
        even_gens.append(compose(refls[i], refls[i + 1]))
    even_gens.append(compose(refls[5], refls[0]))
    even_gens.append(compose(refls[0], refls[2]))
    even_gens.append(compose(refls[1], refls[3]))
    even_gens.append(compose(refls[2], refls[4]))
    even_gens.append(compose(refls[3], refls[5]))

    # Ensure we have 10 generators
    even_gens = even_gens[:10]

    # Check orbit size on roots
    orb = orbit_size(even_gens, start=0)
    print("Even Weyl orbit size on roots:", orb)

    # Try to find a generator mapping that yields bijection
    # We search random permutations of the 10 even generators
    root_base = 0
    edge_word_list = {e: word for e, (_, word) in edge_labels.items()}

    best = None
    for trial in range(200):
        perm = list(range(10))
        random.shuffle(perm)
        mapped = [even_gens[i] for i in perm]
        # compute image roots
        images = []
        for e_idx in range(240):
            word = edge_word_list[e_idx]
            r = apply_word(root_base, mapped, word)
            images.append(r)
        unique = len(set(images))
        if unique == 240:
            best = perm
            print("Found bijection with generator permutation:", perm)
            break
    if best is None:
        print("No bijection found in 200 trials.")
        # still save diagnostic
        best = list(range(10))

    # Construct explicit mapping with best perm
    mapped = [even_gens[i] for i in best]
    edge_to_root = {}
    for e_idx in range(240):
        word = edge_word_list[e_idx]
        r_idx = apply_word(root_base, mapped, word)
        edge_to_root[e_idx] = r_idx

    # Save mapping
    mapping = {
        "edge_to_root_index": edge_to_root,
        "root_coords": [list(r) for r in roots],
        "generator_permutation": best,
    }

    out_path = ROOT / "artifacts" / "explicit_bijection_even_weyl.json"
    out_path.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
