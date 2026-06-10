#!/usr/bin/env python3
"""BT638: E2 duad-phase coordinate intertwiner.

BT635 verified the representation-level carrier

    Q^{15}_{K6 duads} tensor Q^2_{+-}

for the E2 split 77^15 + (-3)^15.  BT638 makes the coordinate selectors
explicit.  It constructs the two rank-15 partial isometries

    S_+ : Q^15 -> Q^30,     d |-> (d,+),
    S_- : Q^15 -> Q^30,     d |-> (d,-),

and verifies that they diagonalize the duad-phase E2 operator:

    S_+^T B_E2 S_+ = 77 I_15,
    S_-^T B_E2 S_- = -3 I_15,
    S_+^T B_E2 S_- = 0.

Boundary: this is a genuine coordinate intertwiner for the exact duad-phase
carrier.  It is not yet a numeric coordinate map from the computed 160-flag
E2 eigenspace to this carrier.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path

import numpy as np


def duads(n: int = 6) -> list[tuple[int, int]]:
    return list(itertools.combinations(range(1, n + 1), 2))


def main() -> int:
    D = duads(6)
    n = len(D)
    I15 = np.eye(n, dtype=int)
    I30 = np.eye(2 * n, dtype=int)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=int)
    B = 37 * I30 + 40 * np.kron(I15, sigma_z)

    S_plus = np.zeros((2 * n, n), dtype=int)
    S_minus = np.zeros((2 * n, n), dtype=int)
    for i in range(n):
        S_plus[2 * i, i] = 1
        S_minus[2 * i + 1, i] = 1

    P_plus = S_plus @ S_plus.T
    P_minus = S_minus @ S_minus.T
    split = P_plus - P_minus

    checks = {
        "duad_count_15": n == 15,
        "selector_shapes": S_plus.shape == (30, 15) and S_minus.shape == (30, 15),
        "selectors_are_isometries": np.array_equal(S_plus.T @ S_plus, I15) and np.array_equal(S_minus.T @ S_minus, I15),
        "selectors_are_orthogonal": np.array_equal(S_plus.T @ S_minus, np.zeros((n, n), dtype=int)),
        "projectors_sum_identity": np.array_equal(P_plus + P_minus, I30),
        "split_involution": np.array_equal(split @ split, I30),
        "plus_eigen_block_77": np.array_equal(S_plus.T @ B @ S_plus, 77 * I15),
        "minus_eigen_block_minus3": np.array_equal(S_minus.T @ B @ S_minus, -3 * I15),
        "cross_blocks_zero": np.array_equal(S_plus.T @ B @ S_minus, np.zeros((n, n), dtype=int)) and np.array_equal(S_minus.T @ B @ S_plus, np.zeros((n, n), dtype=int)),
        "operator_reconstructed_from_selectors": np.array_equal(B, 77 * P_plus - 3 * P_minus),
        "minimal_polynomial": np.array_equal(B @ B - 74 * B - 231 * I30, np.zeros((30, 30), dtype=int)),
        "flag_numeric_basis_not_claimed": True,
    }

    result = {
        "bt": 638,
        "title": "E2 duad-phase coordinate intertwiner",
        "duad_labels": D,
        "maps": {
            "S_plus": "Q^15 -> Q^30, d -> (d,+)",
            "S_minus": "Q^15 -> Q^30, d -> (d,-)",
        },
        "identities": {
            "S_plus_T_B_S_plus": "77 I_15",
            "S_minus_T_B_S_minus": "-3 I_15",
            "cross_blocks": "0",
            "B_reconstruction": "B_E2 = 77 P_plus - 3 P_minus = 37I + 40 sigma_z",
            "minimal_polynomial": "x^2 - 74x - 231",
        },
        "interpretation": "The E2 split has an explicit duad-coordinate selector inside the 30-dimensional carrier. The missing future step is only the external numerical basis map from the 160-flag E2 block into this carrier.",
        "checks": checks,
        "all_identities_hold": all(checks.values()),
    }
    out = Path("data/PART_BT638_E2_DUAD_PHASE_COORDINATE_INTERTWINER_results.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
