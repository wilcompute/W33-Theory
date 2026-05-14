#!/usr/bin/env python3
"""Part DCLXX: holonomy Markov tomography bridge.

After DCLXIX, every power of the averaged witness kernel K is known exactly. The
next question is whether the full projector/tripotent package requires the whole
time evolution, or whether a finite amount of witness-averaged dynamics already
determines it.

This verifier proves the strongest finite statement so far: the first two
non-stationary time slices already determine the entire projector split. If

    X1 = K - P0,
    X2 = K^2 - P0,

then the two-mode coefficients [[1/4, 2/5], [1/16, 4/25]] have determinant 3/200,
so the system is exactly invertible and yields

    P_+ = (32/3) X1 - (80/3) X2,
    P_- = -(25/6) X1 + (50/3) X2.

Hence the canonical tripotent M = P_+ - P_- is already self-tomographed by the
first two steps of the averaged witness dynamics.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
EXPLORATION = ROOT / "exploration"
for path in (SCRIPTS, EXPLORATION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from PART_CCCLIII_EIGENSPACE_PROJECTORS_BRIDGE import (  # noqa: E402
    er_adj,
    er_diag,
    er_non_adj,
    es_adj,
    es_diag,
    es_non_adj,
)
from w33_homology import build_w33  # noqa: E402

OUT_PATH = ROOT / "data" / "dclxx_holonomy_markov_tomography_bridge.json"


@dataclass(frozen=True)
class TomographySummary:
    point_count: int
    determinant_num: int
    determinant_den: int
    recovered_positive_rank: int
    recovered_negative_rank: int
    all_identities_hold: bool


def _adjacency_matrix(adj_lists: list[list[int]]) -> np.ndarray:
    n = len(adj_lists)
    matrix = np.zeros((n, n), dtype=float)
    for i, neighbors in enumerate(adj_lists):
        for j in neighbors:
            matrix[i, j] = 1.0
    return matrix


def _three_values(matrix: np.ndarray, adjacency: np.ndarray) -> dict[str, str]:
    n = matrix.shape[0]
    diag = Fraction(float(matrix[0, 0])).limit_denominator()
    edge = next(Fraction(float(matrix[i, j])).limit_denominator() for i in range(n) for j in range(n) if i != j and adjacency[i, j] == 1.0)
    nonedge = next(Fraction(float(matrix[i, j])).limit_denominator() for i in range(n) for j in range(n) if i != j and adjacency[i, j] == 0.0)
    return {"diagonal": str(diag), "edge": str(edge), "nonedge": str(nonedge)}


def build_bridge() -> dict[str, Any]:
    n, _, adj_lists, _ = build_w33()
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)

    K = (12.0 * I - A + J) / 40.0
    K2 = K @ K
    P0 = J / 40.0
    P_plus = -((A - 12.0 * I) @ (A + 4.0 * I)) / 60.0
    P_minus = ((A - 12.0 * I) @ (A - 2.0 * I)) / 96.0
    M_expected = (A + I - 13.0 * J / 40.0) / 3.0

    x1 = K - P0
    x2 = K2 - P0

    a11 = Fraction(1, 4)
    a12 = Fraction(2, 5)
    a21 = Fraction(1, 16)
    a22 = Fraction(4, 25)
    det = a11 * a22 - a12 * a21

    c_plus_1 = Fraction(32, 3)
    c_plus_2 = Fraction(-80, 3)
    c_minus_1 = Fraction(-25, 6)
    c_minus_2 = Fraction(50, 3)

    P_plus_tomo = float(c_plus_1) * x1 + float(c_plus_2) * x2
    P_minus_tomo = float(c_minus_1) * x1 + float(c_minus_2) * x2
    M_tomo = P_plus_tomo - P_minus_tomo

    identities = {
        "two_slice_mode_matrix_has_nonzero_determinant_3_over_200": det == Fraction(3, 200),
        "positive_projector_is_exactly_recovered_from_K_and_K2": np.allclose(P_plus_tomo, P_plus),
        "negative_projector_is_exactly_recovered_from_K_and_K2": np.allclose(P_minus_tomo, P_minus),
        "recovered_projectors_have_cccliii_entry_values": _three_values(P_plus_tomo, A) == {"diagonal": str(er_diag()), "edge": str(er_adj()), "nonedge": str(er_non_adj())} and _three_values(P_minus_tomo, A) == {"diagonal": str(es_diag()), "edge": str(es_adj()), "nonedge": str(es_non_adj())},
        "recovered_projectors_are_idempotent_orthogonal_and_complete": (
            np.allclose(P_plus_tomo @ P_plus_tomo, P_plus_tomo)
            and np.allclose(P_minus_tomo @ P_minus_tomo, P_minus_tomo)
            and np.allclose(P_plus_tomo @ P_minus_tomo, 0)
            and np.allclose(P0 + P_plus_tomo + P_minus_tomo, I)
        ),
        "tripotent_is_exactly_recovered_from_two_markov_slices": np.allclose(M_tomo, M_expected),
        "tripotent_trace_is_9_after_tomography": abs(float(np.trace(M_tomo)) - 9.0) < 1e-8,
        "therefore_the_first_two_witness_average_steps_self_tomograph_the_full_projector_package": (
            det == Fraction(3, 200)
            and np.allclose(P_plus_tomo, P_plus)
            and np.allclose(P_minus_tomo, P_minus)
            and np.allclose(M_tomo, M_expected)
        ),
    }

    summary = TomographySummary(
        point_count=n,
        determinant_num=det.numerator,
        determinant_den=det.denominator,
        recovered_positive_rank=int(round(np.trace(P_plus_tomo))),
        recovered_negative_rank=int(round(np.trace(P_minus_tomo))),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "tomography_coefficients": {
            "P_plus_from_X1_X2": [str(c_plus_1), str(c_plus_2)],
            "P_minus_from_X1_X2": [str(c_minus_1), str(c_minus_2)],
            "determinant": str(det),
        },
        "recovered_entry_values": {
            "P_plus": _three_values(P_plus_tomo, A),
            "P_minus": _three_values(P_minus_tomo, A),
        },
        "interpretation": {
            "data_used": "K and K^2 after subtracting the stationary mode P0",
            "tomography": "first two witness-average slices determine P_+, P_-, and M exactly",
            "breakthrough": (
                "The finite witness dynamics are now self-identifying: two steps of the averaged witness evolution already reconstruct the full projector split and the canonical tripotent, with no appeal to longer-time asymptotics."
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