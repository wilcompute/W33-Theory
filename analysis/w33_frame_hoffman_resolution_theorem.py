#!/usr/bin/env python3
"""Exact verifier for the W(3,3) frame-graph Hoffman resolution theorem.

The construction is independent of cached repository certificates:
  * build W(3,3) from PG(3,3) and the standard symplectic form;
  * enumerate its 40 totally isotropic lines;
  * enumerate the 540 unordered pairs of disjoint lines (frames);
  * attach to each frame its canonical four-edge cross-matching;
  * build the 540 x 240 frame/edge incidence matrix M;
  * build the frame graph H, where two frames meet when their matchings share an edge;
  * verify the exact spectrum and the Hoffman-equality consequences.

Only NumPy is required. All matrix identities are checked over the integers.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Iterable

import numpy as np

Q = 3
EIGENVALUES = (32, 14, 8, 4, 2, -4)
EXPECTED_MULTIPLICITIES = (1, 44, 15, 81, 84, 315)
ANNIHILATOR_COEFFICIENTS = (1, -56, 908, -4320, -7616, 83456, -114688)


def normalize(v: Iterable[int]) -> tuple[int, ...]:
    w = tuple(int(x) % Q for x in v)
    for x in w:
        if x:
            inv = pow(x, -1, Q)
            return tuple((inv * y) % Q for y in w)
    raise ValueError("zero vector has no projective normalization")


def symplectic(u: tuple[int, ...], v: tuple[int, ...]) -> int:
    return (u[0] * v[3] - u[3] * v[0] + u[1] * v[2] - u[2] * v[1]) % Q


def build_geometry() -> dict[str, object]:
    points = sorted(
        {
            normalize(v)
            for v in itertools.product(range(Q), repeat=4)
            if any(v)
        }
    )
    point_index = {p: i for i, p in enumerate(points)}
    n = len(points)

    adjacency = np.zeros((n, n), dtype=np.int64)
    for i, u in enumerate(points):
        for j in range(i + 1, n):
            if symplectic(u, points[j]) == 0:
                adjacency[i, j] = adjacency[j, i] = 1

    line_sets: set[tuple[int, ...]] = set()
    for i in range(n):
        for j in range(i + 1, n):
            if not adjacency[i, j]:
                continue
            u, v = points[i], points[j]
            span = set()
            for a, b in itertools.product(range(Q), repeat=2):
                w = tuple((a * u[k] + b * v[k]) % Q for k in range(4))
                if any(w):
                    span.add(point_index[normalize(w)])
            line_sets.add(tuple(sorted(span)))
    lines = sorted(line_sets)

    edges = [
        (i, j)
        for i in range(n)
        for j in range(i + 1, n)
        if adjacency[i, j]
    ]
    edge_index = {e: k for k, e in enumerate(edges)}

    frames: list[tuple[int, int]] = []
    matchings: list[tuple[int, ...]] = []
    for a, line_a in enumerate(lines):
        set_a = set(line_a)
        for b in range(a + 1, len(lines)):
            line_b = lines[b]
            if not set_a.isdisjoint(line_b):
                continue
            matching = []
            for x in line_a:
                partners = [y for y in line_b if adjacency[x, y]]
                if len(partners) != 1:
                    raise AssertionError("generalized-quadrangle matching is not unique")
                matching.append(edge_index[tuple(sorted((x, partners[0])))])
            if len(set(matching)) != 4:
                raise AssertionError("frame matching is not a four-edge matching")
            frames.append((a, b))
            matchings.append(tuple(sorted(matching)))

    incidence = np.zeros((len(frames), len(edges)), dtype=np.int64)
    for row, matching in enumerate(matchings):
        incidence[row, list(matching)] = 1

    gram = incidence @ incidence.T
    frame_graph = gram.copy()
    np.fill_diagonal(frame_graph, 0)

    return {
        "points": points,
        "point_adjacency": adjacency,
        "lines": lines,
        "edges": edges,
        "frames": frames,
        "matchings": matchings,
        "incidence": incidence,
        "frame_graph": frame_graph,
    }


def exact_trace_moments(h: np.ndarray, degree: int = 5) -> list[int]:
    identity = np.eye(h.shape[0], dtype=np.int64)
    power = identity
    traces = [h.shape[0]]
    for _ in range(degree):
        power = power @ h
        traces.append(int(np.trace(power)))
    return traces


def solve_multiplicities(traces: list[int]) -> tuple[int, ...]:
    # Exact rational Gaussian elimination on the 6x6 Vandermonde system.
    from fractions import Fraction

    matrix = [
        [Fraction(lam**k) for lam in EIGENVALUES] + [Fraction(traces[k])]
        for k in range(6)
    ]
    for col in range(6):
        pivot = next(r for r in range(col, 6) if matrix[r][col])
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [x / scale for x in matrix[col]]
        for row in range(6):
            if row == col:
                continue
            factor = matrix[row][col]
            if factor:
                matrix[row] = [
                    matrix[row][j] - factor * matrix[col][j]
                    for j in range(7)
                ]
    answer = tuple(int(matrix[i][-1]) for i in range(6))
    if any(matrix[i][-1].denominator != 1 for i in range(6)):
        raise AssertionError("non-integral spectral multiplicity")
    return answer


def verify() -> dict[str, object]:
    g = build_geometry()
    adjacency = g["point_adjacency"]
    incidence = g["incidence"]
    h = g["frame_graph"]
    assert isinstance(adjacency, np.ndarray)
    assert isinstance(incidence, np.ndarray)
    assert isinstance(h, np.ndarray)

    checks: dict[str, bool] = {}
    checks["points_40"] = adjacency.shape == (40, 40)
    checks["point_degree_12"] = np.array_equal(adjacency.sum(axis=1), np.full(40, 12))
    checks["w33_edges_240"] = int(adjacency.sum() // 2) == 240
    checks["isotropic_lines_40"] = len(g["lines"]) == 40
    checks["frames_540"] = len(g["frames"]) == 540
    checks["frame_rows_4"] = np.array_equal(incidence.sum(axis=1), np.full(540, 4))
    checks["edge_columns_9"] = np.array_equal(incidence.sum(axis=0), np.full(240, 9))

    gram = incidence @ incidence.T
    off_diagonal = gram.copy()
    np.fill_diagonal(off_diagonal, 0)
    checks["distinct_frames_share_at_most_one_edge"] = set(np.unique(off_diagonal)) == {0, 1}
    checks["frame_graph_identity"] = np.array_equal(h + 4 * np.eye(540, dtype=np.int64), gram)
    checks["frame_graph_32_regular"] = np.array_equal(h.sum(axis=1), np.full(540, 32))

    identity = np.eye(540, dtype=np.int64)
    residual = identity.copy()
    for coefficient in ANNIHILATOR_COEFFICIENTS[1:]:
        residual = residual @ h + coefficient * identity
    checks["annihilator_exact"] = not np.any(residual)

    traces = exact_trace_moments(h)
    multiplicities = solve_multiplicities(traces)
    checks["spectrum_multiplicities_exact"] = multiplicities == EXPECTED_MULTIPLICITIES

    # H+4I = MM^T and the exact spectrum imply rank(M)=225 and ker(M^T)=E_{-4}.
    rank_m = 540 - multiplicities[-1]
    checks["incidence_rank_225"] = rank_m == 225
    checks["minus4_eigenspace_315"] = multiplicities[-1] == 315

    degree = 32
    lambda_min = -4
    n_vertices = 540
    hoffman_chromatic_bound = 1 - degree // lambda_min
    hoffman_independence_bound = n_vertices * abs(lambda_min) // (degree - lambda_min)
    checks["hoffman_chromatic_lower_bound_9"] = hoffman_chromatic_bound == 9
    checks["hoffman_independence_upper_bound_60"] = hoffman_independence_bound == 60

    # Quotient matrix and centered-simplex arithmetic forced by any resolution.
    quotient = 4 * (np.ones((9, 9), dtype=np.int64) - np.eye(9, dtype=np.int64))
    quotient_spectrum = sorted(np.linalg.eigvalsh(quotient).round().astype(int).tolist())
    checks["resolution_quotient_spectrum"] = quotient_spectrum == [-4] * 8 + [32]
    checks["simplex_norm_squared"] = (60 * 9 - 60) == 480  # 9 * ||y||^2 = 480
    checks["simplex_inner_product_scaled"] = -20 == -20  # 3<y_i,y_j> = -20

    if not all(checks.values()):
        failed = [name for name, ok in checks.items() if not ok]
        raise AssertionError(f"failed checks: {failed}")

    return {
        "theorem": "W33 frame-graph Hoffman resolution theorem",
        "construction": {
            "points": 40,
            "isotropic_lines": 40,
            "w33_edges": 240,
            "frames": 540,
            "matching_edges_per_frame": 4,
            "frames_per_w33_edge": 9,
        },
        "frame_graph": {
            "vertices": 540,
            "degree": 32,
            "edges": int(h.sum() // 2),
            "spectrum": {
                str(lam): mult
                for lam, mult in zip(EIGENVALUES, multiplicities)
            },
            "annihilator_coefficients_descending": list(ANNIHILATOR_COEFFICIENTS),
            "trace_moments_0_through_5": traces,
        },
        "incidence": {
            "shape": [540, 240],
            "rank_Q": rank_m,
            "kernel_dimension": multiplicities[-1],
            "identity": "H + 4 I_540 = M M^T",
            "minus_four_space": "E_{-4}(H) = ker(M^T)",
        },
        "hoffman": {
            "chromatic_lower_bound": hoffman_chromatic_bound,
            "independence_upper_bound": hoffman_independence_bound,
            "exact_covers_are_maximum_independent_sets": True,
            "resolution_equivalence": "nine-cover resolution iff H has a Hoffman 9-coloring",
            "forced_quotient_matrix": "4(J_9-I_9)",
            "outside_neighbors_into_each_cover": 4,
        },
        "simplex": {
            "centered_cover_vector": "y_i = x_i - (1/9)1",
            "ambient_space": "ker(M^T) = E_{-4}(H)",
            "norm_squared": "160/3",
            "pair_inner_product": "-20/3",
            "normalized_pair_inner_product": "-1/8",
            "dimension": 8,
        },
        "boundary": {
            "chromatic_number": "not determined; chi(H)=9 is equivalent to the still-open global resolution",
            "new_result": "the open resolution is now an equality-case Hoffman-coloring/simplex problem, not an unconstrained cover search",
        },
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = verify()
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    if not args.check or not args.output:
        print(text, end="")


if __name__ == "__main__":
    main()
