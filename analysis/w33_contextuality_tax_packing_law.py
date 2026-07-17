#!/usr/bin/env python3
"""Turn the 5184-tick point-star tax into a concurrency packing law.

The previous bridge priced one movable point-star as exactly one tenth of the
S3 admission supercycle:

    4 line contexts * 108 ordered paths/context * 3 completions * 4 ticks = 5184.

The next architecture question is concurrency.  Could ten such one-tenth
reserves tile the 51840-tick supercycle without conflict?

No.  Two point-star reserves are line-disjoint exactly when their centers are
non-collinear in W(3,3).  A disjoint family of tax reserves is therefore a
partial ovoid in the W33 point graph.  The exact independence number is 7, while
the Hoffman/ovoid ideal is 10.  So the single-tax budget is finite, but the
multi-tax fabric has a certified capacity ceiling: at most seven concurrent
star reserves can be pairwise line/path/runtime-disjoint.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_h4_branch_selection_search import _ordered_nonlocal_paths  # noqa: E402
from scripts.w33_h4_orbital_no_go import _line_intersection_graph  # noqa: E402


OUT = ROOT / "data" / "w33_contextuality_tax_packing_law.json"


def _load_json(relpath: str) -> dict[str, Any]:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def _compress_ranges(values: list[int]) -> list[list[int]]:
    if not values:
        return []
    ordered = sorted(set(values))
    ranges: list[list[int]] = []
    start = previous = ordered[0]
    for value in ordered[1:]:
        if value == previous + 1:
            previous = value
            continue
        ranges.append([start, previous])
        start = previous = value
    ranges.append([start, previous])
    return ranges


def _point_graph(lines: list[tuple[int, int, int, int]]) -> tuple[dict[int, set[int]], dict[frozenset[int], int]]:
    points = sorted({point for line in lines for point in line})
    adjacency = {point: set() for point in points}
    pair_to_line: dict[frozenset[int], int] = {}
    for line_id, line in enumerate(lines):
        for left, right in combinations(line, 2):
            adjacency[left].add(right)
            adjacency[right].add(left)
            pair_to_line[frozenset((left, right))] = line_id
    return adjacency, pair_to_line


def _find_independent_set(
    size: int,
    adjacency: dict[int, set[int]],
) -> tuple[tuple[int, ...] | None, int]:
    points = tuple(sorted(adjacency))
    calls = 0

    def search(chosen: tuple[int, ...], candidates: tuple[int, ...]) -> tuple[int, ...] | None:
        nonlocal calls
        calls += 1
        if len(chosen) == size:
            return chosen
        if len(chosen) + len(candidates) < size:
            return None
        for index, point in enumerate(candidates):
            next_candidates = tuple(
                candidate
                for candidate in candidates[index + 1 :]
                if candidate not in adjacency[point]
            )
            result = search(chosen + (point,), next_candidates)
            if result is not None:
                return result
        return None

    return search(tuple(), points), calls


def _reserve_for_center(
    center: int,
    star_lines: dict[int, list[int]],
    path_ids_by_middle_line: dict[int, list[int]],
    *,
    path_word_ticks: int,
    completions_per_path: int,
    runtime_slots_per_probe: int,
) -> dict[str, Any]:
    line_ids = sorted(star_lines[center])
    path_ids = sorted(
        path_id for line_id in line_ids for path_id in path_ids_by_middle_line[line_id]
    )
    probe_ids = [
        path_id * completions_per_path + completion
        for path_id in path_ids
        for completion in range(completions_per_path)
    ]
    runtime_slots = [
        probe_id * runtime_slots_per_probe + offset
        for probe_id in probe_ids
        for offset in range(runtime_slots_per_probe)
    ]
    return {
        "center": center,
        "line_contexts": line_ids,
        "ordered_path_count": len(path_ids),
        "ordered_path_id_ranges": _compress_ranges(path_ids),
        "completion_probe_count": len(probe_ids),
        "completion_probe_id_ranges": _compress_ranges(probe_ids),
        "runtime_tick_count": len(runtime_slots),
        "runtime_tick_ranges": _compress_ranges(runtime_slots),
        "sample_ordered_paths": path_ids[:8],
        "path_word_ticks": path_word_ticks,
    }


def build_certificate() -> dict[str, Any]:
    runtime_bridge = _load_json("data/w33_contextuality_tax_runtime_bridge.json")
    tax_json = _load_json("data/w33_contextuality_tax.json")
    q3_law = next(row for row in tax_json["deficit_law"] if row["q"] == 3)

    lines, line_adjacency = _line_intersection_graph()
    ordered_paths = _ordered_nonlocal_paths(lines, line_adjacency)
    path_ids_by_middle_line: dict[int, list[int]] = defaultdict(list)
    for path_id, path in enumerate(ordered_paths):
        path_ids_by_middle_line[path[1]].append(path_id)

    star_lines: dict[int, list[int]] = defaultdict(list)
    for line_id, line in enumerate(lines):
        for point in line:
            star_lines[point].append(line_id)

    point_adjacency, pair_to_line = _point_graph(lines)
    star_line_overlap_distribution: Counter[int] = Counter()
    star_path_overlap_distribution: Counter[int] = Counter()
    adjacency_overlap_agrees = True
    for left, right in combinations(sorted(point_adjacency), 2):
        shared_lines = set(star_lines[left]) & set(star_lines[right])
        shared_path_count = sum(len(path_ids_by_middle_line[line_id]) for line_id in shared_lines)
        star_line_overlap_distribution[len(shared_lines)] += 1
        star_path_overlap_distribution[shared_path_count] += 1
        centers_collinear = right in point_adjacency[left]
        if centers_collinear != (len(shared_lines) == 1):
            adjacency_overlap_agrees = False
        if (not centers_collinear) != (len(shared_lines) == 0):
            adjacency_overlap_agrees = False

    ideal_ten_star_tile = 10
    search_results: dict[int, dict[str, Any]] = {}
    witness: tuple[int, ...] | None = None
    for size in range(ideal_ten_star_tile, 6, -1):
        result, calls = _find_independent_set(size, point_adjacency)
        search_results[size] = {
            "exists": result is not None,
            "witness": list(result) if result is not None else None,
            "search_calls": calls,
        }
        if result is not None and witness is None:
            witness = result
    assert witness is not None

    word = runtime_bridge["ordered_path_runtime_surface"]
    star_tax = runtime_bridge["point_star_runtime_tax"]
    path_word_ticks = int(word["path_word_ticks"])
    completions_per_path = int(word["completions_per_path"])
    runtime_slots_per_probe = int(word["runtime_slots_per_probe"])
    runtime_ticks_per_star = int(star_tax["runtime_ticks_per_star"])
    max_disjoint_reserves = len(witness)
    capacity_shortfall = ideal_ten_star_tile - max_disjoint_reserves

    reserve_witnesses = [
        _reserve_for_center(
            center,
            star_lines,
            path_ids_by_middle_line,
            path_word_ticks=path_word_ticks,
            completions_per_path=completions_per_path,
            runtime_slots_per_probe=runtime_slots_per_probe,
        )
        for center in witness
    ]
    witness_lines = sorted({line_id for row in reserve_witnesses for line_id in row["line_contexts"]})
    witness_paths = sorted(
        path_id
        for center in witness
        for line_id in star_lines[center]
        for path_id in path_ids_by_middle_line[line_id]
    )

    checks = {
        "source_runtime_bridge_verified": runtime_bridge["verified"] is True,
        "single_star_runtime_tax_is_5184": runtime_ticks_per_star == 5184,
        "line_overlap_matches_point_collinearity": adjacency_overlap_agrees,
        "collinear_star_pairs_share_one_line_context": dict(star_line_overlap_distribution)
        == {0: 540, 1: 240},
        "collinear_star_pairs_share_108_ordered_paths": dict(star_path_overlap_distribution)
        == {0: 540, 108: 240},
        "no_8_disjoint_star_reserves": search_results[8]["exists"] is False,
        "seven_disjoint_star_reserves_exist": search_results[7]["exists"] is True,
        "packing_capacity_matches_alpha": max_disjoint_reserves == int(q3_law["alpha"]) == 7,
        "ideal_ten_pack_matches_hoffman": ideal_ten_star_tile == int(q3_law["hoffman"]) == 10,
        "capacity_gap_is_three_star_reserves": capacity_shortfall
        == int(q3_law["selection_gap_hoffman_minus_alpha"])
        == 3,
        "witness_line_contexts_are_disjoint": len(witness_lines) == 4 * max_disjoint_reserves,
        "witness_ordered_paths_are_disjoint": len(witness_paths)
        == 432 * max_disjoint_reserves,
        "witness_runtime_ticks_are_7_star_budgets": max_disjoint_reserves
        * runtime_ticks_per_star
        == 36_288,
        "capacity_gap_runtime_is_15552_ticks": capacity_shortfall
        * runtime_ticks_per_star
        == 15_552,
    }

    return {
        "theorem": "W33 contextuality tax packing law",
        "verified": all(checks.values()),
        "breakthrough": (
            "A single movable point-star tax is a finite 5184-tick reserve, but "
            "the W33 fabric cannot pack ten such one-tenth reserves without line "
            "conflict.  Pairwise-disjoint tax reserves are exactly partial ovoids; "
            "the exact capacity is seven, not the Hoffman/ovoid ideal ten."
        ),
        "source_certificates": [
            "data/w33_contextuality_tax_runtime_bridge.json",
            "data/w33_contextuality_tax.json",
        ],
        "pairwise_overlap_law": {
            "point_pairs": len(point_adjacency) * (len(point_adjacency) - 1) // 2,
            "collinear_pairs": sum(len(neighbours) for neighbours in point_adjacency.values()) // 2,
            "noncollinear_pairs": star_line_overlap_distribution[0],
            "star_line_overlap_distribution": dict(sorted(star_line_overlap_distribution.items())),
            "star_ordered_path_overlap_distribution": dict(
                sorted(star_path_overlap_distribution.items())
            ),
            "reading": (
                "Two tax reserves are disjoint exactly when their centers are "
                "non-collinear.  If the centers are collinear they share one "
                "line context, hence 108 ordered path words and 1296 runtime ticks."
            ),
        },
        "packing_capacity": {
            "ideal_ten_star_tile": ideal_ten_star_tile,
            "max_pairwise_disjoint_star_reserves": max_disjoint_reserves,
            "capacity_shortfall_star_reserves": capacity_shortfall,
            "single_star_runtime_ticks": runtime_ticks_per_star,
            "max_disjoint_runtime_ticks": max_disjoint_reserves * runtime_ticks_per_star,
            "capacity_shortfall_runtime_ticks": capacity_shortfall * runtime_ticks_per_star,
            "alpha": q3_law["alpha"],
            "hoffman": q3_law["hoffman"],
            "gap": q3_law["selection_gap_hoffman_minus_alpha"],
            "identity": "max disjoint reserves = alpha(W33 point graph) = 7 < Hoffman/ovoid ideal 10",
        },
        "exact_search": search_results,
        "seven_reserve_witness": {
            "centers": list(witness),
            "line_context_count": len(witness_lines),
            "ordered_path_count": len(witness_paths),
            "runtime_tick_count": max_disjoint_reserves * runtime_ticks_per_star,
            "center_reserves": reserve_witnesses,
        },
        "allocator_reading": (
            "The OS can allocate one star cheaply and can allocate up to seven "
            "simultaneous star reserves without any shared line/path/runtime "
            "surface.  The eighth concurrent tax is the first forced collision "
            "frontier.  This turns contextuality from an abstract gap into a "
            "capacity-planning number."
        ),
        "checks": checks,
        "claim_boundary": [
            "This proves a disjoint-reserve capacity ceiling, not a full queueing policy.",
            "Shared-line reserves may still be time-sliced; they are not pairwise disjoint.",
            "The ten-star ideal is the Hoffman/ovoid benchmark, not an attainable W33 schedule.",
            "No measured photonic branch evidence or canonical selector packet is claimed.",
        ],
    }


def main() -> int:
    cert = build_certificate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(cert["theorem"])
    print(f"  verified: {cert['verified']}")
    print("  disjoint tax reserves: max 7 < ideal 10")
    print("  capacity gap: 3*5184 = 15552 ticks")
    print(f"  wrote {OUT}")
    return 0 if cert["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
