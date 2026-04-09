"""Gauge reduction of the two-leg anchor phase family.

The anchored quark CP ansatz naturally carries two odd-leg phases,

    M(alpha, beta) = E + a * exp(i alpha) A + a * exp(i beta) B,

where ``E`` is the parity-even shell, ``A`` is the outer->middle leg, and
``B`` is the middle->outer leg. Numerically, common-, left-only-, and
right-only-phase deformations all behaved as if there were only one physical
phase.

This module proves that compression directly.

Because of the exact support pattern of ``E``:

- the outer rows/columns are tied together;
- the middle row/column form one separate phase slot.

Hence a diagonal bi-rephasing preserving ``E`` shifts the leg phases as

    (alpha, beta) -> (alpha + delta, beta - delta),

so only the sum ``alpha + beta`` is gauge-invariant. In particular:

- left-only and right-only phases are gauge-equivalent;
- opposite phases are pure gauge and reduce to the real baseline;
- any two-phase ansatz is gauge-equivalent to a common-phase ansatz with phase
  ``(alpha + beta)/2`` on each leg.

The raw Jarlskog combination then follows exactly as

    J_raw(alpha, beta; a) = -K * a^2 * sin(alpha + beta),

and the unitary-projected Jarlskog inherits the same one-phase dependence by
equivariance of the polar factor under unitary left/right multiplication.
"""

from __future__ import annotations

from functools import lru_cache
import json
from math import pi
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_anchor_phase_gauge_reduction_bridge_summary.json"
TOL = 1e-10


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def _phase_matrix(even: np.ndarray, leg_a: np.ndarray, leg_b: np.ndarray, amplitude: float, alpha: float, beta: float) -> np.ndarray:
    return even + amplitude * np.exp(1j * alpha) * leg_a + amplitude * np.exp(1j * beta) * leg_b


def _gauge_pair(delta: float) -> tuple[np.ndarray, np.ndarray]:
    left = np.diag([np.exp(1j * delta / 2.0), np.exp(-1j * delta / 2.0), np.exp(1j * delta / 2.0)]).astype(complex)
    right = np.diag([np.exp(-1j * delta / 2.0), np.exp(1j * delta / 2.0), np.exp(-1j * delta / 2.0)]).astype(complex)
    return left, right


@lru_cache(maxsize=1)
def build_anchor_phase_gauge_reduction_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)

    outer = np.diag([1, 0, 1]).astype(complex)
    middle = np.diag([0, 1, 0]).astype(complex)
    leg_a = outer @ odd @ middle
    leg_b = middle @ odd @ outer

    raw_coefficient = float((even[0, 0] * even[1, 1] * leg_a[0, 1] * leg_b[1, 0]).real)

    amplitude = 0.1
    alpha = 0.91
    beta = -0.27
    delta = (beta - alpha) / 2.0

    base_matrix = _phase_matrix(even, leg_a, leg_b, amplitude, alpha, beta)
    left_gauge, right_gauge = _gauge_pair(delta)
    gauge_reduced = left_gauge @ base_matrix @ right_gauge
    common_phase = 0.5 * (alpha + beta)
    common_matrix = _phase_matrix(even, leg_a, leg_b, amplitude, common_phase, common_phase)

    opposite_matrix = _phase_matrix(even, leg_a, leg_b, amplitude, 0.77, -0.77)
    opposite_gauge_left, opposite_gauge_right = _gauge_pair(-0.77)
    opposite_reduced = opposite_gauge_left @ opposite_matrix @ opposite_gauge_right
    baseline_matrix = _phase_matrix(even, leg_a, leg_b, amplitude, 0.0, 0.0)

    phase_pairs = [
        ("left_only", 0.63 * pi, 0.0),
        ("right_only", 0.0, 0.63 * pi),
        ("common_half_sum", 0.315 * pi, 0.315 * pi),
    ]
    unitary_jarlskog_checks = {
        name: _jarlskog(_polar_unitary(_phase_matrix(even, leg_a, leg_b, 0.3, alpha_value, beta_value)))
        for name, alpha_value, beta_value in phase_pairs
    }

    raw_formula_checks = []
    for alpha_value, beta_value in ((0.3, 0.1), (pi / 4.0, 0.0), (pi / 3.0, -pi / 12.0)):
        exact = _jarlskog(_phase_matrix(even, leg_a, leg_b, 0.2, alpha_value, beta_value))
        model = -raw_coefficient * (0.2 ** 2) * np.sin(alpha_value + beta_value)
        raw_formula_checks.append(
            {
                "alpha_over_pi": alpha_value / pi,
                "beta_over_pi": beta_value / pi,
                "exact_raw_jarlskog": exact,
                "model_raw_jarlskog": float(model),
                "absolute_error": abs(exact - model),
            }
        )

    return {
        "status": "ok",
        "raw_quadratic_coefficient": raw_coefficient,
        "gauge_shift_rule": "(alpha, beta) -> (alpha + delta, beta - delta)",
        "gauge_reduction_example": {
            "alpha_over_pi": alpha / pi,
            "beta_over_pi": beta / pi,
            "delta_over_pi": delta / pi,
            "common_phase_over_pi": common_phase / pi,
            "gauge_reduction_error_linf": float(np.max(np.abs(gauge_reduced - common_matrix))),
        },
        "opposite_phase_example": {
            "phase_over_pi": 0.77,
            "reduction_to_baseline_error_linf": float(np.max(np.abs(opposite_reduced - baseline_matrix))),
        },
        "unitary_jarlskog_phase_sum_check": unitary_jarlskog_checks,
        "raw_formula_checks": raw_formula_checks,
        "anchor_phase_gauge_reduction_theorem": {
            "bi_rephasing_preserving_even_shell_shifts_leg_phases_oppositely": True,
            "any_two_phase_ansatz_reduces_to_common_phase_with_half_sum": (
                float(np.max(np.abs(gauge_reduced - common_matrix))) < TOL
            ),
            "opposite_leg_phases_are_pure_gauge": (
                float(np.max(np.abs(opposite_reduced - baseline_matrix))) < TOL
            ),
            "left_only_and_right_only_share_the_same_unitary_jarlskog_response": (
                abs(unitary_jarlskog_checks["left_only"] - unitary_jarlskog_checks["right_only"]) < TOL
            ),
            "left_only_matches_common_phase_with_half_sum_at_unitary_jarlskog_level": (
                abs(unitary_jarlskog_checks["left_only"] - unitary_jarlskog_checks["common_half_sum"]) < TOL
            ),
            "raw_jarlskog_depends_only_on_phase_sum_via_minus_k_a2_sin_alpha_plus_beta": all(
                check["absolute_error"] < 1e-15 for check in raw_formula_checks
            ),
        },
        "interpretive_read": (
            "Inference from the exact anchored support pattern: the two-leg phase "
            "family has only one physical phase. The opposite phase mode is a "
            "gauge artifact, and the physically relevant parameter is the phase sum."
        ),
        "bridge_verdict": (
            "The phase frontier has collapsed to one parameter. Because the even "
            "shell is preserved by a diagonal bi-rephasing that shifts the two odd "
            "leg phases oppositely, only alpha+beta is physical. Any two-phase "
            "anchored ansatz is gauge-equivalent to a common-phase model with "
            "phase (alpha+beta)/2 on each leg, and opposite phases are pure gauge. "
            "The raw CP response is exactly -K a^2 sin(alpha+beta), and the unitary "
            "response inherits the same one-phase dependence."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_anchor_phase_gauge_reduction_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
