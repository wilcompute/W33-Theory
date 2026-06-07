#!/usr/bin/env python3
"""BT501: Counter-BC-Helix Memory Braid Theorem.

Motivation from the user's model:
  two BC helices spin in opposite directions; their interaction launches a
  tetrahedral "now" which is added to a braid of tetrahedral nows.

Conservative mathematical content:
  * The BC twist angle theta=acos(-2/3) has theta/pi irrational, by the
    rational-cosine/Niven obstruction: if theta/pi were rational, cos(theta)
    could only be 0, ±1/2, ±1; but cos(theta)=-2/3.
  * Therefore a 3D BC helix orientation never exactly repeats.
  * A counter-rotating pair has phase state (t theta, -t theta).  The relative
    phase is 2t theta, also nonperiodic in 3D.
  * In the 600-cell compactification we may track a 30-cell index ring.  This
    gives a finite address cycle without contradicting 3D aperiodicity.
  * A tetrahedral now is modeled as a K4 joining one edge from the past helix
    and one counter-oriented edge from the future helix.

The resulting 30-now braid has a clean incidence split:
  vertices: 60 = 30 past + 30 future
  K4 now cells: 30
  edges: 150 = 30 past + 30 future + 90 cross/present
  triangles: 120 = 30 * 4
  Euler characteristic of the 3-complex: 60 - 150 + 120 - 30 = 0
"""
from __future__ import annotations

import json
import math
from collections import Counter
from itertools import combinations
from pathlib import Path

import networkx as nx
import sympy as sp

N = 30


def past(i: int) -> tuple[str, int]:
    return ("P", i % N)


def future(i: int) -> tuple[str, int]:
    return ("F", i % N)


def now_cell(t: int) -> tuple[tuple[str, int], ...]:
    # Past edge advances +1; future edge advances in the opposite direction.
    return tuple(sorted([past(t), past(t + 1), future(t), future(t - 1)]))


def canon_edge(a, b):
    return tuple(sorted([a, b]))


def main() -> dict:
    # Exact irrationality certificate for theta/pi.
    theta = sp.acos(sp.Rational(-2, 3))
    rational_cos_allowed = {sp.Integer(-1), sp.Rational(-1, 2), sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)}
    assert sp.Rational(-2, 3) not in rational_cos_allowed

    # Numerical phase sanity check: no repeats among the first several thousand states.
    # This is only a finite check; the proof above is the exact part.
    th = math.acos(-2 / 3)
    samples = 5000
    rounded_single = {round((t * th) % (2 * math.pi), 14) for t in range(samples)}
    rounded_relative = {round((2 * t * th) % (2 * math.pi), 14) for t in range(samples)}
    assert len(rounded_single) == samples
    assert len(rounded_relative) == samples

    cells = [now_cell(t) for t in range(N)]
    assert len(set(cells)) == N

    vertices = sorted({v for cell in cells for v in cell})
    assert len(vertices) == 2 * N

    edge_counter: Counter[tuple[tuple[str, int], tuple[str, int]]] = Counter()
    triangle_counter: Counter[tuple[tuple[str, int], ...]] = Counter()
    for cell in cells:
        for e in combinations(cell, 2):
            edge_counter[canon_edge(*e)] += 1
        for tri in combinations(cell, 3):
            triangle_counter[tuple(sorted(tri))] += 1

    edges = sorted(edge_counter)
    triangles = sorted(triangle_counter)
    assert len(edges) == 150
    assert len(triangles) == 120
    assert Counter(triangle_counter.values()) == Counter({1: 120})

    def edge_type(e):
        a, b = e
        if a[0] == "P" and b[0] == "P":
            return "past_helix"
        if a[0] == "F" and b[0] == "F":
            return "future_helix"
        return "cross_present"

    edge_types = Counter(edge_type(e) for e in edges)
    assert edge_types == Counter({"cross_present": 90, "past_helix": 30, "future_helix": 30})

    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)
    assert G.number_of_nodes() == 60
    assert G.number_of_edges() == 150
    assert nx.is_connected(G)

    # Automorphism: rotating t -> t+1 preserves the braid. Reflection swaps chirality.
    # We verify the rotation explicitly as a graph automorphism.
    rotation = {past(i): past(i + 1) for i in range(N)} | {future(i): future(i + 1) for i in range(N)}
    rotated_edges = {canon_edge(rotation[a], rotation[b]) for a, b in edges}
    assert rotated_edges == set(edges)

    # Reflection exchanging past/future with index sign also preserves the construction.
    reflection = {past(i): future(-i) for i in range(N)} | {future(i): past(-i) for i in range(N)}
    reflected_edges = {canon_edge(reflection[a], reflection[b]) for a, b in edges}
    assert reflected_edges == set(edges)

    V, E, F, T = len(vertices), len(edges), len(triangles), len(cells)
    chi3 = V - E + F - T
    assert chi3 == 0

    # Each now is a K4 with both adjacency observables: two rail edges plus four cross edges.
    cell_edge_profile = Counter()
    for cell in cells:
        local_edges = [canon_edge(*e) for e in combinations(cell, 2)]
        profile = Counter(edge_type(e) for e in local_edges)
        assert profile == Counter({"cross_present": 4, "past_helix": 1, "future_helix": 1})
        cell_edge_profile[tuple(sorted(profile.items()))] += 1
    assert list(cell_edge_profile.values()) == [30]

    results = {
        "theorem": "BT501 Counter-BC-Helix Memory Braid Theorem",
        "irrationality_certificate": {
            "theta": "acos(-2/3)",
            "claim": "theta/pi is irrational",
            "reason": "rational-cosine obstruction: -2/3 is not in {0, ±1/2, ±1}",
            "finite_no_repeat_check_samples": samples,
        },
        "counter_rotating_phase_model": {
            "past_phase": "t*theta",
            "future_phase": "-t*theta",
            "relative_phase": "2*t*theta",
            "3D_repeat_status": "no exact repeat",
            "600_cell_index_compactification": "t mod 30 gives finite address ring while orientation remains 3D-aperiodic",
        },
        "now_braid_complex": {
            "vertices": V,
            "edges": E,
            "triangles": F,
            "tetrahedral_now_cells": T,
            "euler_characteristic_3_complex": chi3,
            "edge_type_split": dict(edge_types),
            "local_K4_edge_split": "1 past rail + 1 future rail + 4 cross-present edges",
            "rotation_order": 30,
            "reflection_chirality_swap": True,
        },
        "memory_reading": {
            "now": "one K4 generated by interaction of one past rail edge and one future rail edge",
            "chain": "30 addressed nows per 600-cell BC ring compactification",
            "aperiodicity": "3D orientations never repeat, so memory addresses are finite but orientation tags are nonrepeating",
            "opposite_wheels": "past/future phases t*theta and -t*theta create a relative phase 2t*theta",
        },
        "substrate_reading": {
            "30": "BC ring / E8 Coxeter-number address cycle",
            "60": "two counter-rotating 30-rails",
            "90": "cross-present interaction edge shell",
            "120": "triangle face events = 4 per now over 30 nows",
            "150": "total memory-braid graph edge carrier",
        },
    }
    out = Path("data/PART_BT501_COUNTER_BC_HELIX_MEMORY_BRAID_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
