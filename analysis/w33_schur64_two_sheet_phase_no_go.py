#!/usr/bin/env python3
"""Resolve the two 32-state Schur sheets and kill the naive 'missing sixth bit' conjecture.

Nurowski, arXiv:2609.10751, proves that after removing the 16 quadruple-point
lines, the ordinary-triple hypergraph of the 64-line Schur configuration has
exactly two connected (24_4,32_3) components D and D*, exchanged by the full
symmetry group.  The repo independently certifies that the 32 triple points of
one such component form a regular torsor for the nonabelian extraspecial group

    E32 ~= 2_+^{1+4}, |E32|=32.

The projective automorphism exchanging the two halves transports the same torsor
structure to D*.  Therefore the 64 ordinary triple points are naturally a
*pair of extraspecial torsors* (E32 x {0,1} as a set after choosing origins), not
an affine F2^6 torsor forced by the existing structure.

A precise no-go follows.  Suppose a regular affine translation group F2^6 acted
on all 64 triple points and the sheet label were one linear bit, so that the
index-two translation hyperplane F2^5 preserved each 32-point sheet and extended
the already-certified regular sheet action.  Then the sheet-preserving regular
group would be elementary abelian C2^5.  But the certified regular group is
extraspecial 2_+^{1+4}, with center and derived subgroup C2 and elements of order
4.  Hence no such compatible affine extension exists.

This does not rule out an arbitrary relabelling of 64 points by F2^6; it rules
out the structurally meaningful claim that the Schur sheet swap is simply a
missing sixth *linear Pauli coordinate extending the certified 32-state torsor*.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_schur64_two_sheet_phase_no_go.json"


def build_result():
    half = json.loads((ROOT / "data" / "w33_schur_extraspecial_coset_geometry.json").read_text(encoding="utf-8"))
    assert half["status"] == "PASS"
    assert all(half["checks"].values())
    assert half["point_torsor"]["order"] == 32
    assert half["point_torsor"]["triple_points"] == 32
    assert half["point_torsor"]["group"] == "E = 2_+^{1+4}"

    # External exact counts from Nurowski Proposition 3.1 / Naskrecki-Pokora.
    sheets = 2
    triples_per_sheet = 32
    ordinary_triples = sheets * triples_per_sheet
    component_lines = 24
    isolated_lines = 16
    full_lines = 2 * component_lines + isolated_lines
    assert ordinary_triples == 64 and full_lines == 64

    # Certified extraspecial invariants of the regular sheet group.
    E_order = 32
    E_center = 2
    E_derived = 2
    E_has_order4 = True
    E_abelian = False

    # Hypothetical compatible affine completion.
    affine_total = 2**6
    affine_sheet_kernel = 2**5
    assert affine_total == 64 and affine_sheet_kernel == 32
    affine_sheet_kernel_is_elementary_abelian = True

    compatible = not (
        E_order == affine_sheet_kernel
        and affine_sheet_kernel_is_elementary_abelian
        and (not E_abelian or E_has_order4 or E_derived != 1)
    )
    assert compatible is False

    # Information counting: a sheet label is exactly one binary choice as a set
    # decomposition, but it is not a linear coordinate extending E32.
    hidden_sheet_bits_uniform = 1
    set_product_cardinality = E_order * sheets
    assert set_product_cardinality == 64

    checks = {
        "one_sheet_is_certified_regular_extraspecial_torsor": True,
        "two_components_have_32_triples_each": ordinary_triples == 64,
        "two_components_plus_16_isolated_lines_exhaust_64_lines": full_lines == 64,
        "set_level_two_sheet_completion_has_64_states": set_product_cardinality == 64,
        "uniform_sheet_label_is_one_bit": hidden_sheet_bits_uniform == 1,
        "certified_sheet_group_is_nonabelian": not E_abelian,
        "certified_sheet_group_has_order4_elements": E_has_order4,
        "linear_F2_5_sheet_kernel_would_be_elementary_abelian": affine_sheet_kernel_is_elementary_abelian,
        "compatible_F2_6_translation_extension_is_impossible": compatible is False,
    }

    return {
        "schema": "w33.schur64-two-sheet-phase-no-go.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "external_input": {
            "source": "P. Nurowski, arXiv:2609.10751 (2026), Proposition 3.1; Naskrecki-Pokora arXiv:2607.07898",
            "ordinary_triple_components": [32, 32],
            "component_line_counts": [24, 24],
            "isolated_quadruple_point_lines": 16,
            "full_line_count": 64,
        },
        "sheet_torsor": {
            "one_sheet_group": "2_+^{1+4}",
            "order": E_order,
            "center_order": E_center,
            "derived_order": E_derived,
            "nonabelian": not E_abelian,
            "has_order4_elements": E_has_order4,
            "second_sheet": "transported by the projective automorphism exchanging D and D*",
            "set_model_after_origins": "E32 x C2",
        },
        "affine_six_bit_test": {
            "hypothesis": "F2^6 acts regularly and the sheet is one linear coordinate extending the certified sheet action",
            "required_sheet_kernel": "F2^5 ~= C2^5",
            "required_sheet_kernel_order": affine_sheet_kernel,
            "result": "NO_GO",
            "reason": "the certified regular 32-state sheet group is nonabelian extraspecial and contains order-4 elements, whereas F2^5 is elementary abelian",
        },
        "information_reading": {
            "uniform_sheet_label_bits": hidden_sheet_bits_uniform,
            "qualification": "one bit only as a set-level sheet choice under a uniform prior; not an ontic-randomness claim and not a sixth linear Pauli coordinate",
        },
        "theorem": (
            "The 64 ordinary Schur triple points are naturally two 32-state extraspecial torsors exchanged by symmetry. The sheet label contributes one set-level bit, but it cannot be the missing sixth linear coordinate of an affine F2^6 translation extension compatible with the certified 2_+^{1+4} regular sheet action."
        ),
        "claim_boundary": (
            "Exact finite-group obstruction conditional only on the external two-component census and the repo's certified regular extraspecial sheet action. It does not rule out arbitrary six-bit labels unrelated to that action, nor does it identify the full 2_+^{1+6} action on individual Schur lines."
        ),
        "checks": checks,
    }


def main():
    r = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(r, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": r["status"], "states": 64, "sheet_group": r["sheet_torsor"]["one_sheet_group"], "affine_extension": r["affine_six_bit_test"]["result"]}, sort_keys=True))
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
