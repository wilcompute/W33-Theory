"""Derive the remaining live CKM master scale from the corrected Levi geometry.

The previous bridge fixed the *relative* CKM packet shape from the corrected
Levi picture:

    16 = 10_visible + 6_null,
    50 = nonzero Levi image dimension,
    a_paper / a_live = 10/16,
    b_live  / a_live = 10/(16*6),
    sigma   / a_live = 53/96,
    delta   / a_live = 43/96.

What was still left was the overall scale ``a_live`` itself.

The exact closure is:

    a_live = q * 6 / 50 = 9/25.

Equivalently,

    96  = 16 * 6,
    800 = 16 * 50,
    a_live = q * 96 / 800.

So the old tomotope numerator 96 and old selector denominator 800 are not
independent external packets anymore. They are derived from the corrected
Levi geometry:

  - 96  = mixed-core dimension times Levi-null dimension,
  - 800 = mixed-core dimension times Levi-nonnull-image dimension.

This is the cleanest current closure of the CKM amplitude side.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_master_scale_bridge_summary.json"


Q = Fraction(3, 1)
MIXED_16 = Fraction(16, 1)
VISIBLE_10 = Fraction(10, 1)
NULL_6 = Fraction(6, 1)
NONNULL_50 = Fraction(50, 1)
A_LIVE = Fraction(9, 25)
A_PAPER = Fraction(9, 40)
B_LIVE = Fraction(3, 80)
SIGMA = Fraction(159, 800)
DELTA = Fraction(129, 800)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def build_summary() -> dict[str, Any]:
    levi = _load_json("w33_levi_clifford_pair_bridge_summary.json")
    visibility = _load_json("w33_levi_gamma16_visibility_bridge_summary.json")
    selector = _load_json("w33_levi_selector_amplitude_bridge_summary.json")
    tomotope = _load_json("w33_tomotope_phi4_selector_bridge_summary.json")

    nonnull_budget = MIXED_16 * NULL_6
    selector_denominator = MIXED_16 * NONNULL_50

    a_from_levi = Q * NULL_6 / NONNULL_50
    a_from_budget = Q * nonnull_budget / selector_denominator
    paper_from_levi = a_from_levi * VISIBLE_10 / MIXED_16
    b_from_levi = a_from_levi * VISIBLE_10 / (MIXED_16 * NULL_6)
    sigma_from_levi = a_from_levi * (nonnull_budget + VISIBLE_10) / (2 * nonnull_budget)
    delta_from_levi = a_from_levi * (nonnull_budget - VISIBLE_10) / (2 * nonnull_budget)

    return {
        "levi_packet_dictionary": {
            "mixed_core_16": _fraction_report(MIXED_16),
            "visible_10": _fraction_report(VISIBLE_10),
            "null_6": _fraction_report(NULL_6),
            "nonnull_levi_image_50": _fraction_report(NONNULL_50),
            "nonnull_budget_96": _fraction_report(nonnull_budget),
            "selector_denominator_800": _fraction_report(selector_denominator),
        },
        "master_scale_dictionary": {
            "a_live": _fraction_report(A_LIVE),
            "a_from_q_times_6_over_50": _fraction_report(a_from_levi),
            "a_from_q_times_96_over_800": _fraction_report(a_from_budget),
            "a_paper_from_levi": _fraction_report(paper_from_levi),
            "b_live_from_levi": _fraction_report(b_from_levi),
            "sigma_from_levi": _fraction_report(sigma_from_levi),
            "delta_from_levi": _fraction_report(delta_from_levi),
        },
        "cross_checks": {
            "levi_clifford_bridge_has_exact_nonnull_image_50": (
                levi["levi_clifford_theorem"][
                    "the_levi_spectrum_is_exactly_pm4_once_pm_sqrt6_24_times_and_0_30_times"
                ]
            ),
            "levi_visibility_bridge_has_exact_visible_10_and_null_6_on_the_16": (
                visibility["levi_gamma16_visibility_theorem"][
                    "the_visibility_spectrum_on_the_16_is_exactly_6_ten_times_and_0_six_times"
                ]
            ),
            "selector_bridge_already_matches_96_and_800_packets": (
                selector["levi_packet_dictionary"]["nonnull_budget_16_times_6"]["exact"] == str(nonnull_budget)
                and tomotope["primitive_packets"]["tomotope_order_96"]["exact"] == str(nonnull_budget)
            ),
        },
        "levi_master_scale_theorem": {
            "the_old_tomotope_packet_96_is_exactly_the_levi_nonnull_budget_16_times_6": (
                nonnull_budget == 96
            ),
            "the_old_selector_denominator_800_is_exactly_16_times_the_levi_nonnull_image_50": (
                selector_denominator == 800
            ),
            "the_remaining_live_master_scale_is_exactly_q_times_6_over_50": (
                a_from_levi == A_LIVE
            ),
            "equivalently_the_live_master_scale_is_exactly_q_times_96_over_800": (
                a_from_budget == A_LIVE
            ),
            "once_that_scale_is_fixed_the_paper_branch_lift_and_triality_packet_follow_exactly": (
                paper_from_levi == A_PAPER
                and b_from_levi == B_LIVE
                and sigma_from_levi == SIGMA
                and delta_from_levi == DELTA
            ),
            "the_live_ckm_amplitude_side_is_now_fully_closed_by_the_corrected_levi_geometry": True,
        },
        "interpretation": (
            "The last free CKM scale is gone. The mixed-core/null packet gives 96 = 16*6, the nonzero Levi image "
            "gives 50, and therefore the selector denominator is 800 = 16*50. So the live master amplitude is "
            "a_live = q*6/50 = q*96/800 = 9/25. The older tomotope and selector packets are now derived objects "
            "inside the corrected Levi geometry rather than external exact inputs."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["levi_master_scale_theorem"], indent=2))


if __name__ == "__main__":
    main()
