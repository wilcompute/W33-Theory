"""Part MCCCXCIV: explicit spread / double-six scheme isomorphism.

MCCCXCIII proved that the 36 W33 spreads and 36 E6 double-sixes carry the same
two-class association scheme.  This verifier takes the next finite step: it
constructs an explicit deterministic graph isomorphism between the overlap-4
graphs.

The boundary is important.  This is an exact witness that the two schemes are
isomorphic, anchored by the sorted first spread and sorted first double-six.
It is not a uniqueness theorem and does not claim an intrinsic canonical
labeling of spreads by double-sixes.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_spread_double_six_association_scheme import (  # noqa: E402
    double_six_sets,
    w33_spreads,
)


OUTPUT_PATH = ROOT / "PART_MCCCXCIV_SPREAD_DOUBLE_SIX_SCHEME_ISOMORPHISM_results.json"


def adjacency_sets(objects: list[frozenset[int]], overlap_value: int) -> list[set[int]]:
    return [
        {
            other_index
            for other_index, other in enumerate(objects)
            if index != other_index and len(current & other) == overlap_value
        }
        for index, current in enumerate(objects)
    ]


def deterministic_isomorphism(
    source_adjacency: list[set[int]],
    target_adjacency: list[set[int]],
) -> dict[str, Any]:
    """Return a deterministic source->target isomorphism witness.

    The search anchors source vertex 0 to the first target vertex that permits a
    full isomorphism.  In the current W33/E6 scheme that first target is 0 for
    every matter chart.
    """

    vertex_count = len(source_adjacency)
    source_to_target: dict[int, int] = {}
    target_to_source: dict[int, int] = {}
    node_count = 0

    def feasible(source: int, target: int) -> bool:
        return all(
            (mapped_source in source_adjacency[source]) == (mapped_target in target_adjacency[target])
            for mapped_source, mapped_target in source_to_target.items()
        )

    def select_source() -> int:
        unmapped = [vertex for vertex in range(vertex_count) if vertex not in source_to_target]
        return max(
            unmapped,
            key=lambda vertex: (
                sum(1 for neighbor in source_adjacency[vertex] if neighbor in source_to_target),
                -vertex,
            ),
        )

    def search() -> bool:
        nonlocal node_count
        node_count += 1
        if len(source_to_target) == vertex_count:
            return True

        source = select_source()
        for target in range(vertex_count):
            if target in target_to_source:
                continue
            if not feasible(source, target):
                continue

            source_to_target[source] = target
            target_to_source[target] = source
            if search():
                return True
            del source_to_target[source]
            del target_to_source[target]

        return False

    for target_anchor in range(vertex_count):
        source_to_target.clear()
        target_to_source.clear()
        source_to_target[0] = target_anchor
        target_to_source[target_anchor] = 0
        node_count = 0
        if search():
            mapping = [source_to_target[index] for index in range(vertex_count)]
            return {
                "target_anchor": target_anchor,
                "mapping": mapping,
                "search_nodes": node_count,
            }

    raise AssertionError("no scheme isomorphism found")


def verify_mapping(
    spread_objects: list[frozenset[int]],
    double_six_objects: list[frozenset[int]],
    mapping: list[int],
) -> dict[str, Any]:
    spread_overlap_profile: Counter[int] = Counter()
    target_overlap_profile: Counter[int] = Counter()
    relation_failures: list[dict[str, int]] = []

    for left in range(len(mapping)):
        for right in range(left + 1, len(mapping)):
            spread_overlap = len(spread_objects[left] & spread_objects[right])
            target_overlap = len(double_six_objects[mapping[left]] & double_six_objects[mapping[right]])
            spread_overlap_profile[spread_overlap] += 1
            target_overlap_profile[target_overlap] += 1

            expected_target_overlap = 4 if spread_overlap == 4 else 6
            if target_overlap != expected_target_overlap:
                relation_failures.append(
                    {
                        "spread_left": left,
                        "spread_right": right,
                        "target_left": mapping[left],
                        "target_right": mapping[right],
                        "spread_overlap": spread_overlap,
                        "target_overlap": target_overlap,
                    }
                )

    return {
        "spread_overlap_profile_under_mapping": {str(key): int(value) for key, value in spread_overlap_profile.items()},
        "target_overlap_profile_under_mapping": {str(key): int(value) for key, value in target_overlap_profile.items()},
        "relation_failure_count": len(relation_failures),
        "sample_relation_failures": relation_failures[:5],
    }


def isomorphism_report(coordinate: int, sector_key: str) -> dict[str, Any]:
    spreads = w33_spreads()
    double_sixes = double_six_sets(coordinate, sector_key)
    spread_graph = adjacency_sets(spreads, 4)
    double_six_graph = adjacency_sets(double_sixes, 4)
    witness = deterministic_isomorphism(spread_graph, double_six_graph)
    mapping = witness["mapping"]
    verification = verify_mapping(spreads, double_sixes, mapping)

    checks = {
        "mapping_is_permutation_of_36": sorted(mapping) == list(range(36)),
        "source_anchor_maps_to_first_target": witness["target_anchor"] == 0 and mapping[0] == 0,
        "overlap_4_relation_is_preserved": verification["relation_failure_count"] == 0,
        "spread_overlap_profile_is_270_360": verification["spread_overlap_profile_under_mapping"] == {"4": 270, "1": 360},
        "target_overlap_profile_is_270_360": verification["target_overlap_profile_under_mapping"] == {"4": 270, "6": 360},
    }

    return {
        "coordinate": coordinate,
        "sector": sector_key,
        "target_anchor": witness["target_anchor"],
        "mapping_spread_index_to_double_six_index": mapping,
        "search_nodes": witness["search_nodes"],
        "verification": verification,
        "claim_boundary": "anchored explicit isomorphism witness; not a uniqueness or intrinsic canonicity theorem",
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def spread_double_six_scheme_isomorphism_packet() -> dict[str, Any]:
    reports = [
        isomorphism_report(coordinate, sector_key)
        for coordinate in range(4)
        for sector_key in ("matter_81_coset_1", "matter_81_coset_2")
    ]
    first_mapping = reports[0]["mapping_spread_index_to_double_six_index"]

    checks = {
        "all_eight_reports_verify_5_checks": all(report["n_verified"] == 5 for report in reports),
        "all_eight_reports_use_first_target_anchor": all(report["target_anchor"] == 0 for report in reports),
        "all_eight_reports_have_same_mapping": all(
            report["mapping_spread_index_to_double_six_index"] == first_mapping for report in reports
        ),
        "all_eight_reports_have_no_relation_failures": all(
            report["verification"]["relation_failure_count"] == 0 for report in reports
        ),
    }

    return {
        "part": "MCCCXCIV",
        "theorem": "Explicit spread / double-six scheme isomorphism",
        "input_bridge": "MCCCXCIII spread / double-six association scheme",
        "isomorphism_identity": "spread overlap 4 <-> double-six overlap 4; spread overlap 1 <-> double-six overlap 6",
        "reports": reports,
        "claim_boundary": (
            "explicit anchored association-scheme isomorphism; it proves existence "
            "of a label-preserving witness but does not prove uniqueness or an "
            "intrinsic canonical W33-to-E6 labeling"
        ),
        "reading": (
            "The shared 36-object scheme can be matched explicitly. Anchoring the "
            "first sorted W33 spread to the first sorted E6 double-six, a deterministic "
            "backtracking search finds a full isomorphism preserving the overlap-4 "
            "graph and therefore the complementary class. The same mapping works for "
            "all eight E6 matter charts. This closes the existence-level bridge while "
            "leaving the stronger canonical labeling problem open."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = spread_double_six_scheme_isomorphism_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCCCXCIV: Spread / Double-Six Scheme Isomorphism ===")
    print("identity:", packet["isomorphism_identity"])
    print("first mapping:", packet["reports"][0]["mapping_spread_index_to_double_six_index"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("per-chart checks:", [report["n_verified"] for report in packet["reports"]])


if __name__ == "__main__":
    main()
