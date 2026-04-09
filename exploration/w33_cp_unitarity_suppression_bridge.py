"""Raw-vs-unitary suppression law for CP on the anchored odd bridge.

The common-phase anchored ansatz has two distinct CP responses:

1. the raw matrix response before enforcing unitarity;
2. the physical response after polar projection to the nearest unitary matrix.

For the raw matrix

    M(a, phi) = E + a * exp(i phi) * O

the Jarlskog combination is exactly quadratic and second-harmonic:

    J_raw(a, phi) = -K_raw * a^2 * sin(2 phi),

with an explicit coefficient determined by the anchored shell/bridge path.

The unitary response keeps the same quarter-turn quadratic structure at small
amplitude, but with a much smaller coefficient. This module packages that
suppression and compares the resulting target amplitudes for the observed CKM
CP scale.
"""

from __future__ import annotations

from functools import lru_cache
import json
import math
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_cp_unitarity_suppression_bridge_summary.json"
TARGET_J_CKM = 3.12e-5


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _raw_jarlskog_value(even: np.ndarray, odd: np.ndarray, amplitude: float, phase: float) -> float:
    matrix = even + amplitude * np.exp(1j * phase) * odd
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


@lru_cache(maxsize=1)
def build_cp_unitarity_suppression_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")
    onset = _load_json("w33_cp_quarter_turn_onset_bridge_summary.json")
    capacity = _load_json("w33_cp_capacity_curve_bridge_summary.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)

    raw_coefficient = float((even[0, 0] * even[1, 1] * odd[0, 1] * odd[1, 0]).real)
    unitary_onset_coefficient = float(onset["ratio_band"]["min_j_over_a_squared"])
    suppression_factor = unitary_onset_coefficient / raw_coefficient

    raw_target_amplitude = math.sqrt(TARGET_J_CKM / raw_coefficient)
    unitary_small_amplitude_target = math.sqrt(TARGET_J_CKM / unitary_onset_coefficient)
    actual_capacity_threshold = float(capacity["threshold_amplitude_for_target_reachability"])

    sample_checks = []
    for amplitude, phase in ((0.1, math.pi / 4), (0.1, 3.0 * math.pi / 8), (0.2, math.pi / 4)):
        exact_raw = _raw_jarlskog_value(even, odd, amplitude, phase)
        model_raw = -raw_coefficient * amplitude * amplitude * math.sin(2.0 * phase)
        sample_checks.append(
            {
                "amplitude": amplitude,
                "phase_over_pi": phase / math.pi,
                "exact_raw_jarlskog": exact_raw,
                "model_raw_jarlskog": model_raw,
                "absolute_error": abs(exact_raw - model_raw),
            }
        )

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "raw_common_phase_coefficient": raw_coefficient,
        "unitary_small_amplitude_coefficient": unitary_onset_coefficient,
        "suppression_factor_unitary_over_raw": suppression_factor,
        "target_amplitudes": {
            "raw_exact_model": raw_target_amplitude,
            "unitary_small_amplitude_estimate": unitary_small_amplitude_target,
            "unitary_capacity_threshold": actual_capacity_threshold,
        },
        "sample_raw_checks": sample_checks,
        "cp_unitarity_suppression_theorem": {
            "raw_common_phase_jarlskog_is_exactly_second_harmonic_quadratic": all(
                check["absolute_error"] < 1e-15 for check in sample_checks
            ),
            "unitary_small_amplitude_coefficient_is_suppressed_by_about_1_point_24e_minus_3": (
                0.0012 < suppression_factor < 0.0013
            ),
            "raw_target_amplitude_for_observed_ckm_scale_is_about_0_point_0199": (
                abs(raw_target_amplitude - 0.019892234933175816) < 1e-15
            ),
            "small_amplitude_unitary_target_estimate_is_about_0_point_564": (
                0.56 < unitary_small_amplitude_target < 0.57
            ),
            "nonlinear_unitary_enhancement_lowers_target_threshold_to_about_0_point_49": (
                abs(actual_capacity_threshold - 0.49) < 1e-12
                and actual_capacity_threshold < unitary_small_amplitude_target
            ),
        },
        "interpretive_read": (
            "Inference from the anchored bridge coefficients: the raw complex "
            "matrix already carries a large exact second-harmonic CP response, "
            "but enforcing unitarity suppresses the onset coefficient by about "
            "8e2. Nonlinear unitary effects then partially recover capacity and "
            "pull the physical threshold down from the naive small-amplitude "
            "estimate."
        ),
        "bridge_verdict": (
            "The physical CKM CP scale is not small because the raw anchored "
            "bridge barely produces CP. The raw second-harmonic coefficient is "
            "large and exact. The main suppression comes from unitarization: the "
            "small-amplitude unitary coefficient is only about 1.24e-3 of the raw "
            "one. That pushes the naive target amplitude from 0.0199 to 0.564, "
            "before nonlinear enhancement lowers the actual reachability threshold "
            "to about 0.49. So the CP size is largely a unitarity-normalization "
            "effect on the anchored odd bridge."
        ),
        "source_files": [
            "data/w33_cp_capacity_curve_bridge_summary.json",
            "data/w33_cp_quarter_turn_onset_bridge_summary.json",
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_cp_unitarity_suppression_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
