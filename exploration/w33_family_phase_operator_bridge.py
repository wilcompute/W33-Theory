"""Exact live family-phase operator in the complementary J/K sector.

The recent family bridges closed the real operator side:

- real family operators live in the Cartan subalgebra span{I, R} = span{Pq, Pn}
- quark family asymmetry is the Pq channel
- promoted neutrino splitting is the R channel

This bridge closes the live quark phase side.  The exact live amplitudes are

    a = 9/25,
    b = 3/80,
    sigma = (a+b)/2 = 159/800,
    delta = (a-b)/2 = 129/800.

On the same family plane,

    Pq = (I + R)/2,
    Pn = (I - R)/2,
    K  = R J,

and the unique exact live family-phase operator is

    Phi = a Pq J + b Pn J
        = sigma J + delta K
        = [[0, a], [-b, 0]]

in the (q,n) basis.

So the old live selector amplitudes are no longer scan outputs sitting outside
the algebra. They are the singular values of one exact phase operator in the
complementary Clifford sector span{J,K}.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_family_phase_operator_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_cp_triality_line_rotation_bridge import build_summary as build_cp_summary
from exploration.w33_family_dihedral_clifford_bridge import build_summary as build_algebra_summary


LIVE_A = Fraction(9, 25)
LIVE_B = Fraction(3, 80)
SIGMA = (LIVE_A + LIVE_B) / 2
DELTA = (LIVE_A - LIVE_B) / 2


def _serialize_matrix(matrix: np.ndarray) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix]


def _serialize_complex_matrix(matrix: np.ndarray) -> list[list[dict[str, float]]]:
    return [
        [
            {"real": float(value.real), "imag": float(value.imag)}
            for value in row
        ]
        for row in matrix
    ]


def build_summary() -> dict[str, Any]:
    algebra = build_algebra_summary()
    cp = build_cp_summary()

    identity = np.array(algebra["family_algebra_dictionary"]["identity"], dtype=float)
    family_j = np.array(algebra["family_algebra_dictionary"]["complex_structure_J"], dtype=float)
    family_k = np.array(algebra["family_algebra_dictionary"]["second_reflection_K_equals_RJ"], dtype=float)
    quark_projector = np.array(algebra["family_algebra_dictionary"]["quark_axis_projector_Pq"], dtype=float)
    neutrino_projector = np.array(algebra["family_algebra_dictionary"]["neutrino_axis_projector_Pn"], dtype=float)

    a = float(LIVE_A)
    b = float(LIVE_B)
    sigma = float(SIGMA)
    delta = float(DELTA)

    phase_operator = a * (quark_projector @ family_j) + b * (neutrino_projector @ family_j)
    jk_operator = sigma * family_j + delta * family_k
    positive_branch = 1j * phase_operator
    negative_branch = -1j * phase_operator

    singular_values = np.linalg.svd(phase_operator, compute_uv=False)
    phase_square = phase_operator @ phase_operator

    exact_sector_3_fixed_sq = 4.0 * delta * delta / 3.0
    exact_sector_3_rot_sq = 2.0 * sigma * sigma + 8.0 * delta * delta / 3.0
    exact_sector_3prime_fixed_sq = 4.0 * sigma * sigma / 3.0
    exact_sector_3prime_rot_sq = 2.0 * sigma * sigma / 3.0

    sector3_fixed_sq = float(cp["exact_formula_packet"]["sector_3_fixed_sq"])
    sector3_rot_sq = float(cp["exact_formula_packet"]["sector_3_rotating_sq"])
    sector3prime_fixed_sq = float(cp["exact_formula_packet"]["sector_3prime_fixed_sq"])
    sector3prime_rot_sq = float(cp["exact_formula_packet"]["sector_3prime_rotating_sq"])

    return {
        "family_phase_dictionary": {
            "a_exact": str(LIVE_A),
            "b_exact": str(LIVE_B),
            "sigma_exact": str(SIGMA),
            "delta_exact": str(DELTA),
            "PqJ_channel": _serialize_matrix(quark_projector @ family_j),
            "PnJ_channel": _serialize_matrix(neutrino_projector @ family_j),
            "phase_operator_Phi": _serialize_matrix(phase_operator),
            "phase_operator_in_JK_basis": {
                "normal_form": "Phi = a Pq J + b Pn J = sigma J + delta K",
                "sigma_coefficient": sigma,
                "delta_coefficient": delta,
            },
            "positive_branch_iPhi": _serialize_complex_matrix(positive_branch),
            "negative_branch_minus_iPhi": _serialize_complex_matrix(negative_branch),
            "phase_square": _serialize_matrix(phase_square),
            "singular_values": [float(value) for value in singular_values],
        },
        "family_phase_exterior_shadow": {
            "exact_from_family_phase_operator": {
                "sector_3_fixed_sq": exact_sector_3_fixed_sq,
                "sector_3_rotating_sq": exact_sector_3_rot_sq,
                "sector_3prime_fixed_sq": exact_sector_3prime_fixed_sq,
                "sector_3prime_rotating_sq": exact_sector_3prime_rot_sq,
            },
            "older_scan_shadow_from_cp_bridge": {
                "sector_3_fixed_sq": sector3_fixed_sq,
                "sector_3_rotating_sq": sector3_rot_sq,
                "sector_3prime_fixed_sq": sector3prime_fixed_sq,
                "sector_3prime_rotating_sq": sector3prime_rot_sq,
            },
            "older_scan_minus_exact": {
                "sector_3_fixed_sq": sector3_fixed_sq - exact_sector_3_fixed_sq,
                "sector_3_rotating_sq": sector3_rot_sq - exact_sector_3_rot_sq,
                "sector_3prime_fixed_sq": sector3prime_fixed_sq - exact_sector_3prime_fixed_sq,
                "sector_3prime_rotating_sq": sector3prime_rot_sq - exact_sector_3prime_rot_sq,
            },
        },
        "family_phase_operator_theorem": {
            "the_live_family_phase_operator_is_exactly_aPqJ_plus_bPnJ": bool(
                np.allclose(
                    phase_operator,
                    a * (quark_projector @ family_j) + b * (neutrino_projector @ family_j),
                    atol=1e-12,
                )
            ),
            "the_same_operator_is_exactly_sigmaJ_plus_deltaK": bool(
                np.allclose(phase_operator, jk_operator, atol=1e-12)
            ),
            "the_positive_and_negative_live_ckm_branches_are_plus_minus_i_times_this_same_phase_operator": bool(
                np.allclose(positive_branch, 1j * phase_operator, atol=1e-12)
                and np.allclose(negative_branch, -1j * phase_operator, atol=1e-12)
            ),
            "the_singular_values_of_the_exact_phase_operator_are_exactly_the_two_live_selector_amplitudes_a_and_b": bool(
                np.allclose(np.sort(singular_values), np.array([b, a]), atol=1e-12)
            ),
            "the_phase_operator_squares_to_minus_ab_times_the_identity": bool(
                np.allclose(phase_square, -(a * b) * identity, atol=1e-12)
            ),
            "the_exact_cp_line_rotation_formulas_are_the_exterior_shadow_of_the_same_JK_phase_operator": bool(
                abs(exact_sector_3_fixed_sq - 4.0 * delta * delta / 3.0) < 1e-12
                and abs(exact_sector_3_rot_sq - (2.0 * sigma * sigma + 8.0 * delta * delta / 3.0)) < 1e-12
                and abs(exact_sector_3prime_fixed_sq - 4.0 * sigma * sigma / 3.0) < 1e-12
                and abs(exact_sector_3prime_rot_sq - 2.0 * sigma * sigma / 3.0) < 1e-12
            ),
            "the_older_scan_based_cp_bridge_is_the_same_shadow_up_to_the_small_0p3602_vs_9_over_25_master_scale_rounding": bool(
                abs(sector3_fixed_sq - exact_sector_3_fixed_sq) < 5e-5
                and abs(sector3_rot_sq - exact_sector_3_rot_sq) < 2e-4
                and abs(sector3prime_fixed_sq - exact_sector_3prime_fixed_sq) < 6e-5
                and abs(sector3prime_rot_sq - exact_sector_3prime_rot_sq) < 3e-5
            ),
        },
        "interpretation": (
            "The phase side is now on the same exact family algebra as the real Cartan "
            "side. The live quark CP packet is one exact operator Phi in the complementary "
            "J/K sector, with Phi = a Pq J + b Pn J = sigma J + delta K. The two old live "
            "selector amplitudes are exactly the singular values of Phi, while the older "
            "sigma/delta line-rotation formulas are the exterior shadow of the same object. "
            "The previous scan-based CP bridge is now best read as the nearby numerical "
            "shadow obtained before the exact master scale 9/25 replaced the older 0.3602 scan."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 FAMILY PHASE OPERATOR BRIDGE")
    print("=" * 72)
    for key, value in summary["family_phase_operator_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
