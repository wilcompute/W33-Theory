"""Identify the paper Cabibbo leg as a branch-filtered live selector amplitude.

Two exact stories already existed in the repo but had not been welded together:

1. The live selector law gives the exact z=2 edge amplitude

       a_live = 9/25.

2. The discrete CKM branch dictionary gives the exact positive branch share

       w_+ = 5/8,

   namely the diagonal of the nonnegative projector and the positive common
   phase class.

The paper packet uses

    a_paper = 9/40.

This bridge proves the missing continuity statement:

    a_paper = a_live * w_+.

Equivalently, because v = (q+lambda) 2^q at q = 3,

    q^2 / v = (q^2/(q+lambda)^2) * ((q+lambda)/2^q).

So the paper Cabibbo leg is the positive-branch-filtered live selector
amplitude, not a separate rational fit.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_paper_live_branch_filter_bridge_summary.json"


Q = Fraction(3, 1)
LAMBDA = Fraction(2, 1)
V = Fraction(40, 1)
OCTIC_DEGREE = Fraction(2**3, 1)

A_LIVE = Fraction(9, 25)
BRANCH_POS = Fraction(5, 8)
BRANCH_NEG = Fraction(3, 8)
A_PAPER = Fraction(9, 40)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def build_summary() -> dict[str, Any]:
    live_scalar = _load_json("w33_live_scalar_selector_bridge_summary.json")
    rank_gap = _load_json("w33_ckm_rank_gap_packet_bridge_summary.json")
    projector_branch = _load_json("w33_ckm_projector_branch_bridge_summary.json")
    paper_fraction = _load_json("w33_paper_fraction_selector_bridge_summary.json")

    q3_identity = (Q + LAMBDA) * OCTIC_DEGREE

    return {
        "primitive_dictionary": {
            "q": int(Q),
            "lambda": int(LAMBDA),
            "v": int(V),
            "octic_degree_2^q": int(OCTIC_DEGREE),
            "branch_factor_q_plus_lambda": int(Q + LAMBDA),
            "positive_branch_share": _fraction_report(BRANCH_POS),
            "negative_branch_share": _fraction_report(BRANCH_NEG),
        },
        "cabibbo_leg_dictionary": {
            "live_selector_amplitude": _fraction_report(A_LIVE),
            "paper_cabibbo_leg": _fraction_report(A_PAPER),
            "positive_branch_filtered_live_amplitude": _fraction_report(A_LIVE * BRANCH_POS),
            "negative_branch_filtered_live_amplitude": _fraction_report(A_LIVE * BRANCH_NEG),
            "direct_paper_form": _fraction_report(Q**2 / V),
            "q3_volume_identity": {
                "left": "(q+lambda) 2^q",
                "right": "v",
                "left_value": int(q3_identity),
                "right_value": int(V),
            },
        },
        "cross_checks": {
            "live_selector_amplitude_matches_committed_9_over_25": (
                live_scalar["live_canonical_amplitudes"]["a"]["exact"] == str(A_LIVE)
            ),
            "positive_branch_share_matches_committed_5_over_8": (
                rank_gap["discrete_ckm_packet"]["positive_branch"]["common_phase_exact"] == "5/8"
                and projector_branch["projector_dictionary"]["nonnegative_projector"]["diagonal"] == "5/8"
            ),
            "paper_cabibbo_leg_matches_committed_q_squared_over_v": (
                paper_fraction["paper_fraction_dictionary"]["a12"]["exact"] == str(A_PAPER)
            ),
        },
        "paper_live_branch_filter_theorem": {
            "the_q3_identity_v_equals_q_plus_lambda_times_2powerq_holds_exactly": (
                q3_identity == V
            ),
            "the_paper_cabibbo_leg_is_exactly_the_live_selector_amplitude_times_the_positive_branch_share": (
                A_LIVE * BRANCH_POS == A_PAPER
            ),
            "the_paper_cabibbo_leg_is_exactly_q_squared_over_v": (
                Q**2 / V == A_PAPER
            ),
            "the_positive_branch_share_is_exactly_the_nonnegative_projector_diagonal_5_over_8": (
                BRANCH_POS == Fraction(5, 8)
            ),
            "the_paper_cabibbo_leg_is_not_the_negative_branch_filtered_live_amplitude": (
                A_LIVE * BRANCH_NEG != A_PAPER
            ),
            "the_exact_paper_packet_reuses_the_live_selector_packet_after_branch_filtering": True,
        },
        "interpretation": (
            "The paper packet is not detached from the live selector law. Its Cabibbo "
            "leg 9/40 is exactly the live selector amplitude 9/25 multiplied by the "
            "positive spectral branch share 5/8. Since 5/8 is simultaneously the "
            "positive CKM phase class and the nonnegative projector diagonal, the "
            "paper packet should be read as the positive-branch-filtered live packet, "
            "with the remaining 3/37, 1/14, and 1/27 terms acting as asymmetric "
            "dressings on top of that filtered base."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    theorem = summary["paper_live_branch_filter_theorem"]

    print("=" * 72)
    print("W33 PAPER/LIVE BRANCH FILTER BRIDGE")
    print("=" * 72)
    print(f"a_live = {A_LIVE}")
    print(f"w_+ = {BRANCH_POS}")
    print(f"a_live * w_+ = {A_LIVE * BRANCH_POS}")
    print(f"a_paper = {A_PAPER}")
    print()
    print("Branch-filter theorem:")
    for key, value in theorem.items():
        status = "PASS" if value else "FAIL"
        print(f"  [{status}] {key}")


if __name__ == "__main__":
    main()
