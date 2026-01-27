#!/usr/bin/env python3
"""Sage: Map E8 Coxeter 6-cycle orbits to F3^4 projective points.

Discovery:
- Build W33 from F3^4 symplectic form.
- Build W33 from E8 Coxeter 6-cycle orbits.
- Compute explicit graph isomorphism -> orbit-to-point map.
"""
from __future__ import annotations

import json
from pathlib import Path
from itertools import product

from sage.all import Graph, RootSystem, vector

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
    return proj_points, G


def build_w33_from_e8():
    R = RootSystem(['E', 8]).root_lattice()
    roots = list(R.roots())
    root_index = {tuple(r.to_vector()): i for i, r in enumerate(roots)}
    C = R.cartan_type().cartan_matrix()

    # Coxeter element: product of simple reflections in order 1..8
    W = R.weyl_group()
    c = W.simple_reflection(1)
    for i in range(2, 9):
        c = c * W.simple_reflection(i)
    c5 = c**5  # order-6 element

    # Orbits under c5
    orbit_map = {}
    orbits = []
    for idx, r in enumerate(roots):
        if idx in orbit_map:
            continue
        orb = []
        cur = r
        for _ in range(6):
            j = root_index[tuple(cur.to_vector())]
            orbit_map[j] = len(orbits)
            orb.append(j)
            cur = c5.action(cur)
        orbits.append(orb)

    # Build adjacency between orbits via orthogonality
    def ip(a, b):
        va = vector(a.to_vector())
        vb = vector(b.to_vector())
        return (va * C * vb)  # simply-laced: Cartan = Gram in simple-root basis

    edges = []
    for i in range(len(orbits)):
        for j in range(i+1, len(orbits)):
            # check if all 36 pairs orthogonal
            ok = True
            for ri in orbits[i]:
                for rj in orbits[j]:
                    if ip(roots[ri], roots[rj]) != 0:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                edges.append((i, j))

    G = Graph(edges)
    G.add_vertices(range(len(orbits)))
    return roots, orbits, G


def main():
    proj_points, G_f3 = build_w33_f3()
    roots, orbits, G_e8 = build_w33_from_e8()

    # Graph isomorphism
    iso = G_e8.is_isomorphic(G_f3, certificate=True)
    if not iso[0]:
        print("ERROR: graphs not isomorphic")
        return
    mapping = iso[1]  # dict: vertex in G_e8 -> vertex in G_f3

    # Build orbit->point mapping
    orbit_to_point = {str(o): list(proj_points[mapping[o]]) for o in range(len(orbits))}

    out = {
        "orbit_count": len(orbits),
        "mapping": orbit_to_point,
    }

    out_path = ROOT / "artifacts" / "e8_orbit_to_f3_point.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("Wrote", out_path)


if __name__ == "__main__":
    main()
