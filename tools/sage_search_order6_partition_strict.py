#!/usr/bin/env python3
"""Sage: deeper search for order-6 partition of E8 roots into 40 orbits.

We test random order-6 elements and see if orbit graph is W33.
This is heavier: we search longer and prune early.
"""
from __future__ import annotations

import json
import random
from itertools import product
from pathlib import Path

from sage.all import RootSystem, Graph

ROOT = Path(__file__).resolve().parents[1]


def build_w33_f3():
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
    n = len(proj_points)
    for i in range(n):
        for j in range(i+1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    G = Graph(edges)
    G.add_vertices(range(n))
    return G


def main():
    R = RootSystem(['E', 8]).root_lattice()
    W = R.weyl_group()
    roots = list(R.roots())
    root_index = {tuple(r.to_vector()): i for i, r in enumerate(roots)}
    C = R.cartan_type().cartan_matrix()

    G_w33 = build_w33_f3()

    random.seed(0)
    max_iter = 1000

    for it in range(max_iter):
        # random word length
        length = random.randint(6, 30)
        w = W.simple_reflection(random.randint(1, 8))
        for _ in range(length):
            w = w * W.simple_reflection(random.randint(1, 8))

        if w.order() != 6:
            continue

        # compute orbits under w
        orbit_map = {}
        orbits = []
        ok = True
        for idx, r in enumerate(roots):
            if idx in orbit_map:
                continue
            orb = []
            cur = r
            for _ in range(6):
                j = root_index[tuple(cur.to_vector())]
                if j in orbit_map:
                    ok = False
                    break
                orbit_map[j] = len(orbits)
                orb.append(j)
                cur = w.action(cur)
            if not ok or len(set(orb)) != 6:
                ok = False
                break
            orbits.append(orb)
        if not ok or len(orbits) != 40:
            continue

        # build orbit graph by orthogonality (fast prune by degree count)
        def ip(a, b):
            va = a.to_vector()
            vb = b.to_vector()
            return (va * C * vb)

        edges = []
        deg = [0]*40
        for i in range(40):
            for j in range(i+1, 40):
                ok2 = True
                for ri in orbits[i]:
                    for rj in orbits[j]:
                        if ip(roots[ri], roots[rj]) != 0:
                            ok2 = False
                            break
                    if not ok2:
                        break
                if ok2:
                    edges.append((i, j))
                    deg[i] += 1
                    deg[j] += 1
        # quick degree prune for SRG(40,12,2,4)
        if any(d != 12 for d in deg):
            continue

        G = Graph(edges)
        G.add_vertices(range(len(orbits)))
        if G.is_isomorphic(G_w33):
            out = {
                "found": True,
                "iteration": it,
                "word_length": length,
                "element_order": int(w.order()),
            }
            out_path = ROOT / "artifacts" / "e8_order6_partition_strict_found.json"
            out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
            print("Found at iter", it)
            print("Wrote", out_path)
            return

    out = {"found": False, "iterations": max_iter}
    out_path = ROOT / "artifacts" / "e8_order6_partition_strict_found.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Not found")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
