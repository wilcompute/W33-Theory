"""Exact tetra-axis frame law behind the CKM tetrahedral oscillator.

The universal tetra/qutrit bridge identified:

    4 chart/CKM slots  <->  tetrahedron vertices,
    3 transport states <->  tetrahedron opposite-edge axes.

This module upgrades that dictionary to one concrete intertwiner.  Let

    S = [[ 1, 1, 1],
         [ 1,-1,-1],
         [-1, 1,-1],
         [-1,-1, 1]]

be the tetra-axis sign matrix.  Then:

1. ``U = S/2`` is an exact isometry from the real 3-axis packet to the
   centered shell of the 4-vertex tetrahedron:

       U^T U = I_3,
       U U^T = I_4 - J_4/4.

2. Equivalently,

       S S^T = 4I_4 - J_4,

   so the tetra Laplacian is exactly the axis-frame Grammian.

3. The live two-edge CKM ansatz

       v(a,b) = (1, i a, 1, -i b)

   has exact axis coordinates

       U^* v(a,b)
         = ( i(a+b)/2,  1 - i(a-b)/2,  -i(a+b)/2 ).

So the CKM two-edge packet is not using the full tetra shell arbitrarily.
It is an exact "axis-lift" packet:

    - the half-sum ``(a+b)/2`` is the antisymmetric axis amplitude,
    - the half-difference ``(a-b)/2`` is the central phase drift.

This is the sharpest current bridge between the tetrahedral CKM packet and the
transport/qutrit carrier.
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

from exploration.w33_tetrahedral_ckm_oscillator_bridge import (
    _paper_up_down_vectors,
)
from exploration.w33_universal_tetra_qutrit_bridge import (
    _canonical_tetra_axis_sign_matrix,
)


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_tetra_axis_frame_bridge_summary.json"


def _serialize_complex_vector(vector: np.ndarray) -> list[dict[str, float]]:
    return [{"real": float(value.real), "imag": float(value.imag)} for value in vector]


def _serialize_real_matrix(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix]


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _axis_frame() -> np.ndarray:
    return _canonical_tetra_axis_sign_matrix().astype(complex)


def _axis_isometry() -> np.ndarray:
    return _axis_frame() / 2.0


def _centered_projector() -> np.ndarray:
    return np.eye(4, dtype=complex) - np.ones((4, 4), dtype=complex) / 4.0


def _two_edge_vector(a: float, b: float) -> np.ndarray:
    return np.array([1.0, 1j * a, 1.0, -1j * b], dtype=complex)


def _two_edge_axis_formula(a: float, b: float) -> np.ndarray:
    return np.array(
        [
            0.5j * (a + b),
            1.0 - 0.5j * (a - b),
            -0.5j * (a + b),
        ],
        dtype=complex,
    )


def _axis_coordinates(vector: np.ndarray) -> np.ndarray:
    return np.conjugate(_axis_isometry()).T @ vector


def build_summary() -> dict[str, Any]:
    axis_frame = _axis_frame()
    axis_isometry = _axis_isometry()
    projector = _centered_projector()
    frame_gram = np.conjugate(axis_isometry).T @ axis_isometry
    frame_projector = axis_isometry @ np.conjugate(axis_isometry).T
    laplacian = axis_frame @ np.conjugate(axis_frame).T

    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    a = float(quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]["amplitude"])
    b = float(lift["second_layer_lift_edge"]["amplitude"])
    live_vector = _two_edge_vector(a, b)
    live_axis_coordinates = _axis_coordinates(live_vector)
    live_axis_formula = _two_edge_axis_formula(a, b)

    paper_up, paper_down = _paper_up_down_vectors()
    paper_up_axis = _axis_coordinates(paper_up)
    paper_down_axis = _axis_coordinates(paper_down)

    return {
        "tetra_axis_frame": {
            "sign_matrix": _serialize_real_matrix(axis_frame.real),
            "normalized_isometry_real_imag": [
                _serialize_complex_vector(row) for row in axis_isometry
            ],
            "frame_gram_real_imag": [
                _serialize_complex_vector(row) for row in frame_gram
            ],
            "frame_projector_real_imag": [
                _serialize_complex_vector(row) for row in frame_projector
            ],
            "centered_projector_real_imag": [
                _serialize_complex_vector(row) for row in projector
            ],
            "tetra_laplacian_real": _serialize_real_matrix(laplacian.real),
            "tetra_laplacian_eigenvalues": [
                float(value) for value in np.linalg.eigvalsh(laplacian.real)
            ],
        },
        "live_two_edge_axis_packet": {
            "amplitudes": {"a_z2": a, "b_z1": b},
            "vertex_packet_real_imag": _serialize_complex_vector(live_vector),
            "axis_coordinates_real_imag": _serialize_complex_vector(live_axis_coordinates),
            "exact_formula_real_imag": _serialize_complex_vector(live_axis_formula),
            "half_sum_antisymmetric_axis_amplitude": float((a + b) / 2.0),
            "half_difference_central_phase_drift": float((a - b) / 2.0),
        },
        "paper_axis_coordinates": {
            "up_real_imag": _serialize_complex_vector(paper_up_axis),
            "down_real_imag": _serialize_complex_vector(paper_down_axis),
        },
        "tetra_axis_frame_theorem": {
            "the_axis_frame_is_an_exact_isometry_onto_the_centered_tetra_shell": bool(
                np.allclose(frame_gram, np.eye(3), atol=1e-12)
                and np.allclose(frame_projector, projector, atol=1e-12)
            ),
            "the_tetra_laplacian_is_exactly_the_axis_frame_grammian": bool(
                np.allclose(laplacian, 4.0 * projector, atol=1e-12)
            ),
            "the_live_two_edge_ckm_packet_is_an_exact_axis_lift": bool(
                np.allclose(live_axis_coordinates, live_axis_formula, atol=1e-12)
            ),
            "the_half_sum_controls_the_antisymmetric_axis_pair": bool(
                np.allclose(
                    live_axis_coordinates[[0, 2]],
                    np.array([0.5j * (a + b), -0.5j * (a + b)], dtype=complex),
                    atol=1e-12,
                )
            ),
            "the_half_difference_controls_the_central_axis_phase_drift": bool(
                np.allclose(
                    live_axis_coordinates[1],
                    np.array(1.0 - 0.5j * (a - b), dtype=complex),
                    atol=1e-12,
                )
            ),
        },
        "interpretation": (
            "The tetrahedron-to-qutrit bridge is now one exact frame law. The "
            "3-state transport/qutrit packet is the orthonormal axis space, the "
            "centered 4-slot CKM/chart shell is its tetrahedral image under the "
            "axis sign frame, and the live two-edge CKM ansatz occupies the rigid "
            "axis-lift subfamily where the antisymmetric qutrit pair is controlled "
            "by (a+b)/2 and the central phase drift by (a-b)/2."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["tetra_axis_frame_theorem"], indent=2))


if __name__ == "__main__":
    main()
