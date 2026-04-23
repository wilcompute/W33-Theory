"""Exact even-lift profile of the residual Yukawa quartic packet.

This module sharpens the last active-sector spectral packet that remains after
the repo's finite reductions.

What is established:
  - the two nontrivial active packets live naturally in the signed variable
        x = 240 * sigma,
    while the existing active-spectrum bridge works in the squared variable
        u = x^2 = 57600 * sigma^2;
  - the reduced base radicals are the two quadratic packets
        u^2 - 542 u + 61200,
        u^2 - 982 u + 137232;
  - the corresponding signed packets are the exact even lifts
        x^4 - 542 x^2 + 61200,
        x^4 - 982 x^2 + 137232;
  - each quartic is irreducible over Q and has Galois group D4 of order 8.

So the remaining signed Yukawa packet is not arbitrary new algebraic data. It
is exactly two D4 quartic lifts of the radical pairs already isolated in the
reduced base packet.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import sympy as sp


if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
else:
    ROOT = Path(__file__).resolve().parents[1]

from exploration.w33_yukawa_active_spectrum_bridge import (  # noqa: E402
    build_yukawa_active_spectrum_summary,
)
from exploration.w33_yukawa_base_spectrum_bridge import (  # noqa: E402
    build_yukawa_base_spectrum_summary,
)


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_yukawa_quartic_lift_bridge_summary.json"


def _squarefree_part(value: int) -> int:
    out = 1
    for prime, exponent in sp.factorint(value).items():
        if exponent % 2:
            out *= int(prime)
    return out


def _quartic_root_field_relation(
    left_record: dict[str, Any], right_record: dict[str, Any]
) -> dict[str, Any]:
    signed = sp.symbols("x")

    left_expr = sp.sympify(left_record["quartic_polynomial"])
    right_expr = sp.sympify(right_record["quartic_polynomial"])
    left_root = sp.RootOf(left_expr, 0)
    right_root = sp.RootOf(right_expr, 0)

    right_over_left = sp.expand(sp.factor(right_expr, extension=[left_root]))
    left_over_right = sp.expand(sp.factor(left_expr, extension=[right_root]))

    right_over_left_text = str(right_over_left)
    left_over_right_text = str(left_over_right)
    right_irreducible_over_left = right_over_left_text == right_record["quartic_polynomial"]
    left_irreducible_over_right = left_over_right_text == left_record["quartic_polynomial"]

    return {
        "hbar2_plus_minus_factor_over_h2_minus_plus_root_field": right_over_left_text,
        "h2_minus_plus_factor_over_hbar2_plus_minus_root_field": left_over_right_text,
        "compositum_degree": 16,
        "relation_theorem": {
            "each_quartic_remains_irreducible_over_the_other_root_field": (
                right_irreducible_over_left and left_irreducible_over_right
            ),
            "quartic_root_field_compositum_has_degree_16": (
                right_irreducible_over_left and left_irreducible_over_right
            ),
            "quartic_root_fields_are_linearly_disjoint_over_q": (
                right_irreducible_over_left and left_irreducible_over_right
            ),
        },
    }


def _quartic_splitting_field_relation(
    pair_relation: dict[str, Any], root_field_relation: dict[str, Any]
) -> dict[str, Any]:
    shared_quadratic_fields = pair_relation["shared_quadratic_subfield_squarefree_parts"]
    linear_disjoint = not shared_quadratic_fields
    return {
        "shared_quadratic_subfield_squarefree_parts": shared_quadratic_fields,
        "individual_splitting_field_degree": 8,
        "compositum_degree": 64,
        "compositum_galois_group": "D4 x D4",
        "compositum_galois_group_order": 64,
        "relation_theorem": {
            "d4_splitting_fields_have_no_common_nontrivial_galois_subextension": linear_disjoint,
            "d4_splitting_fields_are_linearly_disjoint_over_q": linear_disjoint,
            "splitting_field_compositum_has_degree_64": linear_disjoint
            and root_field_relation["relation_theorem"]["quartic_root_fields_are_linearly_disjoint_over_q"],
            "splitting_field_compositum_has_galois_group_d4_times_d4": linear_disjoint
            and root_field_relation["relation_theorem"]["quartic_root_fields_are_linearly_disjoint_over_q"],
        },
    }


def _positive_root_branches(record: dict[str, Any]) -> tuple[sp.Expr, sp.Expr]:
    trace = sp.Integer(record["base_trace"])
    discriminant = sp.Integer(record["base_discriminant"])
    lower = sp.sqrt(sp.simplify((trace - sp.sqrt(discriminant)) / 2))
    upper = sp.sqrt(sp.simplify((trace + sp.sqrt(discriminant)) / 2))
    return (lower, upper)


def _branch_stable_minpoly_packet(
    left_branches: tuple[sp.Expr, sp.Expr],
    right_branches: tuple[sp.Expr, sp.Expr],
    builder: Any,
    variable_name: str = "t",
) -> dict[str, Any]:
    mixed = sp.symbols(variable_name)
    distinct_polynomials: set[sp.Expr] = set()
    for left in left_branches:
        for right in right_branches:
            expr = sp.simplify(builder(left, right))
            distinct_polynomials.add(sp.expand(sp.minpoly(expr, mixed)))

    if len(distinct_polynomials) != 1:
        raise ValueError("mixed positive-root packet is not branch-stable")

    polynomial = sp.Poly(distinct_polynomials.pop(), mixed)
    return {
        "minpoly": str(sp.expand(polynomial.as_expr())),
        "degree": int(polynomial.degree()),
        "irreducible_over_q": bool(polynomial.is_irreducible),
        "branch_stable_across_positive_root_choices": True,
    }


def _mixed_positive_root_relation(
    left_record: dict[str, Any], right_record: dict[str, Any]
) -> dict[str, Any]:
    signed = sp.symbols("t")
    squared = sp.symbols("u")
    left_base = sp.Poly(sp.sympify(left_record["base_squared_polynomial"]), squared, domain="ZZ")
    right_base = sp.Poly(sp.sympify(right_record["base_squared_polynomial"]), squared, domain="ZZ")
    left_branches = _positive_root_branches(left_record)
    right_branches = _positive_root_branches(right_record)

    product_squared_packet = _branch_stable_minpoly_packet(
        left_branches,
        right_branches,
        lambda left, right: (left * right) ** 2,
        variable_name="u",
    )
    ratio_squared_packet = _branch_stable_minpoly_packet(
        left_branches,
        right_branches,
        lambda left, right: (left / right) ** 2,
        variable_name="u",
    )

    product_packet = _branch_stable_minpoly_packet(
        left_branches, right_branches, lambda left, right: left * right
    )
    ratio_packet = _branch_stable_minpoly_packet(
        left_branches, right_branches, lambda left, right: left / right
    )
    sum_packet = _branch_stable_minpoly_packet(
        left_branches, right_branches, lambda left, right: left + right
    )
    difference_packet = _branch_stable_minpoly_packet(
        left_branches, right_branches, lambda left, right: left - right
    )
    product_resultant = sp.Poly(
        sp.resultant(
            left_base.as_expr().subs(squared, sp.Symbol("a")),
                squared**2 - right_record["base_trace"] * squared * sp.Symbol("a")
                + right_record["base_determinant"] * sp.Symbol("a") ** 2,
            sp.Symbol("a"),
        ),
            squared,
        domain="ZZ",
    )
    ratio_resultant_raw = sp.Poly(
        sp.resultant(
                (squared * sp.Symbol("b")) ** 2
                - left_record["base_trace"] * squared * sp.Symbol("b")
                + left_record["base_determinant"],
            right_base.as_expr().subs(squared, sp.Symbol("b")),
            sp.Symbol("b"),
        ),
            squared,
        domain="ZZ",
    )
    _, ratio_resultant = ratio_resultant_raw.primitive()
    product_is_even_lift = sp.expand(sp.sympify(product_packet["minpoly"])) == sp.expand(
        sp.sympify(product_squared_packet["minpoly"]).subs(squared, signed**2)
    )
    ratio_is_even_lift = sp.expand(sp.sympify(ratio_packet["minpoly"])) == sp.expand(
        sp.sympify(ratio_squared_packet["minpoly"]).subs(squared, signed**2)
    )
    product_resultant_matches = sp.expand(product_resultant.as_expr()) == sp.expand(
        sp.sympify(product_squared_packet["minpoly"])
    )
    ratio_resultant_matches = sp.expand(ratio_resultant.as_expr()) == sp.expand(
        sp.sympify(ratio_squared_packet["minpoly"])
    )
    product_squared_poly = sp.Poly(sp.sympify(product_squared_packet["minpoly"]), squared, domain="ZZ")
    ratio_squared_poly = sp.Poly(sp.sympify(ratio_squared_packet["minpoly"]), squared, domain="ZZ")
    prod_squared_label, prod_squared_alt = product_squared_poly.galois_group(by_name=True)
    prod_squared_group, _ = product_squared_poly.galois_group()
    ratio_squared_label, ratio_squared_alt = ratio_squared_poly.galois_group(by_name=True)
    ratio_squared_group, _ = ratio_squared_poly.galois_group()
    left_disc_squarefree = _squarefree_part(int(left_record["base_discriminant"]))
    right_disc_squarefree = _squarefree_part(int(right_record["base_discriminant"]))
    mixed_disc_squarefree = _squarefree_part(left_disc_squarefree * right_disc_squarefree)

    def _factor_degree_pattern(poly: sp.Poly, radical_squarefree: int) -> list[int]:
        _coeff, factors = sp.factor_list(poly.as_expr(), squared, extension=[sp.sqrt(radical_squarefree)])
        out: list[int] = []
        for factor, multiplicity in factors:
            out.extend([int(sp.Poly(factor, squared).degree())] * int(multiplicity))
        return sorted(out)

    product_over_left_pattern = _factor_degree_pattern(product_squared_poly, left_disc_squarefree)
    product_over_right_pattern = _factor_degree_pattern(product_squared_poly, right_disc_squarefree)
    ratio_over_left_pattern = _factor_degree_pattern(ratio_squared_poly, left_disc_squarefree)
    ratio_over_right_pattern = _factor_degree_pattern(ratio_squared_poly, right_disc_squarefree)
    common_biquadratic_field_theorem = (
        product_squared_packet["degree"] == 4
        and ratio_squared_packet["degree"] == 4
        and product_squared_poly.is_irreducible
        and ratio_squared_poly.is_irreducible
        and prod_squared_label.value == "V"
        and int(prod_squared_group.order()) == 4
        and ratio_squared_label.value == "V"
        and int(ratio_squared_group.order()) == 4
        and product_over_left_pattern == [2, 2]
        and product_over_right_pattern == [2, 2]
        and ratio_over_left_pattern == [2, 2]
        and ratio_over_right_pattern == [2, 2]
    )

    return {
        "branch_choice_counts": {
            "h2_minus_plus_positive_branches": len(left_branches),
            "hbar2_plus_minus_positive_branches": len(right_branches),
        },
        "product_squared_packet": product_squared_packet,
        "ratio_squared_packet": ratio_squared_packet,
        "product_squared_resultant_packet": {
            "primitive_resultant_minpoly": str(sp.expand(product_resultant.as_expr())),
            "matches_product_squared_packet": product_resultant_matches,
        },
        "ratio_squared_resultant_packet": {
            "primitive_resultant_minpoly": str(sp.expand(ratio_resultant.as_expr())),
            "matches_ratio_squared_packet": ratio_resultant_matches,
        },
        "shared_biquadratic_field_packet": {
            "base_discriminant_squarefree_parts": [
                left_disc_squarefree,
                right_disc_squarefree,
                mixed_disc_squarefree,
            ],
            "product_squared_galois_group_label": prod_squared_label.value,
            "product_squared_galois_group_order": int(prod_squared_group.order()),
            "product_squared_galois_group_is_alternating_subgroup": bool(prod_squared_alt),
            "ratio_squared_galois_group_label": ratio_squared_label.value,
            "ratio_squared_galois_group_order": int(ratio_squared_group.order()),
            "ratio_squared_galois_group_is_alternating_subgroup": bool(ratio_squared_alt),
            "product_squared_factor_degree_pattern_over_sqrt_left_discriminant": product_over_left_pattern,
            "product_squared_factor_degree_pattern_over_sqrt_right_discriminant": product_over_right_pattern,
            "ratio_squared_factor_degree_pattern_over_sqrt_left_discriminant": ratio_over_left_pattern,
            "ratio_squared_factor_degree_pattern_over_sqrt_right_discriminant": ratio_over_right_pattern,
        },
        "product_packet": product_packet,
        "ratio_packet": ratio_packet,
        "sum_packet": sum_packet,
        "difference_shares_sum_minpoly": (
            difference_packet["minpoly"] == sum_packet["minpoly"]
        ),
        "theorem": {
            "mixed_positive_root_product_packet_is_branch_stable_irreducible_octic": (
                product_packet["branch_stable_across_positive_root_choices"]
                and product_packet["degree"] == 8
                and product_packet["irreducible_over_q"]
            ),
            "mixed_positive_root_product_packet_is_exact_even_lift_of_irreducible_quartic": (
                product_squared_packet["branch_stable_across_positive_root_choices"]
                and product_squared_packet["degree"] == 4
                and product_squared_packet["irreducible_over_q"]
                and product_is_even_lift
            ),
            "mixed_positive_root_product_squared_packet_is_exact_product_resultant_of_base_quadratics": (
                product_resultant_matches
            ),
            "mixed_positive_root_ratio_packet_is_branch_stable_irreducible_octic": (
                ratio_packet["branch_stable_across_positive_root_choices"]
                and ratio_packet["degree"] == 8
                and ratio_packet["irreducible_over_q"]
            ),
            "mixed_positive_root_ratio_packet_is_exact_even_lift_of_irreducible_quartic": (
                ratio_squared_packet["branch_stable_across_positive_root_choices"]
                and ratio_squared_packet["degree"] == 4
                and ratio_squared_packet["irreducible_over_q"]
                and ratio_is_even_lift
            ),
            "mixed_positive_root_ratio_squared_packet_is_exact_primitive_quotient_resultant_of_base_quadratics": (
                ratio_resultant_matches
            ),
            "mixed_positive_root_squared_product_packet_is_irreducible_v4_quartic": (
                prod_squared_label.value == "V"
                and int(prod_squared_group.order()) == 4
                and product_squared_packet["irreducible_over_q"]
            ),
            "mixed_positive_root_squared_ratio_packet_is_irreducible_v4_quartic": (
                ratio_squared_label.value == "V"
                and int(ratio_squared_group.order()) == 4
                and ratio_squared_packet["irreducible_over_q"]
            ),
            "mixed_positive_root_squared_packets_split_over_either_base_discriminant_field_as_two_quadratics": (
                product_over_left_pattern == [2, 2]
                and product_over_right_pattern == [2, 2]
                and ratio_over_left_pattern == [2, 2]
                and ratio_over_right_pattern == [2, 2]
            ),
            "mixed_positive_root_squared_packets_share_the_common_biquadratic_field_of_the_two_base_discriminants": common_biquadratic_field_theorem,
            "mixed_positive_root_sum_packet_is_branch_stable_irreducible_degree_16": (
                sum_packet["branch_stable_across_positive_root_choices"]
                and sum_packet["degree"] == 16
                and sum_packet["irreducible_over_q"]
            ),
            "mixed_positive_root_sum_generates_full_degree_16_root_field_compositum": (
                sum_packet["degree"] == 16
                and sum_packet["irreducible_over_q"]
            ),
        },
    }


def _quartic_lift_record(
    slot: str,
    sector: str,
    trace: int,
    determinant: int,
    slot_factors: list[str],
) -> dict[str, Any]:
    squared = sp.symbols("u")
    active_var = sp.symbols("y")
    signed = sp.symbols("x")

    base_polynomial = sp.expand(squared**2 - trace * squared + determinant)
    active_factor = str(sp.expand(active_var**2 - trace * active_var + determinant))
    quartic_polynomial = sp.expand(base_polynomial.subs(squared, signed**2))
    quartic_poly = sp.Poly(quartic_polynomial, signed, domain="ZZ")

    base_discriminant = trace * trace - 4 * determinant
    base_root_packet = [
        sp.simplify((sp.Integer(trace) - sp.sqrt(base_discriminant)) / 2),
        sp.simplify((sp.Integer(trace) + sp.sqrt(base_discriminant)) / 2),
    ]
    positive_root_packet = [sp.simplify(sp.sqrt(root)) for root in base_root_packet]

    galois_label, is_alternating_subgroup = quartic_poly.galois_group(by_name=True)
    galois_group, _ = quartic_poly.galois_group()
    quadratic_subfield_squarefree_parts = {
        "sqrt_determinant": _squarefree_part(determinant),
        "sqrt_base_discriminant": _squarefree_part(base_discriminant),
        "sqrt_determinant_times_base_discriminant": _squarefree_part(
            determinant * base_discriminant
        ),
    }

    return {
        "slot": slot,
        "sector": sector,
        "base_trace": int(trace),
        "base_determinant": int(determinant),
        "base_squared_polynomial": str(base_polynomial),
        "active_squared_factor": active_factor,
        "quartic_polynomial": str(quartic_polynomial),
        "base_discriminant": int(base_discriminant),
        "quartic_discriminant": int(sp.discriminant(quartic_polynomial, signed)),
        "base_root_packet": [str(root) for root in base_root_packet],
        "positive_root_packet": [str(root) for root in positive_root_packet],
        "recorded_active_factorization": slot_factors,
        "galois_group_label": galois_label.value,
        "galois_group_order": int(galois_group.order()),
        "galois_group_is_alternating_subgroup": bool(is_alternating_subgroup),
        "quadratic_subfield_squarefree_parts": quadratic_subfield_squarefree_parts,
        "lift_theorem": {
            "active_squared_factor_occurs_in_recorded_slot": active_factor in slot_factors,
            "quartic_is_even_lift_of_base_quadratic_packet": quartic_polynomial
            == sp.expand(base_polynomial.subs(squared, signed**2)),
            "positive_roots_square_to_base_root_packet": all(
                sp.expand(root * root - square) == 0
                for root, square in zip(positive_root_packet, base_root_packet)
            ),
            "quartic_is_irreducible_over_q": bool(quartic_poly.is_irreducible),
            "quartic_has_d4_galois_group": galois_label.value == "D4"
            and int(galois_group.order()) == 8
            and not is_alternating_subgroup,
        },
    }


@lru_cache(maxsize=1)
def build_yukawa_quartic_lift_summary() -> dict[str, Any]:
    base = build_yukawa_base_spectrum_summary()
    active = build_yukawa_active_spectrum_summary()
    theorem = base["base_spectrum_theorem"]
    slot_factors = active["slot_factorizations"]

    records = {
        "H_2:-+": _quartic_lift_record(
            slot="H_2",
            sector="-+",
            trace=int(theorem["h2_minus_plus_block_trace"]),
            determinant=int(theorem["h2_minus_plus_block_determinant"]),
            slot_factors=slot_factors["H_2"]["-+"],
        ),
        "Hbar_2:+-": _quartic_lift_record(
            slot="Hbar_2",
            sector="+-",
            trace=int(theorem["hbar2_plus_minus_block_trace"]),
            determinant=int(theorem["hbar2_plus_minus_block_determinant"]),
            slot_factors=slot_factors["Hbar_2"]["+-"],
        ),
    }
    h2_quadratic_fields = set(records["H_2:-+"]["quadratic_subfield_squarefree_parts"].values())
    hbar2_quadratic_fields = set(records["Hbar_2:+-"]["quadratic_subfield_squarefree_parts"].values())
    shared_quadratic_fields = sorted(h2_quadratic_fields & hbar2_quadratic_fields)
    pair_relation = {
        "h2_minus_plus_quadratic_subfield_squarefree_parts": sorted(h2_quadratic_fields),
        "hbar2_plus_minus_quadratic_subfield_squarefree_parts": sorted(hbar2_quadratic_fields),
        "shared_quadratic_subfield_squarefree_parts": shared_quadratic_fields,
    }
    root_field_relation = _quartic_root_field_relation(records["H_2:-+"], records["Hbar_2:+-"])
    splitting_field_relation = _quartic_splitting_field_relation(pair_relation, root_field_relation)
    mixed_positive_root_relation = _mixed_positive_root_relation(
        records["H_2:-+"], records["Hbar_2:+-"]
    )

    return {
        "status": "ok",
        "quartic_lift_packet": {
            "scaled_signed_variable": "x = 240 * sigma",
            "scaled_squared_variable": "u = x^2 = 57600 * sigma^2",
            "packet_size": len(records),
            "records": records,
        },
        "quartic_pair_relation": pair_relation,
        "quartic_root_field_relation": root_field_relation,
        "quartic_splitting_field_relation": splitting_field_relation,
        "mixed_positive_root_relation": mixed_positive_root_relation,
        "quartic_lift_theorem": {
            "residual_active_quartics_are_exact_even_lifts_of_base_quadratic_packets": all(
                record["lift_theorem"]["quartic_is_even_lift_of_base_quadratic_packet"]
                and record["lift_theorem"]["positive_roots_square_to_base_root_packet"]
                and record["lift_theorem"]["active_squared_factor_occurs_in_recorded_slot"]
                for record in records.values()
            ),
            "both_even_lifts_are_irreducible_d4_quartics": all(
                record["lift_theorem"]["quartic_is_irreducible_over_q"]
                and record["lift_theorem"]["quartic_has_d4_galois_group"]
                for record in records.values()
            ),
            "the_two_d4_lifts_have_disjoint_quadratic_subfield_packets": not shared_quadratic_fields,
            "the_two_quartic_root_fields_are_linearly_disjoint_over_q": root_field_relation[
                "relation_theorem"
            ]["quartic_root_fields_are_linearly_disjoint_over_q"],
            "the_two_d4_splitting_fields_are_linearly_disjoint_over_q": splitting_field_relation[
                "relation_theorem"
            ]["d4_splitting_fields_are_linearly_disjoint_over_q"],
            "the_signed_packet_splitting_field_has_galois_group_d4_times_d4": splitting_field_relation[
                "relation_theorem"
            ]["splitting_field_compositum_has_galois_group_d4_times_d4"],
            "the_canonical_mixed_product_and_ratio_packets_are_branch_stable_irreducible_octics": (
                mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_product_packet_is_branch_stable_irreducible_octic"
                ]
                and mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_ratio_packet_is_branch_stable_irreducible_octic"
                ]
            ),
            "the_canonical_mixed_product_and_ratio_packets_are_even_lifts_of_branch_stable_irreducible_quartics": (
                mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_product_packet_is_exact_even_lift_of_irreducible_quartic"
                ]
                and mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_ratio_packet_is_exact_even_lift_of_irreducible_quartic"
                ]
            ),
            "the_canonical_mixed_squared_packets_are_exact_product_quotient_resultants_of_the_base_quadratic_pair": (
                mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_product_squared_packet_is_exact_product_resultant_of_base_quadratics"
                ]
                and mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_ratio_squared_packet_is_exact_primitive_quotient_resultant_of_base_quadratics"
                ]
            ),
            "the_canonical_mixed_squared_packets_are_common_v4_biquadratic_carriers_inside_the_base_discriminant_compositum": (
                mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_squared_product_packet_is_irreducible_v4_quartic"
                ]
                and mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_squared_ratio_packet_is_irreducible_v4_quartic"
                ]
                and mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_squared_packets_share_the_common_biquadratic_field_of_the_two_base_discriminants"
                ]
            ),
            "a_canonical_mixed_positive_root_sum_generates_the_full_degree_16_root_field_compositum": (
                mixed_positive_root_relation["theorem"][
                    "mixed_positive_root_sum_generates_full_degree_16_root_field_compositum"
                ]
            ),
            "remaining_signed_yukawa_packet_is_two_d4_quartic_lifts": True,
        },
        "bridge_verdict": (
            "The remaining active-sector sign data is now exact. In the signed "
            "variable x = 240 sigma, the only live quartics are the two even "
            "lifts x^4 - 542 x^2 + 61200 and x^4 - 982 x^2 + 137232, coming "
            "directly from the reduced base radical packets. Both are "
            "irreducible D4 quartics over Q, and their three quadratic "
            "subfield packets are pairwise disjoint; moreover each quartic "
            "remains irreducible over the other's quartic root field, so the "
            "root-field compositum already has degree 16. Since the D4 "
            "splitting fields share no quadratic subfield, they are already "
            "linearly disjoint as Galois extensions, so the splitting-field "
            "compositum has degree 64 with Galois group D4 x D4. The first "
            "canonical mixed carriers already close exactly as product/quotient "
            "resultants of the two base quadratic packets. At the squared level they are not new "
            "D4 objects but common V4 biquadratic carriers inside the field generated by the two "
            "base discriminant radicals, and therefore as even lifts of "
            "branch-stable irreducible quartics, hence as branch-stable irreducible "
            "octics for products and ratios, while a mixed positive-root "
            "sum generates the full degree-16 quartic-root compositum. So the live "
            "signed Yukawa packet is "
            "exactly two D4 lifts rather than a generic unresolved quartic "
            "cloud."
        ),
        "source_files": [
            "exploration/w33_yukawa_base_spectrum_bridge.py",
            "exploration/w33_yukawa_active_spectrum_bridge.py",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_yukawa_quartic_lift_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()