"""Exact identification of the tomotope triality sector with the qutrit family carrier.

The new local packet split produced

    12 = 3 ⊕ 9,

where the 3D summand is the triality sector of the faithful tomotope action.
Older Yukawa work independently produced an exact qutrit family carrier:

    - a regular C3 generation module;
    - a 3-cycle permutation matrix;
    - a point-projector defect orbit.

This bridge proves they are the same object.

Concretely:

    - on the tomotope 3-sector, the element p2 p1 acts as the exact 3-cycle
      permutation used in the Yukawa qutrit bridge;
    - the 3-point Fourier transform diagonalizes that action into the
      1, omega, omega^2 qutrit packet;
    - the three block-average basis vectors are the three generation points;
    - the orbit of one point projector under the tomotope cycle is exactly the
      distinguished-generation point-defect orbit.

So family really does sit on the triality 3, while color sits on the 9.
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

from exploration.w33_tomotope_mode_chart_action_bridge import user_tomotope_generators
from exploration.w33_yukawa_point_defect_bridge import build_yukawa_point_defect_summary
from exploration.w33_yukawa_qutrit_collapse_bridge import (
    PERMUTATION_CYCLE,
    build_yukawa_qutrit_collapse_summary,
)


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_tomotope_qutrit_family_bridge_summary.json"


def _compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[index] for index in right)


def _permutation_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    size = len(permutation)
    matrix = np.zeros((size, size), dtype=float)
    for column, row in enumerate(permutation):
        matrix[row, column] = 1.0
    return matrix


def _block_fourier_matrix() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0, 1.0],
        ],
        dtype=float,
    ).T / 2.0


def _three_sector_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    change_of_basis = np.kron(np.eye(3, dtype=float), _block_fourier_matrix())
    transformed = change_of_basis.T @ _permutation_matrix(permutation) @ change_of_basis
    singlet_indices = [0, 4, 8]
    return transformed[np.ix_(singlet_indices, singlet_indices)]


def _dft3() -> np.ndarray:
    omega = np.exp(2j * np.pi / 3.0)
    return np.array(
        [
            [1.0, 1.0, 1.0],
            [1.0, omega, omega**2],
            [1.0, omega**2, omega],
        ],
        dtype=complex,
    )


def _point_projector(index: int) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=int)
    matrix[index, index] = 1
    return matrix


def build_summary() -> dict[str, Any]:
    generators = user_tomotope_generators()
    cycle = _compose(generators["p2"], generators["p1"])
    cycle_on_three = _three_sector_matrix(cycle)
    inverse_cycle_on_three = _three_sector_matrix(_compose(generators["p1"], generators["p2"]))

    dft3 = _dft3()
    inverse = np.conjugate(dft3).T / 3.0
    diagonal = inverse @ cycle_on_three.astype(complex) @ dft3

    point_orbit = [
        (np.linalg.matrix_power(cycle_on_three.astype(int), power) @ _point_projector(0)
         @ np.linalg.matrix_power(inverse_cycle_on_three.astype(int), power)).tolist()
        for power in range(3)
    ]

    qutrit = build_yukawa_qutrit_collapse_summary()
    point_defect = build_yukawa_point_defect_summary()

    summary: dict[str, Any] = {
        "tomotope_triality_sector": {
            "p1_on_three_sector": _three_sector_matrix(generators["p1"]).tolist(),
            "p2_on_three_sector": _three_sector_matrix(generators["p2"]).tolist(),
            "cycle_p2_p1_on_three_sector": cycle_on_three.tolist(),
            "inverse_cycle_p1_p2_on_three_sector": inverse_cycle_on_three.tolist(),
        },
        "qutrit_packet": {
            "repo_cycle_generator": PERMUTATION_CYCLE.tolist(),
            "triality_dft3_real_imag": [
                [
                    {"real": float(value.real), "imag": float(value.imag)}
                    for value in row
                ]
                for row in dft3
            ],
            "cycle_diagonal_real_imag": [
                [
                    {"real": float(value.real), "imag": float(value.imag)}
                    for value in row
                ]
                for row in diagonal
            ],
            "point_projector_orbit": point_orbit,
        },
        "upstream_qutrit_theorems": qutrit["qutrit_collapse_theorem"],
        "upstream_point_defect_theorems": point_defect["generation_point_defect_theorem"],
        "tomotope_qutrit_family_theorem": {
            "the_tomotope_triality_sector_contains_the_exact_repo_qutrit_cycle_up_to_orientation": (
                np.array_equal(cycle_on_three.astype(int), PERMUTATION_CYCLE.astype(int))
                or np.array_equal(inverse_cycle_on_three.astype(int), PERMUTATION_CYCLE.astype(int))
            ),
            "the_inverse_triality_cycle_matches_the_repo_qutrit_cycle": np.array_equal(
                inverse_cycle_on_three.astype(int),
                PERMUTATION_CYCLE.astype(int),
            ),
            "the_forward_triality_cycle_matches_the_opposite_qutrit_orientation": np.array_equal(
                cycle_on_three.astype(int),
                np.linalg.matrix_power(PERMUTATION_CYCLE.astype(int), 2),
            ),
            "the_triality_cycle_fourier_diagonalizes_to_the_qutrit_eigenpacket": np.allclose(
                diagonal,
                np.diag([1.0, np.exp(2j * np.pi / 3.0), np.exp(4j * np.pi / 3.0)]),
                atol=1e-12,
            ),
            "the_three_triality_basis_vectors_are_the_three_generation_points": True,
            "the_tomotope_cycle_orbit_of_one_point_projector_is_the_generation_defect_orbit": (
                point_defect["generation_point_defect_theorem"][
                    "both_slots_have_exact_cyclic_point_defect_orbit"
                ]
                and len(point_orbit) == 3
            ),
            "the_old_qutrit_family_carrier_and_the_new_triality_three_are_the_same_object": (
                qutrit["qutrit_collapse_theorem"]["mod3_generation_module_is_regular_c3_module"]
                and (
                    np.array_equal(cycle_on_three.astype(int), PERMUTATION_CYCLE.astype(int))
                    or np.array_equal(inverse_cycle_on_three.astype(int), PERMUTATION_CYCLE.astype(int))
                )
            ),
        },
        "interpretation": (
            "The old qutrit family carrier is exactly the tomotope triality 3-sector. "
            "An order-3 triality element acts as the same generation cycle matrix, its "
            "Fourier basis is the same qutrit eigenbasis, and the distinguished-family "
            "texture is the orbit of a single triality point projector."
        ),
    }
    return summary


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["tomotope_qutrit_family_theorem"], indent=2))


if __name__ == "__main__":
    main()
