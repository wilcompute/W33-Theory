#!/usr/bin/env python3
"""Part DCLXVIII: holonomy transvection Markov bridge.

After DCLXVII, the universal holonomy-screen bundle has collapsed to one
canonical tripotent polarization. The next honest question is whether that
tripotent already comes from averaging the 40 actual witness transvections
themselves.

This verifier proves the stronger statement. If P_x is the permutation matrix
on the 40 W(3,3) points induced by the anchor transvection at x, then the exact
average

    K = (1/40) sum_x P_x

is already a simple Markov kernel in the adjacency algebra:

    K = (12 I - A + J) / 40
      = 13/40 I + 1/40 (J - I - A).

So K fixes each point with probability 13/40, jumps uniformly to each of the
27 non-neighbors with probability 1/40, and never jumps to a commuting
neighbor. Moreover the DCLXVII tripotent is exactly the quadratic transform

    M = ((K - I)(60 K - 19 I)) / 3,

mapping the spectrum {1, 1/4, 2/5} of K to {0, 1, -1}.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
for path in (SCRIPTS,):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from w33_h1_decomposition import J_matrix, apply_matrix_projective, transvection_matrix
from w33_homology import build_w33

OUT_PATH = ROOT / "data" / "dclxviii_holonomy_transvection_markov_bridge.json"
MODULUS = 3


@dataclass(frozen=True)
class MarkovSummary:
    point_count: int
    anchor_count: int
    stay_probability_num: int
    stay_probability_den: int
    nonneighbor_jump_probability_num: int
    nonneighbor_jump_probability_den: int
    all_identities_hold: bool


def _adjacency_matrix(adj_lists: list[list[int]]) -> np.ndarray:
    n = len(adj_lists)
    matrix = np.zeros((n, n), dtype=float)
    for i, neighbors in enumerate(adj_lists):
        for j in neighbors:
            matrix[i, j] = 1.0
    return matrix


def _rounded_spectrum(matrix: np.ndarray) -> dict[str, int]:
    eigenvalues = np.linalg.eigvalsh(matrix)
    counts: Counter[str] = Counter()
    for value in eigenvalues:
        rounded = Fraction(value).limit_denominator()
        counts[str(rounded)] += 1
    return dict(sorted(counts.items(), key=lambda item: Fraction(item[0])))


def _permutation_matrix(transvection: np.ndarray, vertices: list[tuple[int, int, int, int]], index: dict[tuple[int, int, int, int], int]) -> np.ndarray:
    n = len(vertices)
    matrix = np.zeros((n, n), dtype=float)
    for column, vertex in enumerate(vertices):
        image = tuple(apply_matrix_projective(transvection, vertex))
        matrix[index[image], column] = 1.0
    return matrix


def build_bridge() -> dict[str, Any]:
    n, vertices, adj_lists, _ = build_w33()
    index = {tuple(vertex): i for i, vertex in enumerate(vertices)}
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    Jsym = J_matrix()

    permutation_sum = np.zeros((n, n), dtype=float)
    for anchor in vertices:
        transvection = transvection_matrix(np.array(anchor, dtype=int), Jsym)
        permutation_sum += _permutation_matrix(transvection, vertices, index)

    K = permutation_sum / n
    complement_walk = (12.0 * I - A + J) / 40.0
    routing_counts = np.rint(permutation_sum).astype(int)
    expected_counts = 13 * np.eye(n, dtype=int) + (np.ones((n, n), dtype=int) - np.eye(n, dtype=int) - A.astype(int))

    M_from_K = ((K - I) @ (60.0 * K - 19.0 * I)) / 3.0
    M_expected = (A + I - 13.0 * J / 40.0) / 3.0

    row_sums = sorted(set(str(Fraction(float(x)).limit_denominator()) for x in K.sum(axis=1).tolist()))
    col_sums = sorted(set(str(Fraction(float(x)).limit_denominator()) for x in K.sum(axis=0).tolist()))
    distinct_entries = sorted(set(float(K[i, j]) for i in range(n) for j in range(n)))
    spectrum = _rounded_spectrum(K)

    transformed_spectrum = {
        str(Fraction(((Fraction(value) - 1) * (60 * Fraction(value) - 19)), 3)): multiplicity
        for value, multiplicity in ((Fraction(1, 1), 1), (Fraction(1, 4), 24), (Fraction(2, 5), 15))
    }

    identities = {
        "average_of_40_transvection_permutations_is_in_the_w33_adjacency_algebra": np.allclose(K, complement_walk),
        "markov_kernel_is_symmetric_and_doubly_stochastic": np.allclose(K, K.T) and np.allclose(K.sum(axis=1), 1.0) and np.allclose(K.sum(axis=0), 1.0),
        "markov_kernel_has_entries_13_over_40_0_1_over_40": [str(Fraction(entry).limit_denominator()) for entry in distinct_entries] == ["0", "1/40", "13/40"],
        "stay_probability_is_13_over_40": abs(float(K[0, 0]) - 13.0 / 40.0) < 1e-8,
        "commuting_neighbors_have_zero_transition_probability": all(K[i, j] == 0.0 for i in range(n) for j in range(n) if A[i, j] == 1.0),
        "each_ordered_nonneighbor_pair_is_realized_by_exactly_one_anchor_transvection": np.array_equal(routing_counts, expected_counts),
        "markov_spectrum_is_1_1over4_24_2over5_15": spectrum == {"1/4": 24, "2/5": 15, "1": 1},
        "dclxvii_tripotent_is_the_exact_quadratic_transform_of_the_markov_kernel": np.allclose(M_from_K, M_expected),
        "quadratic_transform_maps_1_1over4_2over5_to_0_1_minus1": transformed_spectrum == {"0": 1, "1": 24, "-1": 15},
        "therefore_the_witness_family_collapses_to_a_complement_walk_then_to_the_canonical_tripotent": (
            np.allclose(K, complement_walk)
            and np.array_equal(routing_counts, expected_counts)
            and spectrum == {"1/4": 24, "2/5": 15, "1": 1}
            and np.allclose(M_from_K, M_expected)
        ),
    }

    summary = MarkovSummary(
        point_count=n,
        anchor_count=n,
        stay_probability_num=13,
        stay_probability_den=40,
        nonneighbor_jump_probability_num=1,
        nonneighbor_jump_probability_den=40,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "markov_coefficients": {"I": "3/10", "A": "-1/40", "J": "1/40"},
        "markov_statistics": {
            "distinct_entries": [str(Fraction(entry).limit_denominator()) for entry in distinct_entries],
            "row_sums": row_sums,
            "column_sums": col_sums,
            "spectrum": spectrum,
            "tripotent_image_of_markov_spectrum": transformed_spectrum,
        },
        "routing_statistics": {
            "diagonal_count": int(routing_counts[0, 0]),
            "edge_count": int(next(routing_counts[i, j] for i in range(n) for j in range(n) if A[i, j] == 1.0)),
            "nonedge_count": int(next(routing_counts[i, j] for i in range(n) for j in range(n) if i != j and A[i, j] == 0.0)),
        },
        "interpretation": {
            "average_operator": "K = (1/40) sum_x P_x = (12I - A + J)/40",
            "walk": "stay put with probability 13/40, jump uniformly to a non-neighbor with probability 1/40 each, never jump to a commuting neighbor",
            "tripotent_transform": "M = ((K-I)(60K-19I))/3",
            "breakthrough": (
                "The 40 witness transvections do not merely generate the holonomy-screen family abstractly. Their exact average is already a canonical complement-walk Markov kernel, and the DCLXVII tripotent is the quadratic Hecke transform of that averaged witness operator."
            ),
        },
        "identities": identities,
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()