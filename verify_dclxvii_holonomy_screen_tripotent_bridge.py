#!/usr/bin/env python3
"""Part DCLXVII: holonomy screen tripotent bridge.

After DCLXVI, the universal fixed-screen family is already known to be the
operator S = A + I inside the W(3,3) adjacency algebra. The next question is
whether this family can be collapsed even further to one canonical normalized
operator with a direct spectral interpretation.

This verifier proves that the normalized screen operator

    M = (S - 13 J / 40) / 3

is the exact three-channel interpolation with spectral values

    f(12) = 0,  f(2) = 1,  f(-4) = -1.

Hence M is a symmetric tripotent with spectrum {0^1, 1^24, (-1)^15}, and its
quadratic idempotents recover precisely the older W(3,3) eigenspace projector
formulas.
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
EXPLORATION = ROOT / "exploration"
for path in (SCRIPTS, EXPLORATION):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from w33_homology import build_w33
from w33_three_channel_operator_bridge import coefficient_matrix, interpolate_three_channel

OUT_PATH = ROOT / "data" / "dclxvii_holonomy_screen_tripotent_bridge.json"


@dataclass(frozen=True)
class TripotentSummary:
    point_count: int
    zero_rank: int
    positive_rank: int
    negative_rank: int
    all_identities_hold: bool


def _adjacency_matrix(adj_lists: list[list[int]]) -> np.ndarray:
    n = len(adj_lists)
    matrix = np.zeros((n, n), dtype=float)
    for i, neighbors in enumerate(adj_lists):
        for j in neighbors:
            matrix[i, j] = 1.0
    return matrix


def _rounded_spectrum(matrix: np.ndarray) -> dict[int, int]:
    eigenvalues = np.linalg.eigvalsh(matrix)
    counts: Counter[int] = Counter()
    for value in eigenvalues:
        rounded = int(round(float(value)))
        if abs(float(value) - rounded) > 1e-8:
            raise ValueError(f"non-integral eigenvalue encountered: {value}")
        counts[rounded] += 1
    return dict(sorted(counts.items()))


def _fraction_coefficients() -> tuple[Fraction, Fraction, Fraction]:
    return interpolate_three_channel(Fraction(0, 1), Fraction(1, 1), Fraction(-1, 1))


def build_bridge() -> dict[str, Any]:
    n, _, adj_lists, _ = build_w33()
    A = _adjacency_matrix(adj_lists)
    I = np.eye(n, dtype=float)
    J = np.ones((n, n), dtype=float)
    S = A + I

    coeffs = _fraction_coefficients()
    coeff_strings = {"I": str(coeffs[0]), "A": str(coeffs[1]), "J": str(coeffs[2])}
    M_from_interpolation = coefficient_matrix(coeffs, adjacency=A)
    M = (S - 13.0 * J / 40.0) / 3.0

    P0 = I - M @ M
    P_plus = (M @ M + M) / 2.0
    P_minus = (M @ M - M) / 2.0

    E0_from_A = J / 40.0
    E24_from_A = -((A - 12.0 * I) @ (A + 4.0 * I)) / 60.0
    E15_from_A = ((A - 12.0 * I) @ (A - 2.0 * I)) / 96.0

    spectrum = _rounded_spectrum(M)

    identities = {
        "tripotent_is_the_exact_three_channel_interpolant_for_0_1_minus1": np.allclose(
            M, M_from_interpolation
        ),
        "tripotent_coefficients_are_1_3_1_3_minus13_120": coeffs
        == (Fraction(1, 3), Fraction(1, 3), Fraction(-13, 120)),
        "tripotent_is_screen_operator_minus_trivial_mode": np.allclose(
            M, (S - 13.0 * J / 40.0) / 3.0
        ),
        "tripotent_is_symmetric": np.allclose(M, M.T),
        "tripotent_square_is_identity_minus_E0": np.allclose(M @ M, I - J / 40.0),
        "tripotent_cube_equals_itself": np.allclose(M @ M @ M, M),
        "tripotent_spectrum_is_0_1_24_minus1_15": spectrum == {-1: 15, 0: 1, 1: 24},
        "positive_projector_matches_cccliii_r_eigenspace_formula": np.allclose(
            P_plus, E24_from_A
        ),
        "negative_projector_matches_cccliii_s_eigenspace_formula": np.allclose(
            P_minus, E15_from_A
        ),
        "zero_projector_matches_trivial_mode": np.allclose(P0, E0_from_A),
        "projectors_are_idempotent_orthogonal_and_complete": (
            np.allclose(P_plus @ P_plus, P_plus)
            and np.allclose(P_minus @ P_minus, P_minus)
            and np.allclose(P0 @ P0, P0)
            and np.allclose(P_plus @ P_minus, 0)
            and np.allclose(P_plus @ P0, 0)
            and np.allclose(P_minus @ P0, 0)
            and np.allclose(P_plus + P_minus + P0, I)
        ),
        "tripotent_trace_recovers_24_minus_15_split": abs(float(np.trace(M)) - 9.0) < 1e-8,
        "therefore_the_universal_screen_bundle_collapses_to_one_canonical_tripotent_polarization": (
            np.allclose(M, M_from_interpolation)
            and np.allclose(M @ M @ M, M)
            and spectrum == {-1: 15, 0: 1, 1: 24}
            and np.allclose(P_plus, E24_from_A)
            and np.allclose(P_minus, E15_from_A)
        ),
    }

    summary = TripotentSummary(
        point_count=n,
        zero_rank=int(round(np.trace(P0))),
        positive_rank=int(round(np.trace(P_plus))),
        negative_rank=int(round(np.trace(P_minus))),
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "operator_coefficients": coeff_strings,
        "operator_statistics": {
            "tripotent_spectrum": spectrum,
            "tripotent_trace": float(np.trace(M)),
            "tripotent_square_trace": float(np.trace(M @ M)),
        },
        "projector_ranks": {
            "rank_P0": int(round(np.trace(P0))),
            "rank_P_plus": int(round(np.trace(P_plus))),
            "rank_P_minus": int(round(np.trace(P_minus))),
        },
        "interpretation": {
            "tripotent": "M = (A + I - 13J/40)/3",
            "screen_family": "normalized universal holonomy-screen operator",
            "spectral_split": "0^1 ⊕ (+1)^24 ⊕ (-1)^15",
            "breakthrough": (
                "The entire universal holonomy-screen family collapses to one canonical rational tripotent. Its quadratic idempotents are exactly the older W(3,3) eigenspace projectors, so the screen bundle, the adjacency algebra, and the projector calculus are one and the same structure."
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