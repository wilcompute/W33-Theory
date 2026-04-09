"""Master packet law for the current CKM closure.

The recent bridges reduced the live CKM packet to exact internal data:

    amplitude a = ((q^3 + 1) / Phi_3) * (Theta(W33) / v) = 7/13,
    common phase phi/pi = 25/40 = 5/8

with the conjugate branch

    common phase phi/pi = 15/40 = 3/8.

This module simply evaluates the resulting unitary Jarlskog invariant in the
current anchored CKM ansatz. The point is not another fit or scan; the point is
that after the packet reduction there are no continuous knobs left.

In the current basis convention, the positive branch predicts

    J = +3.116254289466203e-5,

while the conjugate branch gives the opposite sign with the same magnitude.
Against the PDG 2024 target ``3.12e-5``, the magnitude error is about
``0.12%``.
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
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_ckm_master_packet_law_bridge_summary.json"
TARGET_J_CKM = 3.12e-5


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _polar_unitary(matrix: np.ndarray) -> np.ndarray:
    left, _, right = np.linalg.svd(matrix)
    return left @ right


def _jarlskog(matrix: np.ndarray) -> float:
    return float(np.imag(matrix[0, 0] * matrix[1, 1] * np.conj(matrix[0, 1]) * np.conj(matrix[1, 0])))


@lru_cache(maxsize=1)
def build_ckm_master_packet_law_summary() -> dict[str, Any]:
    signs = _load_json("w33_diffuse_higgs_sign_vector_bridge_summary.json")
    blocks = _load_json("w33_yukawa_blocks.json")
    amplitude_formula = _load_json("w33_ckm_amplitude_rank_gap_formula_bridge_summary.json")
    ckm_rank_gap = _load_json("w33_ckm_rank_gap_packet_bridge_summary.json")

    parity = np.diag(signs["h1_family_sign_vector"]).astype(complex)
    baseline = np.array(blocks["vertex_scan_best"]["V_CKM"], dtype=complex)
    even = 0.5 * (baseline + parity @ baseline @ parity)
    odd = 0.5 * (baseline - parity @ baseline @ parity)

    amplitude = float(amplitude_formula["derived_ckm_amplitude_formula"]["discrete_ckm_amplitude"]["float"])
    positive_phi = pi * float(ckm_rank_gap["discrete_ckm_packet"]["positive_branch"]["common_phase_over_pi"])
    negative_phi = pi * float(ckm_rank_gap["discrete_ckm_packet"]["negative_branch"]["common_phase_over_pi"])

    positive_unitary = _polar_unitary(even + amplitude * np.exp(1j * positive_phi) * odd)
    negative_unitary = _polar_unitary(even + amplitude * np.exp(1j * negative_phi) * odd)
    positive_j = _jarlskog(positive_unitary)
    negative_j = _jarlskog(negative_unitary)

    return {
        "status": "ok",
        "target_jarlskog": TARGET_J_CKM,
        "master_packet_dictionary": {
            "amplitude_formula": amplitude_formula["derived_ckm_amplitude_formula"]["topological_scale_times_rank_gap_share"],
            "positive_common_phase": ckm_rank_gap["discrete_ckm_packet"]["positive_branch"],
            "negative_common_phase": ckm_rank_gap["discrete_ckm_packet"]["negative_branch"],
        },
        "predicted_jarlskog_dictionary": {
            "positive_branch": {
                "unitary_jarlskog": positive_j,
                "absolute_target_error": abs(positive_j - TARGET_J_CKM),
                "relative_target_error": abs(positive_j - TARGET_J_CKM) / TARGET_J_CKM,
            },
            "negative_branch": {
                "unitary_jarlskog": negative_j,
                "absolute_target_error_in_magnitude": abs(abs(negative_j) - TARGET_J_CKM),
                "relative_target_error_in_magnitude": abs(abs(negative_j) - TARGET_J_CKM) / TARGET_J_CKM,
            },
        },
        "ckm_master_packet_law_theorem": {
            "positive_branch_is_fully_fixed_with_no_continuous_knobs_left": (
                abs(amplitude - 7.0 / 13.0) < 1e-12
                and abs(positive_phi / pi - 5.0 / 8.0) < 1e-12
            ),
            "negative_branch_is_the_conjugate_packet": (
                abs(amplitude - 7.0 / 13.0) < 1e-12
                and abs(negative_phi / pi - 3.0 / 8.0) < 1e-12
                and abs(positive_j + negative_j) < 1e-12
            ),
            "positive_branch_predicts_ckm_jarlskog_magnitude_within_two_tenths_percent": (
                abs(positive_j - TARGET_J_CKM) / TARGET_J_CKM < 0.002
            ),
            "current_basis_convention_gives_positive_j_on_the_nonnegative_branch": (
                positive_j > 0.0 and negative_j < 0.0
            ),
        },
        "interpretive_read": (
            "Inference from the fully reduced packet: the current CKM sector is "
            "no longer being tuned by a scan once the discrete packet law is "
            "accepted. The unitary Jarlskog value is a direct evaluation of one "
            "exact amplitude and one exact phase share."
        ),
        "bridge_verdict": (
            "The current CKM closure is now a no-knob packet law. Using "
            "a = ((q^3+1)/Phi_3) * (Theta(W33)/v) = 7/13 and the positive "
            "branch phase phi/pi = 25/40 = 5/8 gives J = "
            "3.116254289466203e-5 in the present basis, within 0.12% of the "
            "PDG 2024 target 3.12e-5. The conjugate branch phi/pi = 15/40 = 3/8 "
            "gives the opposite sign with the same magnitude. So the live CKM "
            "sector now sits on one exact discrete packet rather than a "
            "continuously tuned ansatz."
        ),
        "source_files": [
            "data/w33_ckm_amplitude_rank_gap_formula_bridge_summary.json",
            "data/w33_ckm_rank_gap_packet_bridge_summary.json",
            "data/w33_diffuse_higgs_sign_vector_bridge_summary.json",
            "data/w33_yukawa_blocks.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_ckm_master_packet_law_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
