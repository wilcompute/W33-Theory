"""Part MCCCXCVI: E6 120 Steiner trihedral pairs.

MCCCXCI reconstructed the 45 zero-sum tritangent triples on each W33-derived
E6 matter chart.  MCCCXCII reconstructed the 36 double-sixes.  This verifier
derives the next classical cubic-surface layer from those finite objects:

    120 Steiner trihedral pairs.

In this finite model a trihedral-pair witness is a triple of double-sixes whose
three double-six sets have pairwise overlap 6, empty triple intersection, and
union size 18.  The complementary 9 weights contain exactly six zero-sum
tritangent triples, and those six triples split uniquely into two trihedra of
three disjoint tritangent triples each.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_e6_45_tritangent_zero_sum_bridge import (  # noqa: E402
    edge_list,
    projected_weights,
    triangle_list,
)
from analysis.w33_spread_double_six_association_scheme import double_six_sets  # noqa: E402


OUTPUT_PATH = ROOT / "PART_MCCCXCVI_E6_120_STEINER_TRIHEDRAL_PAIRS_results.json"


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def contained_tritangent_indices(complement: frozenset[int], tritangents: list[frozenset[int]]) -> list[int]:
    return [index for index, tritangent in enumerate(tritangents) if tritangent <= complement]


def trihedra_partition_pairs(local_tritangents: list[frozenset[int]]) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    """Find partitions of six local tritangents into two disjoint trihedra.

    A trihedron here is three disjoint tritangent triples covering the same
    nine weights.  We return unordered pairs of complementary trihedra, using
    local indices 0..5 for the six tritangents contained in the 9-set.
    """

    trihedra: set[tuple[int, int, int]] = set()
    for candidate in combinations(range(len(local_tritangents)), 3):
        union = frozenset().union(*(local_tritangents[index] for index in candidate))
        if len(union) == 9:
            trihedra.add(tuple(candidate))

    pairs: set[tuple[tuple[int, int, int], tuple[int, int, int]]] = set()
    all_indices = frozenset(range(len(local_tritangents)))
    for trihedron in trihedra:
        complement = tuple(sorted(all_indices - set(trihedron)))
        if complement in trihedra:
            pairs.add(tuple(sorted((trihedron, complement))))
    return sorted(pairs)


def steiner_trihedral_pairs(coordinate: int, sector_key: str) -> dict[str, Any]:
    double_sixes = double_six_sets(coordinate, sector_key)
    weights = projected_weights(coordinate, sector_key)
    tritangents = [frozenset(triangle) for triangle in triangle_list(edge_list(weights), 27)]
    witnesses: list[dict[str, Any]] = []

    for double_six_triple in combinations(range(len(double_sixes)), 3):
        sets = [double_sixes[index] for index in double_six_triple]
        pairwise_overlaps = tuple(sorted(len(left & right) for left, right in combinations(sets, 2)))
        union = frozenset().union(*sets)
        triple_intersection = sets[0] & sets[1] & sets[2]

        if pairwise_overlaps != (6, 6, 6) or len(union) != 18 or triple_intersection:
            continue

        complement = frozenset(range(27)) - union
        tritangent_indices = contained_tritangent_indices(complement, tritangents)
        local_tritangents = [tritangents[index] for index in tritangent_indices]
        partition_pairs = trihedra_partition_pairs(local_tritangents)

        witnesses.append(
            {
                "double_sixes": list(double_six_triple),
                "pairwise_double_six_overlaps": list(pairwise_overlaps),
                "union_size": len(union),
                "triple_intersection_size": len(triple_intersection),
                "complement_9_weights": list(sorted(complement)),
                "contained_tritangents": tritangent_indices,
                "trihedra_partition_pair_count": len(partition_pairs),
                "trihedra_partition_pairs_local_indices": [
                    [list(left), list(right)] for left, right in partition_pairs
                ],
            }
        )

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "weights": weights,
        "double_sixes": double_sixes,
        "tritangents": tritangents,
        "witnesses": witnesses,
    }


def trihedral_pair_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    data = steiner_trihedral_pairs(coordinate, sector_key)
    witnesses = data["witnesses"]
    double_sixes = data["double_sixes"]
    tritangents = data["tritangents"]

    weight_participation = Counter(
        weight for witness in witnesses for weight in witness["complement_9_weights"]
    )
    tritangent_participation = Counter(
        tritangent for witness in witnesses for tritangent in witness["contained_tritangents"]
    )
    double_six_participation = Counter(
        double_six for witness in witnesses for double_six in witness["double_sixes"]
    )
    double_six_pair_participation = Counter(
        tuple(sorted(pair))
        for witness in witnesses
        for pair in combinations(witness["double_sixes"], 2)
    )

    checks = {
        "trihedral_pair_count_is_120": len(witnesses) == 120,
        "every_witness_uses_three_double_sixes": Counter(len(witness["double_sixes"]) for witness in witnesses)
        == {3: 120},
        "pairwise_double_six_overlaps_are_all_6": Counter(
            tuple(witness["pairwise_double_six_overlaps"]) for witness in witnesses
        )
        == {(6, 6, 6): 120},
        "union_size_is_18_and_complement_size_is_9": Counter(witness["union_size"] for witness in witnesses)
        == {18: 120}
        and Counter(len(witness["complement_9_weights"]) for witness in witnesses) == {9: 120},
        "triple_intersection_is_empty": Counter(witness["triple_intersection_size"] for witness in witnesses)
        == {0: 120},
        "each_complement_contains_six_tritangents": Counter(
            len(witness["contained_tritangents"]) for witness in witnesses
        )
        == {6: 120},
        "each_complement_has_unique_trihedral_pair_partition": Counter(
            witness["trihedra_partition_pair_count"] for witness in witnesses
        )
        == {1: 120},
        "each_weight_lies_in_40_trihedral_pairs": weight_participation == {weight: 40 for weight in range(27)},
        "each_tritangent_lies_in_16_trihedral_pairs": tritangent_participation
        == {tritangent: 16 for tritangent in range(len(tritangents))},
        "each_double_six_lies_in_10_trihedral_pairs": double_six_participation
        == {double_six: 10 for double_six in range(len(double_sixes))},
        "each_overlap_6_double_six_pair_lies_in_one_trihedral_pair": Counter(
            double_six_pair_participation.values()
        )
        == {1: 360},
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "trihedral_pair_count": len(witnesses),
        "double_six_triple_size_profile": counter_to_json(
            Counter(len(witness["double_sixes"]) for witness in witnesses)
        ),
        "pairwise_double_six_overlap_profile": counter_to_json(
            Counter(tuple(witness["pairwise_double_six_overlaps"]) for witness in witnesses)
        ),
        "union_size_profile": counter_to_json(Counter(witness["union_size"] for witness in witnesses)),
        "complement_size_profile": counter_to_json(
            Counter(len(witness["complement_9_weights"]) for witness in witnesses)
        ),
        "triple_intersection_size_profile": counter_to_json(
            Counter(witness["triple_intersection_size"] for witness in witnesses)
        ),
        "contained_tritangent_count_profile": counter_to_json(
            Counter(len(witness["contained_tritangents"]) for witness in witnesses)
        ),
        "trihedra_partition_pair_count_profile": counter_to_json(
            Counter(witness["trihedra_partition_pair_count"] for witness in witnesses)
        ),
        "weight_participation_profile": counter_to_json(Counter(weight_participation.values())),
        "tritangent_participation_profile": counter_to_json(Counter(tritangent_participation.values())),
        "double_six_participation_profile": counter_to_json(Counter(double_six_participation.values())),
        "double_six_pair_participation_profile": counter_to_json(
            Counter(double_six_pair_participation.values())
        ),
        "sample_witnesses": witnesses[:6],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def e6_120_steiner_trihedral_pairs_packet() -> dict[str, Any]:
    reports = [
        trihedral_pair_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]

    checks = {
        "all_eight_reports_verify_11_checks": all(report["n_verified"] == 11 for report in reports),
        "all_eight_reports_have_120_trihedral_pairs": all(
            report["trihedral_pair_count"] == 120 for report in reports
        ),
        "all_eight_reports_have_weight_participation_40": all(
            report["weight_participation_profile"] == {"40": 27} for report in reports
        ),
        "all_eight_reports_have_tritangent_participation_16": all(
            report["tritangent_participation_profile"] == {"16": 45} for report in reports
        ),
        "all_eight_reports_have_double_six_participation_10": all(
            report["double_six_participation_profile"] == {"10": 36} for report in reports
        ),
    }

    return {
        "part": "MCCCXCVI",
        "theorem": "E6 120 Steiner trihedral pairs",
        "input_bridge": "MCCCXCV spread/double-six automorphism order",
        "trihedral_pair_identity": "36 double-sixes + 45 tritangents -> 120 Steiner trihedral pairs",
        "matter_sector_reports": reports,
        "claim_boundary": (
            "finite cubic-surface incidence theorem on the W33-derived E6 matter "
            "charts; it reconstructs the 120 Steiner trihedral-pair layer without "
            "claiming a continuum surface equation"
        ),
        "reading": (
            "Each W33-derived E6 matter chart contains exactly 120 finite Steiner "
            "trihedral-pair witnesses. Each witness is a triple of double-sixes "
            "with pairwise overlap 6, empty triple intersection, and union size 18. "
            "The complementary 9 weights contain exactly six zero-sum tritangent "
            "triples, and those six split uniquely into a pair of trihedra. The "
            "incidence counts are sharp: every weight appears in 40 such pairs, "
            "every tritangent in 16, every double-six in 10, and every overlap-6 "
            "double-six pair in exactly one."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = e6_120_steiner_trihedral_pairs_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCVI: E6 120 Steiner Trihedral Pairs ===")
    print("identity:", packet["trihedral_pair_identity"])
    first = packet["matter_sector_reports"][0]
    print("sector 0 trihedral pairs:", first["trihedral_pair_count"])
    print("sector 0 weight participation:", first["weight_participation_profile"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-sector checks:", [report["n_verified"] for report in packet["matter_sector_reports"]])


if __name__ == "__main__":
    main()
