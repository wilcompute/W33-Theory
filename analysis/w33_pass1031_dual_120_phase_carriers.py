#!/usr/bin/env python3
"""Pass 1031: the two degree-120 phase carriers are dual and nonconjugate.

Pass 1028 identified two 120=40*3 carriers:
  * E8 antipodal pairs over W(3,3) points;
  * golden-selector sheets over W(3,3) lines.

This verifier reconstructs PSp(4,3) from symplectic transvections and models each
three-phase fibre as the three perfect matchings of the four incident objects.

The two phase stabilizers both have order 216, hence both coset actions have degree
120, but their orbit profiles are reversed:
  point-phase subgroup: points [1,12,27], lines [4,36];
  line-phase subgroup:  points [4,36], lines [1,12,27].

Therefore the subgroups are not conjugate in PSp(4,3), and the two transitive
degree-120 G-sets are not isomorphic. They are point/line-dual carriers, not one
carrier with two names.
"""

from __future__ import annotations

import json
from collections import deque
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

P = 3
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1031_dual_120_phase_carriers.json"

Vec = tuple[int, int, int, int]
Perm = tuple[int, ...]
Matching = frozenset[frozenset[int]]


def canonical(vector: Iterable[int]) -> Vec:
    values = tuple(int(x) % P for x in vector)
    if values == (0, 0, 0, 0):
        raise ValueError("zero vector")
    for entry in values:
        if entry:
            inverse_value = 1 if entry == 1 else 2
            return tuple((inverse_value * x) % P for x in values)  # type: ignore[return-value]
    raise AssertionError


def omega(left: Vec, right: Vec) -> int:
    return (
        left[0] * right[2] - left[2] * right[0]
        + left[1] * right[3] - left[3] * right[1]
    ) % P


def build_w33() -> tuple[list[Vec], list[tuple[int, int, int, int]]]:
    points = sorted(
        {
            canonical(raw)
            for raw in product(range(P), repeat=4)
            if raw != (0, 0, 0, 0)
        }
    )
    point_index = {point: index for index, point in enumerate(points)}
    edges = [
        (left, right)
        for left, right in combinations(range(len(points)), 2)
        if omega(points[left], points[right]) == 0
    ]
    lines: set[tuple[int, int, int, int]] = set()
    for left, right in edges:
        u, v = points[left], points[right]
        line = set()
        for a, b in product(range(P), repeat=2):
            if a == 0 and b == 0:
                continue
            line.add(
                point_index[
                    canonical(
                        (a * u[coordinate] + b * v[coordinate] for coordinate in range(4))
                    )
                ]
            )
        if len(line) == 4:
            lines.add(tuple(sorted(line)))
    return points, sorted(lines)


def compose(left: Perm, right: Perm) -> Perm:
    """Permutation composition left after right."""
    return tuple(left[index] for index in right)


def inverse(permutation: Perm) -> Perm:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def transvections(points: list[Vec]) -> list[Perm]:
    point_index = {point: index for index, point in enumerate(points)}
    generators = []
    for vector in points:
        image = []
        for point in points:
            coefficient = omega(point, vector)
            moved = tuple(
                (point[coordinate] + coefficient * vector[coordinate]) % P
                for coordinate in range(4)
            )
            image.append(point_index[canonical(moved)])
        generators.append(tuple(image))
    return generators


def generated_group(generators: list[Perm], degree: int = 40) -> set[Perm]:
    identity = tuple(range(degree))
    symmetric_generators = generators + [inverse(generator) for generator in generators]
    group = {identity}
    queue: deque[Perm] = deque([identity])
    while queue:
        element = queue.popleft()
        for generator in symmetric_generators:
            candidate = compose(generator, element)
            if candidate not in group:
                group.add(candidate)
                queue.append(candidate)
    return group


def generate_psp(points: list[Vec]) -> set[Perm]:
    return generated_group(transvections(points), len(points))


def act_line(element: Perm, line: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(element[point] for point in line))


def perfect_matchings(items: list[int]) -> list[Matching]:
    if len(items) != 4:
        raise ValueError("four items required")
    a, b, c, d = items
    return [
        frozenset((frozenset((a, b)), frozenset((c, d)))),
        frozenset((frozenset((a, c)), frozenset((b, d)))),
        frozenset((frozenset((a, d)), frozenset((b, c)))),
    ]


def act_point_matching(element: Perm, matching: Matching) -> Matching:
    return frozenset(
        frozenset(element[point] for point in pair)
        for pair in matching
    )


def act_line_matching(
    element: Perm,
    matching: Matching,
    lines: list[tuple[int, int, int, int]],
    line_index: dict[tuple[int, int, int, int], int],
) -> Matching:
    return frozenset(
        frozenset(line_index[act_line(element, lines[line])] for line in pair)
        for pair in matching
    )


def induced_matching_permutation(
    element: Perm,
    matchings: list[Matching],
    action,
) -> tuple[int, int, int]:
    return tuple(matchings.index(action(element, matching)) for matching in matchings)  # type: ignore[return-value]


def orbit_profile(subgroup: list[Perm], domain: range, action) -> list[int]:
    unseen = set(domain)
    sizes = []
    while unseen:
        representative = min(unseen)
        orbit = {action(element, representative) for element in subgroup}
        sizes.append(len(orbit))
        unseen -= orbit
    return sorted(sizes)


def fixed_objects(subgroup: list[Perm], domain: range, action) -> list[int]:
    return [
        obj for obj in domain
        if all(action(element, obj) == obj for element in subgroup)
    ]


def greedy_generators(group: list[Perm], degree: int = 40) -> list[Perm]:
    identity = tuple(range(degree))
    generators: list[Perm] = []
    generated = {identity}
    for element in sorted(group):
        if element not in generated:
            generators.append(element)
            generated = generated_group(generators, degree)
            if len(generated) == len(group):
                break
    return generators


def commutator(left: Perm, right: Perm) -> Perm:
    return compose(inverse(left), compose(inverse(right), compose(left, right)))


def derived_subgroup_order(group: list[Perm]) -> int:
    generators = greedy_generators(group)
    commutators = {
        commutator(left, right)
        for left in generators
        for right in generators
    }
    normal_generators = set(commutators)
    changed = True
    while changed:
        changed = False
        for element in list(normal_generators):
            for generator in generators:
                conjugate = compose(
                    inverse(generator),
                    compose(element, generator),
                )
                if conjugate not in normal_generators:
                    normal_generators.add(conjugate)
                    changed = True
    return len(generated_group(sorted(normal_generators)))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    fibration = json.loads(
        (DATA / "w33_pass1021_e8_fibration_over_forty.json").read_text(encoding="utf-8")
    )
    primary = json.loads(
        (DATA / "w33_pass1023_chirality_and_phase_halves.json").read_text(encoding="utf-8")
    )
    selector = json.loads(
        (DATA / "w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle.json").read_text(
            encoding="utf-8"
        )
    )
    cohomology = json.loads(
        (DATA / "w33_pass341_selector_extension_cohomology.json").read_text(
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

    point_local_image = {
        induced_matching_permutation(element, point_matchings, point_matching_action)
        for element in point_stabilizer
    }
    line_local_image = {
        induced_matching_permutation(element, line_matchings, line_matching_action)
        for element in line_stabilizer
    }

    point_phase_stabilizer = [
        element for element in point_stabilizer
        if point_matching_action(element, point_matchings[0]) == point_matchings[0]
    ]
    line_phase_stabilizer = [
        element for element in line_stabilizer
        if line_matching_action(element, line_matchings[0]) == line_matchings[0]
    ]

    line_action = lambda element, index: line_index[act_line(element, lines[index])]
    point_action = lambda element, index: element[index]

    point_phase_on_points = orbit_profile(point_phase_stabilizer, range(40), point_action)
    point_phase_on_lines = orbit_profile(point_phase_stabilizer, range(40), line_action)
    line_phase_on_points = orbit_profile(line_phase_stabilizer, range(40), point_action)
    line_phase_on_lines = orbit_profile(line_phase_stabilizer, range(40), line_action)

    point_fixed_points = fixed_objects(point_phase_stabilizer, range(40), point_action)
    point_fixed_lines = fixed_objects(point_phase_stabilizer, range(40), line_action)
    line_fixed_points = fixed_objects(line_phase_stabilizer, range(40), point_action)
    line_fixed_lines = fixed_objects(line_phase_stabilizer, range(40), line_action)

    point_derived_order = derived_subgroup_order(point_stabilizer)
    line_derived_order = derived_subgroup_order(line_stabilizer)

    checks = {
        "all_source_certificates_pass": all(
            artifact["status"] == "PASS"
            for artifact in [fibration, primary, cohomology]
        ) and selector["summary"]["all_identities_hold"],
        "w33_has_40_points_and_40_lines": len(points) == len(lines) == 40,
        "psp_order_is_25920": len(group) == 25920,
        "four_lines_through_base_point": len(incident_lines) == 4,
        "four_points_on_base_line": len(base_line) == 4,
        "three_matchings_on_each_local_four_set": (
            len(point_matchings) == len(line_matchings) == 3
        ),
        "point_and_line_stabilizers_have_order_648": (
            len(point_stabilizer) == len(line_stabilizer) == 648
        ),
        "point_local_phase_image_is_regular_C3": (
            len(point_local_image) == 3
            and all(
                permutation in {(0, 1, 2), (1, 2, 0), (2, 0, 1)}
                for permutation in point_local_image
            )
        ),
        "line_local_phase_image_is_full_S3": len(line_local_image) == 6,
        "point_and_line_phase_stabilizers_have_order_216": (
            len(point_phase_stabilizer) == len(line_phase_stabilizer) == 216
        ),
        "both_coset_actions_have_degree_120": (
            len(group) // len(point_phase_stabilizer)
            == len(group) // len(line_phase_stabilizer)
            == 120
        ),
        "point_phase_orbit_profiles_are_1_12_27_and_4_36": (
            point_phase_on_points == [1, 12, 27]
            and point_phase_on_lines == [4, 36]
        ),
        "line_phase_orbit_profiles_are_dual": (
            line_phase_on_points == [4, 36]
            and line_phase_on_lines == [1, 12, 27]
        ),
        "point_phase_fixes_one_point_and_no_line": (
            len(point_fixed_points) == 1 and not point_fixed_lines
        ),
        "line_phase_fixes_one_line_and_no_point": (
            len(line_fixed_lines) == 1 and not line_fixed_points
        ),
        "phase_stabilizers_are_not_conjugate": point_phase_on_points != line_phase_on_points,
        "degree120_coset_actions_are_not_isomorphic": point_phase_on_points != line_phase_on_points,
        "point_stabilizer_abelianization_has_order_three": point_derived_order == 216,
        "line_stabilizer_derived_subgroup_has_order_324": line_derived_order == 324,
        "E8_pair_carrier_is_point_based": (
            fibration["identification"]["conjugate_to_point_action"]
            and not fibration["identification"]["conjugate_to_line_action"]
        ),
        "E8_residual_phase_is_regular_C3": primary["halves"]["phase"]["monodromy_order"] == 3,
        "selector_carrier_is_line_based_with_three_phases": (
            selector["summary"]["base_line_count"] == 40
            and selector["summary"]["phase_fiber_size"] == 3
        ),
        "selector_local_quotient_is_S3": cohomology["checks"]["selector_local_quotient_is_S3"],
    }
    require(all(checks.values()), f"failed checks: {[key for key, value in checks.items() if not value]}")

    result = {
        "schema": "w33.pass1031.dual_120_phase_carriers.python.v1",
        "status": "PASS",
        "headline": (
            "The E8 antipodal-pair carrier and golden-selector sheet carrier are "
            "dual but inequivalent degree-120 PSp(4,3)-sets. Their stabilizers both "
            "have order 216, yet the point-phase stabilizer has orbit profiles "
            "points [1,12,27], lines [4,36], while the line-phase stabilizer has "
            "the reverse. Hence the stabilizers are nonconjugate and the transitive "
            "coset actions are not isomorphic."
        ),
        "group": {
            "name": "PSp(4,3)",
            "order": len(group),
            "construction": "40 projective symplectic transvections on W(3,3)",
        },
        "point_phase_carrier": {
            "interpretation": "E8 antipodal pairs = 3 phases over each W33 point",
            "base_stabilizer_order": len(point_stabilizer),
            "local_phase_image": "C3 regular",
            "phase_stabilizer_order": len(point_phase_stabilizer),
            "degree": len(group) // len(point_phase_stabilizer),
            "point_orbits": point_phase_on_points,
            "line_orbits": point_phase_on_lines,
            "fixed_points": point_fixed_points,
            "fixed_lines": point_fixed_lines,
            "derived_subgroup_order_of_base_stabilizer": point_derived_order,
        },
        "line_phase_carrier": {
            "interpretation": "golden selector = 3 phases over each W33 line",
            "base_stabilizer_order": len(line_stabilizer),
            "local_phase_image": "S3",
            "phase_stabilizer_order": len(line_phase_stabilizer),
            "degree": len(group) // len(line_phase_stabilizer),
            "point_orbits": line_phase_on_points,
            "line_orbits": line_phase_on_lines,
            "fixed_points": line_fixed_points,
            "fixed_lines": line_fixed_lines,
            "derived_subgroup_order_of_base_stabilizer": line_derived_order,
        },
        "nonconjugacy_certificate": {
            "invariant": "orbit profile on the canonical 40-point action",
            "point_phase_profile": point_phase_on_points,
            "line_phase_profile": line_phase_on_points,
            "conclusion": (
                "the order-216 stabilizers are not conjugate in PSp(4,3); "
                "therefore G/H_point and G/H_line are nonisomorphic transitive 120-sets"
            ),
        },
        "new_structural_reading": {
            "shared": "degree 120, fibre size 3, stabilizer order 216",
            "different": (
                "E8 has a normal C3 phase quotient over a point; the selector has "
                "an S3 local controller over a line"
            ),
            "verdict": (
                "the carriers form a point/line-dual pair separated by the same "
                "non-self-duality already visible at degree 40"
            ),
        },
        "consequence_for_pass1026": (
            "The pending degree-120 conjugacy diagnostic should return false. "
            "The correct crosswalk is duality with nonconjugate block orientation, "
            "not a shared PSp G-set."
        ),
        "boundary": (
            "This identifies the natural finite group actions. It does not supply "
            "an outer duality operator; for q=3 no incidence-preserving point-line "
            "duality exists inside the verified substrate."
        ),
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Pass1031 status=PASS checks={len(checks)} output={OUT}")


if __name__ == "__main__":
    main()
