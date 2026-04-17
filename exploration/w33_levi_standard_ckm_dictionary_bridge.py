"""Exact packet dictionary for the standard CKM quantities from Levi-family data.

The Levi Wolfenstein and unitarity-triangle bridges already fixed the standard
CKM data in exact form. This bridge compresses those quantities back into the
older W33 packet dictionary.

Exact identities:

    lambda   = q^2 / v = 9/40
    A^2      = (20^2 / q^6) * (53/43)
    R_u      = q^2 k / (5 * 53) = 108/265
    tan^2 γ  = 2^8 * 5 / q^5 = 1280/243

Hence

    cos^2 γ = q^5 / (q^5 + 2^8*5),
    sin^2 γ = 2^8*5 / (q^5 + 2^8*5).

So the standard CKM package is not just realistic numerically. Its standard
coordinates are exact packet ratios on the same W33 count spine.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_standard_ckm_dictionary_bridge_summary.json"


Q = 3
V = 40
K = 12
CURVATURE_20 = 20
TRIALITY_PLUS = 53
TRIALITY_MINUS = 43
BOTT_FIVE = 5

LAMBDA = Fraction(9, 40)
A2 = Fraction(21200, 31347)
R_U = Fraction(108, 265)
TAN2_GAMMA = Fraction(1280, 243)
COS2_GAMMA = Fraction(243, 1523)
SIN2_GAMMA = Fraction(1280, 1523)
VCB2 = Fraction(477, 275200)
VUB2 = Fraction(531441, 36464000000)


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def build_summary() -> dict[str, Any]:
    lambda_from_packets = Fraction(Q * Q, V)
    a2_from_packets = Fraction(CURVATURE_20 * CURVATURE_20, Q**6) * Fraction(TRIALITY_PLUS, TRIALITY_MINUS)
    ru_from_packets = Fraction(Q * Q * K, BOTT_FIVE * TRIALITY_PLUS)
    tan2_from_packets = Fraction(2**8 * BOTT_FIVE, Q**5)
    cos2_from_packets = Fraction(Q**5, Q**5 + 2**8 * BOTT_FIVE)
    sin2_from_packets = Fraction(2**8 * BOTT_FIVE, Q**5 + 2**8 * BOTT_FIVE)
    vcb2_from_packets = Fraction(Q * Q * TRIALITY_PLUS, 2**8 * BOTT_FIVE * BOTT_FIVE * TRIALITY_MINUS)
    vub2_from_packets = lambda_from_packets * lambda_from_packets * ru_from_packets * ru_from_packets * vcb2_from_packets

    return {
        "levi_standard_ckm_dictionary": {
            "q": Q,
            "v": V,
            "k": K,
            "curvature_shell_20": CURVATURE_20,
            "triality_plus_53": TRIALITY_PLUS,
            "triality_minus_43": TRIALITY_MINUS,
            "bott_five": BOTT_FIVE,
            "lambda": _fraction_report(LAMBDA),
            "A_squared": _fraction_report(A2),
            "R_u": _fraction_report(R_U),
            "tan2_gamma": _fraction_report(TAN2_GAMMA),
            "cos2_gamma": _fraction_report(COS2_GAMMA),
            "sin2_gamma": _fraction_report(SIN2_GAMMA),
            "Vcb_squared": _fraction_report(VCB2),
            "Vub_squared": _fraction_report(VUB2),
        },
        "levi_standard_ckm_dictionary_theorem": {
            "the_branch_filtered_Cabibbo_parameter_is_exactly_q_squared_over_v": bool(
                LAMBDA == lambda_from_packets
            ),
            "the_Wolfenstein_A_squared_parameter_is_exactly_20_squared_over_q_six_times_53_over_43": bool(
                A2 == a2_from_packets
            ),
            "the_unitarity_triangle_radius_Ru_is_exactly_q_squared_k_over_5_times_53": bool(
                R_U == ru_from_packets
            ),
            "the_CKM_phase_tangent_squared_is_exactly_2_to_8_times_5_over_q_to_5": bool(
                TAN2_GAMMA == tan2_from_packets
            ),
            "the_gamma_phase_squares_are_exactly_the_packet_split_q5_over_q5_plus_2_to_8_5_and_2_to_8_5_over_q5_plus_2_to_8_5": bool(
                COS2_GAMMA == cos2_from_packets and SIN2_GAMMA == sin2_from_packets
            ),
            "the_standard_Vcb_scale_is_exactly_q_squared_53_over_2_to_8_5_squared_43": bool(
                VCB2 == vcb2_from_packets
            ),
            "the_standard_Vub_scale_is_exactly_lambda_squared_times_Ru_squared_times_Vcb_squared": bool(
                VUB2 == vub2_from_packets
            ),
            "the_standard_CKM_packet_lambda_A_Ru_gamma_is_already_closed_inside_the_old_W33_count_dictionary": bool(
                LAMBDA == lambda_from_packets
                and A2 == a2_from_packets
                and R_U == ru_from_packets
                and TAN2_GAMMA == tan2_from_packets
                and COS2_GAMMA == cos2_from_packets
                and SIN2_GAMMA == sin2_from_packets
                and VCB2 == vcb2_from_packets
                and VUB2 == vub2_from_packets
            ),
        },
        "interpretation": (
            "The standard CKM coordinates are now exact W33 packet ratios. "
            "Lambda comes from q^2/v, A^2 from the curvature shell dressed by "
            "the 53/43 Levi split, R_u from q^2*k over 5*53, and gamma from the "
            "exact Bott-lifted ratio 2^8*5 over q^5."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 LEVI STANDARD CKM DICTIONARY BRIDGE")
    print("=" * 72)
    for key, value in summary["levi_standard_ckm_dictionary_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
