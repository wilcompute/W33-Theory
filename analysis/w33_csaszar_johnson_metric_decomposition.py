#!/usr/bin/env python3
"""
BT495: Csaszar Johnson Metric Decomposition Theorem

After BT490 flagged the current Szilassi metric parser as non-closed,
this theorem returns to the safe metric carrier: the five Csaszar K7
realizations. Every Csaszar realization has an unambiguous 21-edge metric
vector over the complete graph K7.

The edge space R^{E(K7)} has a canonical Johnson/Triangular-graph
spectral decomposition. Let B be the 21x7 edge-vertex incidence matrix.
Then:
    B^T B = 5I + J
    A_{T(7)} = B B^T - 2I
and the triangular graph T(7)=L(K7) has spectrum:
    10^1, 3^6, (-2)^14.

Therefore any Csaszar squared-edge-length vector decomposes as:
    R^21 = scalar(1) ⊕ vertex-potential(6) ⊕ G2/cycle-residual(14).

This extracts a genuine dim(G2)=14 metric channel from each realization.
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp


q, r, E1, g1, dim_g2 = 3, 2, 10, 21, 14

C1 = {0: (0, 0, 0), 1: (3, 0, 0), 2: (0, 3, 0), 3: (1, 1, 2), 4: (2, 1, -1), 5: (1, 2, -1), 6: (2, 2, 3)}
C2 = {0: (0, 0, 0), 1: (4, 0, 0), 2: (0, 4, 0), 3: (2, 2, 3), 4: (3, 1, -1), 5: (1, 3, -1), 6: (2, 2, 4)}
C3 = {
    0: (0, 0, 0),
    1: (4, 0, 0),
    2: (2, 2 * math.sqrt(3), 0),
    3: (2, 2 / math.sqrt(3), 4 / math.sqrt(6)),
    4: (1, math.sqrt(3), -math.sqrt(2)),
    5: (3, math.sqrt(3), -math.sqrt(2)),
    6: (2, 0, 2 * math.sqrt(2)),
}
C4 = {0: (0, 0, 0), 1: (6, 0, 0), 2: (3, 5, 0), 3: (3, 1, 4), 4: (2, -1, 1), 5: (4, -1, 1), 6: (3, 4, -2)}
C5 = {0: (0, 0, 0), 1: (5, 0, 0), 2: (0, 5, 0), 3: (2, 2, 3), 4: (3, 1, -1), 5: (1, 3, -1), 6: (3, 3, 4)}

REALIZATIONS = [
    ("Csaszar-1", C1),
    ("Csaszar-2", C2),
    ("Csaszar-3", C3),
    ("Csaszar-4", C4),
    ("Csaszar-5", C5),
]
EDGES = list(itertools.combinations(range(7), 2))


def sqdist(C: dict[int, tuple[float, float, float]], u: int, v: int) -> float:
    return sum((C[u][i] - C[v][i]) ** 2 for i in range(3))


def rounded(x: float) -> float:
    return round(float(x), 10)


def main() -> dict:
    x = sp.Symbol("x")
    B = sp.zeros(21, 7)
    for i, (u, v) in enumerate(EDGES):
        B[i, u] = 1
        B[i, v] = 1

    I21 = sp.eye(21)
    I7 = sp.eye(7)
    J7 = sp.ones(7, 7)
    AT = B * B.T - 2 * I21

    assert B.T * B == 5 * I7 + J7
    assert sp.factor(AT.charpoly(x).as_expr()) == (x - 10) * (x - 3) ** 6 * (x + 2) ** 14

    # Confirm AT is exactly the triangular graph T(7)=L(K7).
    K7 = nx.complete_graph(7)
    T7 = nx.line_graph(K7)
    edge_index = {tuple(sorted(e)): i for i, e in enumerate(EDGES)}
    A_nx = np.zeros((21, 21), dtype=int)
    for e1, e2 in T7.edges():
        i = edge_index[tuple(sorted(e1))]
        j = edge_index[tuple(sorted(e2))]
        A_nx[i, j] = A_nx[j, i] = 1
    assert np.array_equal(np.array(AT.tolist(), dtype=int), A_nx)

    # Exact orthogonal projectors.
    one = sp.ones(21, 1)
    P1 = one * one.T / 21
    PB = B * (B.T * B).inv() * B.T
    P6 = sp.simplify(PB - P1)
    P14 = sp.simplify(I21 - PB)
    for P, rank in [(P1, 1), (P6, 6), (P14, 14)]:
        assert P * P == P
        assert P.rank() == rank
    assert P1 * P6 == sp.zeros(21)
    assert P1 * P14 == sp.zeros(21)
    assert P6 * P14 == sp.zeros(21)
    assert P1 + P6 + P14 == I21

    # Numeric projector versions for metric vectors.
    Bn = np.array(B.tolist(), float)
    ones = np.ones((21, 1))
    P1n = ones @ ones.T / 21
    PBn = Bn @ np.linalg.inv(Bn.T @ Bn) @ Bn.T
    P6n = PBn - P1n
    P14n = np.eye(21) - PBn

    packets = []
    for name, C in REALIZATIONS:
        vec = np.array([sqdist(C, u, v) for u, v in EDGES], dtype=float)
        c1, c6, c14 = P1n @ vec, P6n @ vec, P14n @ vec
        energies = [float(c @ c) for c in (c1, c6, c14)]
        assert abs(sum(energies) - float(vec @ vec)) < 1e-6
        assert abs(float(c1 @ c6)) < 1e-6
        assert abs(float(c1 @ c14)) < 1e-6
        assert abs(float(c6 @ c14)) < 1e-6
        star = Bn.T @ vec
        packets.append(
            {
                "name": name,
                "complete_edge_metric_sum": rounded(vec.sum()),
                "mean_edge_metric": rounded(vec.mean()),
                "total_metric_energy_norm2": rounded(vec @ vec),
                "johnson_energy_decomposition_1_6_14": {
                    "scalar_dim1": rounded(energies[0]),
                    "vertex_potential_dim6": rounded(energies[1]),
                    "G2_residual_dim14": rounded(energies[2]),
                },
                "G2_residual_fraction": rounded(energies[2] / float(vec @ vec)),
                "vertex_star_sums": [rounded(s) for s in star],
                "integer_edge_count": int(sum(abs(v - round(v)) < 1e-8 for v in vec)),
                "distinct_metric_values": len(set(round(v, 8) for v in vec)),
            }
        )

    results = {
        "theorem": "BT495 Csaszar Johnson Metric Decomposition Theorem",
        "carrier": "K7 edge space, dimension 21",
        "triangular_graph": "T(7)=line graph L(K7)",
        "incidence_identity": "B^T B = 5I + J and A_T = B B^T - 2I",
        "T7_spectrum": "10^1, 3^6, (-2)^14",
        "projector_decomposition": "R^21 = scalar(1) ⊕ vertex-potential(6) ⊕ cycle/G2-residual(14)",
        "projector_ranks": {"scalar": 1, "vertex_potential": 6, "G2_residual": 14},
        "metric_packets": packets,
        "substrate_reading": {
            "21": "K7 edge shell / g1",
            "1+6+14": "scalar + positive-G2-root selector + dim(G2) residual",
            "T7_eigenvalues": "10=E1, 3=q, -2=-r",
            "G2_residual": "the part of Csaszar metric data invisible to vertex-star potentials",
        },
    }

    out = Path("data/PART_BT495_CSASZAR_JOHNSON_METRIC_DECOMPOSITION_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
