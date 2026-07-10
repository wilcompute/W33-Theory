#!/usr/bin/env python3
"""Exact Levi duality-defect / characteristic-two incidence-Dirac verifier.

The symplectic generalized quadrangle W(3,3) has 40 points and 40 totally
isotropic lines.  If M is its 40 x 40 point-line incidence matrix, define

    D = [[0, M], [M^T, 0]].

Over characteristic zero, D is a graded self-adjoint incidence Dirac operator.
Its two Hamiltonian halves are the point and line collinearity graphs shifted
by four.  They have identical non-zero spectrum, but the two underlying graphs
are not isomorphic: the point half is W(3,3), while the line half is the point
graph of its non-isomorphic dual Q(4,3).

Over F_2, the shift by four disappears.  The two Hamiltonian halves become
square-zero differentials and D becomes nilpotent of exact index four.  This
script verifies the complete rank/kernel/Jordan filtration and identifies the
8/20 half-homology split that matches the previously computed W/Q
code-lattice glue ranks.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
from typing import Iterable

import networkx as nx
import numpy as np

Q = 3
ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "data" / "PART_2026_07_10_LEVI_DUALITY_DEFECT_results.json"


def normalize_projective(vector: Iterable[int], q: int = Q) -> tuple[int, ...]:
    """Return the canonical projective representative over F_q."""
    v = tuple(int(x) % q for x in vector)
    if not any(v):
        raise ValueError("the zero vector has no projective representative")
    first = next(x for x in v if x)
    inverse = pow(first, -1, q)
    return tuple((inverse * x) % q for x in v)


def symplectic_form(x: tuple[int, ...], y: tuple[int, ...], q: int = Q) -> int:
    """The standard alternating form on F_q^4."""
    return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % q


def build_w33() -> tuple[list[tuple[int, ...]], list[frozenset[int]], np.ndarray, np.ndarray]:
    """Construct points, isotropic lines, incidence M, and point adjacency A_W."""
    points = sorted(
        {
            normalize_projective(v)
            for v in product(range(Q), repeat=4)
            if any(v)
        }
    )
    point_index = {p: i for i, p in enumerate(points)}

    adjacency = np.zeros((len(points), len(points)), dtype=np.int64)
    for i, x in enumerate(points):
        for j in range(i + 1, len(points)):
            if symplectic_form(x, points[j]) == 0:
                adjacency[i, j] = adjacency[j, i] = 1

    line_set: set[frozenset[int]] = set()
    for i, j in combinations(range(len(points)), 2):
        if not adjacency[i, j]:
            continue
        x, y = points[i], points[j]
        line = frozenset(
            point_index[
                normalize_projective(
                    tuple((a * x[t] + b * y[t]) % Q for t in range(4))
                )
            ]
            for a, b in product(range(Q), repeat=2)
            if (a, b) != (0, 0)
        )
        line_set.add(line)

    lines = sorted(line_set, key=lambda line: tuple(sorted(line)))
    incidence = np.zeros((len(points), len(lines)), dtype=np.int64)
    for point in range(len(points)):
        for line_index, line in enumerate(lines):
            incidence[point, line_index] = int(point in line)

    return points, lines, incidence, adjacency


def gf2_rref(matrix: np.ndarray) -> tuple[np.ndarray, list[int]]:
    """Reduced row-echelon form and pivot columns over F_2."""
    a = np.asarray(matrix, dtype=np.uint8).copy() % 2
    rows, cols = a.shape
    pivots: list[int] = []
    pivot_row = 0
    for col in range(cols):
        selected = next((r for r in range(pivot_row, rows) if a[r, col]), None)
        if selected is None:
            continue
        if selected != pivot_row:
            a[[pivot_row, selected]] = a[[selected, pivot_row]]
        for r in range(rows):
            if r != pivot_row and a[r, col]:
                a[r] ^= a[pivot_row]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == rows:
            break
    return a, pivots


def gf2_rank(matrix: np.ndarray) -> int:
    return len(gf2_rref(matrix)[1])


def gf2_nullspace(matrix: np.ndarray) -> np.ndarray:
    """Return a matrix whose columns form a nullspace basis over F_2."""
    rref, pivots = gf2_rref(matrix)
    cols = rref.shape[1]
    free = [c for c in range(cols) if c not in pivots]
    basis: list[np.ndarray] = []
    for free_col in free:
        vector = np.zeros(cols, dtype=np.uint8)
        vector[free_col] = 1
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = rref[row, free_col]
        basis.append(vector)
    if not basis:
        return np.zeros((cols, 0), dtype=np.uint8)
    return np.stack(basis, axis=1)


def spectrum_multiplicities(matrix: np.ndarray) -> dict[str, int]:
    values = np.linalg.eigvalsh(matrix.astype(float))
    rounded = [round(float(value), 10) for value in values]
    counts: dict[str, int] = {}
    for value in rounded:
        if abs(value - round(value)) < 1e-8:
            key = str(int(round(value)))
        else:
            key = f"{value:.10g}"
        counts[key] = counts.get(key, 0) + 1
    return counts


def nilpotent_jordan_counts(dimension: int, ranks: list[int]) -> dict[str, int]:
    """Recover Jordan block counts from rank(N^k), k=1..nilpotency index."""
    rank_sequence = [dimension] + ranks
    kernel_dimensions = [dimension - rank for rank in rank_sequence]
    # Number of blocks of size at least k is ker(N^k)-ker(N^(k-1)).
    at_least = [
        kernel_dimensions[k] - kernel_dimensions[k - 1]
        for k in range(1, len(kernel_dimensions))
    ]
    exact: dict[str, int] = {}
    for size in range(1, len(at_least) + 1):
        next_count = at_least[size] if size < len(at_least) else 0
        exact[str(size)] = at_least[size - 1] - next_count
    return {size: count for size, count in exact.items() if count}


def maximum_independent_set(graph: nx.Graph) -> list[int]:
    clique, _ = nx.algorithms.clique.max_weight_clique(nx.complement(graph), weight=None)
    return sorted(int(vertex) for vertex in clique)


@lru_cache(maxsize=1)
def analyze() -> dict:
    points, lines, incidence, point_adjacency = build_w33()
    identity40 = np.eye(40, dtype=np.int64)
    line_adjacency = incidence.T @ incidence - 4 * identity40

    point_graph = nx.from_numpy_array(point_adjacency)
    line_graph = nx.from_numpy_array(line_adjacency)
    point_independent = maximum_independent_set(point_graph)
    line_independent = maximum_independent_set(line_graph)
    nonisomorphic_by_alpha = len(point_independent) != len(line_independent)

    zero40 = np.zeros((40, 40), dtype=np.int64)
    dirac = np.block([[zero40, incidence], [incidence.T, zero40]])
    grading = np.diag(np.r_[np.ones(40, dtype=np.int64), -np.ones(40, dtype=np.int64)])
    hamiltonian = dirac @ dirac

    incidence_gram_spectrum = spectrum_multiplicities(incidence @ incidence.T)
    dirac_spectrum_numeric = np.linalg.eigvalsh(dirac.astype(float))
    dirac_spectrum = {
        "-4": int(np.sum(np.isclose(dirac_spectrum_numeric, -4.0))),
        "-sqrt(6)": int(np.sum(np.isclose(dirac_spectrum_numeric, -np.sqrt(6.0)))),
        "0": int(np.sum(np.isclose(dirac_spectrum_numeric, 0.0))),
        "+sqrt(6)": int(np.sum(np.isclose(dirac_spectrum_numeric, np.sqrt(6.0)))),
        "+4": int(np.sum(np.isclose(dirac_spectrum_numeric, 4.0))),
    }

    incidence2 = incidence.astype(np.uint8) % 2
    point2 = point_adjacency.astype(np.uint8) % 2
    line2 = line_adjacency.astype(np.uint8) % 2
    zero40_2 = np.zeros((40, 40), dtype=np.uint8)
    dirac2 = np.block([[zero40_2, incidence2], [incidence2.T, zero40_2]]) % 2

    powers2: list[np.ndarray] = []
    current = np.eye(80, dtype=np.uint8)
    for _ in range(4):
        current = (current @ dirac2) % 2
        powers2.append(current.copy())
    dirac2_ranks = [gf2_rank(power) for power in powers2]
    kernel_filtration = [80 - rank for rank in dirac2_ranks]
    jordan = nilpotent_jordan_counts(80, dirac2_ranks)

    rank_point2 = gf2_rank(point2)
    rank_line2 = gf2_rank(line2)
    point_homology_dimension = 40 - 2 * rank_point2
    line_homology_dimension = 40 - 2 * rank_line2

    point_kernel = gf2_nullspace(point2)
    line_kernel = gf2_nullspace(line2)
    point_to_line = (incidence2.T @ point_kernel) % 2
    line_to_point = (incidence2 @ line_kernel) % 2
    induced_point_to_line_rank = (
        gf2_rank(np.concatenate([line2, point_to_line], axis=1)) - rank_line2
    )
    induced_line_to_point_rank = (
        gf2_rank(np.concatenate([point2, line_to_point], axis=1)) - rank_point2
    )

    checks = {
        "geometry_40_points": len(points) == 40,
        "geometry_40_lines": len(lines) == 40,
        "geometry_160_flags": int(incidence.sum()) == 160,
        "four_lines_through_each_point": bool(np.all(incidence.sum(axis=1) == 4)),
        "four_points_on_each_line": bool(np.all(incidence.sum(axis=0) == 4)),
        "point_gram_identity": bool(np.array_equal(incidence @ incidence.T, point_adjacency + 4 * identity40)),
        "line_gram_identity": bool(np.array_equal(incidence.T @ incidence, line_adjacency + 4 * identity40)),
        "graded_anticommutation": bool(np.array_equal(grading @ dirac + dirac @ grading, np.zeros((80, 80), dtype=np.int64))),
        "hamiltonian_block_identity": bool(
            np.array_equal(
                hamiltonian,
                np.block(
                    [
                        [point_adjacency + 4 * identity40, zero40],
                        [zero40, line_adjacency + 4 * identity40],
                    ]
                ),
            )
        ),
        "incidence_rank_char0_25": int(np.linalg.matrix_rank(incidence)) == 25,
        "incidence_gram_spectrum_16_6_0": incidence_gram_spectrum == {"0": 15, "6": 24, "16": 1},
        "dirac_spectrum_expected": dirac_spectrum == {"-4": 1, "-sqrt(6)": 24, "0": 30, "+sqrt(6)": 24, "+4": 1},
        "balanced_zero_modes_15_plus_15": 40 - int(np.linalg.matrix_rank(incidence)) == 15,
        "point_line_graphs_nonisomorphic": nonisomorphic_by_alpha,
        "point_alpha_7": len(point_independent) == 7,
        "line_alpha_10": len(line_independent) == 10,
        "char2_half_factorization_point": bool(np.array_equal((incidence2 @ incidence2.T) % 2, point2)),
        "char2_half_factorization_line": bool(np.array_equal((incidence2.T @ incidence2) % 2, line2)),
        "point_differential_square_zero": bool(not np.any((point2 @ point2) % 2)),
        "line_differential_square_zero": bool(not np.any((line2 @ line2) % 2)),
        "dirac_nilpotency_index_4": bool(np.any(powers2[2]) and not np.any(powers2[3])),
        "dirac_rank_ladder_50_26_2_0": dirac2_ranks == [50, 26, 2, 0],
        "dirac_kernel_filtration_30_54_78_80": kernel_filtration == [30, 54, 78, 80],
        "dirac_jordan_type_4x2_3x22_1x6": jordan == {"1": 6, "3": 22, "4": 2},
        "half_ranks_16_10": [rank_point2, rank_line2] == [16, 10],
        "half_homology_8_20": [point_homology_dimension, line_homology_dimension] == [8, 20],
        "half_homology_sum_28": point_homology_dimension + line_homology_dimension == 28,
        "incidence_induced_maps_zero_on_homology": induced_point_to_line_rank == induced_line_to_point_rank == 0,
    }

    result = {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "title": "Levi Duality-Defect and Characteristic-Two Incidence-Dirac Theorem",
        "geometry": {
            "q": Q,
            "points": len(points),
            "lines": len(lines),
            "flags": int(incidence.sum()),
            "point_graph": "W(3,3)",
            "line_graph": "Q(4,3) point graph",
            "point_line_graphs_isomorphic": False if nonisomorphic_by_alpha else None,
            "maximum_independent_set_point_graph": point_independent,
            "alpha_point_graph": len(point_independent),
            "maximum_independent_set_line_graph": line_independent,
            "alpha_line_graph": len(line_independent),
        },
        "characteristic_zero": {
            "incidence_rank": int(np.linalg.matrix_rank(incidence)),
            "incidence_gram_spectrum": incidence_gram_spectrum,
            "dirac_spectrum": dirac_spectrum,
            "point_zero_modes": 40 - int(np.linalg.matrix_rank(incidence.T)),
            "line_zero_modes": 40 - int(np.linalg.matrix_rank(incidence)),
            "witten_index": 0,
            "grading_flip_automorphism_exists": False,
        },
        "characteristic_two": {
            "incidence_rank": gf2_rank(incidence2),
            "dirac_power_ranks": {str(i + 1): rank for i, rank in enumerate(dirac2_ranks)},
            "dirac_kernel_filtration": {str(i + 1): dim for i, dim in enumerate(kernel_filtration)},
            "dirac_jordan_blocks": jordan,
            "point_half_rank": rank_point2,
            "line_half_rank": rank_line2,
            "point_half_homology_dimension": point_homology_dimension,
            "line_half_homology_dimension": line_homology_dimension,
            "homology_dimension_sum": point_homology_dimension + line_homology_dimension,
            "induced_point_to_line_homology_rank": induced_point_to_line_rank,
            "induced_line_to_point_homology_rank": induced_line_to_point_rank,
            "rank_ladder_reading": {
                "50": "5*Phi_4",
                "26": "2*Phi_3",
                "2": "lambda",
                "0": "nilpotent closure",
            },
            "kernel_ladder_reading": {
                "30": "h(E8)",
                "54": "2*q^3",
                "78": "dim(E6)",
                "80": "2*v",
            },
        },
        "interpretation": {
            "spectrally_paired": True,
            "geometrically_swappable": False,
            "type_bit_is_intrinsic": True,
            "char2_glue_dimensions_explained": [8, 20],
            "boundary": (
                "The exceptional-number labels are exact arithmetic readings of the "
                "verified filtration; they are not by themselves a continuum-physics derivation."
            ),
        },
        "checks": checks,
    }
    return result


def main() -> int:
    result = analyze()
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
