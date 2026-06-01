"""Part MMCCCLXX: golden failure K2,2 x F3^3 carrier.

MMCCCLXIX proves that the selector obstruction count is 864.  This verifier
looks inside the 108 unique golden-selector failures before the eight ordered
orientations are added.

The failure carrier is not random.  In the gauge used by the draft selector:

* every failed quadrangle contains one anchor line;
* the four points on that anchor line split into two matched pairs;
* failures occur only across the complementary K2,2 cross-pairs;
* each of the four active cross-pairs carries exactly 27 = 3^3 failures;
* each 27 is a 3 x 3 x 3 cube: three off-anchor lines at one endpoint,
  three off-anchor lines at the other endpoint, and three bridge choices.

So the unique carrier is K2,2 x F3^3 = 4*27 = 108, and the ordered carrier is
2^3 times that: 864.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from math import factorial
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_golden_selector_z20_cochain_lift import (  # noqa: E402
    build_transport_edges,
    build_unique_quadrangles,
    golden_selector_z20_cochain_lift_packet,
    load_selector_data,
)


OUTPUT_PATH = ROOT / "PART_MMCCCLXX_GOLDEN_FAILURE_K22_CUBE_CARRIER_results.json"

Q = 3
V = 40
MU = 4


def counter_to_json(counter: Counter[Any]) -> dict[str, int]:
    return {str(key): int(value) for key, value in sorted(counter.items(), key=lambda item: str(item[0]))}


def pair_key(pair: tuple[int, int]) -> str:
    return f"{pair[0]}-{pair[1]}"


def point_line_maps(lines: list[tuple[int, ...]]) -> tuple[list[set[int]], dict[int, list[int]]]:
    line_points = [set(line) for line in lines]
    point_to_lines: dict[int, list[int]] = defaultdict(list)
    for line_index, line in enumerate(lines):
        for point in line:
            point_to_lines[point].append(line_index)
    return line_points, {point: sorted(indices) for point, indices in point_to_lines.items()}


def golden_failure_quadrangles() -> tuple[list[tuple[int, ...]], list[Any], dict[str, Any]]:
    lines, sigma = load_selector_data()
    _transport_edges, edge_index = build_transport_edges(lines)
    quadrangles = build_unique_quadrangles(lines, sigma, edge_index)
    failures = [quadrangle for quadrangle in quadrangles if quadrangle.holonomy == -1]
    golden = golden_selector_z20_cochain_lift_packet()
    return lines, failures, golden


def base_pair_failure_summaries(
    lines: list[tuple[int, ...]],
    failures: list[Any],
    anchor_line: int,
    active_pairs: list[tuple[int, int]],
) -> dict[str, dict[str, Any]]:
    line_points, point_to_lines = point_line_maps(lines)
    anchor_points = set(lines[anchor_line])
    summaries: dict[str, dict[str, Any]] = {}

    for pair in active_pairs:
        endpoint_lines = {point: sorted(line for line in point_to_lines[point] if line != anchor_line) for point in pair}
        pair_failures = [
            quadrangle
            for quadrangle in failures
            if tuple(sorted(set(quadrangle.points) & anchor_points)) == pair
        ]

        endpoint_line_pairs: Counter[tuple[int, int]] = Counter()
        bridge_lines: Counter[int] = Counter()
        nonanchor_point_pairs: Counter[tuple[int, int]] = Counter()

        for quadrangle in pair_failures:
            other_lines = [line for line in quadrangle.lines if line != anchor_line]
            left_endpoint_lines = [line for line in other_lines if pair[0] in line_points[line]]
            right_endpoint_lines = [line for line in other_lines if pair[1] in line_points[line]]
            if len(left_endpoint_lines) != 1 or len(right_endpoint_lines) != 1:
                raise AssertionError(f"failure is not based at pair {pair}: {quadrangle}")
            left_line = left_endpoint_lines[0]
            right_line = right_endpoint_lines[0]
            bridge_line_candidates = [line for line in other_lines if line not in (left_line, right_line)]
            if len(bridge_line_candidates) != 1:
                raise AssertionError(f"failure does not have one bridge line: {quadrangle}")
            bridge_line = bridge_line_candidates[0]

            endpoint_line_pairs[(left_line, right_line)] += 1
            bridge_lines[bridge_line] += 1
            nonanchor_point_pairs[tuple(sorted(set(quadrangle.points) - anchor_points))] += 1

        summaries[pair_key(pair)] = {
            "failure_count": len(pair_failures),
            "endpoint_lines": {str(point): endpoint_lines[point] for point in pair},
            "endpoint_line_pair_count": len(endpoint_line_pairs),
            "endpoint_line_pair_multiplicity_profile": counter_to_json(Counter(endpoint_line_pairs.values())),
            "bridge_line_count": len(bridge_lines),
            "bridge_line_multiplicity_profile": counter_to_json(Counter(bridge_lines.values())),
            "nonanchor_point_pair_count": len(nonanchor_point_pairs),
            "nonanchor_point_pair_multiplicity_profile": counter_to_json(Counter(nonanchor_point_pairs.values())),
        }

    return summaries


def golden_failure_k22_cube_carrier_packet() -> dict[str, Any]:
    lines, failures, golden = golden_failure_quadrangles()
    line_points, point_to_lines = point_line_maps(lines)
    line_counts = Counter(line for quadrangle in failures for line in quadrangle.lines)
    point_counts = Counter(point for quadrangle in failures for point in quadrangle.points)

    anchor_candidates = [line for line, count in line_counts.items() if count == len(failures)]
    anchor_line = anchor_candidates[0]
    anchor_points = set(lines[anchor_line])
    all_anchor_pairs = sorted(tuple(sorted(pair)) for pair in combinations(sorted(anchor_points), 2))
    base_pair_counts = Counter(tuple(sorted(set(quadrangle.points) & anchor_points)) for quadrangle in failures)
    active_pairs = sorted(pair for pair, count in base_pair_counts.items() if count > 0)
    inactive_pairs = sorted(pair for pair in all_anchor_pairs if pair not in active_pairs)
    expected_active_from_matching = sorted(
        tuple(sorted((left, right)))
        for left in inactive_pairs[0]
        for right in inactive_pairs[1]
    )

    through_anchor_lines = {anchor_line}
    for point in anchor_points:
        through_anchor_lines.update(point_to_lines[point])
    bridge_lines = sorted(set(range(len(lines))) - through_anchor_lines)
    endpoint_lines = sorted(through_anchor_lines - {anchor_line})
    bridge_line_counts = Counter({line: line_counts[line] for line in bridge_lines})
    endpoint_line_counts = Counter({line: line_counts[line] for line in endpoint_lines})

    pair_summaries = base_pair_failure_summaries(lines, failures, anchor_line, active_pairs)
    ordered_failures = int(golden["draft_obstruction"]["ordered_violations"])

    active_pair_degrees: Counter[int] = Counter()
    for left, right in active_pairs:
        active_pair_degrees[left] += 1
        active_pair_degrees[right] += 1

    checks = {
        "unique_failure_count_is_mu_q3": len(failures) == MU * Q**3 == 108,
        "single_anchor_line_supports_all_failures": len(anchor_candidates) == 1,
        "anchor_line_has_q_plus_one_points": len(anchor_points) == Q + 1,
        "active_anchor_pairs_are_k22_edges": active_pairs == expected_active_from_matching
        and Counter(active_pair_degrees.values()) == {2: Q + 1},
        "inactive_anchor_pairs_are_a_matching": len(inactive_pairs) == 2
        and len(set(inactive_pairs[0]) & set(inactive_pairs[1])) == 0,
        "each_active_pair_carries_q3_failures": Counter(base_pair_counts.values()) == {Q**3: MU},
        "each_active_pair_is_3_by_3_by_3": all(
            summary["endpoint_line_pair_multiplicity_profile"] == {str(Q): Q**2}
            and summary["bridge_line_multiplicity_profile"] == {"1": Q**3}
            for summary in pair_summaries.values()
        ),
        "bridge_lines_are_27_and_each_seen_mu_times": len(bridge_lines) == Q**3
        and Counter(bridge_line_counts.values()) == {MU: Q**3},
        "endpoint_lines_are_12_and_each_seen_18_times": len(endpoint_lines) == (Q + 1) * Q
        and Counter(endpoint_line_counts.values()) == {2 * Q**2: (Q + 1) * Q},
        "anchor_points_are_each_seen_54_times": Counter(point_counts[point] for point in anchor_points)
        == {2 * Q**3: Q + 1},
        "nonanchor_points_are_each_seen_q_factorial_times": Counter(
            point_counts[point] for point in set(point_counts) - anchor_points
        )
        == {factorial(Q): V - (Q + 1)},
        "ordered_failures_are_2q_times_unique": ordered_failures == 2**Q * len(failures) == 864,
    }

    return {
        "part": "MMCCCLXX",
        "theorem": "Golden failure K2,2 x F3^3 carrier",
        "input_packet": "MCCXLVI golden selector Z20 cochain lift",
        "unique_failure_count": len(failures),
        "ordered_failure_count": ordered_failures,
        "anchor_line": anchor_line,
        "anchor_points": sorted(anchor_points),
        "active_anchor_pairs": [list(pair) for pair in active_pairs],
        "inactive_matching_pairs": [list(pair) for pair in inactive_pairs],
        "base_pair_failure_counts": {pair_key(pair): int(count) for pair, count in sorted(base_pair_counts.items())},
        "line_incidence_profiles": {
            "anchor_line": {str(anchor_line): line_counts[anchor_line]},
            "endpoint_lines": counter_to_json(Counter(endpoint_line_counts.values())),
            "bridge_lines": counter_to_json(Counter(bridge_line_counts.values())),
        },
        "point_incidence_profiles": {
            "anchor_points": counter_to_json(Counter(point_counts[point] for point in anchor_points)),
            "nonanchor_points": counter_to_json(Counter(point_counts[point] for point in set(point_counts) - anchor_points)),
        },
        "pair_summaries": pair_summaries,
        "carrier_identity": {
            "unique": "K2,2 x F3^3 = 4*27 = 108 = mu*q^3",
            "ordered": "2^q * K2,2 * F3^3 = 8*108 = 864",
            "endpoint_cube": "for each active anchor pair: 3 endpoint lines x 3 endpoint lines x 3 bridge choices",
        },
        "reading": (
            "The golden-selector obstruction is an anchor-line, cross-pair cube. "
            "The anchor line splits into two inactive matched pairs; only the "
            "four cross-pairs fail. Each cross-pair carries a full ternary cube "
            "of 27 failures. This refines the 864 count into a self-dual binary "
            "cut on the anchor line times a ternary F3^3 transport volume."
        ),
        "claim_boundary": (
            "The decomposition is gauge-local to the draft selector's chosen "
            "anchor line. It explains the 108 unique failures and their 864 "
            "ordered orientations, but it does not yet identify these cubes with "
            "specific O^-(6,2)/A5 cosets."
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }


def main() -> None:
    packet = golden_failure_k22_cube_carrier_packet()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MMCCCLXX: Golden Failure K2,2 x F3^3 Carrier ===")
    print("anchor line:", packet["anchor_line"], "points:", packet["anchor_points"])
    print("active pairs:", packet["active_anchor_pairs"])
    print("base pair counts:", packet["base_pair_failure_counts"])
    print("verified:", packet["n_verified"], "/", len(packet["checks"]))


if __name__ == "__main__":
    main()
