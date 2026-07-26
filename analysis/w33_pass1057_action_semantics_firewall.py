#!/usr/bin/env python3
"""Pass 1057: fail-closed action-semantics firewall.

A whole-group orbit partition and point-stabilizer subdegrees are not
interchangeable invariants. The code embedding is transitive on the 120
anisotropic classes, yet its point stabilizer has subdegrees
[1,1,1,27,27,27,36].
"""
from __future__ import annotations

import json
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

from w33_pass1054_1059_core import build_axes, build_quotient, build_w33_bundle


class ActionSemanticsError(ValueError):
    pass


def validate_fingerprint(*, degree, whole_group_orbits, point_stabilizer_subdegrees, declared_transitive):
    if sum(whole_group_orbits) != degree:
        raise ActionSemanticsError("whole-group orbit sizes do not sum to the degree")
    if sum(point_stabilizer_subdegrees) != degree:
        raise ActionSemanticsError("subdegrees do not sum to the degree")
    if declared_transitive and sorted(whole_group_orbits) != [degree]:
        raise ActionSemanticsError("a transitive action must have one whole-group orbit")
    if point_stabilizer_subdegrees == whole_group_orbits and declared_transitive and len(whole_group_orbits) > 1:
        raise ActionSemanticsError("subdegrees were supplied as whole-group orbits")


def restrict_action(generators: list[Permutation], domain: list[int]) -> PermutationGroup:
    index = {value: position for position, value in enumerate(domain)}
    return PermutationGroup([Permutation([index[generator(value)] for value in domain]) for generator in generators])


def main() -> dict[str, object]:
    bundle = build_w33_bundle()
    quotient = build_quotient(bundle)
    axes = build_axes(bundle, quotient)

    quotient_orbits = sorted(len(orbit) for orbit in quotient.quotient_group.orbits())
    anisotropic_group = restrict_action(quotient.quotient_generators, quotient.anisotropic)
    anisotropic_orbits = sorted(len(orbit) for orbit in anisotropic_group.orbits())
    anisotropic_subdegrees = sorted(len(orbit) for orbit in anisotropic_group.stabilizer(0).orbits())
    axis_group = PermutationGroup(axes.axis_generators)
    axis_orbits = sorted(len(orbit) for orbit in axis_group.orbits())
    axis_subdegrees = sorted(len(orbit) for orbit in axis_group.stabilizer(0).orbits())

    validate_fingerprint(degree=120, whole_group_orbits=anisotropic_orbits, point_stabilizer_subdegrees=anisotropic_subdegrees, declared_transitive=True)
    misuse_rejected = False
    try:
        validate_fingerprint(degree=120, whole_group_orbits=[1,1,1,27,27,27,36], point_stabilizer_subdegrees=[1,1,1,27,27,27,36], declared_transitive=True)
    except ActionSemanticsError:
        misuse_rejected = True

    point, line = bundle.point_stabilizer, bundle.line_stabilizer
    point_fingerprint = {"order": int(point.order()), "center": int(point.center().order()), "derived": int(point.derived_subgroup().order()), "abelianization": int(point.order() // point.derived_subgroup().order())}
    line_fingerprint = {"order": int(line.order()), "center": int(line.center().order()), "derived": int(line.derived_subgroup().order()), "abelianization": int(line.order() // line.derived_subgroup().order())}

    checks = {
        "quotient_whole_orbits_are_1_120_135": quotient_orbits == [1, 120, 135],
        "code_embedding_is_transitive_on_anisotropic_120": anisotropic_orbits == [120],
        "code_embedding_has_rank7_subdegrees": anisotropic_subdegrees == [1, 1, 1, 27, 27, 27, 36],
        "axis_action_is_same_transitive_rank7_action": axis_orbits == [120] and axis_subdegrees == anisotropic_subdegrees and axis_group.order() == anisotropic_group.order() == 25920,
        "rank7_list_does_not_imply_nontransitive_orbits": anisotropic_orbits != anisotropic_subdegrees,
        "intentional_subdegree_as_orbit_misuse_is_rejected": misuse_rejected,
        "point_line_648_firewall_remains_distinct": point_fingerprint != line_fingerprint,
        "Springer_fingerprint_selects_point_class": point_fingerprint == {"order": 648, "center": 3, "derived": 216, "abelianization": 3},
    }
    if not all(checks.values()):
        raise AssertionError([name for name, passed in checks.items() if not passed])

    return {
        "schema": "w33.pass1057.action_semantics_firewall.v1",
        "status": "PASS",
        "headline": "Pass 1043's embedding inference is not valid: it compared point-stabilizer subdegrees with whole-group orbit sizes. The code embedding itself is transitive on all 120 anisotropic classes and nevertheless has the same rank-7 subdegrees [1,1,1,27,27,27,36].",
        "computed_actions": {"full_256_quotient_orbits": quotient_orbits, "anisotropic_120_whole_group_orbits": anisotropic_orbits, "anisotropic_120_point_stabilizer_subdegrees": anisotropic_subdegrees, "axis_120_whole_group_orbits": axis_orbits, "axis_120_point_stabilizer_subdegrees": axis_subdegrees},
        "firewall_rule": "Embedding identification must compare the same acting group on the same ambient set and the same invariant type. Subdegrees may only be compared with subdegrees; whole-group orbit partitions only with whole-group orbit partitions.",
        "supersession": {"claim": "Pass 1043: Springer realizes the Pass-117 embedding", "status": "OPEN / NOT ESTABLISHED BY THE PASS-1043 TEST", "reason": "the reported [1,1,1,27,27,27,36] list is computed with Stabilizer(Q120,1)"},
        "point_stabilizer_fingerprint": point_fingerprint,
        "line_stabilizer_fingerprint": line_fingerprint,
        "check_count": len(checks),
        "checks": checks,
        "scope": "This retracts an inference, not the raw Pass-1043 computation. The subdegree list is correct; its use as a whole-orbit embedding fingerprint is not. The actual Springer W(E6) embedding remains to be decided using matched whole-orbit or character-fusion data.",
    }


if __name__ == "__main__":
    result = main()
    output = Path(__file__).resolve().parents[1] / "data" / "w33_pass1057_action_semantics_firewall.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "headline": result["headline"], "computed_actions": result["computed_actions"], "check_count": result["check_count"]}, indent=2))
