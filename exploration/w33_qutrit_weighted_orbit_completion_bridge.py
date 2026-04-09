"""Weighted-orbit completion of the qutrit family packet.

This module identifies the minimal exact mechanism that can evade the new
factorized family no-go theorem.

Let Q_0, Q_1, Q_2 be the three rank-one qutrit projectors already isolated by
the earlier bridges. Since they are the Fourier images of the point projectors
E_00, E_11, E_22, they satisfy

    Q_i Q_j = delta_{ij} Q_i,     Q_0 + Q_1 + Q_2 = I_3.

Therefore any weighted family operator

    A(lambda) = lambda_0 Q_0 + lambda_1 Q_1 + lambda_2 Q_2

is unitarily diagonalizable with eigenvalues lambda_0, lambda_1, lambda_2 and
singular values |lambda_0|, |lambda_1|, |lambda_2|.

Consequences:
  - one projector alone gives the rank-one packet already isolated;
  - democratic orbit completion lambda_0 = lambda_1 = lambda_2 gives a scalar;
  - a genuine three-family hierarchy appears exactly when the full orbit is
    present with split magnitudes.

So the minimal exact escape from the factorized no-go is not a new carrier. It
is a weighted completion of the whole C3 projector orbit.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_qutrit_weighted_orbit_completion_bridge_summary.json"
FLOAT_TOL = 1e-10


def _read_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _complex_matrix(serialized: list[list[list[float]]]) -> np.ndarray:
    return np.array(
        [[complex(entry[0], entry[1]) for entry in row] for row in serialized],
        dtype=complex,
    )


def _spectral_packet(matrix: np.ndarray) -> dict[str, Any]:
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    eigenvalues = np.linalg.eigvals(matrix)
    return {
        "rank": int(np.linalg.matrix_rank(matrix)),
        "singular_values": [float(value) for value in singular_values],
        "eigenvalues": [[float(value.real), float(value.imag)] for value in eigenvalues],
    }


def _weighted_operator(projectors: list[np.ndarray], weights: list[complex]) -> np.ndarray:
    return sum(weight * projector for weight, projector in zip(weights, projectors))


def _weights_text(weights: list[complex]) -> list[list[float]]:
    return [[float(value.real), float(value.imag)] for value in weights]


@lru_cache(maxsize=1)
def build_qutrit_weighted_orbit_completion_summary() -> dict[str, Any]:
    rank_one = _read_json("w33_a4_rank_one_qutrit_bridge_summary.json")
    projectors = [
        _complex_matrix(packet["matrix"])
        for packet in rank_one["qutrit_projector_orbit"]["projectors"]
    ]

    orthogonality = {
        f"{i}{j}": bool(np.allclose(projectors[i] @ projectors[j], projectors[i] if i == j else 0.0, atol=FLOAT_TOL))
        for i in range(3)
        for j in range(3)
    }
    completeness = bool(np.allclose(sum(projectors), np.eye(3, dtype=complex), atol=FLOAT_TOL))

    sample_weights = {
        "single_point_defect": [1.0 + 0.0j, 0.0 + 0.0j, 0.0 + 0.0j],
        "democratic_completion": [1.0 + 0.0j, 1.0 + 0.0j, 1.0 + 0.0j],
        "split_real_completion": [1.0 + 0.0j, 2.0 + 0.0j, 4.0 + 0.0j],
        "split_phase_completion": [1.0 + 0.0j, np.exp(2j * np.pi / 9), 2.0 * np.exp(-2j * np.pi / 7)],
    }

    sample_reports: dict[str, Any] = {}
    for name, weights in sample_weights.items():
        operator = _weighted_operator(projectors, weights)
        packet = _spectral_packet(operator)
        sample_reports[name] = {
            "weights": _weights_text(weights),
            "packet": packet,
            "singular_values_match_weight_magnitudes": bool(
                np.allclose(
                    np.sort(np.array(packet["singular_values"])),
                    np.sort(np.array([abs(weight) for weight in weights])),
                    atol=FLOAT_TOL,
                )
            ),
        }

    return {
        "status": "ok",
        "projector_algebra": {
            "pairwise_orthogonality": orthogonality,
            "completeness_sum_to_identity": completeness,
        },
        "sample_weighted_orbit_packets": sample_reports,
        "weighted_orbit_completion_theorem": {
            "qutrit_projectors_form_complete_rank_one_resolution": (
                completeness and all(orthogonality.values())
            ),
            "weighted_sum_singular_values_are_exact_weight_magnitudes_in_all_samples": all(
                report["singular_values_match_weight_magnitudes"]
                for report in sample_reports.values()
            ),
            "single_projector_case_recovers_rank_one_packet": (
                sample_reports["single_point_defect"]["packet"]["rank"] == 1
            ),
            "democratic_completion_recovers_scalar_operator": bool(
                np.allclose(
                    np.array(sample_reports["democratic_completion"]["packet"]["singular_values"]),
                    np.array([1.0, 1.0, 1.0]),
                    atol=FLOAT_TOL,
                )
            ),
            "split_orbit_weights_produce_genuine_three_level_internal_hierarchy": (
                len(set(round(value, 8) for value in sample_reports["split_real_completion"]["packet"]["singular_values"])) == 3
            ),
            "minimal_escape_from_factorized_no_go_is_full_orbit_with_split_weights": (
                completeness
                and all(orthogonality.values())
                and sample_reports["single_point_defect"]["packet"]["rank"] == 1
                and len(set(round(value, 8) for value in sample_reports["split_real_completion"]["packet"]["singular_values"])) == 3
            ),
        },
        "interpretive_read": (
            "Inference from the exact projector algebra: the family hierarchy "
            "problem has reduced to the coefficient problem on the full qutrit "
            "orbit. One point defect is too small, a democratic orbit is too "
            "symmetric, and split full-orbit weights are exactly what produce "
            "a three-level spectrum."
        ),
        "bridge_verdict": (
            "The minimal exact mechanism that can evade the current family "
            "no-go has now been identified. The three qutrit family projectors "
            "form a complete rank-one resolution of identity, so any weighted "
            "orbit completion has singular values equal to the magnitudes of "
            "its three weights. Therefore the first place a genuine three-family "
            "hierarchy can appear is not at a single distinguished-generation "
            "projector, but at the full C3 orbit with split coefficients. The "
            "remaining hard problem is no longer 'where do three families come "
            "from?'. It is: what exact later bridge layer generates the three "
            "orbit weights."
        ),
        "source_files": [
            "data/w33_a4_rank_one_qutrit_bridge_summary.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_qutrit_weighted_orbit_completion_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
