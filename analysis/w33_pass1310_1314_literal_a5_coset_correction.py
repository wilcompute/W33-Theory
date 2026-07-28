#!/usr/bin/env python3
"""Passes 1310-1314: literal A5 coset action and carrier-separation correction.

This verifier reconstructs W(E6) from the E8 root system, finds the three
432-point A2-triple orbits, restricts to the derived subgroup PSp(4,3),
extracts the A5 point stabilizer, and computes the *literal* A5 orbit and
fixed-point data on PSp(4,3)/A5.

It also installs a fail-closed arithmetic guard against two recent mistakes:
  * (432,4,0,1,1) has Burnside average 43/5, not 9;
  * the Hashimoto packet dimensions 1+201+200+48+30 sum to 480, so they
    cannot be used as a decomposition of the 432-point coset carrier.

Dependency: sympy >= 1.12 (PermutationGroup / Schreier-Sims).
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from typing import Iterable

from sympy.combinatorics import Permutation, PermutationGroup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1310_1314_literal_a5_coset_correction.json"

A5_CLASS_SIZES = {"1A": 1, "2A": 15, "3A": 20, "5A": 12, "5B": 12}
A5_IRREP_DIMS = {"1": 1, "3": 3, "3prime": 3, "4": 4, "5": 5}


def build_e8_roots() -> list[tuple[int, ...]]:
    roots: list[tuple[int, ...]] = []
    for i, j in combinations(range(8), 2):
        for si in (-2, 2):
            for sj in (-2, 2):
                vector = [0] * 8
                vector[i], vector[j] = si, sj
                roots.append(tuple(vector))
    for mask in range(256):
        vector = tuple(1 - 2 * ((mask >> bit) & 1) for bit in range(8))
        if sum(vector) % 4 == 0:
            roots.append(vector)
    assert len(roots) == len(set(roots)) == 240
    assert all(sum(x * x for x in root) == 8 for root in roots)
    return roots


def build_a2_triples(roots: list[tuple[int, ...]]) -> list[tuple[int, int, int]]:
    position = {root: index for index, root in enumerate(roots)}
    triples: list[tuple[int, int, int]] = []
    for i in range(len(roots)):
        for j in range(i + 1, len(roots)):
            third = tuple(-(roots[i][k] + roots[j][k]) for k in range(8))
            h = position.get(third)
            if h is not None and h > j:
                triples.append((i, j, h))
    assert len(triples) == 2240
    return triples


def reflection_on_roots(
    roots: list[tuple[int, ...]], root: tuple[int, ...]
) -> list[int]:
    position = {value: index for index, value in enumerate(roots)}
    images: list[int] = []
    for vector in roots:
        dot = sum(x * y for x, y in zip(vector, root))
        assert dot % 4 == 0
        coefficient = dot // 4
        image = tuple(vector[k] - coefficient * root[k] for k in range(8))
        images.append(position[image])
    return images


def build_we6_action() -> tuple[PermutationGroup, list[tuple[int, int, int]]]:
    roots = build_e8_roots()
    triples = build_a2_triples(roots)
    triple_position = {triple: index for index, triple in enumerate(triples)}
    fixed_a2 = triples[0]
    e6_indices = [
        index
        for index, root in enumerate(roots)
        if all(
            sum(root[k] * roots[a2_index][k] for k in range(8)) == 0
            for a2_index in fixed_a2
        )
    ]
    assert len(e6_indices) == 72

    generators: list[Permutation] = []
    group: PermutationGroup | None = None
    current_order = 1
    for root_index in e6_indices:
        root_permutation = reflection_on_roots(roots, roots[root_index])
        induced = []
        for triple in triples:
            image = tuple(sorted(root_permutation[index] for index in triple))
            induced.append(triple_position[image])
        candidate_generator = Permutation(induced)
        candidate_group = PermutationGroup(generators + [candidate_generator])
        candidate_order = candidate_group.order()
        if candidate_order > current_order:
            generators.append(candidate_generator)
            group = candidate_group
            current_order = candidate_order
            if current_order == 51840:
                break

    assert group is not None
    assert group.order() == 51840
    assert len(generators) == 6
    return group, triples


def subgroup_intersection(
    left: PermutationGroup, right: PermutationGroup
) -> PermutationGroup:
    elements = [element for element in left.generate_schreier_sims() if right.contains(element)]
    return PermutationGroup(elements)


def restricted_orbit_sizes(group: PermutationGroup, carrier: Iterable[int]) -> list[int]:
    carrier_set = set(carrier)
    seen: set[int] = set()
    sizes: list[int] = []
    for point in sorted(carrier_set):
        if point in seen:
            continue
        orbit = set(group.orbit(point))
        assert orbit <= carrier_set
        seen |= orbit
        sizes.append(len(orbit))
    assert seen == carrier_set
    return sorted(sizes)


def classwise_fixed_points(group: PermutationGroup, carrier: Iterable[int]) -> dict[str, int]:
    points = tuple(sorted(carrier))
    by_order: dict[int, set[int]] = {}
    order_counts: Counter[int] = Counter()
    for element in group.generate_schreier_sims():
        order = int(element.order())
        fixed = sum(1 for point in points if element(point) == point)
        order_counts[order] += 1
        by_order.setdefault(order, set()).add(fixed)

    assert order_counts == Counter({1: 1, 2: 15, 3: 20, 5: 24})
    assert all(len(values) == 1 for values in by_order.values())
    result = {
        "1A": next(iter(by_order[1])),
        "2A": next(iter(by_order[2])),
        "3A": next(iter(by_order[3])),
        "5A": next(iter(by_order[5])),
        "5B": next(iter(by_order[5])),
    }
    return result


def burnside_orbits(fixed: dict[str, int]) -> Fraction:
    return Fraction(
        sum(A5_CLASS_SIZES[label] * fixed[label] for label in A5_CLASS_SIZES),
        60,
    )


def a5_character_multiplicities(fixed: dict[str, int]) -> dict[str, int]:
    # Since a rational permutation character has equal multiplicities for the
    # Galois-conjugate 3 and 3' characters, the two 5-class values must enter
    # only through their sum. The formulas below are the A5 character inner
    # products specialized to equal 5A/5B fixed counts.
    assert fixed["5A"] == fixed["5B"]
    f1, f2, f3, f5 = fixed["1A"], fixed["2A"], fixed["3A"], fixed["5A"]
    values = {
        "1": Fraction(f1 + 15 * f2 + 20 * f3 + 24 * f5, 60),
        "3": Fraction(3 * f1 - 15 * f2 + 12 * f5, 60),
        "3prime": Fraction(3 * f1 - 15 * f2 + 12 * f5, 60),
        "4": Fraction(4 * f1 + 20 * f3 - 24 * f5, 60),
        "5": Fraction(5 * f1 + 15 * f2 - 20 * f3, 60),
    }
    assert all(value.denominator == 1 and value >= 0 for value in values.values())
    result = {label: int(value) for label, value in values.items()}
    assert sum(A5_IRREP_DIMS[label] * result[label] for label in result) == f1
    return result


def main() -> dict:
    we6, triples = build_we6_action()
    orbit_sizes = sorted(len(orbit) for orbit in we6.orbits())
    assert orbit_sizes == [1, 1, 27, 27, 27, 27, 27, 27, 240, 270, 270, 432, 432, 432]
    carriers = [set(orbit) for orbit in we6.orbits() if len(orbit) == 432]
    derived = we6.derived_subgroup()
    assert derived.order() == 25920

    carrier_records = []
    for carrier_index, carrier in enumerate(carriers, start=1):
        representative = min(carrier)
        s5 = we6.stabilizer(representative)
        a5 = subgroup_intersection(s5, derived)
        assert s5.order() == 120
        assert a5.order() == 60
        assert len(derived.orbit(representative)) == 432

        fixed = classwise_fixed_points(a5, carrier)
        orbit_profile = restricted_orbit_sizes(a5, carrier)
        multiplicities = a5_character_multiplicities(fixed)
        hecke_dimension = burnside_orbits(fixed)
        restriction_commutant_dimension = sum(value * value for value in multiplicities.values())

        assert fixed == {"1A": 432, "2A": 24, "3A": 36, "5A": 2, "5B": 2}
        assert hecke_dimension == 26
        assert orbit_profile == [1, 1, 5, 5, 5, 5, 5, 5, 10, 10, 10, 10,
                                 20, 20, 20, 20, 20, 20, 20, 20, 20,
                                 30, 30, 30, 30, 60]
        assert multiplicities == {"1": 26, "3": 16, "3prime": 16, "4": 40, "5": 30}
        assert restriction_commutant_dimension == 3688

        carrier_records.append(
            {
                "carrier_index": carrier_index,
                "carrier_size": len(carrier),
                "s5_stabilizer_order": s5.order(),
                "a5_intersection_order": a5.order(),
                "a5_fixed_points": fixed,
                "a5_orbit_count": int(hecke_dimension),
                "a5_orbit_sizes": orbit_profile,
                "a5_permutation_character_multiplicities": multiplicities,
                "restriction_commutant_dimension": restriction_commutant_dimension,
            }
        )

    old_fixed = {"1A": 432, "2A": 4, "3A": 0, "5A": 1, "5B": 1}
    old_burnside = burnside_orbits(old_fixed)
    assert old_burnside == Fraction(43, 5)

    hashimoto_packets = [1, 201, 200, 48, 30]
    assert sum(hashimoto_packets) == 480
    assert sum(hashimoto_packets) != 432

    result = {
        "schema": "w33.pass1310_1314.literal_a5_coset_correction.v1",
        "status": "PASS",
        "scope": "Exact finite permutation-group and character-theory certificate; no physics claim.",
        "construction": {
            "e8_roots": 240,
            "a2_triples": len(triples),
            "we6_order": we6.order(),
            "psp43_order": derived.order(),
            "we6_a2_orbit_sizes": orbit_sizes,
            "number_of_432_carriers": len(carriers),
        },
        "literal_432_carrier_theorem": {
            "all_three_carriers_agree": len({json.dumps(record["a5_fixed_points"], sort_keys=True) for record in carrier_records}) == 1,
            "records": carrier_records,
            "exact_fixed_point_vector": [432, 24, 36, 2, 2],
            "exact_hecke_dimension": 26,
            "exact_restriction": "26*1 + 16*3 + 16*3' + 40*4 + 30*5",
        },
        "corrections": {
            "pass1260_1263_fixed_vector": old_fixed,
            "pass1260_1263_burnside_value": str(old_burnside),
            "pass1260_1263_claimed_value": 9,
            "pass1260_1263_verdict": "FALSE: 43/5 is not an integer and is not 9.",
            "carrier_firewall": {
                "coset_carrier_dimension": 432,
                "hashimoto_packet_dimensions": hashimoto_packets,
                "hashimoto_packet_sum": sum(hashimoto_packets),
                "verdict": "The 480-dimensional Hashimoto packet decomposition cannot be used as a decomposition of the 432-point coset carrier.",
            },
            "pass1264_verdict": "PROVISIONAL CAPACITY TABLE, not an exact restriction table: divisibility/floor bounds do not compute character inner products.",
            "pass1265_verdict": "SCAFFOLD: coordinate matrix units verify M_20 identities tautologically but do not yet include a W(E6) action or AtlasRep basis.",
            "pass1273_1277_verdict": "PROVISIONAL where packet assignments are inferred from dimension fits; exactness requires literal character/projector computation.",
        },
        "checks": {
            "we6_order_51840": we6.order() == 51840,
            "psp_order_25920": derived.order() == 25920,
            "three_432_carriers": len(carriers) == 3,
            "literal_fixed_vector": all(record["a5_fixed_points"] == carrier_records[0]["a5_fixed_points"] for record in carrier_records),
            "literal_orbit_count_26": all(record["a5_orbit_count"] == 26 for record in carrier_records),
            "character_dimension_432": all(
                sum(A5_IRREP_DIMS[label] * record["a5_permutation_character_multiplicities"][label]
                    for label in A5_IRREP_DIMS) == 432
                for record in carrier_records
            ),
            "old_candidate_rejected": old_burnside == Fraction(43, 5),
            "carrier_dimensions_separated": sum(hashimoto_packets) == 480 != 432,
        },
    }
    assert all(result["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1310-1314 literal A5 coset correction PASS")
    print("fixed vector (432,24,36,2,2); Hecke dimension 26")
    return result


if __name__ == "__main__":
    main()
