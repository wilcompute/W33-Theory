"""Tetrahedral oscillator law for the live four-slot CKM packet.

The recent local/toroidal work produced two independent tetrahedral packets:

- the four-chart atlas with its exact 4-point Fourier basis;
- the live CKM carrier packet on the four quark slots
  ``(Q_1_1, Q_2_1, Q_2_2, Q_3_2)``.

This bridge checks whether those are the same 4-mode object on the family side.
The sharp answer is yes, and it is stronger than a loose analogy:

1. The four live slot Yukawas span an exact 4-dimensional family-operator
   packet whose centered shell has rank 3.
2. The same 4-point tetrahedral Fourier/Hadamard transform used on the chart
   atlas organizes the live CKM coefficient vectors.
3. Any quarter-turn single-edge packet supported on one live sheet is
   tetra-Fourier democratic: all four mode magnitudes are equal.
4. The minimal two-edge packet

       (1, i a, 1, -i b)

   splits exactly into two conjugate carrier modes and two conjugate gap modes:

       F4^* (1, i a, 1, -i b)^T
         = (1 + i(a-b)/2,  i(a+b)/2,  1 - i(a-b)/2,  -i(a+b)/2)^T.

So the live CKM architecture is better read as a tetrahedral oscillator on the
four quark carriers than as four unrelated slot amplitudes.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_mode_major_color_triplet_bridge import _chart_fourier_basis
from exploration.w33_paper_ckm_asymmetric_bridge import (
    EXACT_PACKET,
    PAPER_TARGETS,
    PDG_2025_TARGETS,
    _build_slot_yukawas,
    _evaluate_packet,
)


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_tetrahedral_ckm_oscillator_bridge_summary.json"
SLOT_ORDER = ("Q_1_1", "Q_2_1", "Q_2_2", "Q_3_2")
MODE_ORDER = ("singlet", "tangent_1", "tangent_2", "tangent_3")


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _tetra_fourier_matrix() -> np.ndarray:
    return np.array(
        [
            [1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, -1.0, -1.0],
            [1.0, -1.0, 1.0, -1.0],
            [1.0, -1.0, -1.0, 1.0],
        ],
        dtype=complex,
    ).T / 2.0


def _serialize_complex_vector(vector: np.ndarray) -> list[dict[str, float]]:
    return [{"real": float(value.real), "imag": float(value.imag)} for value in vector]


def _serialize_complex_matrix(matrix: np.ndarray) -> list[list[dict[str, float]]]:
    return [
        [{"real": float(value.real), "imag": float(value.imag)} for value in row]
        for row in matrix
    ]


def _tetra_mode_report(vector: np.ndarray) -> dict[str, Any]:
    fourier = _tetra_fourier_matrix()
    coordinates = np.conjugate(fourier).T @ vector
    return {
        "slot_coefficients_real_imag": _serialize_complex_vector(vector),
        "mode_coordinates_real_imag": _serialize_complex_vector(coordinates),
        "mode_magnitudes": [float(abs(value)) for value in coordinates],
        "mode_norm_squares": [float(abs(value) ** 2) for value in coordinates],
        "pair_magnitude_match": {
            "singlet_vs_tangent_2": float(abs(abs(coordinates[0]) - abs(coordinates[2]))),
            "tangent_1_vs_tangent_3": float(abs(abs(coordinates[1]) - abs(coordinates[3]))),
        },
    }


def _single_edge_vector(amplitude: float, *, leading_slot: int) -> np.ndarray:
    vector = np.zeros(4, dtype=complex)
    if leading_slot == 0:
        vector[0] = 1.0
        vector[1] = 1j * amplitude
        return vector
    if leading_slot == 2:
        vector[2] = 1.0
        vector[3] = -1j * amplitude
        return vector
    raise ValueError(f"unsupported leading slot index {leading_slot}")


def _two_edge_vector(a: float, b: float) -> np.ndarray:
    return np.array([1.0, 1j * a, 1.0, -1j * b], dtype=complex)


def _two_edge_formula(a: float, b: float) -> np.ndarray:
    return np.array(
        [
            1.0 + 0.5j * (a - b),
            0.5j * (a + b),
            1.0 - 0.5j * (a - b),
            -0.5j * (a + b),
        ],
        dtype=complex,
    )


def _paper_up_down_vectors() -> tuple[np.ndarray, np.ndarray]:
    packet = {
        key: (float(value) if isinstance(value, Fraction) else float(value))
        for key, value in EXACT_PACKET.items()
    }
    phase12 = np.exp(1j * np.pi * packet["phase12_over_pi"])
    phase_u32 = np.exp(1j * np.pi * packet["phase_u32_over_pi"])
    phase_d32 = np.exp(1j * np.pi * packet["phase_d32_over_pi"])
    up = np.array(
        [
            1.0,
            packet["a12"] * phase12,
            packet["u22"],
            packet["u32"] * phase_u32,
        ],
        dtype=complex,
    )
    down = np.array(
        [
            1.0,
            -packet["a12"] * phase12,
            packet["d22"],
            packet["d32"] * phase_d32,
        ],
        dtype=complex,
    )
    return up, down


def _slot_operator_packet_report() -> dict[str, Any]:
    slot_yukawas = _build_slot_yukawas()
    packet = np.stack([slot_yukawas[name].reshape(-1) for name in SLOT_ORDER], axis=1)
    centered = packet - np.mean(packet, axis=1, keepdims=True)
    fourier_modes = packet @ _tetra_fourier_matrix()
    mode_norms = {
        name: float(np.linalg.norm(fourier_modes[:, index].reshape(3, 3)) ** 2)
        for index, name in enumerate(MODE_ORDER)
    }
    return {
        "slot_order": list(SLOT_ORDER),
        "packet_rank": int(np.linalg.matrix_rank(packet, tol=1e-12)),
        "centered_rank": int(np.linalg.matrix_rank(centered, tol=1e-12)),
        "centered_singular_values": [
            float(value)
            for value in np.linalg.svd(centered, compute_uv=False)
        ],
        "mode_norm_squares": mode_norms,
    }


def _paper_target_errors(observables: dict[str, float], targets: dict[str, float]) -> dict[str, float]:
    return {key: float(observables[key] - value) for key, value in targets.items()}


def build_summary() -> dict[str, Any]:
    chart_basis = _chart_fourier_basis()
    live_fourier = _tetra_fourier_matrix()
    chart_matrix = np.column_stack(
        [np.array(chart_basis[name], dtype=float) for name in MODE_ORDER]
    ).astype(complex)

    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    cabibbo_edge = quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]
    vcb_lift = lift["second_layer_lift_edge"]

    a = float(cabibbo_edge["amplitude"])
    b = float(vcb_lift["amplitude"])
    z2_edge = _single_edge_vector(a, leading_slot=0)
    z1_edge = _single_edge_vector(b, leading_slot=2)
    two_edge = _two_edge_vector(a, b)
    two_edge_formula = _two_edge_formula(a, b)
    slot_packet_report = _slot_operator_packet_report()
    z2_report = _tetra_mode_report(z2_edge)
    z1_report = _tetra_mode_report(z1_edge)

    paper_up, paper_down = _paper_up_down_vectors()
    paper_up_report = _tetra_mode_report(paper_up)
    paper_down_report = _tetra_mode_report(paper_down)
    slot_yukawas = _build_slot_yukawas()
    paper_record = _evaluate_packet(
        slot_yukawas,
        **{
            key: (float(value) if isinstance(value, Fraction) else float(value))
            for key, value in EXACT_PACKET.items()
        },
    )

    return {
        "tetrahedral_basis": {
            "slot_order": list(SLOT_ORDER),
            "mode_order": list(MODE_ORDER),
            "fourier_matrix_real_imag": _serialize_complex_matrix(live_fourier),
            "matches_chart_fourier_basis_exactly": np.allclose(live_fourier, chart_matrix),
        },
        "slot_operator_packet": slot_packet_report,
        "single_edge_democracy": {
            "z2_cabibbo_cp_edge": z2_report,
            "z1_vcb_lift_edge": z1_report,
        },
        "two_edge_packet": {
            "live_amplitudes": {"a_z2": a, "b_z1": b},
            "slot_coefficients_real_imag": _serialize_complex_vector(two_edge),
            "mode_coordinates_real_imag": _serialize_complex_vector(
                np.conjugate(live_fourier).T @ two_edge
            ),
            "exact_formula_real_imag": _serialize_complex_vector(two_edge_formula),
            "carrier_gap_mode_norm_squares": {
                "singlet": float(abs(two_edge_formula[0]) ** 2),
                "tangent_1_gap": float(abs(two_edge_formula[1]) ** 2),
                "tangent_2": float(abs(two_edge_formula[2]) ** 2),
                "tangent_3_gap": float(abs(two_edge_formula[3]) ** 2),
            },
            "gap_size_half_sum": float((a + b) / 2.0),
            "carrier_imag_shift_half_difference": float((a - b) / 2.0),
        },
        "paper_exact_packet": {
            "up": paper_up_report,
            "down": paper_down_report,
            "observables": paper_record["observables"],
            "paper_target_residuals": _paper_target_errors(
                paper_record["observables"],
                PAPER_TARGETS,
            ),
            "pdg_2025_target_residuals": _paper_target_errors(
                paper_record["observables"],
                PDG_2025_TARGETS,
            ),
        },
        "tetrahedral_ckm_oscillator_theorem": {
            "the_live_four_slot_family_operator_packet_has_exact_rank_four_and_centered_rank_three": (
                slot_packet_report["packet_rank"] == 4
                and slot_packet_report["centered_rank"] == 3
            ),
            "the_live_ckm_fourier_basis_is_the_same_as_the_chart_tetrahedral_fourier_basis": bool(
                np.allclose(live_fourier, chart_matrix)
            ),
            "the_z2_quarter_turn_cabibbo_edge_is_tetra_fourier_democratic": (
                max(z2_report["mode_magnitudes"])
                - min(z2_report["mode_magnitudes"])
                < 1e-12
            ),
            "the_z1_quarter_turn_vcb_lift_edge_is_tetra_fourier_democratic": (
                max(z1_report["mode_magnitudes"])
                - min(z1_report["mode_magnitudes"])
                < 1e-12
            ),
            "the_minimal_two_edge_packet_splits_exactly_into_two_conjugate_carrier_modes_and_two_conjugate_gap_modes": bool(
                np.allclose(np.conjugate(live_fourier).T @ two_edge, two_edge_formula, atol=1e-12)
            ),
            "the_paper_up_and_down_packets_live_in_the_same_pairwise_conjugate_tetra_mode_class": (
                paper_up_report["pair_magnitude_match"]["singlet_vs_tangent_2"] < 1e-12
                and paper_up_report["pair_magnitude_match"]["tangent_1_vs_tangent_3"] < 1e-12
                and paper_down_report["pair_magnitude_match"]["singlet_vs_tangent_2"] < 1e-12
                and paper_down_report["pair_magnitude_match"]["tangent_1_vs_tangent_3"] < 1e-12
            ),
            "the_paper_exact_packet_still_hits_the_ckm_scale_inside_this_tetrahedral_oscillator_class": (
                abs(paper_record["observables"]["Vus"] - PDG_2025_TARGETS["Vus"]) < 5e-4
                and abs(paper_record["observables"]["Vcb"] - PDG_2025_TARGETS["Vcb"]) < 2e-3
                and abs(paper_record["observables"]["Vub"] - PDG_2025_TARGETS["Vub"]) < 5e-4
                and abs(paper_record["observables"]["J"] - PDG_2025_TARGETS["J"]) < 5e-7
            ),
        },
        "interpretation": (
            "The tetrahedral oscillator is now live on the CKM side. The same "
            "4-point Fourier packet used on the chart atlas organizes the four "
            "quark carrier slots. A single quarter-turn edge is perfectly "
            "democratic across the four tetra modes, while the minimal two-edge "
            "architecture splits exactly into a carrier pair and a gap pair. The "
            "paper's asymmetric packet is not outside this story: it is a small "
            "real deformation inside the same pairwise-conjugate tetra mode class."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
