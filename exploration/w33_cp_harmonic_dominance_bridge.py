"""Harmonic dominance of the unitary CP phase response.

After gauge reduction, the anchored quark CP ansatz depends on one physical
phase sum ``theta = alpha + beta``. The remaining functional question is how
complicated the unitary Jarlskog response ``J_unitary(a, theta)`` really is.

This module computes the Fourier content of the one-phase response on a theta
grid for representative bridge amplitudes. Because the response is odd under
``theta -> -theta``, only sine harmonics survive numerically. The main result
is that the first sine harmonic dominates strongly:

- above ``99.99%`` of the first-five-mode power at ``a = 0.1``;
- above ``99.87%`` at ``a = 0.3``;
- above ``99.36%`` at ``a = 0.5``;
- still above ``98.0%`` even at full bridge strength ``a = 1``.

So the physical CP phase law is already very close to a one-harmonic response
curve:

    J_unitary(a, theta) ~= -g1(a) sin(theta),

with higher harmonics providing only controlled corrections.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_cp_harmonic_dominance_bridge_summary.json"
AMPLITUDES = (0.1, 0.3, 0.5, 1.0)
THETA_GRID_SIZE = 720
MAX_HARMONIC = 5


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


@lru_cache(maxsize=1)
def build_cp_harmonic_dominance_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)

    theta_grid = np.linspace(0.0, 2.0 * np.pi, THETA_GRID_SIZE, endpoint=False)
    amplitude_reports: dict[str, Any] = {}

    for amplitude in AMPLITUDES:
        values = np.array(
            [
                _jarlskog(_polar_unitary(even + amplitude * np.exp(1j * theta / 2.0) * odd))
                for theta in theta_grid
            ],
            dtype=float,
        )
        total_power = float(np.dot(values, values) / THETA_GRID_SIZE)

        harmonics: list[dict[str, float]] = []
        for harmonic in range(1, MAX_HARMONIC + 1):
            cosine = np.cos(harmonic * theta_grid)
            sine = np.sin(harmonic * theta_grid)
            a_n = float(2.0 * np.dot(values, cosine) / THETA_GRID_SIZE)
            b_n = float(2.0 * np.dot(values, sine) / THETA_GRID_SIZE)
            power = a_n * a_n + b_n * b_n
            harmonics.append(
                {
                    "harmonic": float(harmonic),
                    "cosine_coefficient": a_n,
                    "sine_coefficient": b_n,
                    "power": power,
                }
            )

        truncated_power = sum(item["power"] for item in harmonics)
        first_harmonic_share = harmonics[0]["power"] / truncated_power
        cosine_power = sum(item["cosine_coefficient"] ** 2 for item in harmonics)
        sine_power = sum(item["sine_coefficient"] ** 2 for item in harmonics)

        amplitude_reports[str(amplitude)] = {
            "total_signal_power": total_power,
            "first_five_harmonics": harmonics,
            "first_harmonic_share_of_first_five_power": first_harmonic_share,
            "cosine_power_within_first_five": cosine_power,
            "sine_power_within_first_five": sine_power,
        }

    return {
        "status": "ok",
        "amplitude_reports": amplitude_reports,
        "cp_harmonic_dominance_theorem": {
            "phase_response_is_numerically_pure_sine_up_to_roundoff_in_first_five_modes": all(
                amplitude_reports[str(amplitude)]["cosine_power_within_first_five"] < 1e-30
                for amplitude in AMPLITUDES
            ),
            "first_harmonic_carries_more_than_99_point_99_percent_of_first_five_mode_power_at_a_0_point_1": (
                amplitude_reports["0.1"]["first_harmonic_share_of_first_five_power"] > 0.9999
            ),
            "first_harmonic_carries_more_than_99_point_8_percent_of_first_five_mode_power_at_a_0_point_3": (
                amplitude_reports["0.3"]["first_harmonic_share_of_first_five_power"] > 0.998
            ),
            "first_harmonic_carries_more_than_99_percent_of_first_five_mode_power_at_a_0_point_5": (
                amplitude_reports["0.5"]["first_harmonic_share_of_first_five_power"] > 0.99
            ),
            "first_harmonic_still_carries_more_than_98_percent_of_first_five_mode_power_at_a_1": (
                amplitude_reports["1.0"]["first_harmonic_share_of_first_five_power"] > 0.98
            ),
        },
        "interpretive_read": (
            "Inference from the harmonic data: once the phase frontier is reduced "
            "to the physical sum theta, the unitary Jarlskog response is already "
            "almost a pure first sine harmonic. Higher harmonics remain present "
            "but are quantitatively small corrections."
        ),
        "bridge_verdict": (
            "The unitary CP response is not a complicated one-phase function in "
            "practice. It is numerically a sine law with small higher-harmonic "
            "corrections. Even at full bridge strength, the first harmonic still "
            "carries over 98% of the first-five-mode power. So the CP sector is "
            "effectively one response curve g1(a) multiplying sin(theta), with "
            "controlled deviations rather than a wild phase landscape."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_cp_harmonic_dominance_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
