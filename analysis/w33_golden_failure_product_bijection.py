"""Part MMCCCLXXII: golden failure product bijection.

MMCCCLXX decomposed the 108 unique golden-selector failures as four ternary
cubes.  MMCCCLXXI identified the shared 27 bridge lines as an affine F3^3
cube.  This verifier proves the stronger carrier statement:

    unique failures = active K2,2 anchor edge x bridge-line affine cube.

For each active anchor cross-pair (a,b) and each bridge line B disjoint from
the anchor line, the generalized-quadrangle incidence forces exactly one
failed quadrangle:

    {anchor line, endpoint_line(a,B), B, endpoint_line(b,B)}.

Thus the 108 failures are not four unrelated cubes.  They are the direct
product K2,2 x B27, where B27 is the bridge-line affine Cayley cube.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import product
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_bridge_line_affine_cayley_cube import (  # noqa: E402
    anchor_geometry,
    bridge_words,
)
from analysis.w33_golden_selector_z20_cochain_lift import (  # noqa: E402
    build_transport_edges,
    build_unique_quadrangles,
    golden_selector_z20_cochain_lift_packet,
    load_selector_data,
)


OUTPUT_PATH = ROOT / "PART_MMCCCLXXII_GOLDEN_FAILURE_PRODUCT_BIJECTION_results.json"

Q = 3

Pair = tuple[int, int]


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def pair_key(pair: Pair) -> str:
    return f"{pair[0]}-{pair[1]}"


def intersect_point(line_points: list[set[int]], left: int, right: int) -> int:
    common = line_points[left] & line_points[right]
    if len(common) != 1:
        raise AssertionError(f"lines {left} and {right} do not meet uniquely: {common}")
    return next(iter(common))


def endpoint_line_for_bridge(geometry: dict[str, Any], anchor_point: int, bridge_line: int) -> int:
    line_points: list[set[int]] = geometry["line_points"]
    choices = [
        endpoint_line
        for endpoint_line in geometry["endpoint_lines"][anchor_point]
        if line_points[endpoint_line] & line_points[bridge_line]
    ]
    if len(choices) != 1:
        raise AssertionError(f"bridge {bridge_line} has endpoint choices {choices} at {anchor_point}")
    return choices[0]


def active_and_inactive_pairs(anchor_points: tuple[int, ...], failures: list[Any]) -> tuple[list[Pair], list[Pair]]:
    anchor_set = set(anchor_points)
    all_pairs = sorted((min(left, right), max(left, right)) for left, right in product(anchor_points, anchor_points) if left < right)
    active = sorted(set(tuple(sorted(set(quadrangle.points) & anchor_set)) for quadrangle in failures))
    inactive = sorted(pair for pair in all_pairs if pair not in active)
    return active, inactive


def failure_product_records() -> dict[str, Any]:
    lines, sigma = load_selector_data()
    _transport_edges, edge_index = build_transport_edges(lines)
    quadrangles = build_unique_quadrangles(lines, sigma, edge_index)
    failures = [quadrangle for quadrangle in quadrangles if quadrangle.holonomy == -1]

    geometry = anchor_geometry(0)
    words = bridge_words(geometry)
    anchor_line = geometry["anchor_line"]
    anchor_points = geometry["anchor_points"]
    anchor_set = set(anchor_points)
    line_points: list[set[int]] = geometry["line_points"]
    bridge_lines: list[int] = geometry["bridge_lines"]
    through_anchor = set(geometry["through_anchor"])
    active_pairs, inactive_pairs = active_and_inactive_pairs(anchor_points, failures)

    by_pair_bridge: dict[tuple[Pair, int], Any] = {}
    duplicates: list[tuple[Pair, int]] = []
    unexpected_bridge_counts = []
    unexpected_anchor_pair_counts = []

    for quadrangle in failures:
        anchor_pair = tuple(sorted(set(quadrangle.points) & anchor_set))
        if len(anchor_pair) != 2:
            unexpected_anchor_pair_counts.append((quadrangle.lines, quadrangle.points, anchor_pair))
            continue
        bridge_candidates = [line for line in quadrangle.lines if line not in through_anchor]
        if len(bridge_candidates) != 1:
            unexpected_bridge_counts.append((quadrangle.lines, bridge_candidates))
            continue
        key = (anchor_pair, bridge_candidates[0])
        if key in by_pair_bridge:
            duplicates.append(key)
        by_pair_bridge[key] = quadrangle

    expected_keys = {(pair, bridge_line) for pair in active_pairs for bridge_line in bridge_lines}
    actual_keys = set(by_pair_bridge)

    forced_line_mismatches = []
    forced_point_mismatches = []
    projection_profiles: dict[str, dict[str, int]] = {}
    pair_to_bridge_words: dict[str, list[list[int]]] = defaultdict(list)

    for pair, bridge_line in sorted(expected_keys):
        quadrangle = by_pair_bridge.get((pair, bridge_line))
        if quadrangle is None:
            continue
        left_line = endpoint_line_for_bridge(geometry, pair[0], bridge_line)
        right_line = endpoint_line_for_bridge(geometry, pair[1], bridge_line)
        expected_lines = {anchor_line, left_line, bridge_line, right_line}
        actual_lines = set(quadrangle.lines)
        if actual_lines != expected_lines:
            forced_line_mismatches.append(
                {
                    "pair": pair,
                    "bridge": bridge_line,
                    "expected": sorted(expected_lines),
                    "actual": sorted(actual_lines),
                }
            )

        expected_points = {
            pair[0],
            pair[1],
            intersect_point(line_points, left_line, bridge_line),
            intersect_point(line_points, right_line, bridge_line),
        }
        actual_points = set(quadrangle.points)
        if actual_points != expected_points:
            forced_point_mismatches.append(
                {
                    "pair": pair,
                    "bridge": bridge_line,
                    "expected": sorted(expected_points),
                    "actual": sorted(actual_points),
                }
            )

        pair_to_bridge_words[pair_key(pair)].append(list(words[bridge_line]))

    for pair in active_pairs:
        indices = [anchor_points.index(point) for point in pair]
        projection_counts = Counter(
            tuple(words[bridge_line][index] for index in indices)
            for bridge_line in bridge_lines
        )
        projection_profiles[pair_key(pair)] = counter_to_json(Counter(projection_counts.values()))

    ordered_failures = int(golden_selector_z20_cochain_lift_packet()["draft_obstruction"]["ordered_violations"])

    return {
        "lines": lines,
        "failures": failures,
        "geometry": geometry,
        "words": words,
        "active_pairs": active_pairs,
        "inactive_pairs": inactive_pairs,
        "by_pair_bridge": by_pair_bridge,
        "expected_keys": expected_keys,
        "actual_keys": actual_keys,
        "duplicates": duplicates,
        "unexpected_bridge_counts": unexpected_bridge_counts,
        "unexpected_anchor_pair_counts": unexpected_anchor_pair_counts,
        "forced_line_mismatches": forced_line_mismatches,
        "forced_point_mismatches": forced_point_mismatches,
        "projection_profiles": projection_profiles,
        "pair_to_bridge_words": pair_to_bridge_words,
        "ordered_failures": ordered_failures,
    }


def golden_failure_product_bijection_packet() -> dict[str, Any]:
    records = failure_product_records()
    geometry = records["geometry"]
    failures = records["failures"]
    bridge_lines = geometry["bridge_lines"]
    active_pairs = records["active_pairs"]
    inactive_pairs = records["inactive_pairs"]
    by_pair_bridge = records["by_pair_bridge"]
    ordered_failures = records["ordered_failures"]

    pair_counts = Counter(pair for pair, _bridge in by_pair_bridge)
    bridge_counts = Counter(bridge for _pair, bridge in by_pair_bridge)
    active_pair_degrees: Counter[int] = Counter()
    for left, right in active_pairs:
        active_pair_degrees[left] += 1
        active_pair_degrees[right] += 1

    checks = {
        "unique_failure_count_is_108": len(failures) == 4 * Q**3 == 108,
        "active_pairs_are_k22": len(active_pairs) == 4
        and len(inactive_pairs) == 2
        and len(set(inactive_pairs[0]) & set(inactive_pairs[1])) == 0
        and Counter(active_pair_degrees.values()) == {2: 4},
        "bridge_cube_has_27_lines": len(bridge_lines) == Q**3,
        "pair_bridge_keys_have_no_duplicates": not records["duplicates"],
        "pair_bridge_keys_cover_complete_product": records["actual_keys"] == records["expected_keys"],
        "each_active_pair_has_all_27_bridges": Counter(pair_counts.values()) == {Q**3: 4},
        "each_bridge_has_all_4_active_pairs": Counter(bridge_counts.values()) == {4: Q**3},
        "no_unexpected_bridge_or_pair_counts": not records["unexpected_bridge_counts"]
        and not records["unexpected_anchor_pair_counts"],
        "line_set_is_forced_by_pair_and_bridge": not records["forced_line_mismatches"],
        "point_set_is_forced_by_pair_and_bridge": not records["forced_point_mismatches"],
        "pair_coordinate_projections_are_3_to_1": all(profile == {str(Q): Q**2} for profile in records["projection_profiles"].values()),
        "ordered_failures_are_8_times_product": ordered_failures == 2**Q * len(records["expected_keys"]) == 864,
    }

    return {
        "part": "MMCCCLXXII",
        "theorem": "Golden failure product bijection",
        "input_packets": [
            "MMCCCLXX golden failure K2,2 x F3^3 carrier",
            "MMCCCLXXI bridge-line affine Cayley cube",
        ],
        "anchor_line": geometry["anchor_line"],
        "anchor_points": list(geometry["anchor_points"]),
        "active_pairs": [list(pair) for pair in active_pairs],
        "inactive_matching_pairs": [list(pair) for pair in inactive_pairs],
        "bridge_line_count": len(bridge_lines),
        "unique_failure_count": len(failures),
        "ordered_failure_count": ordered_failures,
        "product_identity": {
            "unique": "|K2,2_edges| * |B27| = 4*27 = 108",
            "ordered": "2^q * 4*27 = 8*108 = 864",
            "forced_quadrangle": "{anchor, endpoint_line(a,B), B, endpoint_line(b,B)}",
        },
        "pair_count_profile": counter_to_json(Counter(pair_counts.values())),
        "bridge_count_profile": counter_to_json(Counter(bridge_counts.values())),
        "pair_projection_profiles": records["projection_profiles"],
        "sample_product_records": [
            {
                "pair": list(pair),
                "bridge_line": bridge_line,
                "bridge_word": list(records["words"][bridge_line]),
                "quadrangle_lines": list(records["by_pair_bridge"][(pair, bridge_line)].lines),
                "quadrangle_points": list(records["by_pair_bridge"][(pair, bridge_line)].points),
            }
            for pair, bridge_line in sorted(records["expected_keys"])[:12]
        ],
        "reading": (
            "The 108 unique failures are a genuine product, not four unrelated "
            "27-counts. A bridge line B already contains all ternary data. Once "
            "an active anchor cross-pair (a,b) is chosen, the GQ incidence axiom "
            "forces the two endpoint lines meeting B, and therefore forces the "
            "failed quadrangle. The four K2,2 edges reuse the same 27-point "
            "bridge-line affine cube."
        ),
        "claim_boundary": (
            "This is a canonical bijection inside the draft golden-selector "
            "failure carrier. It still does not identify the product coordinates "
            "with explicit O^-(6,2)/A5 cosets."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = golden_failure_product_bijection_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MMCCCLXXII: Golden Failure Product Bijection ===")
    print("product:", packet["product_identity"])
    print("pair profile:", packet["pair_count_profile"])
    print("bridge profile:", packet["bridge_count_profile"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
