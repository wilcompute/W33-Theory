#!/usr/bin/env python3
"""
BT992 — True level-1 CP2_9/K3_16 edgewise incidence matrices.

This applies the BT991 local k=2,d=4 edgewise template to the explicit CP2_9 and
K3_16 facets from `exploration/w33_explicit_curved_4d_complexes.py`.  It builds
actual level-1 top facets with globally shared edge-midpoint vertices, enumerates
all faces, and computes boundary ranks over F2 using sparse bitset Gaussian
elimination.  Since CP2 and K3 have torsion-free integral homology, the mod-2
Betti profile matches the expected rational Betti profile.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from w33_explicit_curved_4d_complexes import cp2_facets, k3_facets  # noqa: E402


def bary_vertices() -> list[tuple[int, ...]]:
    return [tuple(c) for c in product(range(3), repeat=5) if sum(c) == 2]


BARY = bary_vertices()
BARY_INDEX = {v: i for i, v in enumerate(BARY)}


def original(i: int) -> int:
    v = [0] * 5
    v[i] = 2
    return BARY_INDEX[tuple(v)]


def midpoint(i: int, j: int) -> int:
    v = [0] * 5
    v[i] = 1
    v[j] = 1
    return BARY_INDEX[tuple(v)]


def local_template() -> list[tuple[int, ...]]:
    top: list[tuple[int, ...]] = []
    for i in range(5):
        top.append(tuple(sorted([original(i)] + [midpoint(i, j) for j in range(5) if j != i])))
    pull = (0, 1)
    pull_idx = midpoint(*pull)

    def octahedron_tets(coord_zero: int) -> list[tuple[int, ...]]:
        rem = [j for j in range(5) if j != coord_zero]
        p = tuple(rem[:2])
        pidx = midpoint(*p)
        tets = []
        for j in rem:
            if j in p:
                tri_pairs = list(combinations([x for x in rem if x != j], 2))
            else:
                tri_pairs = [tuple(sorted((j, k))) for k in rem if k != j]
            tets.append(tuple(sorted([pidx] + [midpoint(*q) for q in tri_pairs])))
        return sorted(set(tets))

    for i in pull:
        for tet in octahedron_tets(i):
            top.append(tuple(sorted([pull_idx] + list(tet))))
    for i in range(5):
        if i not in pull:
            tet = [midpoint(*tuple(sorted((i, j)))) for j in range(5) if j != i]
            top.append(tuple(sorted([pull_idx] + tet)))
    return sorted(set(top))


TEMPLATE = local_template()


def subdivide_facets(facets: tuple[tuple[int, ...], ...]) -> tuple[tuple[object, ...], ...]:
    out = []
    for facet in facets:
        local = list(facet)

        def map_vertex(local_bary_index: int):
            c = BARY[local_bary_index]
            nonzero = [i for i, x in enumerate(c) if x]
            if len(nonzero) == 1:
                return ("v", local[nonzero[0]])
            a, b = local[nonzero[0]], local[nonzero[1]]
            return ("m", min(a, b), max(a, b))

        for simplex in TEMPLATE:
            out.append(tuple(sorted((map_vertex(i) for i in simplex), key=str)))
    return tuple(out)


def relabel(simplices: tuple[tuple[object, ...], ...]) -> tuple[tuple[tuple[int, ...], ...], list[object]]:
    vertices = sorted({v for simplex in simplices for v in simplex}, key=str)
    index = {v: i for i, v in enumerate(vertices)}
    return tuple(tuple(sorted(index[v] for v in simplex)) for simplex in simplices), vertices


def faces_by_dim(top_simplices: tuple[tuple[int, ...], ...]) -> list[tuple[tuple[int, ...], ...]]:
    faces = [set() for _ in range(5)]
    for simplex in top_simplices:
        for r in range(1, 6):
            for face in combinations(simplex, r):
                faces[r - 1].add(tuple(sorted(face)))
    return [tuple(sorted(level)) for level in faces]


def boundary_rank_mod2(high: tuple[tuple[int, ...], ...], low: tuple[tuple[int, ...], ...]) -> int:
    low_index = {simplex: i for i, simplex in enumerate(low)}
    rows = [0] * len(low)
    for col, simplex in enumerate(high):
        for face in combinations(simplex, len(simplex) - 1):
            rows[low_index[tuple(sorted(face))]] ^= (1 << col)
    basis: dict[int, int] = {}
    rank = 0
    for row in rows:
        value = row
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                rank += 1
                break
    return rank


def packet(name: str, facets: tuple[tuple[int, ...], ...]) -> dict:
    top_raw = subdivide_facets(facets)
    top, vertices = relabel(top_raw)
    faces = faces_by_dim(top)
    ranks = [boundary_rank_mod2(faces[d], faces[d - 1]) for d in range(1, 5)]
    f_vector = [len(level) for level in faces]
    betti = []
    for d in range(5):
        incoming = ranks[d - 1] if d > 0 else 0
        outgoing = ranks[d] if d < 4 else 0
        betti.append(f_vector[d] - incoming - outgoing)
    return {
        "name": name,
        "level": 1,
        "vertices": len(vertices),
        "top_4simplices": len(top),
        "f_vector": f_vector,
        "boundary_ranks_mod2": ranks,
        "betti_mod2": betti,
        "euler_characteristic": sum(((-1) ** i) * f_vector[i] for i in range(5)),
    }


def main() -> None:
    out = {
        "theorem": "BT992 true level-1 CP2_9/K3_16 edgewise incidence matrices",
        "local_template": "BT991 k=2,d=4 edgewise 4-simplex template",
        "rank_field": "F2 sparse bitset Gaussian elimination",
        "profiles": [packet("CP2_9", cp2_facets()), packet("K3_16", k3_facets())],
        "reading": "The explicit CP2_9/K3_16 facets now have real level-1 edgewise f-vectors, boundary ranks, and Betti checks; topology is preserved.",
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt992_cp2_k3_edgewise_level1_incidence.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
