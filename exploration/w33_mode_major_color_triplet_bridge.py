"""Mode-major singlet-plus-triplet gauge decomposition of the chart atlas.

The single-chart basis obscured the color structure.  In the tetrahedral chart
atlas, the right basis is the orthonormal chart-Fourier packet

    u0 = (1, 1, 1, 1)/2,
    u1 = (1, 1,-1,-1)/2,
    u2 = (1,-1, 1,-1)/2,
    u3 = (1,-1,-1, 1)/2.

Applying this basis to the four chart Yukawa slices gives four mode-major
operators:

    M0 = singlet mode,
    M1, M2, M3 = tangential packet.

The new result is exact:

    - all tested weak generators act trivially on the 4-mode multiplicity;
    - all tested color generators preserve the split 1 ⊕ 3;
    - the 3 tangential modes carry an exact SU(3) fundamental packet
      (for the tested Gell-Mann subset λ1, λ2, λ3, λ8) after a fixed
      permutation of basis vectors.

So the old "parabolic color obstruction" was a coordinate artifact of the
single-chart basis.  Full color appears exactly on the atlas after moving to
the mode-major basis.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "exploration") not in sys.path:
    sys.path.insert(0, str(ROOT / "exploration"))

from exploration.w33_clean_weak_intertwiner_bridge import (
    _left_color_generators,
    _left_pauli_generators,
)
from exploration.w33_toroidal_tetrahedral_color_atlas_bridge import _chart_yukawas


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_mode_major_color_triplet_bridge_summary.json"
CHART_ORDER = ("chart_1", "chart_2", "chart_3", "chart_4")
MODE_ORDER = ("singlet", "tangent_1", "tangent_2", "tangent_3")


def _chart_fourier_basis() -> dict[str, np.ndarray]:
    return {
        "singlet": np.array([1.0, 1.0, 1.0, 1.0]) / 2.0,
        "tangent_1": np.array([1.0, 1.0, -1.0, -1.0]) / 2.0,
        "tangent_2": np.array([1.0, -1.0, 1.0, -1.0]) / 2.0,
        "tangent_3": np.array([1.0, -1.0, -1.0, 1.0]) / 2.0,
    }


def _chart_packet() -> np.ndarray:
    chart_yukawas = _chart_yukawas()
    return np.stack([chart_yukawas[name].reshape(-1) for name in CHART_ORDER], axis=1)


def _mode_packet() -> dict[str, np.ndarray]:
    chart_packet = _chart_packet()
    return {
        name: (chart_packet @ vector).reshape(8, 8).astype(complex)
        for name, vector in _chart_fourier_basis().items()
    }


def _solve_packet_action(
    left_operator: np.ndarray,
    packet: list[np.ndarray],
) -> tuple[np.ndarray, np.ndarray, float]:
    packet_size = len(packet)
    rows = []
    rhs = []

    for packet_index, yukawa in enumerate(packet):
        image = left_operator @ yukawa
        for left_index in range(8):
            for right_index in range(8):
                row = np.zeros(packet_size * packet_size + 64, dtype=complex)
                for mode_index, basis_yukawa in enumerate(packet):
                    row[packet_size * mode_index + packet_index] = basis_yukawa[left_index, right_index]
                for inner in range(8):
                    row[packet_size * packet_size + inner * 8 + right_index] += yukawa[left_index, inner]
                rows.append(row)
                rhs.append(image[left_index, right_index])

    matrix = np.stack(rows, axis=0)
    target = np.asarray(rhs, dtype=complex)
    solution, *_ = np.linalg.lstsq(matrix, target, rcond=None)
    action = solution[: packet_size * packet_size].reshape(packet_size, packet_size)
    right_operator = solution[packet_size * packet_size :].reshape(8, 8)

    max_residual = 0.0
    for packet_index, yukawa in enumerate(packet):
        reconstructed = sum(
            action[mode_index, packet_index] * packet[mode_index]
            for mode_index in range(packet_size)
        ) + yukawa @ right_operator
        max_residual = max(
            max_residual,
            float(np.linalg.norm(left_operator @ yukawa - reconstructed)),
        )

    return action, right_operator, max_residual


def _standard_gell_mann_subset() -> dict[str, np.ndarray]:
    return {
        "lambda_1": np.array([[0, 1, 0], [1, 0, 0], [0, 0, 0]], dtype=complex),
        "lambda_2": np.array([[0, -1j, 0], [1j, 0, 0], [0, 0, 0]], dtype=complex),
        "lambda_3": np.array([[1, 0, 0], [0, -1, 0], [0, 0, 0]], dtype=complex),
        "lambda_8": np.array(
            [[1 / np.sqrt(3), 0, 0], [0, 1 / np.sqrt(3), 0], [0, 0, -2 / np.sqrt(3)]],
            dtype=complex,
        ),
    }


def build_summary() -> dict[str, Any]:
    modes = _mode_packet()
    packet = [modes[name] for name in MODE_ORDER]
    tangential_packet = [modes[name] for name in MODE_ORDER[1:]]

    weak_actions: dict[str, dict[str, Any]] = {}
    for name, generator in _left_pauli_generators().items():
        action, _, residual = _solve_packet_action(generator, packet)
        weak_actions[name] = {
            "action_matrix": [[complex(value).real for value in row] for row in action],
            "residual_norm": residual,
        }

    color_actions: dict[str, dict[str, Any]] = {}
    tangential_actions: dict[str, dict[str, Any]] = {}
    permutation = np.array(
        [
            [1, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
        ],
        dtype=complex,
    )
    phase_gauge = np.diag([-1.0, 1.0, 1.0]).astype(complex)
    standard_subset = _standard_gell_mann_subset()
    for name, generator in _left_color_generators().items():
        action, _, residual = _solve_packet_action(generator, packet)
        tangential_action, _, tangential_residual = _solve_packet_action(generator, tangential_packet)
        conjugated = permutation @ tangential_action @ permutation.T
        gauge_fixed = phase_gauge @ conjugated @ phase_gauge
        color_actions[name] = {
            "action_matrix_real_imag": [
                [
                    {"real": float(value.real), "imag": float(value.imag)}
                    for value in row
                ]
                for row in action
            ],
            "residual_norm": residual,
            "singlet_column_norm": float(np.linalg.norm(action[1:, 0])),
            "singlet_row_norm": float(np.linalg.norm(action[0, 1:])),
        }
        tangential_actions[name] = {
            "action_matrix_real_imag": [
                [
                    {"real": float(value.real), "imag": float(value.imag)}
                    for value in row
                ]
                for row in tangential_action
            ],
            "conjugated_action_real_imag": [
                [
                    {"real": float(value.real), "imag": float(value.imag)}
                    for value in row
                ]
                for row in conjugated
            ],
            "gauge_fixed_action_real_imag": [
                [
                    {"real": float(value.real), "imag": float(value.imag)}
                    for value in row
                ]
                for row in gauge_fixed
            ],
            "residual_norm": tangential_residual,
            "matches_standard_gell_mann_after_permutation_and_phase_gauge": (
                name in standard_subset
                and np.allclose(gauge_fixed, standard_subset[name], atol=1e-12)
            ),
        }

    mode_norms = {name: float(np.linalg.norm(matrix) ** 2) for name, matrix in modes.items()}
    mode_ranks = {name: int(np.linalg.matrix_rank(matrix, tol=1e-10)) for name, matrix in modes.items()}

    summary: dict[str, Any] = {
        "chart_fourier_basis": {
            name: vector.tolist() for name, vector in _chart_fourier_basis().items()
        },
        "mode_packet": {
            "mode_norm_squares": mode_norms,
            "mode_ranks": mode_ranks,
        },
        "weak_mode_actions": weak_actions,
        "color_mode_actions": color_actions,
        "tangential_triplet_actions": tangential_actions,
        "mode_major_color_triplet_theorem": {
            "the_chart_packet_splits_as_one_plus_three_with_norms_56_and_8_8_8": (
                abs(mode_norms["singlet"] - 56.0) < 1e-10
                and all(abs(mode_norms[name] - 8.0) < 1e-10 for name in MODE_ORDER[1:])
            ),
            "all_tested_weak_generators_act_trivially_on_mode_multiplicity": all(
                action["residual_norm"] < 1e-12
                and np.linalg.norm(
                    np.array(action["action_matrix"], dtype=float)
                ) < 1e-12
                for action in weak_actions.values()
            ),
            "all_tested_color_generators_preserve_the_singlet_plus_triplet_split": all(
                action["residual_norm"] < 1e-12
                and action["singlet_column_norm"] < 1e-12
                and action["singlet_row_norm"] < 1e-12
                for action in color_actions.values()
            ),
            "the_tangential_three_packet_carries_the_exact_tested_su3_fundamental": all(
                tangential_actions[name]["residual_norm"] < 1e-12
                and tangential_actions[name]["matches_standard_gell_mann_after_permutation_and_phase_gauge"]
                for name in standard_subset
            ),
        },
        "interpretation": (
            "In the chart-Fourier basis, the atlas packet is exactly 1 ⊕ 3 under the "
            "tested color generators: one color-singlet common mode and one genuine "
            "color triplet of tangential modes. Weak generators act only through the "
            "common right intertwiner and do not mix the mode multiplicity. So the old "
            "single-chart parabolic obstruction disappears on the atlas after moving to "
            "the mode-major basis."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["mode_major_color_triplet_theorem"], indent=2))


if __name__ == "__main__":
    main()
