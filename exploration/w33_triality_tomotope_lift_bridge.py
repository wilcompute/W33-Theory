"""Lift the CKM triality carrier into the tomotope 3 ⊕ 9 split.

This is the next exact step after the tetra-axis frame and triality-middle-
anchor bridges.

Inputs already established:

1. the live CKM/tetra packet maps to a 3-state triality vector;
2. the tomotope faithful packet splits exactly as 12 = 3 ⊕ 9;
3. the old qutrit family carrier is exactly the tomotope triality 3-sector.

This bridge checks the strongest remaining structural question:

    when the live CKM branch pair and the paper up/down packet are written in the
    U/M/O family basis and lifted into the tomotope 12-packet, does any family
    or CP data leak into the colored nonet?

The exact answer is no. The family packet lifts entirely into the triality 3,
and the 9 stays inert.
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

from exploration.w33_tetra_axis_frame_bridge import (
    _axis_coordinates,
    _two_edge_vector,
)
from exploration.w33_tetrahedral_ckm_oscillator_bridge import _paper_up_down_vectors
from exploration.w33_tomotope_mode_chart_action_bridge import user_tomotope_generators


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_triality_tomotope_lift_bridge_summary.json"
SINGLET_INDICES = [0, 4, 8]
NONET_INDICES = [index for index in range(12) if index not in SINGLET_INDICES]


def _serialize_complex_vector(vector: np.ndarray) -> list[dict[str, float]]:
    return [{"real": float(value.real), "imag": float(value.imag)} for value in vector]


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _family_basis() -> dict[str, np.ndarray]:
    return {
        "fixed_line": np.array([1.0, 1.0, 1.0], dtype=complex),
        "middle_anchor": np.array([1.0, -2.0, 1.0], dtype=complex),
        "outer_shell": np.array([1.0, 0.0, -1.0], dtype=complex),
    }


def _family_coefficients(vector: np.ndarray) -> dict[str, complex]:
    basis = _family_basis()
    coefficient_matrix = np.column_stack([basis[name] for name in ("fixed_line", "middle_anchor", "outer_shell")])
    coefficients, *_ = np.linalg.lstsq(coefficient_matrix, vector, rcond=None)
    return {
        name: value
        for name, value in zip(("fixed_line", "middle_anchor", "outer_shell"), coefficients)
    }


def _chart_average() -> np.ndarray:
    return np.array([1.0, 1.0, 1.0, 1.0], dtype=complex) / 2.0


def _block_fourier_matrix() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0, 1.0],
        ],
        dtype=complex,
    ).T / 2.0


def _tomotope_change_of_basis() -> np.ndarray:
    return np.kron(np.eye(3, dtype=complex), _block_fourier_matrix())


def _embed_triality_vector(vector: np.ndarray) -> np.ndarray:
    return np.kron(vector, _chart_average())


def _three_plus_nine_coordinates(vector12: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    transformed = np.conjugate(_tomotope_change_of_basis()).T @ vector12
    return transformed[SINGLET_INDICES], transformed[NONET_INDICES]


def _permutation_matrix(permutation: tuple[int, ...]) -> np.ndarray:
    size = len(permutation)
    matrix = np.zeros((size, size), dtype=complex)
    for column, row in enumerate(permutation):
        matrix[row, column] = 1.0
    return matrix


def _generator_nonet_leakage(vector12: np.ndarray) -> dict[str, float]:
    reports: dict[str, float] = {}
    for name, permutation in user_tomotope_generators().items():
        image = _permutation_matrix(permutation) @ vector12
        _, nonet = _three_plus_nine_coordinates(image)
        reports[name] = float(np.linalg.norm(nonet))
    return reports


def _packet_report(vector3: np.ndarray) -> dict[str, Any]:
    coefficients = _family_coefficients(vector3)
    embedded = _embed_triality_vector(vector3)
    singlet, nonet = _three_plus_nine_coordinates(embedded)
    leakage = _generator_nonet_leakage(embedded)
    return {
        "triality_vector_real_imag": _serialize_complex_vector(vector3),
        "umo_coefficients": {
            name: {"real": float(value.real), "imag": float(value.imag)}
            for name, value in coefficients.items()
        },
        "tomotope_three_sector_coordinates_real_imag": _serialize_complex_vector(singlet),
        "tomotope_nine_sector_norm": float(np.linalg.norm(nonet)),
        "generator_nonet_leakage_norms": leakage,
        "max_generator_nonet_leakage_norm": float(max(leakage.values())),
    }


def build_summary() -> dict[str, Any]:
    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    a = float(quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]["amplitude"])
    b = float(lift["second_layer_lift_edge"]["amplitude"])

    live_axis = _axis_coordinates(_two_edge_vector(a, b))
    live_conjugate = np.conjugate(live_axis)
    paper_up, paper_down = _paper_up_down_vectors()
    paper_up_axis = _axis_coordinates(paper_up)
    paper_down_axis = _axis_coordinates(paper_down)
    paper_avg_axis = 0.5 * (paper_up_axis + paper_down_axis)
    paper_diff_axis = 0.5 * (paper_up_axis - paper_down_axis)

    reports = {
        "live_positive_branch": _packet_report(live_axis),
        "live_conjugate_branch": _packet_report(live_conjugate),
        "paper_up": _packet_report(paper_up_axis),
        "paper_down": _packet_report(paper_down_axis),
        "paper_average": _packet_report(paper_avg_axis),
        "paper_half_difference": _packet_report(paper_diff_axis),
    }

    max_nonet = max(report["tomotope_nine_sector_norm"] for report in reports.values())
    max_generator_leak = max(report["max_generator_nonet_leakage_norm"] for report in reports.values())

    return {
        "triality_family_basis": {
            name: _serialize_complex_vector(vector)
            for name, vector in _family_basis().items()
        },
        "live_packet_parameters": {
            "a_z2": a,
            "b_z1": b,
            "half_sum_sigma": (a + b) / 2.0,
            "half_difference_delta": (a - b) / 2.0,
        },
        "packets": reports,
        "triality_tomotope_lift_theorem": {
            "the_live_ckm_branch_pair_lifts_entirely_into_the_tomotope_triality_three": (
                reports["live_positive_branch"]["tomotope_nine_sector_norm"] < 1e-12
                and reports["live_conjugate_branch"]["tomotope_nine_sector_norm"] < 1e-12
            ),
            "the_paper_up_and_down_packets_lift_entirely_into_the_same_triality_three": (
                reports["paper_up"]["tomotope_nine_sector_norm"] < 1e-12
                and reports["paper_down"]["tomotope_nine_sector_norm"] < 1e-12
            ),
            "tomotope_generators_preserve_these_lifted_family_packets_without_nine_sector_leakage": (
                max_generator_leak < 1e-12
            ),
            "the_colored_nine_sector_is_inert_for_the_current_family_and_cp_packets": (
                max_nonet < 1e-12 and max_generator_leak < 1e-12
            ),
            "the_paper_asymmetry_relaxes_the_live_equal_opposite_lock_but_stays_inside_the_same_u_m_o_triality_carrier": (
                abs(
                    reports["live_positive_branch"]["umo_coefficients"]["fixed_line"]["real"]
                    + reports["live_positive_branch"]["umo_coefficients"]["middle_anchor"]["real"]
                ) < 1e-12
                and reports["paper_up"]["tomotope_nine_sector_norm"] < 1e-12
                and reports["paper_down"]["tomotope_nine_sector_norm"] < 1e-12
            ),
        },
        "interpretation": (
            "The CKM family packet and its CP-conjugate branch pair do not need the "
            "tomotope nonet at all. After the tetra-axis map, they live entirely on "
            "the triality 3-sector, and the tomotope generators keep them there "
            "exactly. The paper's asymmetric up/down packet is more general than the "
            "live equal-opposite lock, but it still stays inside the same U/M/O "
            "triality carrier with zero nonet leakage."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["triality_tomotope_lift_theorem"], indent=2))


if __name__ == "__main__":
    main()
