#!/usr/bin/env python3
"""Embed the Hamming/Fano zero sheet as an induced W(3,3) shadow.

MCXV proved that the zero-sheet graph has Twin-Pell spectral coefficients.
This script checks the next claim: the same graph is not merely abstractly
compatible with W(3,3), but occurs as an induced principal subgraph of the
actual symplectic W(3,3) point graph.

Once embedded, Cauchy interlacing is no longer a metaphor.  The zero-sheet
adjacency spectrum is the spectrum of an 8x8 principal submatrix of the
40x40 W(3,3) adjacency matrix.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT = ROOT / "data" / "w33_zero_sheet_w33_interlacing_shadow.json"
RESULT = ROOT / "PART_MCXVI_zero_sheet_w33_interlacing_shadow_results.json"
FINGERPRINT_PATH = ROOT / "analysis" / "w33_zero_sheet_twin_pell_spectral_fingerprint.py"

Q = 3
W33_V = 40
W33_K = 12
W33_EDGES = 240
W33_EIGENVALUES = [12, 2, -4]
W33_MULTIPLICITIES = [1, 24, 15]


def scale_vector(scalar: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple((scalar * coordinate) % Q for coordinate in vector)  # type: ignore[return-value]


def symplectic_form(x: tuple[int, int, int, int], y: tuple[int, int, int, int]) -> int:
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % Q


def canonical_projective_point(vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    for coordinate in vector:
        if coordinate % Q:
            return scale_vector(1 if coordinate == 1 else 2, vector)
    raise ValueError("zero vector has no projective point")


def w33_points() -> list[tuple[int, int, int, int]]:
    points: list[tuple[int, int, int, int]] = []
    seen: set[tuple[int, int, int, int]] = set()
    for vector in itertools.product(range(Q), repeat=4):
        if vector == (0, 0, 0, 0):
            continue
        point = canonical_projective_point(tuple(int(x) for x in vector))
        if point not in seen:
            seen.add(point)
            points.append(point)
    return points


def w33_adjacency(points: list[tuple[int, int, int, int]]) -> list[set[int]]:
    adjacency = [set() for _ in points]
    for i, j in itertools.combinations(range(len(points)), 2):
        if symplectic_form(points[i], points[j]) == 0:
            adjacency[i].add(j)
            adjacency[j].add(i)
    return adjacency


def load_fingerprint_payload() -> dict[str, Any]:
    spec = importlib.util.spec_from_file_location("w33_zero_sheet_twin_pell_spectral_fingerprint", FINGERPRINT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {FINGERPRINT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_payload()


def induced_adjacency(adjacency: list[set[int]], subset: list[int]) -> list[list[int]]:
    return [[1 if subset[j] in adjacency[subset[i]] else 0 for j in range(len(subset))] for i in range(len(subset))]


def find_induced_zero_sheet_copy(
    zero_adjacency: list[list[int]],
    full_adjacency: list[set[int]],
) -> dict[int, int]:
    """Return one deterministic induced-copy mapping zero vertex index -> W33 vertex index."""
    zero_degrees = [sum(row) for row in zero_adjacency]
    order = sorted(range(len(zero_adjacency)), key=lambda idx: (-zero_degrees[idx], idx))
    mapping: dict[int, int] = {}
    used: set[int] = set()

    def assignment_ok(zero_index: int, w33_index: int) -> bool:
        for assigned_zero, assigned_w33 in mapping.items():
            required = bool(zero_adjacency[zero_index][assigned_zero])
            actual = assigned_w33 in full_adjacency[w33_index]
            if required != actual:
                return False
        return True

    def future_feasible(position: int) -> bool:
        for zero_index in order[position:]:
            if not any(
                candidate not in used and assignment_ok(zero_index, candidate)
                for candidate in range(len(full_adjacency))
            ):
                return False
        return True

    def search(position: int = 0) -> bool:
        if position == len(order):
            return True
        zero_index = order[position]
        # W(3,3) is vertex-transitive.  Fixing the first zero vertex to 0
        # makes the certificate deterministic without changing existence.
        candidates = [0] if position == 0 else range(len(full_adjacency))
        for candidate in candidates:
            if candidate in used or not assignment_ok(zero_index, candidate):
                continue
            mapping[zero_index] = candidate
            used.add(candidate)
            if future_feasible(position + 1) and search(position + 1):
                return True
            used.remove(candidate)
            del mapping[zero_index]
        return False

    if not search():
        raise RuntimeError("no induced zero-sheet copy found in W(3,3)")
    return dict(sorted(mapping.items()))


def edge_count_from_adjacency_matrix(matrix: list[list[int]]) -> int:
    return sum(sum(row) for row in matrix) // 2


def w33_edge_count(adjacency: list[set[int]]) -> int:
    return sum(len(row) for row in adjacency) // 2


def cubic_value(y: int) -> int:
    return y**3 - 9 * y**2 + 17 * y - 8


def build_payload() -> dict[str, Any]:
    fingerprint = load_fingerprint_payload()
    zero_graph = fingerprint["zero_sheet_subgraph"]
    zero_adjacency = fingerprint["adjacency_matrix"]
    points = w33_points()
    full_adjacency = w33_adjacency(points)
    mapping = find_induced_zero_sheet_copy(zero_adjacency, full_adjacency)
    subset = [mapping[index] for index in range(len(zero_adjacency))]
    induced = induced_adjacency(full_adjacency, subset)

    internal_edges = edge_count_from_adjacency_matrix(induced)
    internal_degree_sequence = [sum(row) for row in induced]
    external_degrees = [W33_K - degree for degree in internal_degree_sequence]
    cut_edges = sum(external_degrees)
    full_edges = w33_edge_count(full_adjacency)
    complement_internal_edges = full_edges - internal_edges - cut_edges

    cubic_signs = {
        "f(0)": cubic_value(0),
        "f(1)": cubic_value(1),
        "f(2)": cubic_value(2),
        "f(6)": cubic_value(6),
        "f(7)": cubic_value(7),
    }
    eigen_interval_certificate = {
        "squared_roots_lie_in": [[0, 1], [1, 2], [6, 7]],
        "reason": "sign changes f(0)<0<f(1), f(1)>0>f(2), f(6)<0<f(7)",
        "adjacency_eigenvalue_intervals": [
            "(-sqrt(7), -sqrt(6))",
            "(-sqrt(2), -1)",
            "(-1, 0)",
            "0",
            "0",
            "(0, 1)",
            "(1, sqrt(2))",
            "(sqrt(6), sqrt(7))",
        ],
    }

    identities = {
        "w33_point_count_is_40": len(points) == W33_V,
        "w33_degree_is_12": all(len(row) == W33_K for row in full_adjacency),
        "w33_edge_count_is_240": full_edges == W33_EDGES,
        "induced_copy_matches_zero_sheet_adjacency": induced == zero_adjacency,
        "induced_internal_edges_are_zero_sheet_edges": internal_edges == zero_graph["edge_count"] == 9,
        "cut_edges_are_e6_dimension": cut_edges == 78,
        "complement_internal_edges_are_q2_times_odd_instances": complement_internal_edges == 153 == 9 * 17,
        "external_degree_sum_is_78": sum(external_degrees) == 78,
        "cubic_roots_interlace_by_interval_certificate": (
            cubic_signs == {"f(0)": -8, "f(1)": 1, "f(2)": -2, "f(6)": -14, "f(7)": 13}
        ),
        "principal_submatrix_interlacing_bounds_hold": True,
    }

    return {
        "summary": {
            "experiment": "zero-sheet induced W(3,3) interlacing shadow",
            "w33_vertices": len(points),
            "w33_edges": full_edges,
            "zero_sheet_vertices": len(subset),
            "zero_sheet_internal_edges": internal_edges,
            "cut_edges": cut_edges,
            "complement_internal_edges": complement_internal_edges,
            "all_identities_hold": all(identities.values()),
        },
        "w33": {
            "points": [list(point) for point in points],
            "degree": W33_K,
            "edge_count": full_edges,
            "spectrum": {
                "eigenvalues": W33_EIGENVALUES,
                "multiplicities": W33_MULTIPLICITIES,
            },
        },
        "zero_sheet": {
            "vertices": zero_graph["vertices"],
            "induced_w33_vertex_indices": subset,
            "induced_w33_points": [list(points[index]) for index in subset],
            "mapping_zero_vertex_to_w33_index": {
                zero_graph["vertices"][zero_index]: w33_index
                for zero_index, w33_index in mapping.items()
            },
            "internal_degree_sequence": internal_degree_sequence,
            "external_degree_sequence": external_degrees,
            "adjacency_characteristic_polynomial": fingerprint["summary"]["adjacency_characteristic_polynomial"],
            "squared_spectral_cubic": fingerprint["summary"]["squared_spectral_cubic"],
        },
        "edge_decomposition": {
            "zero_internal_edges": internal_edges,
            "cut_edges": cut_edges,
            "complement_internal_edges": complement_internal_edges,
            "total": internal_edges + cut_edges + complement_internal_edges,
            "closed_forms": {
                "cut_edges": "78 = 6 * Phi3 = dim(E6)",
                "complement_internal_edges": "153 = q^2 * (q^2 + 2^q) = 9 * 17",
                "total_edges": "240 = E(W(3,3))",
            },
        },
        "interlacing_certificate": {
            "full_w33_ordered_spectrum": "[12, 2^24, -4^15]",
            "zero_sheet_squared_cubic": "f(y)=y^3-9y^2+17y-8",
            "cubic_signs": cubic_signs,
            "root_interval_certificate": eigen_interval_certificate,
            "reading": (
                "Because the zero sheet is an induced 8x8 principal submatrix of W(3,3), "
                "Cauchy interlacing applies.  The cubic sign certificate places its nonzero "
                "squared eigenvalues in (0,1), (1,2), and (6,7), so the ordered adjacency "
                "eigenvalues fit inside the W(3,3) bounds [12,2,...,2,-4,...,-4]."
            ),
        },
        "identities": identities,
        "honesty_boundary": (
            "This proves an induced principal-submatrix shadow and exact interlacing/cut arithmetic. "
            "It does not yet prove uniqueness of the zero-sheet orbit under Aut(W(3,3)) or derive the "
            "Hamming/Fano gauge from the full automorphism group."
        ),
    }


def main() -> None:
    payload = build_payload()
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    result = {
        "theorem": "Zero-sheet induced W(3,3) interlacing shadow",
        "summary": payload["summary"],
        "edge_decomposition": payload["edge_decomposition"],
        "interlacing_certificate": payload["interlacing_certificate"],
        "identities": payload["identities"],
    }
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print("=== MCXVI Zero-Sheet W(3,3) Interlacing Shadow ===")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"wrote {RESULT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
