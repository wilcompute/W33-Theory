"""Atmospheric-selector closure of the anchored CKM CP bridge.

The anchored quark CP reduction left two physical ingredients:

1. the odd-bridge strength ``a``; and
2. the physical phase sum ``theta``.

The older repo line already contains a distinguished exact ratio on the
electroweak / PMNS side:

    sin²(theta_23) = 7/13.

This module tests that ratio directly inside the new anchored CKM bridge.
The result is unexpectedly tight:

- at the quarter-turn phase classes ``theta = 3pi/4`` and ``5pi/4``,
- with the exact amplitude ``a = 7/13``,

the unitary Jarlskog invariant comes out

    J = ±3.116254289e-5,

which matches the 2024 PDG CKM target ``3.12e-5`` to about ``0.12%``.

So the strongest current closure is not the older ``14pi/13`` PMNS phase
carried over blindly to CKM. It is the older atmospheric selector ``7/13``
reappearing as the anchored odd-bridge strength, paired with the quarter-turn
phase class already favored by the small-amplitude CP onset.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_atmospheric_quarter_turn_ckm_bridge_summary.json"
TARGET_J_CKM = 3.12e-5
PMNS_ATMOSPHERIC_SELECTOR = 7.0 / 13.0
COMPARISON_PHASES = {
    "3pi_over_4": 3.0 * pi / 4.0,
    "5pi_over_4": 5.0 * pi / 4.0,
    "12pi_over_13": 12.0 * pi / 13.0,
    "14pi_over_13": 14.0 * pi / 13.0,
}


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


def _anchored_cp_blocks() -> tuple[np.ndarray, np.ndarray]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")
    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)
    return even, odd


def _unitary_jarlskog(amplitude: float, theta: float, even: np.ndarray, odd: np.ndarray) -> float:
    unitary = _polar_unitary(even + amplitude * np.exp(1j * theta / 2.0) * odd)
    return _jarlskog(unitary)


@lru_cache(maxsize=1)
def build_atmospheric_quarter_turn_ckm_bridge_summary() -> dict[str, Any]:
    even, odd = _anchored_cp_blocks()
    electroweak = _load_json("w33_heawood_electroweak_polarization_bridge_summary.json")
    root_gap = float(electroweak["polarization_dictionary"]["root_gap"]["float"])
    hypercharge_share = float(electroweak["polarization_dictionary"]["hypercharge_share"]["float"])

    atmospheric_reports: dict[str, Any] = {}
    denominator_thirteen_scan: dict[str, Any] = {}
    global_candidates: list[tuple[float, str, int, float, float]] = []

    for phase_name, theta in COMPARISON_PHASES.items():
        atmospheric_j = _unitary_jarlskog(PMNS_ATMOSPHERIC_SELECTOR, theta, even, odd)
        atmospheric_reports[phase_name] = {
            "theta_over_pi": theta / pi,
            "selector_amplitude": PMNS_ATMOSPHERIC_SELECTOR,
            "unitary_jarlskog": atmospheric_j,
            "absolute_target_error": abs(abs(atmospheric_j) - TARGET_J_CKM),
            "relative_target_error": abs(abs(atmospheric_j) - TARGET_J_CKM) / TARGET_J_CKM,
        }

        best_error = float("inf")
        best_numerator = -1
        best_j = 0.0
        by_numerator: dict[str, Any] = {}
        for numerator in range(1, 13):
            amplitude = numerator / 13.0
            j_value = _unitary_jarlskog(amplitude, theta, even, odd)
            error = abs(abs(j_value) - TARGET_J_CKM)
            by_numerator[str(numerator)] = {
                "amplitude": amplitude,
                "unitary_jarlskog": j_value,
                "absolute_target_error": error,
                "relative_target_error": error / TARGET_J_CKM,
            }
            global_candidates.append((error, phase_name, numerator, amplitude, j_value))
            if error < best_error:
                best_error = error
                best_numerator = numerator
                best_j = j_value

        denominator_thirteen_scan[phase_name] = {
            "theta_over_pi": theta / pi,
            "best_numerator": best_numerator,
            "best_amplitude": best_numerator / 13.0,
            "best_unitary_jarlskog": best_j,
            "best_absolute_target_error": best_error,
            "all_numerator_reports": by_numerator,
        }

    global_candidates.sort()
    best_error, best_phase_name, best_numerator, best_amplitude, best_j = global_candidates[0]
    opposite_error, opposite_phase_name, opposite_numerator, opposite_amplitude, opposite_j = global_candidates[1]

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "pmns_atmospheric_selector": PMNS_ATMOSPHERIC_SELECTOR,
        "heawood_electroweak_dictionary": {
            "weak_share": electroweak["polarization_dictionary"]["weak_share"],
            "hypercharge_share": electroweak["polarization_dictionary"]["hypercharge_share"],
            "root_gap": electroweak["polarization_dictionary"]["root_gap"],
            "polarization_amplitude": electroweak["polarization_dictionary"]["polarization_amplitude"],
        },
        "phase_reports_at_atmospheric_selector": atmospheric_reports,
        "denominator_thirteen_amplitude_scan_by_phase": denominator_thirteen_scan,
        "best_simple_q13_candidates": [
            {
                "phase_name": best_phase_name,
                "theta_over_pi": COMPARISON_PHASES[best_phase_name] / pi,
                "numerator": best_numerator,
                "amplitude": best_amplitude,
                "unitary_jarlskog": best_j,
                "absolute_target_error": best_error,
            },
            {
                "phase_name": opposite_phase_name,
                "theta_over_pi": COMPARISON_PHASES[opposite_phase_name] / pi,
                "numerator": opposite_numerator,
                "amplitude": opposite_amplitude,
                "unitary_jarlskog": opposite_j,
                "absolute_target_error": opposite_error,
            },
        ],
        "atmospheric_quarter_turn_ckm_bridge_theorem": {
            "pmns_atmospheric_selector_7_over_13_hits_observed_ckm_jarlskog_scale_at_three_pi_over_4": (
                atmospheric_reports["3pi_over_4"]["relative_target_error"] < 0.002
            ),
            "pmns_atmospheric_selector_7_over_13_hits_observed_ckm_jarlskog_scale_at_five_pi_over_4": (
                atmospheric_reports["5pi_over_4"]["relative_target_error"] < 0.002
            ),
            "quarter_turn_classes_are_the_unique_best_simple_q13_phase_choices_in_the_tested_native_set": (
                best_phase_name in {"3pi_over_4", "5pi_over_4"}
                and opposite_phase_name in {"3pi_over_4", "5pi_over_4"}
                and best_numerator == 7
                and opposite_numerator == 7
            ),
            "seven_thirteenths_is_the_unique_best_denominator_13_amplitude_at_each_quarter_turn_class": (
                denominator_thirteen_scan["3pi_over_4"]["best_numerator"] == 7
                and denominator_thirteen_scan["5pi_over_4"]["best_numerator"] == 7
            ),
            "ckm_quarter_turn_closure_uses_exact_heawood_root_gap": (
                abs(best_amplitude - root_gap) < 1e-12
                and abs(opposite_amplitude - root_gap) < 1e-12
            ),
            "older_pmns_phase_fourteen_pi_over_13_prefers_exact_heawood_hypercharge_share_in_the_q13_scan": (
                abs(denominator_thirteen_scan["14pi_over_13"]["best_amplitude"] - hypercharge_share) < 1e-12
                and abs(denominator_thirteen_scan["12pi_over_13"]["best_amplitude"] - hypercharge_share) < 1e-12
            ),
            "older_pmns_phase_fourteen_pi_over_13_is_not_the_best_simple_closure_for_ckm_cp": (
                atmospheric_reports["5pi_over_4"]["absolute_target_error"]
                < denominator_thirteen_scan["14pi_over_13"]["best_absolute_target_error"]
            ),
        },
        "interpretive_read": (
            "Inference from the exact q/13 scan: the strongest simple closure of "
            "the anchored CKM CP bridge is amplitude-side, not phase-side. The "
            "old atmospheric selector 7/13 reappears as the odd-bridge strength, "
            "and that same value is already the exact Heawood electroweak root "
            "gap. By contrast, the older PMNS phase 14pi/13 does not control "
            "the best CKM closure directly; in the same q/13 dictionary it "
            "prefers the Heawood hypercharge share 10/13."
        ),
        "bridge_verdict": (
            "The first clean closure between the older PMNS line and the new "
            "anchored CKM mechanism is now explicit. Setting the anchored odd "
            "bridge strength to the exact atmospheric selector 7/13 and the "
            "physical phase sum to a quarter-turn class produces |J| = "
            "3.116254289e-5, matching the observed CKM scale to about 0.12%. "
            "Within the tested native q/13 amplitude and phase classes, that is "
            "the unique best simple hit. The same amplitude is already the exact "
            "Heawood electroweak root gap, while the old 14pi/13 phase line "
            "naturally pairs instead with the exact hypercharge share 10/13."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_heawood_electroweak_polarization_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_atmospheric_quarter_turn_ckm_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
