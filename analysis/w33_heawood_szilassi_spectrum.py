#!/usr/bin/env python3
"""
BT493: Heawood / Szilassi Spectral Split Theorem

BT492 identified the corrected abstract Szilassi skeleton with the Heawood
graph. This script extracts the exact spectral certificate.

Let B be the 7x7 Fano incidence matrix. Then:
    B B^T = 2I + J.

The Heawood adjacency matrix is:
    A = [[0, B], [B^T, 0]].

Therefore the spectrum is:
    +3^1, +sqrt(2)^6, -sqrt(2)^6, -3^1.

This gives a repaired Szilassi metric-carrier invariant independent of the
broken 31-edge parser from BT490.
"""

from __future__ import annotations

import json
from pathlib import Path
from itertools import combinations

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


def main() -> dict:
    B = fano_incidence_matrix()
    I = sp.eye(7)
    J = sp.ones(7, 7)

    assert B.shape == (7, 7)
    assert all(sum(B.row(i)) == 3 for i in range(7))
    assert all(sum(B.col(j)) == 3 for j in range(7))
    assert B * B.T == 2 * I + J
    assert B.T * B == 2 * I + J

    A = sp.zeros(14, 14)
    A[:7, 7:] = B
    A[7:, :7] = B.T

    characteristic = sp.factor(A.charpoly().as_expr())
    assert characteristic == (sp.Symbol('lambda') - 3) * (sp.Symbol('lambda') + 3) * (sp.Symbol('lambda')**2 - 2) ** 6

    eigenvals = A.eigenvals()
    assert eigenvals == {sp.Integer(-3): 1, sp.Integer(3): 1, -sp.sqrt(2): 6, sp.sqrt(2): 6}

    # Graph cross-check with NetworkX Heawood graph.
    g = nx.Graph()
    g.add_nodes_from(range(14))
    for p in range(7):
        for l in range(7):
            if B[p, l] == 1:
                g.add_edge(p, 7 + l)
    assert nx.is_isomorphic(g, nx.heawood_graph())
    assert g.number_of_edges() == 21
    assert sorted(dict(g.degree()).values()) == [3] * 14
    assert nx.diameter(g) == 3

    dist_counts = {d: 0 for d in range(1, 4)}
    for u, v in combinations(g.nodes(), 2):
        dist_counts[nx.shortest_path_length(g, u, v)] += 1
    assert dist_counts == {1: 21, 2: 42, 3: 28}

    # Spectral energy checks.
    trace_A2 = int((A**2).trace())
    assert trace_A2 == 42  # = 2E
    macro_squared = 3**2 + (-3)**2
    root_squared = trace_A2 - macro_squared
    assert macro_squared == 18
    assert root_squared == 24

    # Projector/rank checks for the point-side incidence operator.
    BBt = B * B.T
    assert BBt.eigenvals() == {sp.Integer(9): 1, sp.Integer(2): 6}
    assert sp.factor(BBt.charpoly().as_expr()) == (sp.Symbol('lambda') - 9) * (sp.Symbol('lambda') - 2) ** 6

    results = {
        "theorem": "BT493 Heawood / Szilassi Spectral Split Theorem",
        "incidence_identity": "B B^T = 2I + J",
        "heawood_adjacency_block_form": "A=[[0,B],[B^T,0]]",
        "characteristic_polynomial": "(x-3)(x+3)(x^2-2)^6",
        "spectrum": {
            "3": 1,
            "sqrt(2)": 6,
            "-sqrt(2)": 6,
            "-3": 1,
        },
        "point_side_operator_spectrum_BBt": {
            "9": 1,
            "2": 6,
        },
        "graph_certificates": {
            "is_heawood": True,
            "vertices": 14,
            "edges": 21,
            "degree": 3,
            "diameter": 3,
            "distance_pair_profile": {str(k): v for k, v in dist_counts.items()},
        },
        "spectral_energy_split": {
            "trace_A2": trace_A2,
            "macro_squared_contribution": macro_squared,
            "root_squared_contribution": root_squared,
            "reading": "42=18+24, so after the ±3 macro modes the sqrt(2) root shell contributes 24=f",
        },
        "substrate_reading": {
            "spectral_radius_3": "q=3",
            "sqrt2_shell_multiplicity_12": "six positive plus six negative root modes",
            "root_squared_contribution_24": "matter eigenmultiplicity f=24",
            "distance_profile_21_42_28": "edge/flag/defect profile of corrected Szilassi carrier",
        },
    }

    out = Path("data/PART_BT493_HEAWOOD_SZILASSI_SPECTRUM_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
