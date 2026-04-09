"""Compress the live CKM phase onto the triality outer shell.

The exact live triality packet was

    c = ((1 - i delta)/3) U - ((1 - i delta)/3) M + i sigma O,

with

    sigma = (a+b)/2,
    delta = (a-b)/2.

This module proves that a single global triality rephasing removes the complex
phase from the locked ``U/M`` pair entirely:

    g = (1 + i delta) / sqrt(1 + delta^2) = exp(i arctan delta)

gives

    g c = r U - r M + O_term,
    r = sqrt(1 + delta^2) / 3,

so the fixed-line and middle-anchor coefficients become exactly real and equal
and opposite.  All remaining complex phase lives on the outer shell.

This is the triality-side compression of the earlier anchor-phase gauge
reduction theorem.
"""

from __future__ import annotations

import json
from math import atan, sqrt
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_triality_phase_compression_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_tetra_axis_frame_bridge import _axis_coordinates, _two_edge_vector
from exploration.w33_triality_tomotope_lift_bridge import _family_coefficients


def _serialize_complex(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imag": float(value.imag)}


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def build_summary() -> dict[str, Any]:
    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    lift = _load_json("w33_two_sheet_ckm_lift_bridge_summary.json")
    a = float(quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]["amplitude"])
    b = float(lift["second_layer_lift_edge"]["amplitude"])
    sigma = (a + b) / 2.0
    delta = (a - b) / 2.0

    axis = _axis_coordinates(_two_edge_vector(a, b))
    coeffs = _family_coefficients(axis)

    gauge = (1.0 + 1j * delta) / sqrt(1.0 + delta**2)
    gauged_coeffs = {name: gauge * value for name, value in coeffs.items()}

    expected_real_lock = sqrt(1.0 + delta**2) / 3.0
    expected_outer = gauge * (1j * sigma)

    conj_axis = np.conjugate(axis)
    conj_coeffs = _family_coefficients(conj_axis)
    gauged_conj_coeffs = {name: np.conjugate(gauge) * value for name, value in conj_coeffs.items()}

    return {
        "live_packet_parameters": {
            "a_z2": a,
            "b_z1": b,
            "sigma_half_sum": sigma,
            "delta_half_difference": delta,
            "gauge_phase_radians": atan(delta),
            "gauge_phase_over_pi": atan(delta) / np.pi,
        },
        "ungauged_triality_coefficients": {
            name: _serialize_complex(value) for name, value in coeffs.items()
        },
        "gauged_triality_coefficients": {
            name: _serialize_complex(value) for name, value in gauged_coeffs.items()
        },
        "gauged_conjugate_branch_coefficients": {
            name: _serialize_complex(value) for name, value in gauged_conj_coeffs.items()
        },
        "triality_phase_compression_theorem": {
            "a_single_global_triality_phase_makes_the_fixed_line_coefficient_exactly_real": bool(
                abs(gauged_coeffs["fixed_line"].imag) < 1e-12
                and abs(gauged_coeffs["fixed_line"].real - expected_real_lock) < 1e-12
            ),
            "the_same_phase_makes_the_middle_anchor_exactly_real_and_equal_opposite": bool(
                abs(gauged_coeffs["middle_anchor"].imag) < 1e-12
                and abs(gauged_coeffs["middle_anchor"].real + expected_real_lock) < 1e-12
            ),
            "all_remaining_complex_phase_lives_on_the_outer_shell": bool(
                abs(gauged_coeffs["fixed_line"].imag) < 1e-12
                and abs(gauged_coeffs["middle_anchor"].imag) < 1e-12
                and abs(gauged_coeffs["outer_shell"] - expected_outer) < 1e-12
            ),
            "the_conjugate_ckm_branch_keeps_the_same_real_lock_and_conjugates_only_the_outer_shell": bool(
                abs(gauged_conj_coeffs["fixed_line"].imag) < 1e-12
                and abs(gauged_conj_coeffs["middle_anchor"].imag) < 1e-12
                and abs(gauged_conj_coeffs["fixed_line"].real - expected_real_lock) < 1e-12
                and abs(gauged_conj_coeffs["middle_anchor"].real + expected_real_lock) < 1e-12
                and abs(gauged_conj_coeffs["outer_shell"] - np.conjugate(expected_outer)) < 1e-12
            ),
        },
        "interpretation": (
            "The live triality packet has only one physical phase. After one global "
            "triality rephasing, the fixed-line and middle-anchor lock is exactly "
            "real and equal-opposite, and all complex phase sits on the outer shell. "
            "So CP on the live family carrier is literally an outer-shell phase."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["triality_phase_compression_theorem"], indent=2))


if __name__ == "__main__":
    main()
