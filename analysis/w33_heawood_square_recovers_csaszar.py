#!/usr/bin/env python3
"""
BT494: Heawood Square Recovers Csaszar K7 Theorem

BT491/BT492 repaired the Szilassi carrier as the Heawood graph, the dual
of the cyclic Csaszar triangulation.

This theorem gives the sharp algebraic bridge:
    If A_H = [[0,B],[B^T,0]] is the Heawood adjacency matrix built from
    Fano incidence B, then
        A_H^2 = [[BB^T,0],[0,B^T B]] = [[2I+J,0],[0,2I+J]].

Therefore, after subtracting 3I on each side, the distance-2 graph on each
bipartition is K7. In words:
    Szilassi/Heawood squared recovers two Csaszar K7 carriers.

This is not a count match: it is an exact adjacency-algebra identity.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import networkx as nx
import sympy as sp


FANO_LINES = [
    (0, 1, 3),
    (0, 2, 5),
    (0, 4, 6),
    (1, 2, 4),
    (1, 5, 6),
    (2, 3, 6),
    (3, 4, 5),
]


def fano_incidence_matrix() -> sp.Matrix:
    B = sp.zeros(7, 7)
    for li, line in enumerate(FANO_LINES):
        for p in line:
            B[p, li] = 1
    return B


def graph_from_adjacency(A: sp.Matrix) -> nx.Graph:
    g = nx.Graph()
    n = A.shape[0]
    g.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i + 1, n):
            if A[i, j] != 0:
                g.add_edge(i, j)
    return g


def main() -> dict:
    x = sp.Symbol("x")
    B = fano_incidence_matrix()
    I7 = sp.eye(7)
    J7 = sp.ones(7, 7)
    K7_adj = J7 - I7

    assert B * B.T == 2 * I7 + J7
    assert B.T * B == 2 * I7 + J7

    A = sp.zeros(14, 14)
    A[:7, 7:] = B
    A[7:, :7] = B.T
    A2 = A**2

    expected_A2 = sp.zeros(14, 14)
    expected_A2[:7, :7] = 2 * I7 + J7
    expected_A2[7:, 7:] = 2 * I7 + J7
    assert A2 == expected_A2

    point_distance2_adj = A2[:7, :7] - 3 * I7
    line_distance2_adj = A2[7:, 7:] - 3 * I7
    assert point_distance2_adj == K7_adj
    assert line_distance2_adj == K7_adj

    point_graph = graph_from_adjacency(point_distance2_adj)
    line_graph = graph_from_adjacency(line_distance2_adj)
    assert nx.is_isomorphic(point_graph, nx.complete_graph(7))
    assert nx.is_isomorphic(line_graph, nx.complete_graph(7))
    assert point_graph.number_of_edges() == 21
    assert line_graph.number_of_edges() == 21

    # Heawood graph from block matrix.
    H = graph_from_adjacency(A)
    assert nx.is_isomorphic(H, nx.heawood_graph())
    assert H.number_of_edges() == 21

    # The distance-2 graph of the Heawood graph is exactly K7 disjoint union K7.
    D2 = nx.Graph()
    D2.add_nodes_from(H.nodes())
    for u, v in combinations(H.nodes(), 2):
        if nx.shortest_path_length(H, u, v) == 2:
            D2.add_edge(u, v)
    comps = sorted(len(c) for c in nx.connected_components(D2))
    assert comps == [7, 7]
    assert D2.number_of_edges() == 42
    for comp in nx.connected_components(D2):
        sub = D2.subgraph(comp)
        assert nx.is_isomorphic(sub, nx.complete_graph(7))

    # Spectral square: Heawood eigenvalues square to 9^2 + 2^12.
    char_H = sp.factor(A.charpoly(x).as_expr())
    assert char_H == (x - 3) * (x + 3) * (x**2 - 2) ** 6
    char_K7 = sp.factor(point_distance2_adj.charpoly(x).as_expr())
    assert char_K7 == (x - 6) * (x + 1) ** 6

    results = {
        "theorem": "BT494 Heawood Square Recovers Csaszar K7 Theorem",
        "matrix_identity": "A_H^2 = diag(2I+J, 2I+J)",
        "distance2_identity": "A_H^2 - 3I on either bipartition = J-I = A(K7)",
        "heawood_carrier": {
            "vertices": 14,
            "edges": 21,
            "spectrum": "(x-3)(x+3)(x^2-2)^6",
        },
        "distance2_graph": {
            "structure": "K7 disjoint union K7",
            "components": comps,
            "edge_count": D2.number_of_edges(),
            "component_edge_count": 21,
            "component_spectrum": "(x-6)(x+1)^6",
        },
        "interpretation": {
            "Szilassi": "Heawood/Fano incidence graph, face-complete torus carrier",
            "Csaszar": "K7 complete vertex-adjacency torus carrier",
            "bridge": "two-step motion in Szilassi/Heawood equals one complete Csaszar adjacency layer",
            "duality": "point and line bipartitions each recover a K7 carrier",
        },
        "substrate_reading": {
            "21": "each recovered K7 has 21 edges",
            "42": "total distance-2 edges = two K7 shells = flag-orbit resonance",
            "spectrum_square": "Heawood sqrt(2) modes square to the K7 -1 modes after loop subtraction",
        },
    }

    out = Path("data/PART_BT494_HEAWOOD_SQUARE_RECOEVRS_CSASZAR_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
