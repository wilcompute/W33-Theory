#!/usr/bin/env python3
"""Zero-sheet Twin-Pell spectral fingerprint.

The Hamming/Fano zero sheet already matched the completed spectral branch by
cycle scales 4, 4, 6.  This script follows the graph itself.

For the zero-sheet adjacency matrix A, the characteristic polynomial is

    det(xI - A) = x^8 - 9 x^6 + 17 x^4 - 8 x^2
                = x^2 * (y^3 - 9 y^2 + 17 y - 8), y=x^2.

The coefficients are not generic graph data:

    9  = q^2
    17 = q^2 + 2^q
    8  = 2^q

so the same Twin-Pell pair (2^q, q^2) from the spectral tower is now the
literal adjacency fingerprint of the zero sheet.  The Laplacian cofactor is
15, matching the W(3,3) g multiplicity.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "w33_zero_sheet_twin_pell_spectral_fingerprint.json"
RESULT = ROOT / "PART_MCXV_zero_sheet_twin_pell_spectral_fingerprint_results.json"
FUNCTOR_PATH = ROOT / "analysis" / "w33_hamming_horizon_functor_search.py"

Q = 3
Q2 = Q * Q
TOMOTOPE_CELLS = 2**Q
ODD_METRIC_INSTANCES = Q2 + TOMOTOPE_CELLS
G_MULTIPLICITY = 15


def load_zero_sheet_graph() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("w33_hamming_horizon_functor_search", FUNCTOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {FUNCTOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_payload()["zero_sheet_subgraph"]


def adjacency_matrix(graph: dict[str, Any]) -> list[list[int]]:
    vertices = graph["vertices"]
    index = {vertex: idx for idx, vertex in enumerate(vertices)}
    matrix = [[0 for _ in vertices] for _ in vertices]
    for left, right in graph["edges"]:
        i = index[left]
        j = index[right]
        matrix[i][j] = 1
        matrix[j][i] = 1
    return matrix


def laplacian_matrix(adjacency: list[list[int]]) -> list[list[int]]:
    matrix = []
    for i, row in enumerate(adjacency):
        degree = sum(row)
        matrix.append([degree if i == j else -row[j] for j in range(len(row))])
    return matrix


def matrix_multiply(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(left)
    return [
        [sum(left[i][k] * right[k][j] for k in range(n)) for j in range(n)]
        for i in range(n)
    ]


def matrix_trace(matrix: list[list[Fraction]]) -> Fraction:
    return sum(matrix[i][i] for i in range(len(matrix)))


def identity_matrix(size: int) -> list[list[Fraction]]:
    return [[Fraction(1 if i == j else 0, 1) for j in range(size)] for i in range(size)]


def matrix_add(left: list[list[Fraction]], right: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(left)
    return [[left[i][j] + right[i][j] for j in range(n)] for i in range(n)]


def matrix_scale(scalar: Fraction, matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    n = len(matrix)
    return [[scalar * matrix[i][j] for j in range(n)] for i in range(n)]


def characteristic_coefficients(matrix: list[list[int]]) -> list[int]:
    """Return [1,c1,...,cn] for det(xI-M)=x^n+c1*x^(n-1)+...+cn."""
    n = len(matrix)
    mat = [[Fraction(value, 1) for value in row] for row in matrix]
    identity = identity_matrix(n)
    running = identity
    coeffs: list[Fraction] = []
    for order in range(1, n + 1):
        product = matrix_multiply(mat, running)
        coeff = -matrix_trace(product) / order
        coeffs.append(coeff)
        running = matrix_add(product, matrix_scale(coeff, identity))
    if any(coeff.denominator != 1 for coeff in coeffs):
        raise RuntimeError(f"nonintegral characteristic coefficients: {coeffs}")
    return [1] + [int(coeff) for coeff in coeffs]


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Exact integer determinant by the Bareiss fraction-free algorithm."""
    mat = [row[:] for row in matrix]
    n = len(mat)
    if n == 0:
        return 1
    sign = 1
    previous = 1
    for k in range(n - 1):
        if mat[k][k] == 0:
            for swap in range(k + 1, n):
                if mat[swap][k] != 0:
                    mat[k], mat[swap] = mat[swap], mat[k]
                    sign *= -1
                    break
            else:
                return 0
        pivot = mat[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                mat[i][j] = (mat[i][j] * pivot - mat[i][k] * mat[k][j]) // previous
        previous = pivot
        for i in range(k + 1, n):
            mat[i][k] = 0
        for j in range(k + 1, n):
            mat[k][j] = 0
    return sign * mat[-1][-1]


def polynomial_text(coefficients: list[int]) -> str:
    degree = len(coefficients) - 1
    terms = []
    for index, coeff in enumerate(coefficients):
        if coeff == 0:
            continue
        power = degree - index
        sign = "-" if coeff < 0 else "+"
        magnitude = abs(coeff)
        if power == 0:
            core = str(magnitude)
        elif power == 1:
            core = "x" if magnitude == 1 else f"{magnitude}x"
        else:
            core = f"x^{power}" if magnitude == 1 else f"{magnitude}x^{power}"
        terms.append((sign, core))
    if not terms:
        return "0"
    first_sign, first_core = terms[0]
    rendered = first_core if first_sign == "+" else f"-{first_core}"
    for sign, core in terms[1:]:
        rendered += f" {sign} {core}"
    return rendered


def build_payload() -> dict[str, Any]:
    graph = load_zero_sheet_graph()
    adjacency = adjacency_matrix(graph)
    laplacian = laplacian_matrix(adjacency)
    adjacency_char = characteristic_coefficients(adjacency)
    laplacian_char = characteristic_coefficients(laplacian)
    laplacian_minor = [row[:-1] for row in laplacian[:-1]]
    spanning_tree_count = bareiss_determinant(laplacian_minor)
    squared_cubic = [1, -Q2, ODD_METRIC_INSTANCES, -TOMOTOPE_CELLS]

    identities = {
        "adjacency_char_matches_twin_pell_fingerprint": adjacency_char == [1, 0, -9, 0, 17, 0, -8, 0, 0],
        "squared_cubic_uses_q2_odd_instances_and_2q": squared_cubic == [1, -9, 17, -8],
        "adjacency_nullity_equals_cycle_rank": (
            adjacency_char[-1] == 0
            and adjacency_char[-2] == 0
            and graph["cycle_rank"] == 2
        ),
        "laplacian_has_one_zero_mode": laplacian_char[-1] == 0 and laplacian_char[-2] != 0,
        "matrix_tree_count_is_g_multiplicity": spanning_tree_count == G_MULTIPLICITY,
        "degree_sum_is_twice_zero_edges": sum(sum(row) for row in adjacency) == 2 * graph["edge_count"],
        "zero_sheet_is_8_vertices_9_edges_rank2": (
            graph["vertex_count"] == 8
            and graph["edge_count"] == 9
            and graph["cycle_rank"] == 2
        ),
    }

    return {
        "summary": {
            "experiment": "zero-sheet Twin-Pell adjacency fingerprint",
            "adjacency_characteristic_polynomial": polynomial_text(adjacency_char),
            "squared_spectral_cubic": "y^3 - 9y^2 + 17y - 8",
            "laplacian_characteristic_polynomial": polynomial_text(laplacian_char),
            "spanning_tree_count": spanning_tree_count,
            "all_identities_hold": all(identities.values()),
        },
        "zero_sheet_subgraph": graph,
        "adjacency_matrix": adjacency,
        "laplacian_matrix": laplacian,
        "adjacency_characteristic_coefficients": adjacency_char,
        "laplacian_characteristic_coefficients": laplacian_char,
        "twin_pell_dictionary": {
            "q^2": Q2,
            "2^q": TOMOTOPE_CELLS,
            "q^2+2^q": ODD_METRIC_INSTANCES,
            "squared_spectral_cubic_coefficients": squared_cubic,
            "reading": (
                "The nonzero squared adjacency spectrum of the zero sheet is governed by "
                "the cubic y^3 - q^2 y^2 + (q^2+2^q)y - 2^q."
            ),
        },
        "matrix_tree": {
            "spanning_tree_count": spanning_tree_count,
            "w33_g_multiplicity": G_MULTIPLICITY,
            "reading": "The zero-sheet Laplacian cofactor equals g=15, the W(3,3) -4 eigenspace multiplicity.",
        },
        "identities": identities,
        "honesty_boundary": (
            "This is an exact graph-spectral fingerprint of the Hamming/Fano zero sheet. "
            "It shows the Twin-Pell constants and g=15 inside the residual graph itself; "
            "it does not yet identify the graph as a canonical quotient of the full W(3,3) adjacency algebra."
        ),
    }


def main() -> None:
    payload = build_payload()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    result = {
        "theorem": "Zero-sheet Twin-Pell spectral fingerprint",
        "summary": payload["summary"],
        "twin_pell_dictionary": payload["twin_pell_dictionary"],
        "matrix_tree": payload["matrix_tree"],
        "identities": payload["identities"],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print("=== MCXV Zero-Sheet Twin-Pell Spectral Fingerprint ===")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {RESULT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
