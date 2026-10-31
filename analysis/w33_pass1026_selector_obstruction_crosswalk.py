#!/usr/bin/env python3
"""Pass 1026: rigorous crosswalk from the new C6 cocycle to selector artifacts.

This script does not identify objects from shared cardinalities.  It consumes the
GAP permutation-action diagnostic and then classifies each proposed connection as
proved, compatible-but-unproved, or separated by a concrete invariant.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1026_selector_obstruction_crosswalk.json"


def load(name: str) -> dict[str, Any]:
    path = DATA / name
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    p1022 = load("w33_pass1022_equivariant_section_obstruction.json")
    p1023 = load("w33_pass1023_c6_factor_obstruction.json")
    p1025 = load("w33_pass1025_explicit_c6_groupoid_cocycle.json")
    bridge = load("w33_pass1026_selector_c6_bridge_diagnostic.json")
    p341 = load("w33_pass341_selector_extension_cohomology.json")
    golden = load("w33_BREAKTHROUGH_363_golden_failure_single_phase_sheet.json")
    orbit864 = load("w33_BREAKTHROUGH_374_864_orbit_stabilizer_theorem.json")
    chirality = load("bt869_involution_chirality_classes.json")

    require(p1022["status"] == "PASS", "Pass 1022 is not certified")
    require(p1023["status"] == "PASS", "Pass 1023 is not certified")
    require(p1025["status"] == "PASS", "Pass 1025 is not certified")
    require(bridge["status"] == "DIAGNOSTIC_COMPLETE", "Pass 1026 diagnostic missing")
    require(p341["status"] == "PASS", "Pass 341 is not certified")
    require(golden["summary"]["all_identities_hold"], "BT363 identities failed")

    actions_conjugate = bool(bridge["degree120_actions_conjugate"])
    natural_index = bridge["natural_selector_block_system_index"]
    transported_index = bridge["transported_pair_block_system_index"]
    distinct_block_systems = (
        actions_conjugate
        and natural_index not in (None, "fail")
        and transported_index not in (None, "fail")
        and natural_index != transported_index
    )

    if not actions_conjugate:
        gset_verdict = "inequivalent_degree120_actions"
        gset_explanation = (
            "The E8 antipodal-pair action and selector-sheet action are not "
            "conjugate in S120; their equal degree and stabilizer order do not "
            "define an objectwise bridge."
        )
    elif distinct_block_systems:
        gset_verdict = "same_PSp_G_set_distinct_point_line_block_systems"
        gset_explanation = (
            "The 120 E8 antipodal pairs and 120 selector sheets are the same "
            "transitive PSp(4,3)-set up to relabelling, but their natural "
            "three-element fibres are distinct invariant block systems.  One "
            "quotient is point-like and the other line-like."
        )
    elif bridge["transported_pair_blocks_equal_natural_selector_blocks"]:
        gset_verdict = "same_PSp_G_set_same_block_system"
        gset_explanation = (
            "The degree-120 actions and their natural three-element block "
            "systems coincide up to relabelling."
        )
    else:
        gset_verdict = "same_PSp_G_set_block_alignment_unresolved"
        gset_explanation = (
            "The degree-120 actions are conjugate, but the diagnostic did not "
            "align the transported E8 blocks with a certified selector block "
            "system."
        )

    comparisons = [
        {
            "target": "Pass341 signed-E8 Schur class",
            "source_component": "C2 projection of the Pass1025 H1 groupoid cocycle",
            "verdict": "compatible_via_central_double_cover_not_identical_yet",
            "reason": (
                "Both detect the central sign double cover, but Pass1025 lives "
                "in action-groupoid H1 while Pass341 records group-extension H2. "
                "An explicit transgression is required before equality can be stated."
            ),
        },
        {
            "target": "Pass341 selector-sign Bockstein",
            "source_component": "C2 projection",
            "verdict": "separated_by_globalizability_and_degree",
            "reason": (
                "Pass341 proves the selector Bockstein is a local H2 direction "
                "that does not globalize.  The new C2 component is already a "
                "global action-groupoid H1 obstruction on the E8 bundle."
            ),
        },
        {
            "target": "BT363 120 selector sheets",
            "source_component": "120 antipodal pairs and the C3 layer",
            "verdict": gset_verdict,
            "reason": gset_explanation,
        },
        {
            "target": "BT363 single 108-support failure sheet",
            "source_component": "one object of the degree-120 carrier",
            "verdict": (
                "decoration_on_a_bridged_carrier_object"
                if actions_conjugate
                else "shared_count_only_no_object_map"
            ),
            "reason": (
                "The 108 failures are supports attached to one selector-sheet "
                "object.  They are not the C6 cocycle itself.  When the G-sets "
                "are conjugate, the failure sheet can be transported to one E8 "
                "antipodal-pair object, providing a precise pullback target."
            ),
        },
        {
            "target": "BT374 ordered failure multiplicity 864",
            "source_component": "C6 cocycle",
            "verdict": "different_level_D4_decoration",
            "reason": (
                "864=108*8 is the selector support sheet times a D4 ordering "
                "torsor.  It is a decorated multiplicity, not a cohomology class."
            ),
        },
        {
            "target": "BT869 chirality involution split",
            "source_component": "C2 projection",
            "verdict": "parity_compatible_but_carrier_map_absent",
            "reason": (
                "Both use an involutive parity, but BT869 acts on the 81-dimensional "
                "Steinberg carrier with 45+36 or 39+42 splits.  No equivariant map "
                "from the E8 phase bundle to that carrier has yet been constructed."
            ),
        },
    ]

    checks = {
        "c6_factorization_is_240_120_40": p1023["counts"]
        == {"roots": 240, "antipodal_pairs": 120, "omega_triples": 80, "base_points": 40},
        "both_crt_components_nonzero": (
            not p1025["coboundary_tests"]["mod2_coboundary"]
            and not p1025["coboundary_tests"]["mod3_coboundary"]
        ),
        "selector_design_is_40_times_3": golden["summary"]["sheet_count"] == 120,
        "single_failure_sheet_has_108_supports": golden["summary"]["selected_sheet_supports"] == 108,
        "ordered_failures_are_108_times_d4": golden["summary"]["ordered_failures"] == 108 * 8,
        "orbit864_double_cover_stabilizer_is_32": orbit864["orbit_stabilizer_verification"]["double_cover_stab"] == 32,
        "pass341_has_two_global_h2_directions": p341["dimensions"]["H2_PGSp"] == 2,
        "pass341_selector_bockstein_is_not_globalizable": "not globalizable" in p341["restriction_verdict"],
        "chirality_has_45_36_split": any(
            row["steinberg_split"] == [45, 36] for row in chirality["classes"]
        ),
        "no_comparison_claims_unproved_identity": all(
            row["verdict"]
            not in {"identical_cohomology_class", "proved_same_obstruction"}
            for row in comparisons
        ),
    }
    require(all(checks.values()), f"crosswalk checks failed: {[k for k, v in checks.items() if not v]}")

    result = {
        "schema": "w33.pass1026.selector_obstruction_crosswalk.python.v1",
        "status": "PASS",
        "headline": (
            "The selector comparison is now objectwise rather than numerical: "
            f"{gset_explanation} The 108/864 failure data are decorations on that "
            "carrier, while the Pass341 H2 classes remain degree-shifted candidates "
            "requiring an explicit transgression."
        ),
        "degree120_bridge": {
            "verdict": gset_verdict,
            "actions_conjugate": actions_conjugate,
            "size3_block_system_count": bridge["size3_block_system_count"],
            "natural_selector_block_system_index": natural_index,
            "transported_pair_block_system_index": transported_index,
            "quotient_rows": bridge["quotient_rows"],
            "explanation": gset_explanation,
        },
        "comparisons": comparisons,
        "next_exact_map": {
            "name": "transgression_and_failure_support_pullback",
            "requirements": [
                "construct H1(action groupoid,C2) -> H2(stabilizer,C2) transgression",
                "transport the selected 108-support sheet through an explicit S120 conjugator",
                "test whether the support indicator pairs nontrivially with the C3 cocycle",
            ],
        },
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "Pass1026 crosswalk: PASS — "
        f"degree120={gset_verdict}, comparisons={len(comparisons)}"
    )


if __name__ == "__main__":
    main()
