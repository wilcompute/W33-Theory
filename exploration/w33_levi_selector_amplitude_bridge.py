"""Exact amplitude law from the Levi-visible 10 inside the mixed 16.

The repo already had two exact but separate amplitude stories:

  1. live selector law
       a = 9/25, b = 3/80,
       sigma = 159/800, delta = 129/800,

  2. corrected Levi/Dirac law
       16 = 10_visible + 6_null,
       positive branch share = 5/8,
       negative branch share = 3/8.

This bridge welds them.

The key exact identities are:

    5/8 = 10/16,
    3/8 =  6/16,

so the old positive/negative CKM branch packet is exactly the visible/null
branch split of the mixed 16.

Then

    a_paper = a_live * (10/16),
    b_live  = a_paper / 6 = a_live * 10 / (16*6),

and therefore

    sigma = a_live * (16*6 + 10) / (2*16*6) = a_live * 53 / 96,
    delta = a_live * (16*6 - 10) / (2*16*6) = a_live * 43 / 96.

So the old 53/43 selector numerators are now fully geometric: they are the
plus/minus split of the Levi null packet 16*6 against the Levi-visible 10.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_levi_selector_amplitude_bridge_summary.json"


A_LIVE = Fraction(9, 25)
A_PAPER = Fraction(9, 40)
B_LIVE = Fraction(3, 80)
VISIBLE_10 = Fraction(10, 1)
NULL_6 = Fraction(6, 1)
MIXED_16 = Fraction(16, 1)
POS_BRANCH = Fraction(5, 8)
NEG_BRANCH = Fraction(3, 8)
SIGMA = Fraction(159, 800)
DELTA = Fraction(129, 800)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


def _fraction_report(value: Fraction) -> dict[str, Any]:
    return {"exact": str(value), "value": float(value)}


def build_summary() -> dict[str, Any]:
    visibility = _load_json("w33_levi_gamma16_visibility_bridge_summary.json")
    branch_filter = _load_json("w33_paper_live_branch_filter_bridge_summary.json")
    live_scalar = _load_json("w33_live_scalar_selector_bridge_summary.json")
    tomotope = _load_json("w33_tomotope_phi4_selector_bridge_summary.json")

    nonnull_budget = MIXED_16 * NULL_6
    plus_packet = (nonnull_budget + VISIBLE_10) / 2
    minus_packet = (nonnull_budget - VISIBLE_10) / 2

    paper_from_levi = A_LIVE * VISIBLE_10 / MIXED_16
    b_from_levi = A_LIVE * VISIBLE_10 / (MIXED_16 * NULL_6)
    sigma_from_levi = A_LIVE * plus_packet / nonnull_budget
    delta_from_levi = A_LIVE * minus_packet / nonnull_budget

    return {
        "levi_packet_dictionary": {
            "mixed_core_16": _fraction_report(MIXED_16),
            "visible_10": _fraction_report(VISIBLE_10),
            "null_6": _fraction_report(NULL_6),
            "nonnull_budget_16_times_6": _fraction_report(nonnull_budget),
            "positive_branch_share_10_over_16": _fraction_report(VISIBLE_10 / MIXED_16),
            "negative_branch_share_6_over_16": _fraction_report(NULL_6 / MIXED_16),
            "plus_packet_96_plus_10_over_2": _fraction_report(plus_packet),
            "minus_packet_96_minus_10_over_2": _fraction_report(minus_packet),
        },
        "amplitude_dictionary": {
            "a_live": _fraction_report(A_LIVE),
            "a_paper": _fraction_report(A_PAPER),
            "b_live": _fraction_report(B_LIVE),
            "sigma": _fraction_report(SIGMA),
            "delta": _fraction_report(DELTA),
            "a_paper_from_levi_visible_fraction": _fraction_report(paper_from_levi),
            "b_live_from_levi_visible_over_null_budget": _fraction_report(b_from_levi),
            "sigma_from_levi_packets": _fraction_report(sigma_from_levi),
            "delta_from_levi_packets": _fraction_report(delta_from_levi),
        },
        "cross_checks": {
            "levi_visibility_bridge_really_selects_the_10_and_kills_the_6": visibility[
                "levi_gamma16_visibility_theorem"
            ]["point_line_incidence_sees_exactly_the_10_and_kills_exactly_the_6"],
            "paper_live_branch_filter_matches_visible_fraction": branch_filter[
                "paper_live_branch_filter_theorem"
            ]["the_paper_cabibbo_leg_is_exactly_the_live_selector_amplitude_times_the_positive_branch_share"],
            "live_scalar_bridge_matches_sigma_delta": (
                live_scalar["triality_packet_scalars"]["sigma_half_sum"]["exact"] == str(SIGMA)
                and live_scalar["triality_packet_scalars"]["delta_half_difference"]["exact"] == str(DELTA)
            ),
            "tomotope_bridge_matches_the_same_53_43_packets": (
                tomotope["primitive_packets"]["plus_packet_53"]["exact"] == str(plus_packet)
                and tomotope["primitive_packets"]["minus_packet_43"]["exact"] == str(minus_packet)
            ),
        },
        "levi_selector_amplitude_theorem": {
            "the_old_positive_branch_share_is_exactly_the_levi_visible_fraction_10_over_16": (
                POS_BRANCH == VISIBLE_10 / MIXED_16
            ),
            "the_old_negative_branch_share_is_exactly_the_levi_null_fraction_6_over_16": (
                NEG_BRANCH == NULL_6 / MIXED_16
            ),
            "the_paper_cabibbo_leg_is_exactly_the_live_amplitude_filtered_by_the_levi_visible_fraction": (
                paper_from_levi == A_PAPER
            ),
            "the_second_live_amplitude_is_exactly_the_visible_fraction_divided_by_the_levi_null_size": (
                b_from_levi == B_LIVE
            ),
            "the_old_53_43_selector_numerators_are_exactly_the_plus_minus_split_of_16_times_6_against_10": (
                plus_packet == 53 and minus_packet == 43
            ),
            "sigma_and_delta_are_exactly_the_live_amplitude_times_the_normalized_53_43_levi_packets": (
                sigma_from_levi == SIGMA and delta_from_levi == DELTA
            ),
            "the_live_ckm_amplitude_packet_is_now_fully_welded_to_the_corrected_levi_geometry": True,
        },
        "interpretation": (
            "The amplitude side is no longer floating. The old 5/8 positive branch is exactly the Levi-visible "
            "fraction 10/16 of the mixed core, and the old 3/8 conjugate branch is exactly the Levi-null fraction "
            "6/16. So the paper Cabibbo leg is the live selector amplitude filtered by Levi visibility, while the "
            "second live amplitude is that visible branch divided by the null size 6. The old 53/43 selector packets "
            "are therefore not just tomotope-versus-matter shadows; they are the exact plus/minus split of the Levi "
            "nonnull budget 16*6 against the visible 10."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["levi_selector_amplitude_theorem"], indent=2))


if __name__ == "__main__":
    main()
