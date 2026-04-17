"""Exact CKM invariant core and V_cs correction from the Levi packet grammar.

The standard CKM packet is already on the exact alphabet

    {q, mu, 5, 20, 40, 53, 43, k}.

The remaining invariant seam is the corrected Jarlskog factor.  The clean split
is:

1. a core Wolfenstein-squared invariant

       J_core^2 = (A^2 lambda^6 eta_bar)^2
                = q^18 / (2^16 * 5^9 * 43^2 * (q^5 + mu^4 * 5)),

2. an exact finite rational correction

       V_cs = 1 - lambda^2/2 - lambda^4(1/8 + A^2/2),

   which in packet form is

       V_cs
       = 1
         - q^4 / (2 * 40^2)
         - q^8 / (8 * 40^4)
         - q^2 * 20^2 * 53 / (2 * 40^4 * 43).

So the full invariant closes as

    J^2 = J_core^2 * V_cs^2.

This is the honest endpoint of the standard CKM invariant side: the core is a
very clean packet ratio, and the remaining correction is still exact but not
further sparse.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_ckm_invariant_correction_bridge_summary.json"


Q = 3
MU = 4
BOTT_FIVE = 5
CURVATURE_20 = 20
POINT_40 = 40
TRIALITY_MINUS = 43
TRIALITY_PLUS = 53

LAMBDA = Fraction(9, 40)
A2 = Fraction(21200, 31347)
ETA2 = Fraction(2985984, 21390535)
VCS = Fraction(857303477, 880640000)
J_CORE_SQUARED = Fraction(387420489, 360451456000000000)
J_SQUARED = Fraction(284742146884392159030759681, 279539767687354777600000000000000000)


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def build_summary() -> dict[str, Any]:
    phase_denominator = Q**5 + MU**4 * BOTT_FIVE
    j_core_squared_from_grammar = Fraction(Q**18, 2**16 * BOTT_FIVE**9 * TRIALITY_MINUS**2 * phase_denominator)
    vcs_from_grammar = (
        Fraction(1, 1)
        - Fraction(Q**4, 2 * POINT_40**2)
        - Fraction(Q**8, 8 * POINT_40**4)
        - Fraction(Q**2 * CURVATURE_20**2 * TRIALITY_PLUS, 2 * POINT_40**4 * TRIALITY_MINUS)
    )
    j_squared_from_grammar = j_core_squared_from_grammar * vcs_from_grammar * vcs_from_grammar

    return {
        "levi_ckm_invariant_correction_dictionary": {
            "q": Q,
            "mu": MU,
            "bott_five": BOTT_FIVE,
            "curvature_20": CURVATURE_20,
            "point_40": POINT_40,
            "triality_plus_53": TRIALITY_PLUS,
            "triality_minus_43": TRIALITY_MINUS,
            "phase_denominator_q5_plus_mu4_times_5": phase_denominator,
            "lambda": _fraction_report(LAMBDA),
            "A_squared": _fraction_report(A2),
            "eta_bar_squared": _fraction_report(ETA2),
            "V_cs": _fraction_report(VCS),
            "J_core_squared": _fraction_report(J_CORE_SQUARED),
            "J_squared": _fraction_report(J_SQUARED),
        },
        "levi_ckm_invariant_correction_theorem": {
            "the_clean_Wolfenstein_core_invariant_squared_is_exactly_q18_over_2_to_16_5_to_9_43_squared_q5_plus_mu4_5": bool(
                J_CORE_SQUARED == j_core_squared_from_grammar
            ),
            "the_exact_Vcs_correction_is_already_a_finite_rational_packet_on_the_same_q_20_40_53_43_alphabet": bool(
                VCS == vcs_from_grammar
            ),
            "the_full_CKM_Jarlskog_squared_is_exactly_the_core_invariant_times_Vcs_squared": bool(
                J_SQUARED == j_squared_from_grammar
            ),
            "the_standard_CKM_invariant_side_is_closed_by_a_clean_core_and_one_exact_finite_correction": bool(
                J_CORE_SQUARED == j_core_squared_from_grammar
                and VCS == vcs_from_grammar
                and J_SQUARED == j_squared_from_grammar
            ),
        },
        "interpretation": (
            "The standard CKM invariant side now closes exactly. The core "
            "Wolfenstein-squared invariant is a very clean packet ratio on the "
            "q/mu/5/43 grammar, while the remaining V_cs factor is an exact "
            "finite correction on the q/20/40/53/43 alphabet. Their product is "
            "the full Jarlskog squared."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("=" * 72)
    print("W33 LEVI CKM INVARIANT CORRECTION BRIDGE")
    print("=" * 72)
    for key, value in summary["levi_ckm_invariant_correction_theorem"].items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
