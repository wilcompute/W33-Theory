#!/usr/bin/env python3
"""
BT490: Toroidal Metric Edge-Count Audit

This audits a discrepancy found while mining the toroidal HTML + metric files.

The toroidal-triad HTML correctly lists Szilassi as:
    V=14, E=21, F=7.

But EDGE_LENGTH_ANALYSIS.py constructs Szilassi edges by taking all cyclic
adjacent pairs in S_FACES. The seven listed 6-cycles have 42 face-edge
incidences, but they identify to 31 unique edges with incidence profile:
    20 singleton edges + 11 double edges.

A closed Szilassi polyhedron should have:
    42 face-edge incidences = 2E => E=21,
with every edge incident to exactly two faces.

Therefore the current S_FACES parser is not a valid closed Szilassi
edge carrier. Metric identities using those parsed Szilassi edges should be
marked as parser-dependent until the correct 21-edge incidence data is restored.
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx


S_FACES = [
    [0, 1, 7, 8, 9, 3],
    [1, 2, 8, 9, 10, 4],
    [2, 3, 9, 10, 11, 5],
    [3, 4, 10, 11, 12, 6],
    [4, 5, 11, 12, 13, 7],
    [5, 6, 12, 13, 0, 8],
    [6, 0, 13, 1, 2, 7],
]


def cyclic_face_edges(face: list[int]) -> list[tuple[int, int]]:
    return [tuple(sorted((face[i], face[(i + 1) % len(face)]))) for i in range(len(face))]


def main() -> dict:
    V_expected = 14
    F_expected = 7
    E_expected = 21
    face_degree = 6

    all_face_edges: list[tuple[int, int]] = []
    for face in S_FACES:
        assert len(face) == face_degree
        all_face_edges.extend(cyclic_face_edges(face))

    incidence_count = len(all_face_edges)
    edge_counter = Counter(all_face_edges)
    unique_edges = sorted(edge_counter)
    incidence_profile = Counter(edge_counter.values())

    assert incidence_count == F_expected * face_degree == 42
    assert E_expected == incidence_count // 2

    # The actual parser output from EDGE_LENGTH_ANALYSIS.py.
    parsed_unique_edge_count = len(unique_edges)
    assert parsed_unique_edge_count == 31
    assert incidence_profile == Counter({1: 20, 2: 11})

    singleton_edges = sorted(e for e, c in edge_counter.items() if c == 1)
    shared_edges = sorted(e for e, c in edge_counter.items() if c == 2)
    assert len(singleton_edges) == 20
    assert len(shared_edges) == 11

    # Euler check: parsed graph is not the Szilassi closed polyhedral graph.
    parsed_graph = nx.Graph()
    parsed_graph.add_nodes_from(range(V_expected))
    parsed_graph.add_edges_from(unique_edges)
    assert parsed_graph.number_of_nodes() == V_expected
    assert parsed_graph.number_of_edges() == 31
    parsed_euler = V_expected - parsed_graph.number_of_edges() + F_expected
    correct_euler = V_expected - E_expected + F_expected
    assert parsed_euler == -10
    assert correct_euler == 0

    # If the incidence were closed, every edge would have count 2 and there would be 21 unique edges.
    closed_condition = parsed_unique_edge_count == E_expected and incidence_profile == Counter({2: E_expected})
    assert closed_condition is False

    # Csaszar side remains clean: K7 has C(7,2)=21 edges.
    csaszar_edge_count = len(list(combinations(range(7), 2)))
    assert csaszar_edge_count == 21

    results = {
        "theorem": "BT490 Toroidal Metric Edge-Count Audit",
        "source_files": [
            "visualizations/w33-toroidal-triad.html states Szilassi E=21",
            "EDGE_LENGTH_ANALYSIS.py derives S_edges from cyclic S_FACES",
        ],
        "expected_szilassi_closed_polyhedron": {
            "V": V_expected,
            "E": E_expected,
            "F": F_expected,
            "face_degree": face_degree,
            "face_edge_incidences": incidence_count,
            "required_edge_incidence_profile": {"2": E_expected},
            "euler_characteristic": correct_euler,
        },
        "current_parser_output": {
            "unique_edges": parsed_unique_edge_count,
            "face_edge_incidences": incidence_count,
            "edge_incidence_profile": {str(k): v for k, v in sorted(incidence_profile.items())},
            "singleton_edge_count": len(singleton_edges),
            "double_edge_count": len(shared_edges),
            "parsed_euler_characteristic_with_F7": parsed_euler,
            "closed_szilassi_condition": closed_condition,
        },
        "singleton_edges": singleton_edges,
        "double_edges": shared_edges,
        "audit_conclusion": (
            "The current S_FACES cyclic parser produces 31 unique edges, not 21. "
            "It is not a closed Szilassi incidence structure. Metric identities "
            "depending on these Szilassi edges are parser-dependent and need a "
            "restored 21-edge Szilassi graph before being promoted as polyhedral facts."
        ),
        "safe_result": {
            "csaszar_K7_edge_count": csaszar_edge_count,
            "toroidal_triad_symbolic_ladder": "unaffected; it uses Euler/completeness equations rather than S_FACES parser",
        },
    }

    out = Path("data/PART_BT490_TOROIDAL_METRIC_EDGE_COUNT_AUDIT_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
