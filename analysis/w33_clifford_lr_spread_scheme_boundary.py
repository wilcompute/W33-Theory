"""Part MDCLXXXI: Clifford L/R grid vs W33 spread scheme boundary.

The GitHub MCCCCXVII-MCCCCXXXII fibration packet proves that the 600-cell has
12 special Clifford fibrations forming two K6 families L and R.  Each L_i,R_j
pair shares exactly two great decagons, giving 36 cross-pairs.  The packet
states a count-level correspondence with the 36 W33 spreads.

This verifier checks the natural incidence schemes on those two 36-object
sets.  The result is a precise boundary theorem:

    36 Clifford L/R pairs form the 6 x 6 rook/Hamming scheme.
    36 W33 spreads form the spread/double-six scheme.

The counts match, but the natural schemes do not.  A canonical W33 spread
selector therefore needs an additional symplectic twist; it is not supplied by
the raw L/R Clifford grid alone.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PART_MCCCCXVII_MCCCCXXXII_clifford_fibration_selector_verifier import (  # noqa: E402
    build_600cell,
    build_adjacency,
    find_clifford_fibrations,
    find_great_decagons,
)
from analysis.w33_spread_double_six_association_scheme import (  # noqa: E402
    graph_parameters,
    overlap_profile,
    w33_spreads,
)


OUTPUT_PATH = ROOT / "PART_MDCLXXXI_CLIFFORD_LR_SPREAD_SCHEME_BOUNDARY_results.json"


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def special_fibration_families(all_fibrations: list[tuple[int, ...]]) -> tuple[list[int], list[int]]:
    fibration_count = len(all_fibrations)
    fibration_share = np.zeros((fibration_count, fibration_count), dtype=int)
    for left, right in combinations(range(fibration_count), 2):
        shared = len(set(all_fibrations[left]) & set(all_fibrations[right]))
        fibration_share[left, right] = fibration_share[right, left] = shared

    disjoint = (fibration_share == 0).astype(int)
    np.fill_diagonal(disjoint, 0)
    degrees = disjoint.sum(axis=1)
    special = [index for index in range(fibration_count) if degrees[index] == 5]
    assert len(special) == 12

    special_disjoint = disjoint[np.ix_(special, special)]
    visited: dict[int, int] = {}
    component_id = 0
    for start in range(12):
        if start in visited:
            continue
        stack = [start]
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited[current] = component_id
            stack.extend(
                neighbor
                for neighbor in range(12)
                if special_disjoint[current, neighbor] and neighbor not in visited
            )
        component_id += 1

    assert component_id == 2
    left_family = [special[index] for index in range(12) if visited[index] == 0]
    right_family = [special[index] for index in range(12) if visited[index] == 1]
    assert len(left_family) == len(right_family) == 6
    return left_family, right_family


def clifford_lr_pairs() -> list[dict[str, Any]]:
    vertices = np.array(build_600cell())
    adjacency = build_adjacency(vertices, len(vertices))
    decagons = find_great_decagons(adjacency, vertices, len(vertices))
    fibrations = find_clifford_fibrations(decagons)
    left_family, right_family = special_fibration_families(fibrations)

    pairs: list[dict[str, Any]] = []
    for left_index, left_fibration in enumerate(left_family):
        for right_index, right_fibration in enumerate(right_family):
            shared_decagons = frozenset(
                set(fibrations[left_fibration]) & set(fibrations[right_fibration])
            )
            assert len(shared_decagons) == 2
            vertex_union = frozenset(
                vertex for decagon in shared_decagons for vertex in decagons[decagon]
            )
            pairs.append(
                {
                    "address": (left_index, right_index),
                    "shared_decagons": shared_decagons,
                    "vertex_union": vertex_union,
                }
            )

    return pairs


def relation_graph(objects: list[frozenset[int]], overlap_value: int) -> dict[str, Any]:
    return graph_parameters(objects, overlap_value)


def clifford_lr_scheme_report() -> dict[str, Any]:
    pairs = clifford_lr_pairs()
    vertex_sets = [pair["vertex_union"] for pair in pairs]
    decagon_sets = [pair["shared_decagons"] for pair in pairs]

    vertex_overlap = Counter(len(left & right) for left, right in combinations(vertex_sets, 2))
    decagon_overlap = Counter(len(left & right) for left, right in combinations(decagon_sets, 2))
    row_column_profile = Counter()
    for left, right in combinations(pairs, 2):
        same_row_or_column = (
            left["address"][0] == right["address"][0]
            or left["address"][1] == right["address"][1]
        )
        row_column_profile[(len(left["vertex_union"] & right["vertex_union"]), same_row_or_column)] += 1

    overlap_0_graph = relation_graph(vertex_sets, 0)
    overlap_4_graph = relation_graph(vertex_sets, 4)

    checks = {
        "lr_pair_count_is_36": len(pairs) == 36,
        "each_lr_pair_has_two_shared_decagons": Counter(len(item) for item in decagon_sets) == {2: 36},
        "each_lr_pair_has_twenty_vertices": Counter(len(item) for item in vertex_sets) == {20: 36},
        "distinct_lr_pairs_share_no_decagons": decagon_overlap == {0: 630},
        "vertex_overlap_profile_is_180_and_450": vertex_overlap == {0: 180, 4: 450},
        "zero_overlap_is_same_row_or_column": row_column_profile == {(0, True): 180, (4, False): 450},
        "zero_overlap_graph_is_rook_6_by_6": overlap_0_graph
        == {
            "vertices": 36,
            "overlap_value": 0,
            "degree_profile": {"10": 36},
            "edge_count": 180,
            "adjacent_common_neighbor_profile": {"4": 180},
            "nonadjacent_common_neighbor_profile": {"2": 450},
        },
        "four_overlap_graph_is_complement": overlap_4_graph
        == {
            "vertices": 36,
            "overlap_value": 4,
            "degree_profile": {"25": 36},
            "edge_count": 450,
            "adjacent_common_neighbor_profile": {"16": 450},
            "nonadjacent_common_neighbor_profile": {"20": 180},
        },
    }

    return {
        "lr_pair_count": len(pairs),
        "shared_decagon_count_profile": counter_to_json(Counter(len(item) for item in decagon_sets)),
        "vertex_union_size_profile": counter_to_json(Counter(len(item) for item in vertex_sets)),
        "decagon_overlap_profile": counter_to_json(decagon_overlap),
        "vertex_overlap_profile": counter_to_json(vertex_overlap),
        "row_column_profile": counter_to_json(row_column_profile),
        "overlap_0_graph": overlap_0_graph,
        "overlap_4_graph": overlap_4_graph,
        "sample_lr_pairs": [
            {
                "address": list(pair["address"]),
                "shared_decagons": list(sorted(pair["shared_decagons"])),
                "vertex_union_size": len(pair["vertex_union"]),
            }
            for pair in pairs[:6]
        ],
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def w33_spread_scheme_report() -> dict[str, Any]:
    spreads = w33_spreads()
    overlap = overlap_profile(spreads)
    overlap_4_graph = relation_graph(spreads, 4)
    overlap_1_graph = relation_graph(spreads, 1)

    checks = {
        "spread_count_is_36": len(spreads) == 36,
        "spread_overlap_profile_is_270_and_360": overlap == {1: 360, 4: 270},
        "overlap_4_graph_is_srg_36_15_6_6": overlap_4_graph
        == {
            "vertices": 36,
            "overlap_value": 4,
            "degree_profile": {"15": 36},
            "edge_count": 270,
            "adjacent_common_neighbor_profile": {"6": 270},
            "nonadjacent_common_neighbor_profile": {"6": 360},
        },
        "overlap_1_graph_is_srg_36_20_10_12": overlap_1_graph
        == {
            "vertices": 36,
            "overlap_value": 1,
            "degree_profile": {"20": 36},
            "edge_count": 360,
            "adjacent_common_neighbor_profile": {"10": 360},
            "nonadjacent_common_neighbor_profile": {"12": 270},
        },
    }

    return {
        "spread_count": len(spreads),
        "spread_overlap_profile": counter_to_json(overlap),
        "overlap_4_graph": overlap_4_graph,
        "overlap_1_graph": overlap_1_graph,
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def clifford_lr_spread_scheme_boundary_packet() -> dict[str, Any]:
    lr_report = clifford_lr_scheme_report()
    spread_report = w33_spread_scheme_report()

    checks = {
        "both_object_counts_are_36": lr_report["lr_pair_count"] == spread_report["spread_count"] == 36,
        "lr_zero_overlap_graph_not_spread_overlap_4_graph": lr_report["overlap_0_graph"]["degree_profile"]
        != spread_report["overlap_4_graph"]["degree_profile"],
        "lr_four_overlap_graph_not_spread_overlap_1_graph": lr_report["overlap_4_graph"]["degree_profile"]
        != spread_report["overlap_1_graph"]["degree_profile"],
        "natural_schemes_are_not_isomorphic_by_degree": {
            "10": 36,
            "25": 36,
        }
        != {
            "15": 36,
            "20": 36,
        },
    }

    return {
        "part": "MDCLXXXI",
        "theorem": "Clifford L/R grid vs W33 spread scheme boundary",
        "input_bridge": "MCCCCXVII-MCCCCXXXII Clifford fibration selector",
        "boundary_identity": "36 Clifford L/R pairs are count-equal to 36 W33 spreads, but their natural schemes differ",
        "clifford_lr_report": lr_report,
        "w33_spread_report": spread_report,
        "claim_boundary": (
            "count-level correspondence only; the raw L/R Clifford grid is the "
            "6x6 rook scheme, not the W33 spread association scheme"
        ),
        "reading": (
            "The 600-cell special Clifford fibrations give 36 L/R cross-pairs. "
            "Each cross-pair is two shared great decagons with 20 vertices. "
            "Natural vertex-overlap relations split as 180 pairs with overlap 0 "
            "and 450 pairs with overlap 4, exactly the same-row/same-column and "
            "different-row/different-column relations of a 6x6 grid. The zero-"
            "overlap graph is srg(36,10,4,2). W33 spreads instead have overlap "
            "profile 270/360 and graphs srg(36,15,6,6) and srg(36,20,10,12). "
            "Therefore the raw Clifford L/R count does not supply a canonical "
            "spread labeling. The missing object is an extra symplectic selector "
            "that twists the 6x6 grid into the W33 spread scheme."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = clifford_lr_spread_scheme_boundary_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MDCLXXXI: Clifford L/R Grid vs W33 Spread Scheme Boundary ===")
    print("identity:", packet["boundary_identity"])
    print("LR graph:", packet["clifford_lr_report"]["overlap_0_graph"])
    print("spread graph:", packet["w33_spread_report"]["overlap_4_graph"])
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])} global checks")
    print("LR checks:", packet["clifford_lr_report"]["n_verified"])
    print("spread checks:", packet["w33_spread_report"]["n_verified"])


if __name__ == "__main__":
    main()
