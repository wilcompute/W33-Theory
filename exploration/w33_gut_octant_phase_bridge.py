"""GUT-octant phase closure of the anchored CKM bridge at Heawood amplitude.

The strongest current amplitude-side result is already exact in the repo's
native q/13 dictionary:

    a = 7/13

is the Heawood root gap and gives an observed-CKM-scale hit.

The remaining question is whether the corresponding common phase is also
naturally quantized inside an existing repo dictionary. This module tests the
16 octant common phases

    phi = n pi / 8,   n = 0,...,15

in the minimal ansatz

    E + (7/13) exp(i phi) O.

The outcome is sharp:

- the unique best octant target hits are
      phi/pi = 3/8, 5/8, 11/8, 13/8;
- the two fundamental classes are therefore
      phi/pi = 3/8, 5/8;
- those are exactly the old GUT electroweak shares
      sin²(theta_W)|_GUT = 3/8,
      cos²(theta_W)|_GUT = 5/8.

So once the amplitude is fixed to the Heawood root gap 7/13, the observed CKM
scale selects the GUT electroweak octant pair on the common-phase side.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_gut_octant_phase_bridge_summary.json"
TARGET_J_CKM = 3.12e-5
GUT_SIN2 = 3.0 / 8.0
GUT_COS2 = 5.0 / 8.0
OCTANT_DENOMINATOR = 8


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def _anchored_blocks() -> tuple[np.ndarray, np.ndarray]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")
    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)
    return even, odd


@lru_cache(maxsize=1)
def build_gut_octant_phase_bridge_summary() -> dict[str, Any]:
    even, odd = _anchored_blocks()
    heawood = _load_json("w33_heawood_electroweak_polarization_bridge_summary.json")
    root_gap = float(heawood["polarization_dictionary"]["root_gap"]["float"])

    reports: list[dict[str, Any]] = []
    for numerator in range(2 * OCTANT_DENOMINATOR):
        phi = numerator * pi / OCTANT_DENOMINATOR
        unitary = _polar_unitary(even + root_gap * np.exp(1j * phi) * odd)
        j_value = _jarlskog(unitary)
        reports.append(
            {
                "octant_numerator": numerator,
                "common_phase_over_pi": numerator / OCTANT_DENOMINATOR,
                "physical_theta_over_pi": numerator / (OCTANT_DENOMINATOR / 2.0),
                "unitary_jarlskog": j_value,
                "absolute_target_error": abs(abs(j_value) - TARGET_J_CKM),
                "relative_target_error": abs(abs(j_value) - TARGET_J_CKM) / TARGET_J_CKM,
            }
        )

    sorted_reports = sorted(reports, key=lambda item: item["absolute_target_error"])
    best_four = sorted_reports[:4]
    best_numerators = sorted(item["octant_numerator"] for item in best_four)
    reduced_best_classes = sorted({item["octant_numerator"] % OCTANT_DENOMINATOR for item in best_four})

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "heawood_root_gap_amplitude": {
            "exact": heawood["polarization_dictionary"]["root_gap"]["exact"],
            "float": root_gap,
        },
        "gut_electroweak_octant_dictionary": {
            "sin2_theta_w_gut": {"exact": "3/8", "float": GUT_SIN2},
            "cos2_theta_w_gut": {"exact": "5/8", "float": GUT_COS2},
        },
        "octant_phase_reports_sorted_by_target_error": sorted_reports,
        "best_octant_candidates": best_four,
        "gut_octant_phase_bridge_theorem": {
            "best_octant_candidates_are_exactly_three_five_eleven_thirteen_mod_sixteen": (
                best_numerators == [3, 5, 11, 13]
            ),
            "fundamental_best_common_phase_classes_are_three_eighths_and_five_eighths": (
                reduced_best_classes == [3, 5]
            ),
            "best_common_phase_classes_match_exact_gut_electroweak_shares": (
                reduced_best_classes == [int(8 * GUT_SIN2), int(8 * GUT_COS2)]
            ),
            "heawood_root_gap_plus_gut_octant_phases_hit_observed_ckm_scale_within_two_tenths_percent": (
                all(item["relative_target_error"] < 0.002 for item in best_four)
            ),
            "all_best_common_phase_classes_correspond_to_physical_phase_sum_quarter_turn_classes": (
                all(
                    abs(((item["physical_theta_over_pi"] % 2.0) - target)) < 1e-12
                    for item in best_four
                    for target in ([0.75] if (item["octant_numerator"] % 8 in {3, 11}) else [1.25])
                )
            ),
        },
        "interpretive_read": (
            "Inference from the discrete octant scan: once the anchored bridge "
            "strength is fixed to the Heawood root gap 7/13, the common-phase "
            "side is not wandering freely. The observed CKM target selects the "
            "GUT electroweak octant pair 3/8 and 5/8, together with their "
            "half-turn translates."
        ),
        "bridge_verdict": (
            "The phase side now has a native discrete closure too. At exact "
            "Heawood amplitude 7/13, the unique best octant common phases are "
            "3pi/8, 5pi/8, 11pi/8, and 13pi/8. Modulo the half-turn symmetry, "
            "the fundamental classes are 3/8 and 5/8, exactly the old GUT "
            "electroweak shares sin^2(theta_W)|_GUT and cos^2(theta_W)|_GUT. "
            "So the current strongest CKM closure is a full Heawood/GUT "
            "dictionary: amplitude 7/13, phase 3/8 or 5/8."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_heawood_electroweak_polarization_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_gut_octant_phase_bridge_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
