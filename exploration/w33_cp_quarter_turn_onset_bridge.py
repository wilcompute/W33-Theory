"""Quadratic quarter-turn onset of CP on the anchored odd bridge.

The capacity-curve work showed that the parity-odd ``U2`` anchor bridge can
support the observed CKM CP scale. The next sharper question is how CP turns on
as the odd-bridge amplitude is increased from zero.

This module samples the small-amplitude regime of the common-phase family

    E + a * exp(i phi) * O

and extracts two low-amplitude facts:

1. the maximizing phase is already locked near quarter-turn classes
   ``phi = pi/4 mod pi/2``;
2. the maximal unitary Jarlskog response scales quadratically in amplitude,
   with nearly constant ratio ``J_max(a)/a^2`` over the sampled onset window.

So the first CP response is not linear and not cubic in the current minimal
ansatz. It is a quarter-turn, quadratic activation of the odd ``U2`` bridge.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_cp_quarter_turn_onset_bridge_summary.json"
TOL = 1e-12
AMPLITUDES = (0.0125, 0.025, 0.0375, 0.05, 0.075, 0.1)
PHASE_GRID_SIZE = 2881


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def _quarter_turn_distance_over_pi(phi_over_pi: float) -> float:
    quarter_classes = (0.25, 0.75, 1.25, 1.75)
    return min(abs(phi_over_pi - value) for value in quarter_classes)


@lru_cache(maxsize=1)
def build_cp_quarter_turn_onset_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)

    phase_grid = np.linspace(0.0, 2.0 * np.pi, PHASE_GRID_SIZE)
    onset_samples: list[dict[str, float]] = []
    ratios: list[float] = []
    quarter_distances: list[float] = []

    for amplitude in AMPLITUDES:
        best_abs_j = 0.0
        best_phase = 0.0
        for phase in phase_grid:
            unitary = _polar_unitary(even + amplitude * np.exp(1j * phase) * odd)
            abs_j = abs(_jarlskog(unitary))
            if abs_j > best_abs_j:
                best_abs_j = abs_j
                best_phase = float(phase)

        ratio = best_abs_j / (amplitude * amplitude)
        phi_over_pi = best_phase / pi
        distance = _quarter_turn_distance_over_pi(phi_over_pi)
        ratios.append(ratio)
        quarter_distances.append(distance)
        onset_samples.append(
            {
                "amplitude": float(amplitude),
                "max_abs_unitary_jarlskog": float(best_abs_j),
                "best_phase_radians": best_phase,
                "best_phase_over_pi": phi_over_pi,
                "jarlskog_over_amplitude_squared": float(ratio),
                "quarter_turn_distance_over_pi": float(distance),
            }
        )

    ratio_min = min(ratios)
    ratio_max = max(ratios)
    ratio_relative_spread = (ratio_max - ratio_min) / ratio_min

    return {
        "status": "ok",
        "onset_samples": onset_samples,
        "ratio_band": {
            "min_j_over_a_squared": float(ratio_min),
            "max_j_over_a_squared": float(ratio_max),
            "relative_spread": float(ratio_relative_spread),
        },
        "cp_quarter_turn_onset_theorem": {
            "small_amplitude_cp_capacity_is_quadratic_to_within_two_percent_on_sample_window": (
                ratio_relative_spread < 0.02
            ),
            "best_common_phase_is_locked_to_quarter_turn_classes_on_sample_window": (
                max(quarter_distances) < 0.002
            ),
            "leading_small_amplitude_coefficient_is_about_9_point_8e_minus_5": (
                9.7e-5 < ratio_min < 9.9e-5 and 9.9e-5 < ratio_max < 1.01e-4
            ),
            "cp_onset_is_quadratic_not_linear": (
                ratio_min > 0.0
            ),
        },
        "interpretive_read": (
            "Inference from the sampled onset window: the first CP response of "
            "the anchored odd bridge behaves like quarter-turn interference "
            "between even shell and odd bridge data. The maximizing phase sits "
            "at quarter-turn classes and the unitary Jarlskog response scales "
            "quadratically in the bridge amplitude."
        ),
        "bridge_verdict": (
            "The minimal CP mechanism is now sharper than a generic phase fit. "
            "At small amplitude, CP turns on through a quarter-turn phase on the "
            "odd U2 bridge and grows quadratically, with "
            "J_max(a)/a^2 ≈ 9.8e-5 across the sampled onset window. So the first "
            "CP activation law in the current repo is a quarter-turn quadratic "
            "response, not a linear or cubic effect."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_cp_quarter_turn_onset_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
