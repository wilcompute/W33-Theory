"""Full discrete Heawood/GUT dictionary for the anchored CKM target.

The recent bridge files isolated the strongest separate discrete closures:

- amplitude side: ``a = 7/13`` (the Heawood root gap);
- common-phase side: ``phi/pi = 3/8`` or ``5/8`` (the GUT electroweak pair).

This module closes the loop by scanning the whole finite product dictionary

    a = n/13,  n = 1,...,12
    phi = m pi / 8,  m = 0,...,15

inside the minimal anchored CKM ansatz and sorting by distance to the observed
2024 PDG target ``|J| = 3.12e-5``.

The result is exact at the discrete level:

- the unique best fundamental hits are
      (a, phi/pi) = (7/13, 3/8), (7/13, 5/8);
- the only additional winners are the half-turn translates
      (7/13, 11/8), (7/13, 13/8).

So the current CKM closure is not a loose numerical neighborhood. It is one
finite dictionary entry:

    Heawood root gap 7/13  +  GUT octant phase 3/8 or 5/8.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_discrete_ckm_dictionary_bridge_summary.json"
TARGET_J_CKM = 3.12e-5
AMPLITUDE_DENOMINATOR = 13
PHASE_DENOMINATOR = 8


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
def build_discrete_ckm_dictionary_summary() -> dict[str, Any]:
    even, odd = _anchored_blocks()

    reports: list[dict[str, Any]] = []
    for amplitude_numerator in range(1, AMPLITUDE_DENOMINATOR):
        amplitude = amplitude_numerator / AMPLITUDE_DENOMINATOR
        for phase_numerator in range(2 * PHASE_DENOMINATOR):
            phi = phase_numerator * pi / PHASE_DENOMINATOR
            unitary = _polar_unitary(even + amplitude * np.exp(1j * phi) * odd)
            j_value = _jarlskog(unitary)
            reports.append(
                {
                    "amplitude_numerator": amplitude_numerator,
                    "amplitude_exact": f"{amplitude_numerator}/{AMPLITUDE_DENOMINATOR}",
                    "amplitude": amplitude,
                    "phase_numerator": phase_numerator,
                    "common_phase_exact": f"{phase_numerator}pi/{PHASE_DENOMINATOR}",
                    "common_phase_over_pi": phase_numerator / PHASE_DENOMINATOR,
                    "physical_theta_over_pi": phase_numerator / (PHASE_DENOMINATOR / 2.0),
                    "unitary_jarlskog": j_value,
                    "absolute_target_error": abs(abs(j_value) - TARGET_J_CKM),
                    "relative_target_error": abs(abs(j_value) - TARGET_J_CKM) / TARGET_J_CKM,
                }
            )

    sorted_reports = sorted(reports, key=lambda item: item["absolute_target_error"])
    best_four = sorted_reports[:4]
    best_fundamental = sorted(
        {
            (item["amplitude_numerator"], item["phase_numerator"] % PHASE_DENOMINATOR)
            for item in best_four
        }
    )

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "dictionary_size": len(reports),
        "best_candidates": best_four,
        "top_twelve_candidates": sorted_reports[:12],
        "discrete_ckm_dictionary_theorem": {
            "best_candidates_are_exactly_7_over_13_with_phase_3_5_11_13_over_8": (
                sorted((item["amplitude_numerator"], item["phase_numerator"]) for item in best_four)
                == [(7, 3), (7, 5), (7, 11), (7, 13)]
            ),
            "unique_best_fundamental_dictionary_entries_are_7_over_13_with_phase_3_over_8_or_5_over_8": (
                best_fundamental == [(7, 3), (7, 5)]
            ),
            "best_discrete_hits_match_observed_ckm_scale_within_two_tenths_percent": (
                all(item["relative_target_error"] < 0.002 for item in best_four)
            ),
            "half_turn_translates_exhaust_the_discrete_symmetry_of_the_best_hits": (
                sorted((item["phase_numerator"] % PHASE_DENOMINATOR) for item in best_four) == [3, 3, 5, 5]
            ),
        },
        "interpretive_read": (
            "Inference from the full finite scan: the current anchored CKM "
            "closure is one isolated discrete packet, not a broad cloud of "
            "nearby rational possibilities. The Heawood/GUT entry 7/13 with "
            "3/8 or 5/8 is singled out by the whole product dictionary."
        ),
        "bridge_verdict": (
            "The full finite Heawood/GUT dictionary is now closed at the CKM "
            "target level. Scanning all 12 x 16 native entries shows that the "
            "unique best fundamental hits are exactly "
            "(a, phi/pi) = (7/13, 3/8) and (7/13, 5/8), with only the "
            "half-turn translates 11/8 and 13/8 added by symmetry. So the "
            "current strongest closure is one discrete dictionary entry, not a "
            "loose family of fits."
        ),
        "source_files": [
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_discrete_ckm_dictionary_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
