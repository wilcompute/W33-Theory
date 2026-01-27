#!/usr/bin/env python3
"""Search for an equivariant W33 edge -> E8 root bijection.

We try to find a small generating set for the edge group (PSp(4,3))
then match it to a subgroup of W(E8) by sampling elements with the
same order/cycle structure, and verifying the generated subgroup has
order 25920 and is transitive on 240 roots.
"""
from __future__ import annotations

import random
from collections import deque, Counter
from itertools import product, combinations
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
            edge_gens.append(tuple(eperm))
    return edge_gens

# ---------------- E8 reflection group ----------------

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
        perms.append(tuple(perm))
    return perms


def compose(p, q):
    return tuple(p[i] for i in q)


def perm_order(p):
    n = len(p)
    visited = [False] * n
    order = 1
    for i in range(n):
        if not visited[i]:
            # cycle length
            j = i
            l = 0
            while not visited[j]:
                visited[j] = True
                j = p[j]
                l += 1
            # lcm
            if l > 0:
                order = order * l // np.gcd(order, l)
    return order


def group_order(gens, limit=30000):
    gens = list(gens)
    # add inverses
    invs = []
    for g in gens:
        inv = [0] * len(g)
        for i, j in enumerate(g):
            inv[j] = i
        invs.append(tuple(inv))
    gens_all = gens + invs

    id_perm = tuple(range(len(gens[0])))
    seen = {id_perm}
    q = deque([id_perm])
    while q:
        p = q.popleft()
        for g in gens_all:
            comp = compose(g, p)
            if comp not in seen:
                seen.add(comp)
                if len(seen) > limit:
                    return None
                q.append(comp)
    return len(seen)


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

# ---------------- Main search ----------------

def main():
    points = construct_w33_points()
    edges = construct_w33_edges(points)
    edge_gens = get_w33_edge_generators(points, edges)
    print("W33 generators:", len(edge_gens))

    # compute orders and cycle structures for edge generators
    edge_orders = [perm_order(g) for g in edge_gens]
    print("Edge generator orders:", edge_orders)

    # try to find a small generating subset of size 3
    best_subset = None
    for comb in combinations(range(len(edge_gens)), 3):
        gens = [edge_gens[i] for i in comb]
        ord_val = group_order(gens, limit=26000)
        if ord_val == 25920:
            best_subset = comb
            print("Found edge generating subset:", comb)
            break
    if best_subset is None:
        print("No 3-gen subset found; using first 4 generators")
        best_subset = (0, 1, 2, 3)

    edge_subgens = [edge_gens[i] for i in best_subset]
    edge_sub_orders = [perm_order(g) for g in edge_subgens]
    print("Edge subgenerator orders:", edge_sub_orders)

    # build W(E8) reflection permutations
    roots = build_e8_roots_scaled()
    simples = simple_roots_from_positive(roots)
    refls = build_reflection_perms(roots, simples)

    # build a pool of candidate elements: reflections and products
    pool = list(refls)
    for i in range(len(refls)):
        for j in range(i + 1, len(refls)):
            pool.append(compose(refls[i], refls[j]))
    random.shuffle(pool)

    # bucket pool by order
    order_buckets = {}
    for p in pool[:400]:
        o = perm_order(p)
        order_buckets.setdefault(o, []).append(p)

    # attempt to match edge generator orders
    candidates = []
    for o in edge_sub_orders:
        candidates.append(order_buckets.get(o, []))

    if any(len(c) == 0 for c in candidates):
        print("Not enough candidates with matching orders.")
        return

    # random search for matching subgroup
    for trial in range(200):
        gens = [random.choice(c) for c in candidates]
        ord_val = group_order(gens, limit=26000)
        if ord_val == 25920:
            orb = orbit_size(gens)
            print("Found subgroup order 25920, orbit size", orb)
            # build mapping via BFS word labels
            # BFS on edge subgroup to label edges
            edge_labels = {0: ()}
            q = deque([0])
            while q:
                cur = q.popleft()
                word = edge_labels[cur]
                for gi, g in enumerate(edge_subgens):
                    nxt = g[cur]
                    if nxt not in edge_labels:
                        edge_labels[nxt] = word + (gi,)
                        q.append(nxt)
            # Apply same words to root subgroup
            root_base = 0
            mapping = {}
            for e, word in edge_labels.items():
                r = root_base
                for gi in word:
                    r = gens[gi][r]
                mapping[e] = r

            # Verify bijection
            if len(set(mapping.values())) == 240:
                print("Equivariant bijection found!")
                out = {
                    "edge_to_root_index": mapping,
                    "edge_generators": list(best_subset),
                    "root_generators_orders": edge_sub_orders,
                }
                out_path = ROOT / "artifacts" / "equivariant_bijection.json"
                out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
                print("Wrote", out_path)
                return

    print("No equivariant bijection found in search.")


if __name__ == "__main__":
    main()
