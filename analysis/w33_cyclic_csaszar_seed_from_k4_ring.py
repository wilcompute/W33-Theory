#!/usr/bin/env python3
"""
BT488: Cyclic Csaszar Seed from Consecutive K4 Ring

This extracts the n=7 endpoint of BT487.

For n=7:
    T_i = {i, i+1, i+2, i+3} in Z/7Z.

Because C_7^3 is the complete graph K_7, the boundary complex has:
    V=7, E=21, F=14, chi=0, betti=(1,2,1).

Thus the same consecutive-K4 ring law whose n=30 case models the
600-cell/BC 30-ring has a minimal nondegenerate endpoint which is the
Csaszar K7 torus carrier.

The face-preserving automorphism group of this cyclic triangulation has
order 42 = 6*7 = g2*Phi6.
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import networkx as nx
from networkx.algorithms import isomorphism as iso


def rational_rank(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    mat = [[Fraction(x) for x in row] for row in rows]
    m, n = len(mat), len(mat[0])
    rank = 0
    col = 0
    while rank < m and col < n:
        pivot = None
        for r in range(rank, m):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            col += 1
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        pv = mat[rank][col]
        mat[rank] = [x / pv for x in mat[rank]]
        for r in range(m):
            if r != rank and mat[r][col] != 0:
                fac = mat[r][col]
                mat[r] = [a - fac * b for a, b in zip(mat[r], mat[rank])]
        rank += 1
        col += 1
    return rank


def canon_edge(n: int, a: int, b: int) -> tuple[int, int]:
    a %= n
    b %= n
    return (a, b) if a < b else (b, a)


def ring_complex(n: int):
    tets = [tuple(sorted((i + j) % n for j in range(4))) for i in range(n)]
    tri_tet_count: Counter[tuple[int, int, int]] = Counter()
    for t in tets:
        for tri in combinations(t, 3):
            tri_tet_count[tuple(sorted(tri))] += 1
    boundary_faces = sorted(tri for tri, c in tri_tet_count.items() if c == 1)
    boundary_edges: set[tuple[int, int]] = set()
    for tri in boundary_faces:
        for e in combinations(tri, 2):
            boundary_edges.add(canon_edge(n, *e))
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(boundary_edges)
    return tets, boundary_faces, sorted(boundary_edges), g


def betti_of_boundary(n: int, faces: list[tuple[int, int, int]], edges: list[tuple[int, int]]):
    bindex = {e: i for i, e in enumerate(edges)}
    d1 = [[0 for _ in edges] for _ in range(n)]
    for j, (a, b) in enumerate(edges):
        d1[a][j] = -1
        d1[b][j] = 1
    d2 = [[0 for _ in faces] for _ in edges]
    for j, (a, b, c) in enumerate(faces):
        for x, y, coef in ((b, c, 1), (a, c, -1), (a, b, 1)):
            d2[bindex[canon_edge(n, x, y)]][j] += coef
    for r in range(n):
        for c in range(len(faces)):
            assert sum(d1[r][k] * d2[k][c] for k in range(len(edges))) == 0
    r1 = rational_rank(d1)
    r2 = rational_rank(d2)
    return {
        "rank_d1": r1,
        "rank_d2": r2,
        "betti_Q": {
            "H0": n - r1,
            "H1": len(edges) - r1 - r2,
            "H2": len(faces) - r2,
        },
    }


def complex_automorphism_order(g: nx.Graph, faces: list[tuple[int, int, int]]) -> int:
    face_set = {frozenset(f) for f in faces}
    count = 0
    for p in iso.GraphMatcher(g, g).isomorphisms_iter():
        if all(frozenset(p[x] for x in f) in face_set for f in faces):
            count += 1
    return count


def main() -> dict:
    q, g2, phi6 = 3, 6, 7

    tets7, faces7, edges7, g7 = ring_complex(7)
    assert g7.number_of_nodes() == 7
    assert g7.number_of_edges() == 21
    assert nx.is_isomorphic(g7, nx.complete_graph(7))
    assert len(faces7) == 14
    assert len(tets7) == 7
    b7 = betti_of_boundary(7, faces7, edges7)
    assert b7 == {"rank_d1": 6, "rank_d2": 13, "betti_Q": {"H0": 1, "H1": 2, "H2": 1}}
    aut7 = complex_automorphism_order(g7, faces7)
    assert aut7 == 42

    # The seven tetrahedra have 28 face incidences. Exactly 7 faces are internal
    # and 14 are boundary. This mirrors 28=v-k and the Csaszar F=14 shell.
    tri_count7: Counter[tuple[int, int, int]] = Counter()
    for t in tets7:
        for tri in combinations(t, 3):
            tri_count7[tuple(sorted(tri))] += 1
    assert Counter(tri_count7.values()) == Counter({1: 14, 2: 7})
    assert sum(tri_count7.values()) == 28

    # Compare to n=30 endpoint.
    _, faces30, edges30, g30 = ring_complex(30)
    b30 = betti_of_boundary(30, faces30, edges30)
    assert g30.number_of_nodes() == 30
    assert g30.number_of_edges() == 90
    assert len(faces30) == 60
    assert b30["betti_Q"] == {"H0": 1, "H1": 2, "H2": 1}
    aut30 = complex_automorphism_order(g30, faces30)
    assert aut30 == 60

    results = {
        "theorem": "BT488 Cyclic Csaszar Seed from Consecutive K4 Ring",
        "construction": "n=7 endpoint of T_i={i,i+1,i+2,i+3} on Z/nZ",
        "n7_csaszar_seed": {
            "one_skeleton": "C_7^3 = K_7",
            "f_vector": [7, 21, 14],
            "euler_characteristic": 0,
            "rank_d1": b7["rank_d1"],
            "rank_d2": b7["rank_d2"],
            "betti_Q": b7["betti_Q"],
            "tetrahedra": len(tets7),
            "total_tetrahedron_face_incidences": 28,
            "boundary_faces": 14,
            "internal_shared_faces": 7,
            "face_preserving_automorphism_order": aut7,
            "automorphism_factorization": "42 = 6*7 = g2*Phi6",
            "boundary_faces_list": faces7,
        },
        "n30_bc_ring_endpoint": {
            "one_skeleton": "C_30^3 = Circ(30; ±1, ±2, ±3)",
            "f_vector": [30, 90, 60],
            "euler_characteristic": 0,
            "betti_Q": b30["betti_Q"],
            "face_preserving_automorphism_order": aut30,
            "automorphism_factorization": "60 = 2*30 = 2*h(E8)",
        },
        "bridge": {
            "same_law": "T_i={i,i+1,i+2,i+3}",
            "minimal_endpoint": "n=7 gives Csaszar/K7 torus carrier",
            "E8_endpoint": "n=30 gives 600-cell BC ring torus carrier",
            "torus_preserved": "both endpoints have betti_Q=(1,2,1)",
        },
        "substrate_reading": {
            "42": "g2*Phi6 = positive/negative G2 half-cycle times Fano heptad",
            "28": "seven K4 face packets = 7*4 = v-k",
            "14": "boundary face shell = dim(G2)",
            "21": "K7 edge shell = g1",
        },
    }

    out = Path("data/PART_BT488_CYCLIC_CSASZAR_SEED_FROM_K4_RING_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
