#!/usr/bin/env python3
"""
BT492: Heawood / Szilassi Dual Carrier Theorem

BT491 constructed the correct abstract Szilassi carrier as the dual of the
cyclic Csaszar K7 torus triangulation. This theorem identifies that dual
carrier with the Heawood graph.

The result closes the repair path opened by BT490:
  broken S_FACES parser -> 31 edges, not closed
  dual of cyclic Csaszar -> 14 vertices, 21 edges, 7 hexagonal faces
  this graph -> Heawood graph

Consequences:
  * Szilassi skeleton is the Heawood graph carrier.
  * The seven Szilassi faces correspond to the seven points of the primal K7.
  * The fourteen Szilassi vertices correspond to the fourteen triangular
    faces of the Csaszar triangulation.
  * The twenty-one Szilassi edges correspond to the twenty-one K7 edges.
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

import networkx as nx
from networkx.algorithms import isomorphism as iso


N = 7


def cyclic_csaszar_faces() -> list[tuple[int, int, int]]:
    tetrahedra = [tuple(sorted((i + j) % N for j in range(4))) for i in range(N)]
    tri_count: Counter[tuple[int, int, int]] = Counter()
    for tet in tetrahedra:
        for tri in combinations(tet, 3):
            tri_count[tuple(sorted(tri))] += 1
    boundary = sorted(tri for tri, c in tri_count.items() if c == 1)
    assert len(boundary) == 14
    return boundary


def dual_graph_from_faces(faces: list[tuple[int, int, int]]) -> tuple[nx.Graph, dict[tuple[int, int], list[int]]]:
    edge_to_faces: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for fi, face in enumerate(faces):
        for e in combinations(face, 2):
            edge_to_faces[tuple(sorted(e))].append(fi)
    assert Counter(len(v) for v in edge_to_faces.values()) == Counter({2: 21})
    g = nx.Graph()
    g.add_nodes_from(range(len(faces)))
    for pair in edge_to_faces.values():
        g.add_edge(*sorted(pair))
    return g, dict(edge_to_faces)


def main() -> dict:
    faces = cyclic_csaszar_faces()
    dual, edge_to_faces = dual_graph_from_faces(faces)
    heawood = nx.heawood_graph()

    assert dual.number_of_nodes() == 14
    assert dual.number_of_edges() == 21
    assert sorted(dict(dual.degree()).values()) == [3] * 14
    assert nx.is_bipartite(dual)
    assert nx.girth(dual) == 6 if hasattr(nx, "girth") else True
    assert nx.is_isomorphic(dual, heawood)

    gm = iso.GraphMatcher(dual, heawood)
    mapping = next(gm.isomorphisms_iter())

    # Heawood graph facts.
    assert heawood.number_of_nodes() == 14
    assert heawood.number_of_edges() == 21
    assert sorted(dict(heawood.degree()).values()) == [3] * 14
    assert nx.is_bipartite(heawood)

    # Face adjacency of the seven dual hexagons is K7.
    dual_faces = {}
    for primal_vertex in range(N):
        incident_triangles = [i for i, tri in enumerate(faces) if primal_vertex in tri]
        sub = dual.subgraph(incident_triangles)
        assert len(incident_triangles) == 6
        assert sub.number_of_edges() == 6
        assert sorted(dict(sub.degree()).values()) == [2] * 6
        assert nx.is_connected(sub)
        dual_faces[str(primal_vertex)] = incident_triangles

    face_adjacency = nx.Graph()
    face_adjacency.add_nodes_from(range(N))
    shared_edge_certificate = {}
    for a, b in combinations(range(N), 2):
        edge = tuple(sorted((a, b)))
        pair = sorted(edge_to_faces[edge])
        assert len(pair) == 2
        face_adjacency.add_edge(a, b)
        shared_edge_certificate[f"{a}-{b}"] = pair
    assert nx.is_isomorphic(face_adjacency, nx.complete_graph(7))

    # Distances in Heawood/Szilassi carrier.
    dist_counts = Counter()
    for u, v in combinations(dual.nodes(), 2):
        dist_counts[nx.shortest_path_length(dual, u, v)] += 1
    # Heawood diameter 3 with pair profile 21 at d=1, 42 at d=2, 28 at d=3.
    assert dist_counts == Counter({1: 21, 2: 42, 3: 28})

    results = {
        "theorem": "BT492 Heawood / Szilassi Dual Carrier Theorem",
        "csaszar_primal": {
            "vertices": 7,
            "edges": 21,
            "triangular_faces": 14,
            "face_list": faces,
        },
        "dual_szilassi_carrier": {
            "graph": "Heawood graph",
            "vertices": dual.number_of_nodes(),
            "edges": dual.number_of_edges(),
            "degree_profile": {"3": 14},
            "is_bipartite": nx.is_bipartite(dual),
            "diameter": nx.diameter(dual),
            "distance_pair_profile": {str(k): v for k, v in sorted(dist_counts.items())},
            "heawood_isomorphism": {str(k): v for k, v in sorted(mapping.items())},
        },
        "szilassi_faces": {
            "count": 7,
            "size_profile": {"6": 7},
            "faces_as_dual_cycles": dual_faces,
            "face_adjacency": "K7",
            "shared_edge_certificate_by_face_pair": shared_edge_certificate,
        },
        "incidence_correspondence": {
            "Szilassi vertices": "14 Csaszar triangular faces",
            "Szilassi edges": "21 Csaszar K7 edges",
            "Szilassi faces": "7 Csaszar vertices",
        },
        "substrate_reading": {
            "21_distance1_pairs": "edge shell / K7 duads",
            "42_distance2_pairs": "flag-orbit resonance 6*7",
            "28_distance3_pairs": "v-k / nonassociative octonion triples",
            "Heawood": "canonical Fano incidence graph; exact Szilassi skeleton carrier",
        },
    }

    out = Path("data/PART_BT492_HEAWOOD_SZILASSI_DUAL_CARRIER_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
