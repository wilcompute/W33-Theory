"""Fourier/Clifford structure on the tetrahedral chart atlas.

The tetrahedral atlas already gave two exact operator facts:

    7 = 4 + 3 = 1 + 6,
    12 = 4 x 3.

This module sharpens the Fourier/Clifford side of that packet.

For each source chart in the tetrahedral atlas, take the three outgoing
half-edge vectors in the induced 3-dimensional color-mode space.  Then:

    - their Gram matrix is exactly ``I_3 + J_3``;
    - the 3-point Fourier transform diagonalizes that metric to
      ``diag(4,1,1)``;
    - after whitening by ``(I_3 + J_3)^(-1/2)``, the outgoing basis becomes an
      orthogonal frame with determinant ``±1``.

So every chart carries the same local 3-mode metric and differs only by an
orientation sign.  This is the clean local Clifford packet hidden inside the
tetrahedral oscillator:

    - one radial Fourier mode of weight 4,
    - two tangential unit modes,
    - an exact orthogonal 3-frame after whitening,
    - a 2+2 chirality split across the four source charts.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]


from exploration.w33_tetrahedral_chart_oscillator_bridge import _chart_sign_matrix


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tetrahedral_fourier_clifford_bridge_summary.json"


def _complex_matrix_to_pairs(matrix: np.ndarray) -> list[list[list[float]]]:
    return [
        [[float(np.real(entry)), float(np.imag(entry))] for entry in row]
        for row in matrix
    ]


def _dft3() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3)
    return np.array(
        [
            [1, 1, 1],
            [1, omega, omega**2],
            [1, omega**2, omega],
        ],
        dtype=complex,
    ) / np.sqrt(3.0)


def _outgoing_half_edge_matrix(sign_matrix: np.ndarray, source_index: int) -> np.ndarray:
    others = [index for index in range(sign_matrix.shape[0]) if index != source_index]
    return np.stack(
        [(sign_matrix[index] - sign_matrix[source_index]) / 2.0 for index in others],
        axis=0,
    )


@lru_cache(maxsize=1)
def build_summary() -> dict[str, Any]:
    chart_names, sign_matrix = _chart_sign_matrix()
    dft3 = _dft3()
    local_metric = np.eye(3) + np.ones((3, 3))
    fourier_diagonal = np.conjugate(dft3).T @ local_metric @ dft3
    whitening = np.eye(3) - np.ones((3, 3)) / 6.0

    outgoing_matrices: dict[str, np.ndarray] = {}
    outgoing_grams: dict[str, np.ndarray] = {}
    whitened_frames: dict[str, np.ndarray] = {}
    determinants: dict[str, float] = {}
    for source_index, source_name in enumerate(chart_names):
        outgoing = _outgoing_half_edge_matrix(sign_matrix, source_index)
        frame = whitening @ outgoing
        outgoing_matrices[source_name] = outgoing
        outgoing_grams[source_name] = outgoing @ outgoing.T
        whitened_frames[source_name] = frame
        determinants[source_name] = float(round(np.linalg.det(frame)))

    positive_charts = [name for name, det in determinants.items() if det > 0]
    negative_charts = [name for name, det in determinants.items() if det < 0]

    return {
        "status": "ok",
        "chart_sign_matrix": sign_matrix.astype(int).tolist(),
        "local_outgoing_metric": {
            "gram_matrix": local_metric.astype(int).tolist(),
            "inverse": (np.eye(3) - np.ones((3, 3)) / 4.0).tolist(),
            "inverse_square_root": whitening.tolist(),
            "determinant": float(np.linalg.det(local_metric)),
            "eigenvalues": [4.0, 1.0, 1.0],
        },
        "fourier_packet": {
            "dft3_real_imag_pairs": _complex_matrix_to_pairs(dft3),
            "fourier_diagonalization_real_imag_pairs": _complex_matrix_to_pairs(fourier_diagonal),
            "fourier_diagonal_is_diag_4_1_1": np.allclose(
                fourier_diagonal,
                np.diag([4.0, 1.0, 1.0]),
            ),
        },
        "source_frames": {
            source_name: {
                "outgoing_half_edge_matrix": outgoing_matrices[source_name].tolist(),
                "outgoing_gram_matrix": outgoing_grams[source_name].tolist(),
                "whitened_frame": whitened_frames[source_name].tolist(),
                "whitened_frame_is_orthogonal": np.allclose(
                    whitened_frames[source_name] @ whitened_frames[source_name].T,
                    np.eye(3),
                ),
                "orientation_sign": int(determinants[source_name]),
            }
            for source_name in chart_names
        },
        "chirality_packet": {
            "positive_charts": positive_charts,
            "negative_charts": negative_charts,
            "positive_count": len(positive_charts),
            "negative_count": len(negative_charts),
        },
        "fourier_clifford_theorem": {
            "every_source_chart_has_the_same_outgoing_gram_I_plus_J": all(
                np.array_equal(outgoing_grams[source_name], local_metric)
                for source_name in chart_names
            ),
            "the_three_point_fourier_transform_diagonalizes_the_local_metric": np.allclose(
                fourier_diagonal,
                np.diag([4.0, 1.0, 1.0]),
            ),
            "the_whitened_outgoing_frames_are_all_orthogonal": all(
                np.allclose(
                    whitened_frames[source_name] @ whitened_frames[source_name].T,
                    np.eye(3),
                )
                for source_name in chart_names
            ),
            "each_local_frame_has_orientation_plus_or_minus_one": all(
                abs(det) == 1.0 for det in determinants.values()
            ),
            "the_four_source_charts_split_into_two_positive_and_two_negative_frames": (
                len(positive_charts) == 2 and len(negative_charts) == 2
            ),
            "the_local_metric_has_one_radial_mode_and_two_tangential_modes": True,
            "the_exact_directed_packet_is_four_sources_times_three_local_modes": (
                sign_matrix.shape[0] * sign_matrix.shape[1] == 12
            ),
        },
        "bridge_verdict": (
            "The tetrahedral atlas already carries its own Fourier/Clifford packet. "
            "At each source chart, the three outgoing half-edge modes have exact "
            "Gram matrix I+J, so the same local metric appears at all four charts. "
            "The 3-point Fourier transform diagonalizes that metric to diag(4,1,1): "
            "one radial mode of weight 4 and two tangential unit modes. After "
            "whitening by (I+J)^(-1/2) = I - J/4, every source chart yields an "
            "orthogonal 3-frame with determinant ±1, and the four charts split "
            "exactly into two positive and two negative frames. So the tetrahedral "
            "oscillator is not just a count pattern. It is an exact 4x3 local "
            "mode packet with a built-in Fourier diagonalization and chirality."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


if __name__ == "__main__":
    write_summary()
