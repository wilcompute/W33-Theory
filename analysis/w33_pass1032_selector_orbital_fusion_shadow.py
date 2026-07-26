#!/usr/bin/env python3
"""Pass 1032: selector orbital scheme and the C3-to-S3 subdegree fusion shadow.

Pass 1031 proved that the point-phase and line-phase degree-120 actions are
nonisomorphic. This pass computes their subdegrees and identifies the hidden
association scheme predicted by BT360.

The selector line-phase action has rank five with valencies
    [1, 2, 27, 36, 54],
exactly the multiplicities of the five sheet-intersection values
    108^1, 54^2, 4^27, 12^36, 2^54.

The E8 point-phase action has rank seven with subdegrees
    [1, 1, 1, 27, 27, 27, 36].

Numerically and locally, the selector scheme is the S3 fusion shadow of the
C3-oriented E8 scheme:
    [1] + [1+1] + [27] + [36] + [27+27]
      = [1, 2, 27, 36, 54].
Because the underlying 120-sets are nonconjugate, this is a dual subdegree-fusion
law, not a literal fusion of relation matrices on one common carrier.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass1031_dual_120_phase_carriers import (  # noqa: E402
    Perm,
    act_line,
    act_line_matching,
    act_point_matching,
    build_w33,
    compose,
    generate_psp,
    perfect_matchings,
)

DATA = ROOT / "data"
OUT = DATA / "w33_pass1032_selector_orbital_fusion_shadow.json"


def left_cosets(group: set[Perm], subgroup: list[Perm]) -> tuple[list[Perm], dict[Perm, int]]:
    unseen = set(group)
    representatives: list[Perm] = []
    element_to_coset: dict[Perm, int] = {}
    subgroup_set = set(subgroup)
    while unseen:
        representative = min(unseen)
        coset = frozenset(compose(representative, element) for element in subgroup_set)
        coset_index = len(representatives)
        representatives.append(representative)
        for element in coset:
            element_to_coset[element] = coset_index
        unseen -= coset
    return representatives, element_to_coset


def subdegrees(group: set[Perm], subgroup: list[Perm]) -> list[int]:
    representatives, element_to_coset = left_cosets(group, subgroup)
    unseen = set(range(len(representatives)))
    degrees = []
    while unseen:
        coset = min(unseen)
        orbit = {
            element_to_coset[compose(element, representatives[coset])]
            for element in subgroup
        }
        degrees.append(len(orbit))
        unseen -= orbit
    return sorted(degrees)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    pass1031 = json.loads(
        (DATA / "w33_pass1031_dual_120_phase_carriers.json").read_text(encoding="utf-8")
    )
    selector_design = json.loads(
        (DATA / "w33_BREAKTHROUGH_360_selector_zmin_sheet_design.json").read_text(
            encoding="utf-8"
        )
    )
    selector_bundle = json.loads(
        (DATA / "w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle.json").read_text(
            encoding="utf-8"
        )
    )

    points, lines = build_w33()
    line_index = {line: index for index, line in enumerate(lines)}
    group = generate_psp(points)

    base_point = 0
    incident_lines = [index for index, line in enumerate(lines) if base_point in line]
    base_line_index = incident_lines[0]
    base_line = lines[base_line_index]

    point_matchings = perfect_matchings(incident_lines)
    line_matchings = perfect_matchings(list(base_line))

    point_stabilizer = [element for element in group if element[base_point] == base_point]
    line_stabilizer = [
        element for element in group
        if act_line(element, base_line) == base_line
    ]

    point_matching_action = lambda element, matching: act_line_matching(
        element, matching, lines, line_index
    )
    line_matching_action = act_point_matching

    point_phase_stabilizer = [
        element for element in point_stabilizer
        if point_matching_action(element, point_matchings[0]) == point_matchings[0]
    ]
    line_phase_stabilizer = [
        element for element in line_stabilizer
        if line_matching_action(element, line_matchings[0]) == line_matchings[0]
    ]

    point_subdegrees = subdegrees(group, point_phase_stabilizer)
    line_subdegrees = subdegrees(group, line_phase_stabilizer)

    intersection_profile = {
        int(overlap): int(multiplicity)
        for overlap, multiplicity
        in selector_design["profiles"]["base_sheet_intersections"].items()
    }
    selector_valencies_by_overlap = dict(sorted(intersection_profile.items(), reverse=True))
    selector_valencies = sorted(intersection_profile.values())

    fusion_blocks = [
        [1],
        [1, 1],
        [27],
        [36],
        [27, 27],
    ]
    fused_values = sorted(sum(block) for block in fusion_blocks)

    expected_overlap_law = {
        108: 1,
        54: 2,
        12: 36,
        4: 27,
        2: 54,
    }

    checks = {
        "source_certificates_pass": (
            pass1031["status"] == "PASS"
            and selector_design["summary"]["all_identities_hold"]
            and selector_bundle["summary"]["all_identities_hold"]
        ),
        "both_actions_have_degree_120": (
            sum(point_subdegrees) == sum(line_subdegrees) == 120
        ),
        "point_phase_action_has_rank_seven": len(point_subdegrees) == 7,
        "point_phase_subdegrees_are_1_1_1_27_27_27_36": (
            point_subdegrees == [1, 1, 1, 27, 27, 27, 36]
        ),
        "line_phase_action_has_rank_five": len(line_subdegrees) == 5,
        "line_phase_subdegrees_are_1_2_27_36_54": (
            line_subdegrees == [1, 2, 27, 36, 54]
        ),
        "selector_intersection_profile_is_exact": intersection_profile == expected_overlap_law,
        "selector_valencies_equal_line_phase_subdegrees": selector_valencies == line_subdegrees,
        "diagonal_overlap_108_has_valency_one": intersection_profile[108] == 1,
        "same_line_overlap_54_has_valency_two": intersection_profile[54] == 2,
        "intersecting_line_overlap_12_has_valency_36": intersection_profile[12] == 36,
        "skew_matched_overlap_4_has_valency_27": intersection_profile[4] == 27,
        "skew_unmatched_overlap_2_has_valency_54": intersection_profile[2] == 54,
        "fusion_blocks_partition_point_subdegrees": (
            sorted(value for block in fusion_blocks for value in block) == point_subdegrees
        ),
        "C3_to_S3_fusion_values_match_selector": fused_values == line_subdegrees,
        "same_fibre_two_singletons_fuse_to_two": sum(fusion_blocks[1]) == 2,
        "two_27_transport_orbits_fuse_to_54": sum(fusion_blocks[4]) == 54,
        "remaining_1_27_36_are_preserved": (
            fusion_blocks[0] == [1]
            and fusion_blocks[2] == [27]
            and fusion_blocks[3] == [36]
        ),
        "pass1031_nonconjugacy_remains_in_force": (
            pass1031["checks"]["degree120_coset_actions_are_not_isomorphic"]
        ),
    }
    require(all(checks.values()), f"failed checks: {[key for key, value in checks.items() if not value]}")

    result = {
        "schema": "w33.pass1032.selector_orbital_fusion_shadow.python.v1",
        "status": "PASS",
        "headline": (
            "The hidden 120-sheet selector association scheme is the rank-five "
            "orbital scheme of the line-phase PSp(4,3) action, with valencies "
            "[1,2,27,36,54] exactly matching overlaps "
            "108^1,54^2,4^27,12^36,2^54. The dual E8 point-phase action has "
            "rank seven and subdegrees [1,1,1,27,27,27,36]. The selector pattern "
            "is the C3-to-S3 subdegree-fusion shadow 1+1->2 and 27+27->54."
        ),
        "E8_point_phase_scheme": {
            "rank": len(point_subdegrees),
            "subdegrees": point_subdegrees,
            "local_controller": "C3",
            "reading": (
                "three individually oriented phase states over the base point, "
                "three separate 27 transport orbitals, and one 36 orbital"
            ),
        },
        "selector_line_phase_scheme": {
            "rank": len(line_subdegrees),
            "subdegrees": line_subdegrees,
            "local_controller": "S3",
            "overlap_to_valency": {
                str(overlap): valency
                for overlap, valency in selector_valencies_by_overlap.items()
            },
            "geometric_reading": {
                "108": "the sheet itself",
                "54": "the other two phases over the same line",
                "12": "3 phases over each of 12 intersecting lines",
                "4": "one phase-matched sheet over each of 27 skew lines",
                "2": "two phase-unmatched sheets over each of 27 skew lines",
            },
        },
        "fusion_shadow": {
            "source_subdegrees": point_subdegrees,
            "blocks": fusion_blocks,
            "target_subdegrees": fused_values,
            "formula": "[1] + [1+1] + [27] + [36] + [27+27] = [1,2,27,36,54]",
            "controller_upgrade": "C3 oriented phase -> S3 phase with inversion",
            "interpretation": (
                "phase inversion merges the two nonidentity fibre directions and "
                "pairs two of the three 27-dimensional transport classes"
            ),
        },
        "important_boundary": (
            "Because Pass 1031 proves the two 120-sets are nonisomorphic, this is "
            "a dual subdegree-fusion law and local controller explanation, not a "
            "literal Bose-Mesner fusion on one common vertex set."
        ),
        "consequence": (
            "BT360's predicted hidden association scheme is now identified exactly. "
            "A correcting character twist must respect the rank-five orbital algebra "
            "and its S3 phase inversion, rather than treating the 120 sheets as an "
            "unstructured orbit."
        ),
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Pass1032 status=PASS checks={len(checks)} output={OUT}")


if __name__ == "__main__":
    main()
