"""Part MCCCXCIII: W33 spread / E6 double-six association scheme.

W33 has exactly 36 spreads: each spread is a partition of the 40 W33 points
into ten disjoint isotropic lines.  MCCCXCII showed that every W33-derived E6
matter chart has exactly 36 double-sixes.

This verifier checks the stronger finite association-scheme resonance.  The
36 W33 spreads have pairwise line-overlap profile

    overlap 4: 270 pairs, overlap 1: 360 pairs.

The 36 E6 double-sixes have pairwise weight-overlap profile

    overlap 4: 270 pairs, overlap 6: 360 pairs.

In both cases, the overlap-4 graph is srg(36,15,6,6), and the complementary
class is srg(36,20,10,12).  This is not claimed as a canonical bijection; it is
the exact two-class incidence scheme shared by the W33 spread/MUB side and the
E6 double-six side.
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

import w33_e8_spectral_bridge as spectral  # noqa: E402
from analysis.w33_e6_36_double_six_bridge import (  # noqa: E402
    double_sixes,
    projected_weights,
    schlaefli_adjacency,
    six_cliques,
)


OUTPUT_PATH = ROOT / "PART_MCCCXCIII_SPREAD_DOUBLE_SIX_ASSOCIATION_SCHEME_results.json"


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def w33_spreads() -> list[frozenset[int]]:
    line_sets = [frozenset(line) for line in spectral.lines]
    spreads: list[frozenset[int]] = []

    def extend(chosen: list[int], covered: frozenset[int], start: int) -> None:
        if len(chosen) == 10:
            if len(covered) == 40:
                spreads.append(frozenset(chosen))
            return

        missing = next((point for point in range(40) if point not in covered), None)
        if missing is None:
            return

        for line_index in range(start, len(line_sets)):
            line = line_sets[line_index]
            if missing in line and not (line & covered):
                extend(chosen + [line_index], covered | line, line_index + 1)

    extend([], frozenset(), 0)
    return sorted(spreads, key=lambda spread: tuple(sorted(spread)))


def double_six_sets(coordinate: int, sector_key: str) -> list[frozenset[int]]:
    weights = projected_weights(coordinate, sector_key)
    adjacency = schlaefli_adjacency(weights)
    pairs = double_sixes(six_cliques(adjacency), adjacency)
    return sorted((frozenset(first) | frozenset(second) for first, second in pairs), key=lambda item: tuple(sorted(item)))


def overlap_profile(objects: list[frozenset[int]]) -> Counter[int]:
    return Counter(len(left & right) for left, right in combinations(objects, 2))


def graph_parameters(objects: list[frozenset[int]], overlap_value: int) -> dict[str, Any]:
    adjacency = {
        idx: {
            jdx
            for jdx, other in enumerate(objects)
            if idx != jdx and len(current & other) == overlap_value
        }
        for idx, current in enumerate(objects)
    }

    adjacent_common_neighbors: Counter[int] = Counter()
    nonadjacent_common_neighbors: Counter[int] = Counter()
    for left, right in combinations(range(len(objects)), 2):
        common = len(adjacency[left] & adjacency[right])
        if right in adjacency[left]:
            adjacent_common_neighbors[common] += 1
        else:
            nonadjacent_common_neighbors[common] += 1

    return {
        "vertices": len(objects),
        "overlap_value": overlap_value,
        "degree_profile": counter_to_json(Counter(len(neighbors) for neighbors in adjacency.values())),
        "edge_count": sum(len(neighbors) for neighbors in adjacency.values()) // 2,
        "adjacent_common_neighbor_profile": counter_to_json(adjacent_common_neighbors),
        "nonadjacent_common_neighbor_profile": counter_to_json(nonadjacent_common_neighbors),
    }


def is_srg_36_15_6_6(params: dict[str, Any]) -> bool:
    return params == {
        "vertices": 36,
        "overlap_value": params["overlap_value"],
        "degree_profile": {"15": 36},
        "edge_count": 270,
        "adjacent_common_neighbor_profile": {"6": 270},
        "nonadjacent_common_neighbor_profile": {"6": 360},
    }


def is_srg_36_20_10_12(params: dict[str, Any]) -> bool:
    return params == {
        "vertices": 36,
        "overlap_value": params["overlap_value"],
        "degree_profile": {"20": 36},
        "edge_count": 360,
        "adjacent_common_neighbor_profile": {"10": 360},
        "nonadjacent_common_neighbor_profile": {"12": 270},
    }


def spread_report() -> dict[str, Any]:
    spreads = w33_spreads()
    line_participation = Counter(line for spread in spreads for line in spread)
    overlap = overlap_profile(spreads)
    overlap_4 = graph_parameters(spreads, 4)
    overlap_1 = graph_parameters(spreads, 1)

    checks = {
        "spread_count_is_36": len(spreads) == 36,
        "each_spread_has_10_lines": Counter(len(spread) for spread in spreads) == {10: 36},
        "each_line_lies_in_9_spreads": line_participation == {line: 9 for line in range(40)},
        "spread_overlap_profile_is_270_and_360": overlap == {1: 360, 4: 270},
        "overlap_4_graph_is_srg_36_15_6_6": is_srg_36_15_6_6(overlap_4),
        "overlap_1_graph_is_srg_36_20_10_12": is_srg_36_20_10_12(overlap_1),
    }

    return {
        "spread_count": len(spreads),
        "spread_size_profile": counter_to_json(Counter(len(spread) for spread in spreads)),
        "line_participation_profile": counter_to_json(Counter(line_participation.values())),
        "overlap_profile": counter_to_json(overlap),
        "overlap_4_graph": overlap_4,
        "overlap_1_graph": overlap_1,
        "sample_spreads": [list(sorted(spread)) for spread in spreads[:6]],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def double_six_scheme_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    objects = double_six_sets(coordinate, sector_key)
    weight_participation = Counter(weight for double_six in objects for weight in double_six)
    overlap = overlap_profile(objects)
    overlap_4 = graph_parameters(objects, 4)
    overlap_6 = graph_parameters(objects, 6)

    checks = {
        "double_six_count_is_36": len(objects) == 36,
        "each_double_six_has_12_weights": Counter(len(item) for item in objects) == {12: 36},
        "each_weight_lies_in_16_double_sixes": weight_participation == {weight: 16 for weight in range(27)},
        "double_six_overlap_profile_is_270_and_360": overlap == {4: 270, 6: 360},
        "overlap_4_graph_is_srg_36_15_6_6": is_srg_36_15_6_6(overlap_4),
        "overlap_6_graph_is_srg_36_20_10_12": is_srg_36_20_10_12(overlap_6),
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "double_six_count": len(objects),
        "double_six_size_profile": counter_to_json(Counter(len(item) for item in objects)),
        "weight_participation_profile": counter_to_json(Counter(weight_participation.values())),
        "overlap_profile": counter_to_json(overlap),
        "overlap_4_graph": overlap_4,
        "overlap_6_graph": overlap_6,
        "sample_double_sixes": [list(sorted(item)) for item in objects[:6]],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def spread_double_six_association_packet() -> dict[str, Any]:
    spreads = spread_report()
    double_six_reports = [
        double_six_scheme_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]

    checks = {
        "spread_report_verifies_6_checks": spreads["n_verified"] == 6,
        "all_eight_double_six_reports_verify_6_checks": all(report["n_verified"] == 6 for report in double_six_reports),
        "spread_and_double_six_overlap_4_graphs_have_same_srg_parameters": all(
            report["overlap_4_graph"]["degree_profile"] == spreads["overlap_4_graph"]["degree_profile"]
            and report["overlap_4_graph"]["adjacent_common_neighbor_profile"]
            == spreads["overlap_4_graph"]["adjacent_common_neighbor_profile"]
            and report["overlap_4_graph"]["nonadjacent_common_neighbor_profile"]
            == spreads["overlap_4_graph"]["nonadjacent_common_neighbor_profile"]
            for report in double_six_reports
        ),
        "spread_overlap_1_and_double_six_overlap_6_are_matching_complements": all(
            report["overlap_6_graph"]["degree_profile"] == spreads["overlap_1_graph"]["degree_profile"]
            and report["overlap_6_graph"]["adjacent_common_neighbor_profile"]
            == spreads["overlap_1_graph"]["adjacent_common_neighbor_profile"]
            and report["overlap_6_graph"]["nonadjacent_common_neighbor_profile"]
            == spreads["overlap_1_graph"]["nonadjacent_common_neighbor_profile"]
            for report in double_six_reports
        ),
    }

    return {
        "part": "MCCCXCIII",
        "theorem": "W33 spread / E6 double-six association scheme",
        "input_bridge": "MCCCXCII E6 36 double-six bridge",
        "scheme_identity": "36 W33 spreads and 36 E6 double-sixes share the same two-class SRG scheme",
        "spread_report": spreads,
        "double_six_reports": double_six_reports,
        "claim_boundary": (
            "finite association-scheme match; it verifies identical two-class "
            "parameters but does not choose a canonical spread-to-double-six "
            "bijection"
        ),
        "reading": (
            "The 36 W33 spreads and the 36 E6 double-sixes carry the same exact "
            "two-class overlap scheme. Spread overlap 4 and double-six overlap 4 "
            "both give srg(36,15,6,6); spread overlap 1 and double-six overlap 6 "
            "both give the complementary srg(36,20,10,12). This upgrades the "
            "36=36 count into a verified association-scheme resonance while keeping "
            "the canonical bijection question open."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = spread_double_six_association_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCIII: Spread / Double-Six Association Scheme ===")
    print("identity:", packet["scheme_identity"])
    print("spread overlap:", packet["spread_report"]["overlap_profile"])
    print("double-six overlap:", packet["double_six_reports"][0]["overlap_profile"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("spread checks:", packet["spread_report"]["n_verified"])
    print("double-six checks:", [report["n_verified"] for report in packet["double_six_reports"]])


if __name__ == "__main__":
    main()
