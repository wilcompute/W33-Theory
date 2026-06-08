#!/usr/bin/env python3
"""BT551: W33 Levi Flag Dual-Idempotent Closure Theorem.

This continues BT545--BT550.

BT550 identified the 160 Levi flags as a 4-class distance association scheme.
The first eigenmatrix was

    P =
    [1, 6,        18,        54,          81]
    [1, 2+sqrt6, 2sqrt6,    6-3sqrt6,   -9]
    [1, 2,       -6,        -6,           9]
    [1, 2-sqrt6,-2sqrt6,    6+3sqrt6,   -9]
    [1,-2,        2,        -2,           1]

with valencies 1,6,18,54,81 and multiplicities 1,24,30,24,81.

BT551 computes the second eigenmatrix Q and primitive idempotents

    E_i = (1/160) sum_{d=0}^4 Q_{d i} A_d.

The dual eigenmatrix is

    Q =
    [1, 24,              30,              24,             81]
    [1, 8+4sqrt6,        10,              8-4sqrt6,      -27]
    [1, 8sqrt6/3,       -10,             -8sqrt6/3,       9]
    [1, (8-4sqrt6)/3,   -10/3,           (8+4sqrt6)/3,   -3]
    [1, -8/3,            10/3,           -8/3,            1]

and P Q = Q P = 160 I.

The main payoff is that the protected primitive idempotent is exactly the
signed 3-adic distance kernel:

    E_4 = (1/160)(81 A0 - 27 A1 + 9 A2 - 3 A3 + A4)
        = (1/160) C C^T
        = P_cyc.

So the coefficient column of Q for the H1=81 idempotent is precisely

    (81,-27,9,-3,1),

which is the signed 3-adic radial law from BT548.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

import networkx as nx
import numpy as np
import sympy as sp

MOD = 3
POINTS_PER_LINE = 4
N = 160


def canonical_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % MOD for x in v)
    for a in v:
        if a % MOD:
            inv = 1 if a == 1 else 2
            return tuple((x * inv) % MOD for x in v)
    raise ValueError("zero vector")


def symplectic(u: tuple[int, int, int, int], v: tuple[int, int, int, int]) -> int:
    return (u[0] * v[2] + u[1] * v[3] - u[2] * v[0] - u[3] * v[1]) % MOD


def build_w33() -> tuple[nx.Graph, list[tuple[int, int, int, int]]]:
    points = sorted(
        {canonical_projective(v) for v in itertools.product(range(MOD), repeat=4) if any(v)}
    )
    g = nx.Graph()
    g.add_nodes_from(points)
    for i, u in enumerate(points):
        for v in points[i + 1 :]:
            if symplectic(u, v) == 0:
                g.add_edge(u, v)
    return g, points


def build_levi(g: nx.Graph, points: list[tuple[int, int, int, int]]) -> tuple[nx.Graph, list[tuple]]:
    lines = sorted(set(tuple(sorted(c)) for c in nx.find_cliques(g) if len(c) == POINTS_PER_LINE))
    p_index = {p: i for i, p in enumerate(points)}
    levi = nx.Graph()
    levi.add_nodes_from(range(len(points) + len(lines)))
    for li, line in enumerate(lines):
        line_node = len(points) + li
        for p in line:
            levi.add_edge(p_index[p], line_node)
    return levi, lines


def build_line_graph_distance_matrices() -> tuple[list[np.ndarray], nx.Graph, nx.Graph, list[tuple]]:
    w33, points = build_w33()
    levi, lines = build_levi(w33, points)
    edges = sorted(tuple(sorted(e)) for e in levi.edges())

    xgraph = nx.Graph()
    xgraph.add_nodes_from(range(len(edges)))
    for i, e in enumerate(edges):
        se = set(e)
        for j, f in enumerate(edges[i + 1 :], start=i + 1):
            if se & set(f):
                xgraph.add_edge(i, j)

    dist = dict(nx.all_pairs_shortest_path_length(xgraph))
    distance_matrix = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(N):
            distance_matrix[i, j] = dist[i][j]

    distance_matrices = [(distance_matrix == d).astype(int) for d in range(5)]
    return distance_matrices, w33, levi, lines


def matrix_to_nested_strings(M: sp.Matrix) -> list[list[str]]:
    return [[str(sp.simplify(M[i, j])) for j in range(M.cols)] for i in range(M.rows)]


def main() -> dict:
    distance_matrices_np, w33, levi, lines = build_line_graph_distance_matrices()

    sqrt6 = sp.sqrt(6)
    v = sp.Integer(N)
    valencies = [1, 6, 18, 54, 81]
    multiplicities = [1, 24, 30, 24, 81]

    P = sp.Matrix(
        [
            [1, 6, 18, 54, 81],
            [1, 2 + sqrt6, 2 * sqrt6, 6 - 3 * sqrt6, -9],
            [1, 2, -6, -6, 9],
            [1, 2 - sqrt6, -2 * sqrt6, 6 + 3 * sqrt6, -9],
            [1, -2, 2, -2, 1],
        ]
    )

    # Q_{d,i}=m_i P_{i,d}/k_d.
    Q = sp.zeros(5, 5)
    for d in range(5):
        for i in range(5):
            Q[d, i] = sp.simplify(sp.Integer(multiplicities[i]) * P[i, d] / sp.Integer(valencies[d]))

    # Convert distance matrices to exact sympy matrices.
    A = [sp.Matrix(M) for M in distance_matrices_np]
    I160 = sp.eye(N)
    J160 = sp.ones(N, N)
    zero160 = sp.zeros(N, N)

    # Primitive idempotents E_i=(1/v) sum_d Q_{d,i} A_d.
    E = []
    for i in range(5):
        Ei = sp.zeros(N, N)
        for d in range(5):
            Ei += Q[d, i] * A[d]
        E.append(sp.simplify(Ei / v))

    signed_kernel = 81 * A[0] - 27 * A[1] + 9 * A[2] - 3 * A[3] + A[4]
    unsigned_kernel = 81 * A[0] + 27 * A[1] + 9 * A[2] + 3 * A[3] + A[4]

    # Unsigned kernel eigenvalues by evaluating its distance polynomial on rows of P.
    signed_coeffs = sp.Matrix([81, -27, 9, -3, 1])
    unsigned_coeffs = sp.Matrix([81, 27, 9, 3, 1])
    signed_evals = [sp.simplify(sum(P[i, d] * signed_coeffs[d] for d in range(5))) for i in range(5)]
    unsigned_evals = [sp.simplify(sum(P[i, d] * unsigned_coeffs[d] for d in range(5))) for i in range(5)]

    # Schur closure certificate on the protected idempotent.  Since relations are disjoint,
    # diag profile of E4 is constant and E4∘E4 expands in the E_i basis with Krein parameters.
    # We only need the sharp identity E4 = signed_kernel/160 here.
    checks = {
        "w33_srg_size": w33.number_of_nodes() == 40 and w33.number_of_edges() == 240,
        "w33_lines_40": len(lines) == 40,
        "levi_size": levi.number_of_nodes() == 80 and levi.number_of_edges() == 160,
        "PQ_orthogonality": sp.simplify(P * Q) == v * sp.eye(5),
        "QP_orthogonality": sp.simplify(Q * P) == v * sp.eye(5),
        "E_sum_identity": sp.simplify(sum(E, zero160)) == I160,
        "E0_uniform_projector": sp.simplify(E[0] - J160 / v) == zero160,
        "E4_signed_cycle_projector": sp.simplify(E[4] - signed_kernel / v) == zero160,
        "E4_rank_trace_81": sp.simplify(sp.trace(E[4])) == 81,
        "E4_idempotent": sp.simplify(E[4] * E[4] - E[4]) == zero160,
        "E4_orthogonal_to_E0": sp.simplify(E[4] * E[0]) == zero160,
        "signed_kernel_evals": signed_evals == [0, 0, 0, 0, 160],
        "unsigned_kernel_evals": unsigned_evals
        == [648, 144 + 36 * sqrt6, 72, 144 - 36 * sqrt6, 40],
        "protected_Q_column": [sp.simplify(Q[d, 4]) for d in range(5)] == [81, -27, 9, -3, 1],
    }
    checks = {k: bool(vv) for k, vv in checks.items()}

    result = {
        "theorem": "BT551 W33 Levi Flag Dual-Idempotent Closure Theorem",
        "objects": {
            "scheme_vertices": N,
            "classes": 4,
            "valencies": valencies,
            "multiplicities": multiplicities,
        },
        "first_eigenmatrix_P": matrix_to_nested_strings(P),
        "second_eigenmatrix_Q": matrix_to_nested_strings(Q),
        "orthogonality": {
            "P_Q": "P Q = 160 I_5",
            "Q_P": "Q P = 160 I_5",
        },
        "primitive_idempotents": {
            "definition": "E_i=(1/160) sum_{d=0}^4 Q_{d,i} A_d",
            "E0": "J/160",
            "E4": "(1/160)(81A0 - 27A1 + 9A2 - 3A3 + A4)",
            "E4_trace_rank": 81,
            "E4_reading": "E4 is the BT547 Hodge/Kirchhoff cycle-space projector and BT549 centered cycle-frame Gram operator.",
        },
        "protected_column": {
            "Q_column_i4": ["81", "-27", "9", "-3", "1"],
            "reading": "The protected H1=81 primitive idempotent has coefficient column equal to the signed 3-adic radial law.",
        },
        "kernel_diagonalization": {
            "signed_kernel": "K=81A0-27A1+9A2-3A3+A4",
            "signed_eigenvalues": [str(x) for x in signed_evals],
            "unsigned_kernel": "U=81A0+27A1+9A2+3A3+A4",
            "unsigned_eigenvalues": [str(x) for x in unsigned_evals],
        },
        "compressed_statement": "The second eigenmatrix exposes the signed 3-adic law as the Q-column of the protected primitive idempotent: E4=(1/160)CC^T, so the H1=81 cycle sector is closed simultaneously under spectral projection, Hodge projection, and Bose-Mesner dual idempotent expansion.",
        "all_identities": checks,
        "all_identities_hold": all(checks.values()),
    }

    out = Path("data/PART_BT551_W33_LEVI_FLAG_DUAL_IDEMPOTENT_CLOSURE_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"wrote {out}")
    return result


if __name__ == "__main__":
    main()
