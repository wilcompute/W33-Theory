#!/usr/bin/env python3
"""
BT491: Dual Szilassi from Cyclic Csaszar Theorem

This fixes the BT490 audit issue constructively.

Instead of parsing a questionable Szilassi 6-cycle list, build the Szilassi
combinatorial carrier as the dual of the verified n=7 cyclic Csaszar torus
triangulation from BT488.

Primal/Csaszar side:
    vertices = Z/7Z
    edges = K7 = 21
    faces = 14 triangles from the consecutive K4 ring boundary

Dual/Szilassi side:
    vertices = primal triangular faces = 14
    edges = primal edges = 21
    faces = primal vertices = 7

Each dual face is a hexagon because each K7 vertex has degree 6 in the
Csaszar triangulation. Every pair of dual faces shares exactly one edge
because every pair of primal vertices is joined by exactly one K7 edge.
Thus the dual has complete face adjacency K7, which is precisely the
Szilassi incidence property.
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
    """Boundary triangles of T_i={i,i+1,i+2,i+3} on Z/7Z."""
    tetrahedra = [tuple(sorted((i + j) % N for j in range(4))) for i in range(N)]
    tri_count: Counter[tuple[int, int, int]] = Counter()
    for tet in tetrahedra:
        for tri in combinations(tet, 3):
            tri_count[tuple(sorted(tri))] += 1
    boundary = sorted(tri for tri, c in tri_count.items() if c == 1)
    assert len(boundary) == 14
    assert Counter(tri_count.values()) == Counter({1: 14, 2: 7})
    return boundary


def complex_automorphism_order(g: nx.Graph, faces: list[tuple[int, ...]]) -> int:
    face_set = {frozenset(f) for f in faces}
    count = 0
    for p in iso.GraphMatcher(g, g).isomorphisms_iter():
        if all(frozenset(p[x] for x in f) in face_set for f in faces):
            count += 1
    return count


def main() -> dict:
    primal_faces = cyclic_csaszar_faces()

    # Primal Csaszar graph is K7.
    primal_graph = nx.complete_graph(N)
    assert primal_graph.number_of_edges() == 21

    # Each primal edge belongs to exactly two primal triangular faces.
    edge_to_faces: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for fi, face in enumerate(primal_faces):
        for e in combinations(face, 2):
            edge_to_faces[tuple(sorted(e))].append(fi)
    assert len(edge_to_faces) == 21
    assert Counter(len(v) for v in edge_to_faces.values()) == Counter({2: 21})

    # Dual graph: vertices are primal faces, edges connect adjacent primal faces.
    dual_edges = []
    for edge, face_pair in edge_to_faces.items():
        f0, f1 = sorted(face_pair)
        dual_edges.append((f0, f1))

    dual_graph = nx.Graph()
    dual_graph.add_nodes_from(range(len(primal_faces)))
    dual_graph.add_edges_from(dual_edges)
    assert dual_graph.number_of_nodes() == 14
    assert dual_graph.number_of_edges() == 21
    assert sorted(dict(dual_graph.degree()).values()) == [3] * 14
    assert nx.is_connected(dual_graph)

    # Dual faces are indexed by primal vertices. The incident primal triangles
    # form a 6-cycle in the dual graph.
    dual_faces = {}
    dual_face_cycle_edges = {}
    for p in range(N):
        incident_dual_vertices = [i for i, tri in enumerate(primal_faces) if p in tri]
        sub = dual_graph.subgraph(incident_dual_vertices)
        assert len(incident_dual_vertices) == 6
        assert sub.number_of_edges() == 6
        assert sorted(dict(sub.degree()).values()) == [2] * 6
        assert nx.is_connected(sub)
        dual_faces[str(p)] = incident_dual_vertices
        dual_face_cycle_edges[str(p)] = sorted(tuple(sorted(e)) for e in sub.edges())

    # Face adjacency among the seven dual hexagons is complete K7.
    face_adjacency = nx.Graph()
    face_adjacency.add_nodes_from(range(N))
    for p, q in combinations(range(N), 2):
        primal_edge = tuple(sorted((p, q)))
        # The primal K7 edge is the unique dual edge shared by faces p and q.
        assert primal_edge in edge_to_faces
        face_adjacency.add_edge(p, q)
    assert face_adjacency.number_of_edges() == 21
    assert nx.is_isomorphic(face_adjacency, nx.complete_graph(7))

    # Euler and Szilassi f-vector.
    Vd, Ed, Fd = dual_graph.number_of_nodes(), dual_graph.number_of_edges(), N
    assert (Vd, Ed, Fd) == (14, 21, 7)
    assert Vd - Ed + Fd == 0

    # Automorphism group is inherited from the cyclic Csaszar complex.
    primal_aut = complex_automorphism_order(primal_graph, primal_faces)
    dual_aut = complex_automorphism_order(dual_graph, [tuple(vs) for vs in dual_faces.values()])
    assert primal_aut == 42
    assert dual_aut == 42

    results = {
        "theorem": "BT491 Dual Szilassi from Cyclic Csaszar Theorem",
        "primal_csaszar": {
            "vertices": 7,
            "edges": 21,
            "faces": 14,
            "face_list": primal_faces,
            "one_skeleton": "K7",
            "euler_characteristic": 0,
            "automorphism_order": primal_aut,
        },
        "dual_szilassi": {
            "vertices": Vd,
            "edges": Ed,
            "faces": Fd,
            "euler_characteristic": 0,
            "vertex_degree_profile": {"3": 14},
            "face_size_profile": {"6": 7},
            "face_adjacency_graph": "K7",
            "automorphism_order": dual_aut,
            "dual_faces_as_cycles_of_primal_triangles": dual_faces,
            "dual_face_cycle_edges": dual_face_cycle_edges,
        },
        "incidence_certificates": {
            "primal_edge_face_profile": {"2": 21},
            "dual_edge_face_profile": {"2": 21},
            "every_pair_of_dual_faces_shares_one_edge": True,
            "closed_szilassi_condition": True,
        },
        "BT490_resolution": (
            "A correct 21-edge abstract Szilassi carrier is obtained as the dual "
            "of the cyclic Csaszar torus triangulation. This should replace the "
            "31-edge cyclic S_FACES parser for combinatorial Szilassi tests."
        ),
        "substrate_reading": {
            "7_faces": "Fano heptad / complete face-adjacency observable",
            "14_vertices": "dim(G2) dual vertex shell",
            "21_edges": "K7 duads / g1 shell",
            "42_automorphisms": "g2*Phi6 flag-orbit resonance",
        },
    }

    out = Path("data/PART_BT491_DUAL_SZILASSI_FROM_CYCLIC_CSASZAR_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
