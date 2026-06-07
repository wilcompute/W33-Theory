#!/usr/bin/env python3
"""
BT487: General Consecutive K4 Ring Torus Law

This generalizes BT486.

For n >= 7, define a cyclic consecutive tetrahedron ring:
    V_n = Z/nZ
    T_i = {i, i+1, i+2, i+3}

The one-skeleton is the circulant graph
    C_n^3 = Circ(n; ±1, ±2, ±3).

The boundary of the tetrahedron ring is a closed triangulated torus with:
    V = n,
    E = 3n,
    F = 2n,
    chi = 0,
    betti_Q = (1,2,1).

The critical bridge is n=7:
    C_7^3 = K_7,
    (V,E,F) = (7,21,14),
which is exactly the Csaszar polyhedron f-vector / K7 torus carrier.

The BT485/BT486 600-cell BC ring is n=30:
    (V,E,F)=(30,90,60),
    step decomposition C30 + 2C15 + 3C10,
    six unoriented step components and twelve oriented sectors.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import networkx as nx


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
                factor = mat[r][col]
                mat[r] = [a - factor * b for a, b in zip(mat[r], mat[rank])]
        rank += 1
        col += 1
    return rank


def canon_edge(n: int, a: int, b: int) -> tuple[int, int]:
    a %= n
    b %= n
    return (a, b) if a < b else (b, a)


def step_edges(n: int, step: int) -> set[tuple[int, int]]:
    return {canon_edge(n, i, i + step) for i in range(n)}


def ring_graph(n: int) -> nx.Graph:
    g = nx.Graph()
    g.add_nodes_from(range(n))
    for s in (1, 2, 3):
        g.add_edges_from(step_edges(n, s))
    return g


def tetrahedra(n: int) -> list[tuple[int, int, int, int]]:
    return [tuple(sorted((i + j) % n for j in range(4))) for i in range(n)]


def analyze_n(n: int) -> dict:
    assert n >= 7, "n>=7 is the nondegenerate torus range for this verifier"
    g = ring_graph(n)
    tets = tetrahedra(n)

    # For n>=7, the three step shells are disjoint and each has n edges.
    assert g.number_of_nodes() == n
    assert g.number_of_edges() == 3 * n
    assert set(dict(g.degree()).values()) == {6}

    maximal_cliques = [tuple(sorted(c)) for c in nx.find_cliques(g)]
    assert len(maximal_cliques) == n
    assert all(len(c) == 4 for c in maximal_cliques)
    assert set(maximal_cliques) == set(tets)

    tri_tet_count: Counter[tuple[int, int, int]] = Counter()
    for t in tets:
        for tri in combinations(t, 3):
            tri_tet_count[tuple(sorted(tri))] += 1

    tri_profile = Counter(tri_tet_count.values())
    assert tri_profile == Counter({1: 2 * n, 2: n})

    boundary_faces = sorted(tri for tri, c in tri_tet_count.items() if c == 1)
    boundary_edges: set[tuple[int, int]] = set()
    boundary_edge_face_count: Counter[tuple[int, int]] = Counter()
    for tri in boundary_faces:
        for e in combinations(tri, 2):
            ce = canon_edge(n, *e)
            boundary_edges.add(ce)
            boundary_edge_face_count[ce] += 1

    V = n
    E = len(boundary_edges)
    F = len(boundary_faces)
    assert (V, E, F) == (n, 3 * n, 2 * n)
    assert V - E + F == 0
    assert Counter(boundary_edge_face_count.values()) == Counter({2: 3 * n})

    bedges = sorted(boundary_edges)
    bindex = {e: i for i, e in enumerate(bedges)}
    d1 = [[0 for _ in bedges] for _ in range(V)]
    for j, (a, b) in enumerate(bedges):
        d1[a][j] = -1
        d1[b][j] = 1

    d2 = [[0 for _ in boundary_faces] for _ in bedges]
    for j, (a, b, c) in enumerate(boundary_faces):
        for x, y, coef in ((b, c, 1), (a, c, -1), (a, b, 1)):
            d2[bindex[canon_edge(n, x, y)]][j] += coef

    for r in range(V):
        for c in range(F):
            assert sum(d1[r][k] * d2[k][c] for k in range(E)) == 0

    rank_d1 = rational_rank(d1)
    rank_d2 = rational_rank(d2)
    assert rank_d1 == n - 1
    assert rank_d2 == 2 * n - 1
    betti = {
        "H0": V - rank_d1,
        "H1": E - rank_d1 - rank_d2,
        "H2": F - rank_d2,
    }
    assert betti == {"H0": 1, "H1": 2, "H2": 1}

    step_decomp = {}
    component_total = 0
    for s in (1, 2, 3):
        gs = nx.Graph()
        gs.add_nodes_from(range(n))
        gs.add_edges_from(step_edges(n, s))
        components = math.gcd(n, s)
        cycle_len = n // components
        assert nx.number_connected_components(gs) == components
        assert sorted(len(c) for c in nx.connected_components(gs)) == [cycle_len] * components
        component_total += components
        step_decomp[str(s)] = {
            "components": components,
            "cycle_length": cycle_len,
            "notation": f"{components}C_{cycle_len}",
        }

    return {
        "n": n,
        "one_skeleton_edges": g.number_of_edges(),
        "one_skeleton_degree": 6,
        "is_complete_graph": g.number_of_edges() == n * (n - 1) // 2,
        "f_vector_boundary": [V, E, F],
        "euler_characteristic": 0,
        "rank_d1": rank_d1,
        "rank_d2": rank_d2,
        "betti_Q": betti,
        "step_decomposition": step_decomp,
        "step_component_total": component_total,
        "oriented_step_sector_total": 2 * component_total,
    }


def main() -> dict:
    sample_ns = [7, 8, 9, 10, 12, 15, 21, 24, 30, 40]
    samples = {str(n): analyze_n(n) for n in sample_ns}

    # Wider sweep certifies the symbolic rank law over a large range.
    sweep = {str(n): analyze_n(n)["betti_Q"] for n in range(7, 61)}
    assert all(b == {"H0": 1, "H1": 2, "H2": 1} for b in sweep.values())

    assert samples["7"]["is_complete_graph"] is True
    assert samples["7"]["f_vector_boundary"] == [7, 21, 14]
    assert samples["30"]["f_vector_boundary"] == [30, 90, 60]
    assert samples["30"]["step_component_total"] == 6
    assert samples["30"]["oriented_step_sector_total"] == 12

    results = {
        "theorem": "BT487 General Consecutive K4 Ring Torus Law",
        "construction": "T_i={i,i+1,i+2,i+3} on Z/nZ, n>=7",
        "general_formula": {
            "one_skeleton": "C_n^3 = Circ(n; ±1, ±2, ±3)",
            "boundary_f_vector": "(n, 3n, 2n)",
            "euler_characteristic": "n - 3n + 2n = 0",
            "rational_betti": "(1,2,1)",
            "rank_d1": "n-1",
            "rank_d2": "2n-1",
        },
        "specializations": {
            "n=7": "C_7^3=K_7 and boundary f-vector=(7,21,14), the Csaszar torus carrier",
            "n=30": "BC/600-cell ring carrier with boundary f-vector=(30,90,60)",
        },
        "samples": samples,
        "sweep_range": "7<=n<=60 all verified with betti_Q=(1,2,1)",
        "substrate_reading": {
            "n=7": "minimal toroidal K7/Csaszar carrier",
            "n=30": "E8 Coxeter-number/BC-ring carrier",
            "lift": "Csaszar genus-one carrier lifts to the 30-cell BC ring by the same consecutive-K4 law",
            "step_rule": "step s gives gcd(n,s) cycles of length n/gcd(n,s)",
        },
    }

    out = Path("data/PART_BT487_GENERAL_K4_RING_TORUS_LAW_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
