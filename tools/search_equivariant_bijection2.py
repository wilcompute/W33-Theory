#!/usr/bin/env python3
"""Search for PSp(4,3) subgroup in W(E8) acting transitively on 240 roots.

We focus on order-3 generators to match the edge generators subset.
"""
from __future__ import annotations

import random
from collections import deque
from itertools import product, combinations
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]

# E8 roots and reflections

def build_e8_roots_scaled():
    roots = []
    for i in range(8):
        for j in range(i + 1, 8):
            for s1 in (2, -2):
                for s2 in (2, -2):
                    r = [0] * 8
                    r[i] = s1
                    r[j] = s2
                    roots.append(tuple(r))
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
            j = i
            l = 0
            while not visited[j]:
                visited[j] = True
                j = p[j]
                l += 1
            if l > 0:
                order = order * l // np.gcd(order, l)
    return order


def group_order(gens, limit=30000):
    gens = list(gens)
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


def main():
    roots = build_e8_roots_scaled()
    simples = simple_roots_from_positive(roots)
    refls = build_reflection_perms(roots, simples)

    # pool: reflections and products of two reflections
    pool = list(refls)
    for i in range(len(refls)):
        for j in range(i + 1, len(refls)):
            pool.append(compose(refls[i], refls[j]))

    # precompute order 3 elements
    order3 = []
    for p in pool:
        if perm_order(p) == 3:
            order3.append(p)

    print("Order-3 pool size:", len(order3))

    # random search for 3 generators of order 3 with subgroup order 25920 and orbit 240
    for trial in range(1000):
        gens = random.sample(order3, 3)
        ord_val = group_order(gens, limit=26000)
        if ord_val == 25920:
            orb = orbit_size(gens)
            print("Trial", trial, "order 25920, orbit", orb)
            if orb == 240:
                print("Found transitive subgroup!")
                out = {
                    "generators": [list(g) for g in gens],
                }
                out_path = ROOT / "artifacts" / "psp43_in_we8.json"
                out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
                print("Wrote", out_path)
                return

    print("No transitive subgroup found in 1000 trials")


if __name__ == "__main__":
    main()
