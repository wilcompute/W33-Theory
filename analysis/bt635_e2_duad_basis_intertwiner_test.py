#!/usr/bin/env python3
"""BT635: E2 duad-basis intertwiner test.

BT632 proposed an explicit carrier for the E2 block:

    E2_model = Q^{15}_{K6 duads} \otimes Q^2_{phase sign},
    B_E2   = 37 I + 40 sigma_z.

BT635 tests what this carrier actually guarantees.  It builds the K6-duad
basis, the T(6)=L(K6) adjacency, the two phase sheets, and the phase split
operator.  The resulting model has the exact E2 spectrum

    77^15 + (-3)^15,

and it commutes with the entire duad permutation action.  Therefore the
candidate is a valid representation-level carrier for the 15+15 split.

Boundary: without a concrete numeric basis for the actual E2 eigenspace in the
folded-Hashimoto 160-flag module, this is not yet a canonical coordinate
intertwiner from the computed E2 matrix to duads.  It is the strongest exact
carrier/intertwiner test available at the representation level.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


def duads(n: int = 6) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(1, n + 1), 2))


def permutation_matrix_on_duads(perm: tuple[int, ...], labels: list[tuple[int, int]]) -> np.ndarray:
    index = {d: i for i, d in enumerate(labels)}
    P = np.zeros((len(labels), len(labels)), dtype=int)
    for j, d in enumerate(labels):
        image = tuple(sorted((perm[d[0] - 1], perm[d[1] - 1])))
        P[index[image], j] = 1
    return P


def main() -> int:
    labels = duads(6)
    n = len(labels)
    A = np.zeros((n, n), dtype=int)
    for i, a in enumerate(labels):
        for j, b in enumerate(labels):
            if i != j and len(set(a) & set(b)) == 1:
                A[i, j] = 1

    I15 = np.eye(n, dtype=int)
    I2 = np.eye(2, dtype=int)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=int)
    B_e2 = 37 * np.eye(2 * n, dtype=int) + 40 * np.kron(I15, sigma_z)
    P_plus = np.kron(I15, np.array([[1, 0], [0, 0]], dtype=int))
    P_minus = np.kron(I15, np.array([[0, 0], [0, 1]], dtype=int))
    A_lift = np.kron(A, I2)

    eigvals = sorted(int(round(x)) for x in np.linalg.eigvalsh(B_e2))
    plus_rank = int(np.linalg.matrix_rank(P_plus))
    minus_rank = int(np.linalg.matrix_rank(P_minus))

    # S6 representation test: sample a generating set for S6, adjacent swaps.
    generators = []
    base = tuple(range(1, 7))
    for s in range(5):
        p = list(base)
        p[s], p[s + 1] = p[s + 1], p[s]
        generators.append(tuple(p))
    commutator_norms = []
    for perm in generators:
        P15 = permutation_matrix_on_duads(perm, labels)
        P30 = np.kron(P15, I2)
        commutator_norms.append(int(np.max(np.abs(P30 @ B_e2 - B_e2 @ P30))))
        commutator_norms.append(int(np.max(np.abs(P30 @ P_plus - P_plus @ P30))))
        commutator_norms.append(int(np.max(np.abs(P30 @ P_minus - P_minus @ P30))))

    # T(6) context: degree 8 and S6-duad spectrum 8^1, 2^5, -2^9.
    A_eig = sorted(round(float(x), 10) for x in np.linalg.eigvalsh(A))
    spectrum_counts = {str(v): A_eig.count(v) for v in sorted(set(A_eig))}

    minpoly_residual = B_e2 @ B_e2 - 74 * B_e2 - 231 * np.eye(2 * n, dtype=int)
    projectors_sum = P_plus + P_minus
    projectors_product = P_plus @ P_minus

    checks = {
        "duad_count_15": n == 15,
        "carrier_dimension_30": B_e2.shape == (30, 30),
        "B_e2_spectrum_77_15_minus3_15": eigvals == ([-3] * 15 + [77] * 15),
        "minimal_polynomial_zero": int(np.max(np.abs(minpoly_residual))) == 0,
        "plus_rank_15": plus_rank == 15,
        "minus_rank_15": minus_rank == 15,
        "projectors_sum_identity": np.array_equal(projectors_sum, np.eye(30, dtype=int)),
        "projectors_orthogonal": np.array_equal(projectors_product, np.zeros((30, 30), dtype=int)),
        "projectors_commute_with_duad_adjacency_lift": int(np.max(np.abs(A_lift @ P_plus - P_plus @ A_lift))) == 0 and int(np.max(np.abs(A_lift @ P_minus - P_minus @ A_lift))) == 0,
        "S6_generators_commute_with_phase_split": max(commutator_norms) == 0,
        "T6_degree_8": sorted(set(np.sum(A, axis=1).tolist())) == [8],
        "T6_spectrum_8_1_2_5_minus2_9": spectrum_counts == {"-2.0": 9, "2.0": 5, "8.0": 1},
        "canonical_numeric_intertwiner_not_claimed": True,
    }

    result = {
        "bt": 635,
        "title": "E2 duad-basis intertwiner test",
        "carrier": "K6 duads x two phase sheets",
        "duad_count": n,
        "basis_dimension": 2 * n,
        "operator": "B_E2 = 37I + 40 sigma_z",
        "spectrum": {"77": 15, "-3": 15},
        "projectors": {
            "P_plus": "rank 15, + phase sheet, eigenvalue 77",
            "P_minus": "rank 15, - phase sheet, eigenvalue -3",
            "sum": "P_plus + P_minus = I_30",
        },
        "duad_adjacency_context": {
            "graph": "T(6)=L(K6)",
            "degree": 8,
            "spectrum": spectrum_counts,
            "interpretation": "The 15 duad labels carry the familiar S6 module 1+5+9. The phase sheet supplies the 15+15 split demanded by E2F3E2.",
        },
        "intertwiner_status": "representation-level carrier test passed; canonical numeric E2-coordinate intertwiner remains a future construction requiring an explicit basis for the computed E2 eigenspace in the 160-flag module.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT635_E2_DUAD_BASIS_INTERTWINER_TEST_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
