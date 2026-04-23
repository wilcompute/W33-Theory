#!/usr/bin/env python3
"""Exact Yukawa frontier audit for the W33 bridge stack.

This module packages the strongest conservative exact statement currently
supported by the repo's Yukawa bridge chain.

What is now exact on the finite side:
1. The internal clean-pair recipe is one fixed backbone plus the V4 orbit,
   hence an exact packet of size 5.
2. The universal clean-pair generation algebra has exact linear rank 3.
3. Therefore the live unresolved family packet is exactly 5 x 3 = 15.
4. That same 15-packet matches the old Bott-five tensor triality-three law,
   with zero leakage into the colored nonet.
5. In a canonical flag basis, the finite family side already closes as a
   one-versus-two exact normal form.

What remains open is no longer support or symmetry data. It is a tiny
nonlinear internal spectral packet on the common exact Gram shell.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[1]
EXPLORATION = ROOT / "exploration"
for candidate in (ROOT, EXPLORATION):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from w33_bott_triality_yukawa_frontier_bridge import (  # noqa: E402
    build_summary as build_bott_triality_frontier_summary,
)
from w33_yukawa_point_defect_bridge import (  # noqa: E402
    build_yukawa_point_defect_summary,
)
from w33_yukawa_family_normal_form_bridge import (  # noqa: E402
    build_yukawa_family_normal_form_summary,
)
from w33_yukawa_five_by_three_frontier_bridge import (  # noqa: E402
    build_summary as build_five_by_three_frontier_summary,
)
from w33_yukawa_nonlinear_frontier_bridge import (  # noqa: E402
    build_yukawa_nonlinear_frontier_summary,
)
from w33_yukawa_quartic_lift_bridge import (  # noqa: E402
    build_yukawa_quartic_lift_summary,
)
from w33_yukawa_quadratic_shadow_bridge import (  # noqa: E402
    build_yukawa_quadratic_shadow_summary,
)


@lru_cache(maxsize=1)
def five_by_three_frontier_summary() -> Dict[str, object]:
    return build_five_by_three_frontier_summary()


@lru_cache(maxsize=1)
def bott_triality_frontier_summary() -> Dict[str, object]:
    return build_bott_triality_frontier_summary()


@lru_cache(maxsize=1)
def finite_family_normal_form_summary() -> Dict[str, object]:
    return build_yukawa_family_normal_form_summary()


@lru_cache(maxsize=1)
def quadratic_shadow_frontier_summary() -> Dict[str, object]:
    return build_yukawa_quadratic_shadow_summary()


@lru_cache(maxsize=1)
def generation_point_defect_summary() -> Dict[str, object]:
    return build_yukawa_point_defect_summary()


@lru_cache(maxsize=1)
def quartic_lift_frontier_summary() -> Dict[str, object]:
    return build_yukawa_quartic_lift_summary()


@lru_cache(maxsize=1)
def nonlinear_spectral_frontier_summary() -> Dict[str, object]:
    return build_yukawa_nonlinear_frontier_summary()


@lru_cache(maxsize=1)
def classify_yukawa_frontier() -> Tuple[Dict[str, object], ...]:
    five = five_by_three_frontier_summary()
    bott = bott_triality_frontier_summary()
    family = finite_family_normal_form_summary()
    quadratic = quadratic_shadow_frontier_summary()
    point_defect = generation_point_defect_summary()
    quartic = quartic_lift_frontier_summary()
    nonlinear = nonlinear_spectral_frontier_summary()

    family_graph = family["a2_channel_graph"]
    family_normal_form = family["generation_normal_form"]
    quadratic_packet = quadratic["normal_form_packet"]
    point_packet = point_defect["slot_profiles"]
    quartic_packet = quartic["quartic_lift_packet"]["records"]
    nonlinear_packet = nonlinear["finite_algebraic_packet"]

    return (
        {
            "name": "five_by_three_frontier_packet",
            "support_level": "repo-exact reduction",
            "statement": (
                "The remaining clean-pair Yukawa family is exactly one backbone plus "
                "four V4 twists, tensored with the three-dimensional universal "
                "generation algebra, so the live frontier is a 5x3 packet of size 15."
            ),
            "evidence": {
                "internal_recipe_count": five["internal_recipe_packet"]["internal_recipe_count"],
                "generation_rank": five["generation_algebra_packet"]["linear_rank"],
                "frontier_packet_size": five["frontier_packet_dictionary"]["five_times_three_packet"],
                "matches_v15_count": five["frontier_packet_dictionary"]["matches_v15_count"],
            },
        },
        {
            "name": "bott_triality_packet_factorization",
            "support_level": "repo-exact identification",
            "statement": (
                "The same 15-packet is the old Bott-five tensor the old triality-three "
                "family carrier, with the colored nonet remaining inert."
            ),
            "evidence": {
                "bott_five": bott["product_dictionary"]["bott_five"],
                "triality_three": bott["product_dictionary"]["triality_three"],
                "product": bott["product_dictionary"]["product"],
                "zero_nonet_leakage": bott["triality_packet_origin"]["live_and_paper_zero_nonet_leakage"],
            },
        },
        {
            "name": "finite_family_normal_form",
            "support_level": "repo-exact normal form",
            "statement": (
                "In the exact flag basis (1,1,0), (0,0,1), (1,-1,0), the finite family "
                "side is already an upper-unitriangular one-versus-two packet with a "
                "common square 2E13."
            ),
            "evidence": {
                "distinguished_generation": family_graph["distinguished_generation"],
                "active_quartet": family_graph["active_quartet"],
                "dormant_pair": family_graph["dormant_pair"],
                "common_square": family_normal_form["common_square"],
            },
        },
        {
            "name": "quadratic_shadow_packet",
            "support_level": "repo-exact nonlinear precursor",
            "statement": (
                "The first nonlinear family packet is already generated internally: "
                "the active simple-root packet squares to the central 2E13 channel, "
                "and the universal nilpotents are exactly active packet minus that "
                "quadratic shadow."
            ),
            "evidence": {
                "active_plus": quadratic_packet["active_plus"],
                "active_minus": quadratic_packet["active_minus"],
                "central_shadow": quadratic_packet["central_shadow"],
            },
        },
        {
            "name": "generation_point_defect_packet",
            "support_level": "repo-exact cyclic texture classification",
            "statement": (
                "The distinguished-generation Yukawa texture is exactly one point defect "
                "on top of an isotropic shell in the cyclic qutrit generation carrier."
            ),
            "evidence": {
                "family_basis_in_cycle_model": point_defect["family_basis_in_cycle_model"],
                "h2_point_defect_amplitude": point_packet["H_2"]["canonical_point_defect_profile"]["point_defect_amplitude"],
                "hbar2_point_defect_amplitude": point_packet["Hbar_2"]["canonical_point_defect_profile"]["point_defect_amplitude"],
            },
        },
        {
            "name": "quartic_lift_packet",
            "support_level": "repo-exact signed spectral classification",
            "statement": (
                "The remaining signed Yukawa packet consists of exactly two even quartic lifts "
                "of the reduced radical pairs, and both lifts are irreducible D4 quartics over Q."
            ),
            "evidence": {
                "h2_minus_plus_quartic": quartic_packet["H_2:-+"]["quartic_polynomial"],
                "hbar2_plus_minus_quartic": quartic_packet["Hbar_2:+-"]["quartic_polynomial"],
                "galois_group_label": quartic_packet["H_2:-+"]["galois_group_label"],
                "galois_group_order": quartic_packet["H_2:-+"]["galois_group_order"],
                "shared_quadratic_subfield_squarefree_parts": quartic[
                    "quartic_pair_relation"
                ]["shared_quadratic_subfield_squarefree_parts"],
                "quartic_root_field_compositum_degree": quartic["quartic_root_field_relation"][
                    "compositum_degree"
                ],
                "quartic_splitting_field_compositum_degree": quartic[
                    "quartic_splitting_field_relation"
                ]["compositum_degree"],
                "quartic_splitting_field_galois_group": quartic[
                    "quartic_splitting_field_relation"
                ]["compositum_galois_group"],
                "mixed_product_degree": quartic["mixed_positive_root_relation"][
                    "product_packet"
                ]["degree"],
                "mixed_product_squared_degree": quartic["mixed_positive_root_relation"][
                    "product_squared_packet"
                ]["degree"],
                "mixed_product_squared_matches_resultant": quartic["mixed_positive_root_relation"][
                    "product_squared_resultant_packet"
                ]["matches_product_squared_packet"],
                "mixed_squared_common_biquadratic_field_squarefree_parts": quartic[
                    "mixed_positive_root_relation"
                ]["shared_biquadratic_field_packet"]["base_discriminant_squarefree_parts"],
                "mixed_ratio_degree": quartic["mixed_positive_root_relation"][
                    "ratio_packet"
                ]["degree"],
                "mixed_ratio_squared_degree": quartic["mixed_positive_root_relation"][
                    "ratio_squared_packet"
                ]["degree"],
                "mixed_ratio_squared_matches_resultant": quartic["mixed_positive_root_relation"][
                    "ratio_squared_resultant_packet"
                ]["matches_ratio_squared_packet"],
                "mixed_squared_packets_have_v4_galois_group": quartic[
                    "mixed_positive_root_relation"
                ]["shared_biquadratic_field_packet"]["product_squared_galois_group_order"]
                == 4
                and quartic["mixed_positive_root_relation"]["shared_biquadratic_field_packet"][
                    "ratio_squared_galois_group_order"
                ]
                == 4,
                "mixed_sum_degree": quartic["mixed_positive_root_relation"][
                    "sum_packet"
                ]["degree"],
            },
        },
        {
            "name": "nonlinear_spectral_frontier",
            "support_level": "exact frontier classification",
            "statement": (
                "The remaining open Yukawa content lies above two linearly disjoint exact D4 "
                "splitting fields on the common Gram shell, not in missing support or symmetry data."
            ),
            "evidence": {
                "gram_denominator": nonlinear_packet["gram_denominator"],
                "max_active_factor_degree": nonlinear_packet["max_active_factor_degree"],
                "shared_phi3_mode_numerator": nonlinear_packet["shared_phi3_mode_numerator"],
                "residual_blocks": nonlinear_packet["residual_blocks"],
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    five = five_by_three_frontier_summary()
    bott = bott_triality_frontier_summary()
    family = finite_family_normal_form_summary()
    quadratic = quadratic_shadow_frontier_summary()
    point_defect = generation_point_defect_summary()
    quartic = quartic_lift_frontier_summary()
    nonlinear = nonlinear_spectral_frontier_summary()
    frontier_records = classify_yukawa_frontier()

    return {
        "status": "ok",
        "five_by_three_frontier": five,
        "bott_triality_frontier": bott,
        "family_normal_form": family,
        "quadratic_shadow_frontier": quadratic,
        "generation_point_defect": point_defect,
        "quartic_lift_frontier": quartic,
        "nonlinear_spectral_frontier": nonlinear,
        "frontier_records": frontier_records,
        "frontier_record_names": tuple(record["name"] for record in frontier_records),
        "frontier_packet_summary": {
            "internal_recipe_count": five["internal_recipe_packet"]["internal_recipe_count"],
            "generation_rank": five["generation_algebra_packet"]["linear_rank"],
            "frontier_packet_size": five["frontier_packet_dictionary"]["five_times_three_packet"],
            "bott_triality_product": bott["product_dictionary"]["product"],
            "matches_v15_count": five["frontier_packet_dictionary"]["matches_v15_count"],
        },
        "current_open_problem": {
            "kind": "relation_above_two_linearly_disjoint_d4_splitting_fields",
            "exact_open_problem_is_relation_not_support_or_shape": True,
            "max_active_factor_degree": nonlinear["finite_algebraic_packet"]["max_active_factor_degree"],
            "remaining_base_packet_is_two_radical_pairs_plus_scalar_channels": nonlinear[
                "nonlinear_frontier_theorem"
            ]["remaining_base_packet_is_two_radical_pairs_plus_scalar_channels"],
            "remaining_active_packet_is_finite_algebraic_shell": nonlinear[
                "nonlinear_frontier_theorem"
            ]["remaining_active_packet_is_finite_algebraic_shell"],
            "remaining_signed_packet_is_two_d4_quartic_lifts": quartic["quartic_lift_theorem"][
                "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts"
            ],
            "quadratic_overlap_between_the_two_d4_lifts_is_trivial": not quartic[
                "quartic_pair_relation"
            ]["shared_quadratic_subfield_squarefree_parts"],
            "quartic_root_fields_are_linearly_disjoint_over_q": quartic[
                "quartic_root_field_relation"
            ]["relation_theorem"]["quartic_root_fields_are_linearly_disjoint_over_q"],
            "quartic_root_field_compositum_degree": quartic["quartic_root_field_relation"][
                "compositum_degree"
            ],
            "quartic_splitting_fields_are_linearly_disjoint_over_q": quartic[
                "quartic_splitting_field_relation"
            ]["relation_theorem"]["d4_splitting_fields_are_linearly_disjoint_over_q"],
            "quartic_splitting_field_compositum_degree": quartic[
                "quartic_splitting_field_relation"
            ]["compositum_degree"],
            "quartic_splitting_field_galois_group": quartic[
                "quartic_splitting_field_relation"
            ]["compositum_galois_group"],
            "canonical_mixed_product_degree": quartic["mixed_positive_root_relation"][
                "product_packet"
            ]["degree"],
            "canonical_mixed_product_squared_degree": quartic["mixed_positive_root_relation"][
                "product_squared_packet"
            ]["degree"],
            "canonical_mixed_product_squared_matches_resultant": quartic["mixed_positive_root_relation"][
                "product_squared_resultant_packet"
            ]["matches_product_squared_packet"],
            "canonical_mixed_squared_common_biquadratic_field_squarefree_parts": quartic[
                "mixed_positive_root_relation"
            ]["shared_biquadratic_field_packet"]["base_discriminant_squarefree_parts"],
            "canonical_mixed_ratio_degree": quartic["mixed_positive_root_relation"][
                "ratio_packet"
            ]["degree"],
            "canonical_mixed_ratio_squared_degree": quartic["mixed_positive_root_relation"][
                "ratio_squared_packet"
            ]["degree"],
            "canonical_mixed_ratio_squared_matches_resultant": quartic["mixed_positive_root_relation"][
                "ratio_squared_resultant_packet"
            ]["matches_ratio_squared_packet"],
            "canonical_mixed_squared_packets_have_v4_galois_group": quartic[
                "mixed_positive_root_relation"
            ]["shared_biquadratic_field_packet"]["product_squared_galois_group_order"]
            == 4
            and quartic["mixed_positive_root_relation"]["shared_biquadratic_field_packet"][
                "ratio_squared_galois_group_order"
            ]
            == 4,
            "canonical_mixed_sum_degree": quartic["mixed_positive_root_relation"][
                "sum_packet"
            ]["degree"],
            "canonical_mixed_product_and_ratio_are_branch_stable_irreducible_octics": quartic[
                "quartic_lift_theorem"
            ]["the_canonical_mixed_product_and_ratio_packets_are_branch_stable_irreducible_octics"],
            "canonical_mixed_product_and_ratio_are_even_lifts_of_branch_stable_irreducible_quartics": quartic[
                "quartic_lift_theorem"
            ]["the_canonical_mixed_product_and_ratio_packets_are_even_lifts_of_branch_stable_irreducible_quartics"],
            "canonical_mixed_squared_packets_are_exact_product_quotient_resultants_of_base_quadratics": quartic[
                "quartic_lift_theorem"
            ]["the_canonical_mixed_squared_packets_are_exact_product_quotient_resultants_of_the_base_quadratic_pair"],
            "canonical_mixed_squared_packets_are_common_v4_biquadratic_carriers": quartic[
                "quartic_lift_theorem"
            ]["the_canonical_mixed_squared_packets_are_common_v4_biquadratic_carriers_inside_the_base_discriminant_compositum"],
            "canonical_mixed_sum_generates_quartic_root_field_compositum": quartic[
                "quartic_lift_theorem"
            ]["a_canonical_mixed_positive_root_sum_generates_the_full_degree_16_root_field_compositum"],
        },
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXI_exact_yukawa_frontier_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    packet = payload["frontier_packet_summary"]
    family = payload["family_normal_form"]["a2_channel_graph"]
    quadratic = payload["quadratic_shadow_frontier"]["normal_form_packet"]
    quartic = payload["quartic_lift_frontier"]["quartic_lift_packet"]["records"]
    open_problem = payload["current_open_problem"]

    print("Exact Yukawa frontier audit")
    print(
        "  Frontier packet: "
        f"{packet['internal_recipe_count']} x {packet['generation_rank']} = {packet['frontier_packet_size']}"
    )
    print(
        "  Bott x triality: "
        f"{payload['bott_triality_frontier']['product_dictionary']['bott_five']} x "
        f"{payload['bott_triality_frontier']['product_dictionary']['triality_three']} = "
        f"{packet['bott_triality_product']}"
    )
    print(
        "  Family normal form: "
        f"distinguished_generation={family['distinguished_generation']}, "
        f"dormant_pair={family['dormant_pair']}"
    )
    print(
        "  Nonlinear precursor: "
        f"active_plus^2={quadratic['central_shadow']}"
    )
    print(
        "  Signed packet: "
        f"{quartic['H_2:-+']['quartic_polynomial']}; "
        f"{quartic['Hbar_2:+-']['quartic_polynomial']}"
    )
    print(f"  Remaining open problem: {open_problem['kind']}")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()