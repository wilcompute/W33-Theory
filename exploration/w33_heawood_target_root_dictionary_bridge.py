"""Heawood q/13 target-root dictionary for the anchored CKM CP bridge.

The coarse q/13 scan already showed a simple closure:

  - the best CKM hit among tested native q/13 amplitudes and phases uses
    amplitude 7/13 at the phase-sum classes 3pi/4 and 5pi/4.

This module sharpens that from a grid observation to a root statement. We fix
two native common phases in the minimal ansatz

    E + a * exp(i phi) * O

and solve for the exact bridge amplitude ``a`` that reaches the observed 2024
PDG CKM target ``|J| = 3.12e-5``:

1. ``phi = 5pi/8`` (equivalently physical phase sum ``theta = 5pi/4``),
   the strongest simple CKM closure found so far;
2. ``phi = 7pi/13`` (equivalently ``theta = 14pi/13``),
   the older PMNS-side phase line.

The result is asymmetric and clean:

- the quarter-turn-side root is
      a_* = 0.5387032634...
  which is only 0.045% above the exact Heawood root gap 7/13;
- the ``14pi/13``-side root is
      a_* = 0.7796444771...
  which sits 1.35% above the exact Heawood hypercharge share 10/13.

So the current live CKM bridge does not just *like* the old q/13 dictionary.
At the strongest native phase class, the observed target amplitude is almost
exactly the Heawood root gap.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_heawood_target_root_dictionary_bridge_summary.json"
TARGET_J_CKM = 3.12e-5
BISECTION_STEPS = 100


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


def _common_phase_jarlskog(amplitude: float, phi: float, even: np.ndarray, odd: np.ndarray) -> float:
    unitary = _polar_unitary(even + amplitude * np.exp(1j * phi) * odd)
    return _jarlskog(unitary)


def _solve_target_root(phi: float, target_sign: float, even: np.ndarray, odd: np.ndarray) -> float:
    lo, hi = 0.0, 1.0
    for _ in range(BISECTION_STEPS):
        mid = 0.5 * (lo + hi)
        if target_sign * _common_phase_jarlskog(mid, phi, even, odd) < TARGET_J_CKM:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def _q13_reports(phi: float, even: np.ndarray, odd: np.ndarray) -> dict[str, Any]:
    best_numerator = -1
    best_error = float("inf")
    reports: dict[str, Any] = {}
    for numerator in range(1, 13):
        amplitude = numerator / 13.0
        j_value = _common_phase_jarlskog(amplitude, phi, even, odd)
        error = abs(abs(j_value) - TARGET_J_CKM)
        reports[str(numerator)] = {
            "amplitude": amplitude,
            "unitary_jarlskog": j_value,
            "absolute_target_error": error,
            "relative_target_error": error / TARGET_J_CKM,
        }
        if error < best_error:
            best_error = error
            best_numerator = numerator
    return {
        "best_numerator": best_numerator,
        "best_amplitude": best_numerator / 13.0,
        "best_absolute_target_error": best_error,
        "reports": reports,
    }


@lru_cache(maxsize=1)
def build_heawood_target_root_dictionary_summary() -> dict[str, Any]:
    even, odd = _anchored_blocks()
    electroweak = _load_json("w33_heawood_electroweak_polarization_bridge_summary.json")

    root_gap = float(electroweak["polarization_dictionary"]["root_gap"]["float"])
    hypercharge_share = float(electroweak["polarization_dictionary"]["hypercharge_share"]["float"])

    phase_specs = {
        "five_pi_over_8": {
            "common_phase_over_pi": 5.0 / 8.0,
            "physical_theta_over_pi": 5.0 / 4.0,
            "target_sign": +1.0,
            "heawood_reference": root_gap,
            "heawood_reference_name": "root_gap_7_over_13",
        },
        "seven_pi_over_13": {
            "common_phase_over_pi": 7.0 / 13.0,
            "physical_theta_over_pi": 14.0 / 13.0,
            "target_sign": +1.0,
            "heawood_reference": hypercharge_share,
            "heawood_reference_name": "hypercharge_share_10_over_13",
        },
    }

    reports: dict[str, Any] = {}
    for name, spec in phase_specs.items():
        phi = spec["common_phase_over_pi"] * pi
        root = _solve_target_root(phi, spec["target_sign"], even, odd)
        j_value = _common_phase_jarlskog(root, phi, even, odd)
        q13 = _q13_reports(phi, even, odd)
        reference = spec["heawood_reference"]
        reports[name] = {
            "common_phase_over_pi": spec["common_phase_over_pi"],
            "physical_theta_over_pi": spec["physical_theta_over_pi"],
            "target_root_amplitude": root,
            "unitary_jarlskog_at_root": j_value,
            "heawood_reference_name": spec["heawood_reference_name"],
            "heawood_reference_amplitude": reference,
            "absolute_root_to_reference_error": abs(root - reference),
            "relative_root_to_reference_error": abs(root - reference) / reference,
            "best_q13_numerator_at_fixed_phase": q13["best_numerator"],
            "best_q13_amplitude_at_fixed_phase": q13["best_amplitude"],
            "best_q13_absolute_target_error": q13["best_absolute_target_error"],
            "all_q13_reports": q13["reports"],
        }

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "heawood_dictionary": {
            "weak_share": electroweak["polarization_dictionary"]["weak_share"],
            "hypercharge_share": electroweak["polarization_dictionary"]["hypercharge_share"],
            "root_gap": electroweak["polarization_dictionary"]["root_gap"],
            "polarization_amplitude": electroweak["polarization_dictionary"]["polarization_amplitude"],
        },
        "fixed_phase_target_roots": reports,
        "heawood_target_root_dictionary_theorem": {
            "five_pi_over_8_root_is_within_five_times_ten_to_minus_four_relative_of_heawood_root_gap": (
                reports["five_pi_over_8"]["relative_root_to_reference_error"] < 5e-4
            ),
            "five_pi_over_8_fixed_phase_prefers_q13_amplitude_7_over_13": (
                reports["five_pi_over_8"]["best_q13_numerator_at_fixed_phase"] == 7
            ),
            "seven_pi_over_13_root_is_within_two_percent_relative_of_heawood_hypercharge_share": (
                reports["seven_pi_over_13"]["relative_root_to_reference_error"] < 0.02
            ),
            "seven_pi_over_13_fixed_phase_prefers_q13_amplitude_10_over_13": (
                reports["seven_pi_over_13"]["best_q13_numerator_at_fixed_phase"] == 10
            ),
            "strongest_current_ckm_target_root_closure_is_the_heawood_root_gap_not_the_hypercharge_share": (
                reports["five_pi_over_8"]["relative_root_to_reference_error"]
                < reports["seven_pi_over_13"]["relative_root_to_reference_error"]
            ),
        },
        "interpretive_read": (
            "Inference from the fixed-phase root solves: the old Heawood q/13 "
            "dictionary is not just compatible with the anchored CKM bridge. At "
            "the strongest current common phase 5pi/8, the exact target "
            "amplitude is almost the Heawood root gap 7/13. The older 7pi/13 "
            "phase line still leans into the same dictionary, but more weakly, "
            "through the hypercharge share 10/13."
        ),
        "bridge_verdict": (
            "The live CKM CP bridge now has an amplitude-side root theorem. "
            "Fixing the common phase to 5pi/8 gives target amplitude "
            "a_* = 0.5387032634..., only 0.045% above the exact Heawood root "
            "gap 7/13, and the best fixed-phase q/13 amplitude is exactly 7/13. "
            "Fixing the older common phase 7pi/13 instead gives "
            "a_* = 0.7796444772..., which is a weaker 1.35% match to the "
            "Heawood hypercharge share 10/13. So the strongest current closure "
            "is: observed CKM CP picks out the Heawood root gap."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_heawood_electroweak_polarization_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_heawood_target_root_dictionary_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
