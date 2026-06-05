#!/usr/bin/env python3
"""BT365: unique anchor K4 bipartition behind the Z20 correction.

BT364 identifies one working Z20 correction as the anchor split

    {0,1} | {2,3}.

The anchor K4 has three 2+2 bipartitions, i.e. three perfect matchings.  This
verifier tests all three.  Exactly one bipartition works: the one whose
same-side pairs are the two inactive pairs from the golden failure product.
Choosing either side of that bipartition gives a gauge-equivalent correction.
The other two bipartitions leave 108 corrected failures.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_golden_failure_product_bijection import (  # noqa: E402
    endpoint_line_for_bridge,
    failure_product_records,
    intersect_point,
)
from analysis.w33_golden_selector_z20_cochain_lift import (  # noqa: E402
    build_transport_edges,
    build_unique_quadrangles,
    load_selector_data,
)


OUT = ROOT / "data" / "w33_BREAKTHROUGH_365_unique_anchor_bipartition_correction.json"

Q = 3


def anchor_bipartitions(anchor_points: tuple[int, ...]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    seen = set()
    out = []
    for side in combinations(anchor_points, 2):
        complement = tuple(point for point in anchor_points if point not in side)
        key = tuple(sorted((tuple(side), complement)))
        if key in seen:
            continue
        seen.add(key)
        out.append((tuple(side), complement))
    return out


def selected_edges_for_side(records: dict[str, Any], side: tuple[int, int]) -> set[tuple[int, int, int]]:
    geometry = records["geometry"]
    line_points = geometry["line_points"]
    selected = set()
    for bridge_line in geometry["bridge_lines"]:
        for anchor_point in side:
            endpoint_line = endpoint_line_for_bridge(geometry, anchor_point, bridge_line)
            point = intersect_point(line_points, endpoint_line, bridge_line)
            selected.add((point, *sorted((endpoint_line, bridge_line))))
    return selected


def selected_count(quadrangle, selected_edges: set[tuple[int, int, int]]) -> int:
    total = 0
    for index in range(4):
        edge = (quadrangle.points[index], *sorted((quadrangle.lines[index], quadrangle.lines[(index + 1) % 4])))
        if edge in selected_edges:
            total += 1
    return total


def correction_profile(quadrangles, selected_edges: set[tuple[int, int, int]]) -> dict[str, Any]:
    profile: Counter[tuple[int, int, int]] = Counter()
    corrected_failures = 0
    for quadrangle in quadrangles:
        count = selected_count(quadrangle, selected_edges)
        correction = -1 if count % 2 else 1
        if quadrangle.holonomy * correction != 1:
            corrected_failures += 1
        profile[(quadrangle.holonomy, count % 2, count)] += 1
    return {
        "corrected_failures": corrected_failures,
        "profile": profile,
    }


def same_side_pairs(left: tuple[int, int], right: tuple[int, int]) -> set[tuple[int, int]]:
    return {tuple(sorted(left)), tuple(sorted(right))}


def cross_pairs(left: tuple[int, int], right: tuple[int, int]) -> set[tuple[int, int]]:
    return {tuple(sorted((a, b))) for a in left for b in right}


def build_payload() -> dict[str, Any]:
    lines, sigma = load_selector_data()
    _transport_edges, edge_index = build_transport_edges(lines)
    quadrangles = build_unique_quadrangles(lines, sigma, edge_index)
    records = failure_product_records()
    anchor_points = tuple(records["geometry"]["anchor_points"])
    active_pairs = {tuple(pair) for pair in records["active_pairs"]}
    inactive_pairs = {tuple(pair) for pair in records["inactive_pairs"]}

    bipartition_records = []
    working_bipartitions = []
    side_profiles = []

    for left, right in anchor_bipartitions(anchor_points):
        left_edges = selected_edges_for_side(records, left)
        right_edges = selected_edges_for_side(records, right)
        left_profile = correction_profile(quadrangles, left_edges)
        right_profile = correction_profile(quadrangles, right_edges)
        split_same = same_side_pairs(left, right)
        split_cross = cross_pairs(left, right)
        split_works = left_profile["corrected_failures"] == 0 and right_profile["corrected_failures"] == 0
        if split_works:
            working_bipartitions.append((left, right))
        side_profiles.append(left_profile["corrected_failures"])
        side_profiles.append(right_profile["corrected_failures"])
        bipartition_records.append(
            {
                "left": list(left),
                "right": list(right),
                "same_side_pairs": [list(pair) for pair in sorted(split_same)],
                "cross_pairs": [list(pair) for pair in sorted(split_cross)],
                "same_side_pairs_are_inactive": split_same == inactive_pairs,
                "cross_pairs_are_active": split_cross == active_pairs,
                "left_side_corrected_failures": left_profile["corrected_failures"],
                "right_side_corrected_failures": right_profile["corrected_failures"],
                "left_profile": {str(key): int(value) for key, value in sorted(left_profile["profile"].items())},
                "right_profile": {str(key): int(value) for key, value in sorted(right_profile["profile"].items())},
            }
        )

    working = working_bipartitions[0] if working_bipartitions else ((), ())
    working_left_edges = selected_edges_for_side(records, working[0]) if working_bipartitions else set()
    working_right_edges = selected_edges_for_side(records, working[1]) if working_bipartitions else set()
    symmetric_difference_size = len(working_left_edges ^ working_right_edges)

    identities = {
        "anchor_k4_has_three_bipartitions": len(bipartition_records) == 3,
        "exactly_one_bipartition_works": len(working_bipartitions) == 1,
        "working_same_side_pairs_are_inactive": same_side_pairs(*working) == inactive_pairs,
        "working_cross_pairs_are_active": cross_pairs(*working) == active_pairs,
        "both_sides_of_working_split_are_valid": Counter(side_profiles) == Counter({0: 2, 108: 4}),
        "each_side_selects_2q3_edges": all(
            len(selected_edges_for_side(records, side)) == 2 * Q**3
            for split in anchor_bipartitions(anchor_points)
            for side in split
        ),
        "working_side_complements_differ_by_4q3_edges": symmetric_difference_size == 4 * Q**3 == 108,
        "nonworking_bipartitions_leave_108_failures": sum(1 for value in side_profiles if value == 108) == 4,
    }

    theorem = (
        "Unique Anchor-Bipartition Correction Theorem.  Among the three 2+2 "
        "bipartitions of the anchor K4, exactly one split corrects the golden "
        "selector obstruction: the split whose same-side pairs are the inactive "
        "pairs and whose cross-pairs are the K2,2 failure carrier.  Either side "
        "choice of that split is a valid gauge representative; the other two "
        "bipartitions leave 108 failures."
    )

    return {
        "part": "BT365",
        "title": "The anchor K4 has a unique bipartition correction",
        "summary": {
            "anchor_bipartitions": len(bipartition_records),
            "working_bipartitions": len(working_bipartitions),
            "side_corrected_failure_profile": {str(key): int(value) for key, value in sorted(Counter(side_profiles).items())},
            "all_identities_hold": all(identities.values()),
        },
        "bipartitions": bipartition_records,
        "correction_law": {
            "unique_split": "{0,1} | {2,3} up to side orientation",
            "inactive_pairs": "same-side pairs",
            "active_failure_pairs": "cross-pairs",
            "side_orientation": "choosing either side gives a valid gauge representative",
            "ternary_reading": "the three K4 bipartitions are the ternary alternatives; one is selected by the golden sheet",
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": (
            "This proves uniqueness among anchor K4 bipartition lifts for the "
            "current selected golden sheet.  It does not prove a canonical "
            "global rule selecting the working split before the sheet is known."
        ),
    }


def main() -> int:
    payload = build_payload()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0 if payload["summary"]["all_identities_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
