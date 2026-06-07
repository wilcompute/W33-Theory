#!/usr/bin/env python3
"""
BT486: BC Ring Boundary Torus Theorem

NetworkX + exact rational-rank verifier for the 30-tetrahedron
Boerdijk-Coxeter ring carrier suggested by BT485.

Model:
    vertices = Z/30Z
    tetrahedra T_i = {i, i+1, i+2, i+3}
    graph edges = all pairs contained in some T_i
                = Circ(30; ±1, ±2, ±3) = C_30^3

The key structural result is not a count match: the boundary complex of
this 30-tetrahedron ring is a closed triangulated torus with
    (V,E,F) = (30,90,60), chi=0, H=(1,2,1).

This turns the BT485 BC-helix/600-cell ring into a literal toroidal
substrate carrier parallel to the Csaszar/Szilassi genus-one layer.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import networkx as nx
from networkx.algorithms import isomorphism as iso


N = 30
STEPS = (1, 2, 3)


def canon_edge(a: int, b: int) -> tuple[int, int]:
    a %= N
    b %= N
    return (a, b) if a < b else (b, a)


def step_edges(step: int) -> set[tuple[int, int]]:
    return {canon_edge(i, i + step) for i in range(N)}


def step_graph(step: int) -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(N))
    g.add_edges_from(step_edges(step))
    return g


def ring_graph() -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(N))
    for s in STEPS:
        g.add_edges_from(step_edges(s))
    return g


def tetrahedra() -> list[tuple[int, int, int, int]]:
    return [tuple(sorted((i + j) % N for j in range(4))) for i in range(N)]


def rational_rank(rows: list[list[int]]) -> int:
    """Exact rank over Q by fraction Gaussian elimination."""
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
                factor = mat[r][col]
                mat[r] = [a - factor * b for a, b in zip(mat[r], mat[rank])]
        rank += 1
        col += 1
    return rank


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(col) for col in zip(*matrix)] if matrix else []


def main() -> dict:
    g = ring_graph()
    assert g.number_of_nodes() == 30
    assert g.number_of_edges() == 90
    assert set(dict(g.degree()).values()) == {6}

    # Step-shell decomposition: gcd(30,s) cycles of length 30/gcd(30,s).
    step_decomp = {}
    cycle_components = 0
    for s in STEPS:
        gs = step_graph(s)
        comps = sorted(len(c) for c in nx.connected_components(gs))
        expected_count = math.gcd(N, s)
        expected_len = N // expected_count
        assert nx.number_connected_components(gs) == expected_count
        assert comps == [expected_len] * expected_count
        assert set(dict(gs.degree()).values()) == {2}
        assert gs.number_of_edges() == N
        step_decomp[str(s)] = {
            "components": expected_count,
            "cycle_length": expected_len,
            "notation": f"{expected_count}C_{expected_len}",
            "edges": N,
        }
        cycle_components += expected_count

    assert cycle_components == 6
    assert 2 * cycle_components == 12

    # Maximal K4 cliques are exactly the 30 consecutive tetrahedra.
    tets = tetrahedra()
    maximal_cliques = [tuple(sorted(c)) for c in nx.find_cliques(g)]
    assert len(maximal_cliques) == 30
    assert all(len(c) == 4 for c in maximal_cliques)
    assert set(maximal_cliques) == set(tets)

    # Incidence of graph edges inside tetrahedra.
    edges = sorted(g.edges())
    edge_index = {e: i for i, e in enumerate(edges)}
    edge_tet_count: Counter[tuple[int, int]] = Counter()
    for t in tets:
        assert g.subgraph(t).number_of_edges() == 6
        for e in combinations(t, 2):
            edge_tet_count[canon_edge(*e)] += 1

    assert len(edge_tet_count) == 90
    edge_incidence_total = sum(edge_tet_count.values())
    assert edge_incidence_total == 30 * 6 == 180

    edge_profile_by_step = {}
    for s in STEPS:
        profile = Counter(edge_tet_count[e] for e in step_edges(s))
        assert profile == Counter({4 - s: 30})
        edge_profile_by_step[str(s)] = {str(k): v for k, v in sorted(profile.items())}

    # Tetrahedron face incidences. Shared faces are internal; single faces are boundary.
    tri_tet_count: Counter[tuple[int, int, int]] = Counter()
    for t in tets:
        for tri in combinations(t, 3):
            tri_tet_count[tuple(sorted(tri))] += 1

    assert len(tri_tet_count) == 90
    tri_profile = Counter(tri_tet_count.values())
    assert tri_profile == Counter({1: 60, 2: 30})

    boundary_faces = sorted(tri for tri, c in tri_tet_count.items() if c == 1)
    shared_faces = sorted(tri for tri, c in tri_tet_count.items() if c == 2)
    assert len(boundary_faces) == 60
    assert len(shared_faces) == 30

    boundary_edges: set[tuple[int, int]] = set()
    boundary_edge_face_count: Counter[tuple[int, int]] = Counter()
    for tri in boundary_faces:
        for e in combinations(tri, 2):
            ce = canon_edge(*e)
            boundary_edges.add(ce)
            boundary_edge_face_count[ce] += 1

    assert len(boundary_edges) == 90
    assert Counter(boundary_edge_face_count.values()) == Counter({2: 90})

    V = N
    E = len(boundary_edges)
    F = len(boundary_faces)
    euler = V - E + F
    assert (V, E, F, euler) == (30, 90, 60, 0)

    # Boundary chain complex ranks over Q.
    bedges = sorted(boundary_edges)
    bindex = {e: i for i, e in enumerate(bedges)}

    d1 = [[0 for _ in bedges] for _ in range(V)]
    for j, (a, b) in enumerate(bedges):
        d1[a][j] = -1
        d1[b][j] = 1

    d2 = [[0 for _ in boundary_faces] for _ in bedges]
    for j, (a, b, c) in enumerate(boundary_faces):
        # Oriented boundary of sorted simplex [a,b,c]: [b,c] - [a,c] + [a,b].
        for x, y, coef in ((b, c, 1), (a, c, -1), (a, b, 1)):
            d2[bindex[canon_edge(x, y)]][j] += coef

    # Check d1*d2 = 0 exactly.
    for r in range(V):
        for c in range(F):
            assert sum(d1[r][k] * d2[k][c] for k in range(E)) == 0

    rank_d1 = rational_rank(d1)
    rank_d2 = rational_rank(d2)
    assert rank_d1 == 29
    assert rank_d2 == 59

    betti = {
        "H0": V - rank_d1,
        "H1": E - rank_d1 - rank_d2,
        "H2": F - rank_d2,
    }
    assert betti == {"H0": 1, "H1": 2, "H2": 1}

    # Cell adjacency through shared faces is C30.
    cell_adj = nx.Graph()
    cell_adj.add_nodes_from(range(N))
    tet_sets = [set(t) for t in tets]
    for i, j in combinations(range(N), 2):
        if len(tet_sets[i] & tet_sets[j]) == 3:
            cell_adj.add_edge(i, j)
    assert cell_adj.number_of_edges() == 30
    assert set(dict(cell_adj.degree()).values()) == {2}
    assert nx.is_isomorphic(cell_adj, nx.cycle_graph(30))

    # Full graph automorphism group: dihedral D30, order 60.
    aut_count = sum(1 for _ in iso.GraphMatcher(g, g).isomorphisms_iter())
    assert aut_count == 60

    results = {
        "theorem": "BT486 BC Ring Boundary Torus Theorem",
        "model": "30 tetrahedra T_i={i,i+1,i+2,i+3} on Z/30Z",
        "one_skeleton": "Circ(30; ±1, ±2, ±3) = C_30^3",
        "step_decomposition": step_decomp,
        "cycle_components": cycle_components,
        "oriented_cycle_sectors": 2 * cycle_components,
        "graph_parameters": {
            "vertices": g.number_of_nodes(),
            "edges": g.number_of_edges(),
            "degree": 6,
            "automorphism_order": aut_count,
        },
        "tetrahedra": {
            "maximal_K4_count": len(maximal_cliques),
            "cell_adjacency": "C30",
        },
        "incidence": {
            "edge_tetrahedron_total": edge_incidence_total,
            "edge_tetrahedron_by_step": edge_profile_by_step,
            "triangle_tetrahedron_profile": {str(k): v for k, v in sorted(tri_profile.items())},
            "shared_internal_faces": len(shared_faces),
            "boundary_faces": len(boundary_faces),
            "boundary_edge_face_profile": {str(k): v for k, v in sorted(Counter(boundary_edge_face_count.values()).items())},
        },
        "boundary_complex": {
            "V": V,
            "E": E,
            "F": F,
            "euler_characteristic": euler,
            "rank_d1": rank_d1,
            "rank_d2": rank_d2,
            "betti_Q": betti,
        },
        "substrate_reading": {
            "six_cycle_components": "positive G2 root selector",
            "twelve_oriented_cycle_sectors": "G2 root count / CS level k=12",
            "boundary_torus": "literal genus-one carrier from the 600-cell/BC ring layer",
            "triangulated_torus_law": "V=30, E=3V=90, F=2V=60, chi=0",
            "cell_cycle": "30 tetrahedra close as C30 in the 600-cell ring",
        },
    }

    out = Path("data/PART_BT486_BC_RING_BOUNDARY_TORUS_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
