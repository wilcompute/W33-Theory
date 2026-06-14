#!/usr/bin/env python3
"""
BT991 — Local k=2,d=4 Freudenthal-Kuhn / edgewise 4-simplex template.

This is the missing local template for the corrected R3 fat tower.  Vertices are
integer barycentric coordinates (a0,...,a4) with ai>=0 and sum ai=2:
  - 5 original vertices 2e_i;
  - 10 edge midpoints e_i+e_j.

The top 4-simplices are:
  - 5 corner simplices, one at each original vertex;
  - 11 central simplices triangulating the rectified 4-simplex / hypersimplex
    Delta(2,5), via a pulling triangulation.

The result is a 16-simplex local edgewise subdivision with boundary restrictions
compatible with the k=2 edgewise subdivision of each tetrahedral boundary face.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path


def vertices() -> list[tuple[int, ...]]:
    return [tuple(c) for c in product(range(3), repeat=5) if sum(c) == 2]


VERTS = vertices()
INDEX = {v: i for i, v in enumerate(VERTS)}


def original(i: int) -> int:
    v = [0] * 5
    v[i] = 2
    return INDEX[tuple(v)]


def midpoint(i: int, j: int) -> int:
    v = [0] * 5
    v[i] = 1
    v[j] = 1
    return INDEX[tuple(v)]


def local_template() -> list[tuple[int, ...]]:
    top: list[tuple[int, ...]] = []

    # Five corner simplices.
    for i in range(5):
        top.append(tuple(sorted([original(i)] + [midpoint(i, j) for j in range(5) if j != i])))

    # Central hypersimplex Delta(2,5), pulled from midpoint (0,1).
    pull = (0, 1)
    pull_idx = midpoint(*pull)

    def octahedron_tets(coord_zero: int) -> list[tuple[int, ...]]:
        # Facet x_coord_zero=0 is Delta(2,4), an octahedron. Pull lex-first vertex.
        rem = [j for j in range(5) if j != coord_zero]
        p = tuple(rem[:2])
        pidx = midpoint(*p)
        tets = []
        for j in rem:
            if j in p:
                tri_pairs = list(combinations([x for x in rem if x != j], 2))
            else:
                tri_pairs = [tuple(sorted((j, k))) for k in rem if k != j]
            tri = [midpoint(*q) for q in tri_pairs]
            tets.append(tuple(sorted([pidx] + tri)))
        return sorted(set(tets))

    # Facets of Delta(2,5) not containing the pull vertex.
    # If pull has coordinate i=1, facet x_i=0 is absent from pull -> octahedron.
    for i in pull:
        for tet in octahedron_tets(i):
            top.append(tuple(sorted([pull_idx] + list(tet))))
    # If pull has coordinate i=0, facet x_i=1 is absent from pull -> tetrahedron.
    for i in range(5):
        if i not in pull:
            tet = [midpoint(*tuple(sorted((i, j)))) for j in range(5) if j != i]
            top.append(tuple(sorted([pull_idx] + tet)))

    return sorted(set(top))


def faces(top: list[tuple[int, ...]]) -> list[set[tuple[int, ...]]]:
    out = [set() for _ in range(5)]
    for simplex in top:
        for r in range(1, 6):
            for face in combinations(simplex, r):
                out[r - 1].add(tuple(sorted(face)))
    return out


def main() -> None:
    top = local_template()
    fs = faces(top)
    tetra_counter: Counter[tuple[int, ...]] = Counter()
    for simplex in top:
        for tet in combinations(simplex, 4):
            tetra_counter[tuple(sorted(tet))] += 1
    boundary_tetrahedra = [tet for tet, count in tetra_counter.items() if count == 1]
    internal_tetrahedra = [tet for tet, count in tetra_counter.items() if count == 2]
    bad_tetrahedra = {str(tet): count for tet, count in tetra_counter.items() if count not in {1, 2}}

    out = {
        "theorem": "BT991 local k=2,d=4 edgewise 4-simplex template",
        "vertex_coordinates": {str(i): list(v) for i, v in enumerate(VERTS)},
        "top_4simplices": [list(s) for s in top],
        "top_4simplex_count": len(top),
        "f_vector": [len(level) for level in fs],
        "euler_characteristic": sum(((-1) ** i) * len(fs[i]) for i in range(5)),
        "boundary_tetrahedra": len(boundary_tetrahedra),
        "internal_tetrahedra": len(internal_tetrahedra),
        "bad_tetrahedra": bad_tetrahedra,
        "boundary_restriction_expected_tetrahedra": 5 * 8,
        "reading": "The template is a genuine 4-ball subdivision: 15 vertices, 16 top cells, 40 boundary tetrahedra, 20 internal tetrahedra, Euler characteristic 1.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt991_local_4simplex_edgewise_template.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
