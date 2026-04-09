"""Exact middle-anchor plus outer-shell law in the triality basis.

The tetra-axis frame bridge showed that the live two-edge CKM packet

    v(a,b) = (1, i a, 1, -i b)

maps exactly to the axis/qutrit packet

    c(a,b) = ( i(a+b)/2,  1 - i(a-b)/2,  -i(a+b)/2 ).

This module resolves that 3-vector in the natural real ``1 ⊕ 2`` family basis

    U = (1, 1, 1),      fixed line,
    M = (1,-2, 1),      middle-family anchor,
    O = (1, 0,-1),      outer-pair shell.

The exact law is:

    c(a,b)
      = ((1 - iδ)/3) U  - ((1 - iδ)/3) M  + iσ O,

where

    σ = (a+b)/2,    δ = (a-b)/2.

So the live CKM two-edge ansatz is exactly:

    fixed line  +  middle-family anchor  +  outer-pair shell,

with the fixed-line and middle-anchor coefficients locked equal and opposite.
This makes the old "middle-family anchor + outer shell" picture exact in the
triality carrier, not just a numerical pattern from CKM scans.
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

from exploration.w33_tetra_axis_frame_bridge import (
    _axis_coordinates,
    _two_edge_vector,
)


DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_triality_middle_anchor_bridge_summary.json"


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


def _coefficients_from_half_sum_half_difference(sigma: float, delta: float) -> dict[str, complex]:
    lock = (1.0 - 1j * delta) / 3.0
    return {
        "fixed_line": lock,
        "middle_anchor": -lock,
        "outer_shell": 1j * sigma,
    }


def _reconstruct_from_basis(coefficients: dict[str, complex]) -> np.ndarray:
    basis = _family_basis()
    return sum(coefficients[name] * basis[name] for name in basis)


def build_summary() -> dict[str, Any]:
    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    a = float(quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]["amplitude"])
    b = float(lift["second_layer_lift_edge"]["amplitude"])
    sigma = (a + b) / 2.0
    delta = (a - b) / 2.0

    vertex_packet = _two_edge_vector(a, b)
    axis_packet = _axis_coordinates(vertex_packet)
    basis = _family_basis()
    coefficients = _coefficients_from_half_sum_half_difference(sigma, delta)
    reconstructed = _reconstruct_from_basis(coefficients)

    coefficient_matrix = np.column_stack([basis[name] for name in ("fixed_line", "middle_anchor", "outer_shell")])
    solved, *_ = np.linalg.lstsq(coefficient_matrix, axis_packet, rcond=None)

    return {
        "live_packet": {
            "amplitudes": {"a_z2": a, "b_z1": b},
            "half_sum_sigma": sigma,
            "half_difference_delta": delta,
            "vertex_packet_real_imag": _serialize_complex_vector(vertex_packet),
            "axis_packet_real_imag": _serialize_complex_vector(axis_packet),
        },
        "triality_family_basis": {
            name: _serialize_complex_vector(vector) for name, vector in basis.items()
        },
        "exact_coefficients": {
            name: {"real": float(value.real), "imag": float(value.imag)}
            for name, value in coefficients.items()
        },
        "least_squares_coefficients": {
            name: {"real": float(value.real), "imag": float(value.imag)}
            for name, value in zip(("fixed_line", "middle_anchor", "outer_shell"), solved)
        },
        "reconstructed_axis_packet_real_imag": _serialize_complex_vector(reconstructed),
        "triality_middle_anchor_theorem": {
            "the_live_two_edge_axis_packet_lies_exactly_in_fixed_line_plus_middle_anchor_plus_outer_shell": bool(
                np.allclose(reconstructed, axis_packet, atol=1e-12)
            ),
            "the_fixed_line_and_middle_anchor_coefficients_are_locked_equal_and_opposite": bool(
                abs(coefficients["fixed_line"] + coefficients["middle_anchor"]) < 1e-12
            ),
            "the_half_sum_sigma_controls_the_outer_pair_shell": bool(
                abs(coefficients["outer_shell"] - 1j * sigma) < 1e-12
            ),
            "the_half_difference_delta_controls_the_common_fixed_plus_anchor_lock": bool(
                abs(coefficients["fixed_line"] - (1.0 - 1j * delta) / 3.0) < 1e-12
                and abs(coefficients["middle_anchor"] + (1.0 - 1j * delta) / 3.0) < 1e-12
            ),
        },
        "interpretation": (
            "Inside the triality/qutrit carrier, the live CKM two-edge ansatz is "
            "exactly a middle-family anchor plus an outer-pair shell. The half-sum "
            "of the two quarter-turn amplitudes drives the antisymmetric outer shell, "
            "while the half-difference drives one locked coefficient shared by the "
            "fixed line and the middle-family anchor with opposite signs."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["triality_middle_anchor_theorem"], indent=2))


if __name__ == "__main__":
    main()
