#!/usr/bin/env python3
"""BT361: the selector-sheet design is a qutrit phase bundle over W(3,3).

BT360 found 120 selector sheets.  The 54-overlap relation on those sheets is
2-regular with 40 triangle components.  This verifier identifies those
triangles exactly:

    120 selector sheets = 40 W(3,3) lines * 3 qutrit phases.

Collapsing each triangle recovers the line-intersection graph of W(3,3), the
dual SRG(40,12,2,4).  The phase law is sharp:

  * same base line: the three sheets form a triangle at overlap 54;
  * intersecting base lines: all 3*3 phase pairs have overlap 12;
  * skew base lines: exactly 3 phase pairs have overlap 4 and form a perfect
    matching, while the other 6 phase pairs have overlap 2.

Thus the selector obstruction is not merely on a set of 120 sheets.  It is a
ternary phase bundle over the W(3,3) line geometry, with skew-line transport
carried by canonical qutrit phase matchings.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict, deque
from itertools import combinations
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (  # noqa: E402
    build_w33,
    generate_projective_symplectic_group,
)
from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (  # noqa: E402
    selector_failure_edge_supports,
    sheet_orbit,
)


OUT = ROOT / "data" / "w33_BREAKTHROUGH_361_selector_qutrit_phase_bundle.json"

Q = 3


def sheet_anchor_line(sheet, edges, lines) -> int:
    line_to_index = {tuple(line): index for index, line in enumerate(lines)}
    point_frequency: Counter[int] = Counter()
    for support in sheet:
        for edge_id in support:
            for point in edges[edge_id]:
                point_frequency[point] += 1
    anchor = tuple(sorted(point for point, count in point_frequency.items() if count == 108))
    return line_to_index[anchor]


def components_from_relation(neighbours: list[list[int]]) -> list[tuple[int, ...]]:
    seen: set[int] = set()
    components: list[tuple[int, ...]] = []
    for start in range(len(neighbours)):
        if start in seen:
            continue
        queue: deque[int] = deque([start])
        seen.add(start)
        component = []
        while queue:
            node = queue.popleft()
            component.append(node)
            for nxt in neighbours[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        components.append(tuple(sorted(component)))
    return components


def build_payload() -> dict[str, Any]:
    points, edges, edge_index, lines, _adjacency = build_w33()
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)
    sheet_count = len(sheets)

    intersections = [[0] * sheet_count for _ in range(sheet_count)]
    for left in range(sheet_count):
        for right in range(sheet_count):
            intersections[left][right] = len(sheets[left] & sheets[right])

    r54_neighbours = [
        [right for right in range(sheet_count) if right != left and intersections[left][right] == 54]
        for left in range(sheet_count)
    ]
    r54_components = components_from_relation(r54_neighbours)

    anchor_line_by_sheet = [sheet_anchor_line(sheet, edges, lines) for sheet in sheets]
    fiber_by_line: dict[int, list[int]] = defaultdict(list)
    for sheet_index, line_index in enumerate(anchor_line_by_sheet):
        fiber_by_line[line_index].append(sheet_index)

    line_meets = {}
    for left, right in combinations(range(len(lines)), 2):
        line_meets[(left, right)] = bool(set(lines[left]) & set(lines[right]))

    relation_profiles: dict[str, dict[str, Any]] = {}
    skew_matching_failures = []
    adjacent_full_failures = []
    same_line_failures = []

    for left_line, right_line in combinations(sorted(fiber_by_line), 2):
        left_fiber = fiber_by_line[left_line]
        right_fiber = fiber_by_line[right_line]
        meet = line_meets[(min(left_line, right_line), max(left_line, right_line))]
        counts = Counter(
            intersections[left_sheet][right_sheet]
            for left_sheet in left_fiber
            for right_sheet in right_fiber
        )
        relation_profiles[f"{left_line}-{right_line}"] = {
            "line_relation": "intersecting" if meet else "skew",
            "overlap_counts": {str(key): int(value) for key, value in sorted(counts.items())},
        }
        if meet and counts != Counter({12: 9}):
            adjacent_full_failures.append((left_line, right_line, counts))
        if not meet:
            r4_degree_left = Counter(
                sum(1 for right_sheet in right_fiber if intersections[left_sheet][right_sheet] == 4)
                for left_sheet in left_fiber
            )
            r4_degree_right = Counter(
                sum(1 for left_sheet in left_fiber if intersections[left_sheet][right_sheet] == 4)
                for right_sheet in right_fiber
            )
            if counts != Counter({2: 6, 4: 3}) or r4_degree_left != Counter({1: 3}) or r4_degree_right != Counter({1: 3}):
                skew_matching_failures.append((left_line, right_line, counts, r4_degree_left, r4_degree_right))

    for line_index, fiber in sorted(fiber_by_line.items()):
        same_counts = Counter(
            intersections[left][right]
            for left, right in combinations(fiber, 2)
        )
        if same_counts != Counter({54: 3}):
            same_line_failures.append((line_index, same_counts))

    quotient_adjacent_counts = Counter()
    quotient_skew_counts = Counter()
    for left, right in combinations(sorted(fiber_by_line), 2):
        r12_count = sum(
            1
            for left_sheet in fiber_by_line[left]
            for right_sheet in fiber_by_line[right]
            if intersections[left_sheet][right_sheet] == 12
        )
        if line_meets[(min(left, right), max(left, right))]:
            quotient_adjacent_counts[r12_count] += 1
        else:
            quotient_skew_counts[r12_count] += 1

    component_anchor_profile = Counter(
        len({anchor_line_by_sheet[sheet_index] for sheet_index in component})
        for component in r54_components
    )
    line_fiber_profile = Counter(len(fiber) for fiber in fiber_by_line.values())

    identities = {
        "sheet_count_is_40_times_q": sheet_count == 40 * Q == 120,
        "r54_components_are_40_triangles": len(r54_components) == 40 and Counter(len(c) for c in r54_components) == Counter({3: 40}),
        "r54_components_equal_anchor_line_fibers": component_anchor_profile == Counter({1: 40}) and line_fiber_profile == Counter({3: 40}),
        "same_line_relation_is_k3": not same_line_failures,
        "quotient_intersection_graph_has_w33_line_counts": quotient_adjacent_counts == Counter({9: 240}) and quotient_skew_counts == Counter({0: 540}),
        "intersecting_line_fibers_are_complete_k33_at_overlap_12": not adjacent_full_failures,
        "skew_line_fibers_have_r4_perfect_matching": not skew_matching_failures,
        "line_quotient_is_srg_40_12_2_4_dual": (
            len(lines) == 40
            and sum(1 for value in line_meets.values() if value) == 240
            and sum(1 for value in line_meets.values() if not value) == 540
        ),
    }

    theorem = (
        "Selector Qutrit Phase Bundle Theorem.  The 120 BT360 selector sheets "
        "are exactly a 3-sheet qutrit phase fiber over the 40 lines of W(3,3).  "
        "The 54-overlap relation gives the same-line K3 fibers.  Collapsing "
        "those fibers recovers the W(3,3) line-intersection SRG.  Intersecting "
        "base lines have full K3,3 phase coupling at overlap 12; skew base "
        "lines carry a canonical relative-phase perfect matching at overlap 4 "
        "with the other six phase pairs at overlap 2."
    )

    return {
        "part": "BT361",
        "title": "Selector sheets are a qutrit phase bundle over W(3,3) lines",
        "summary": {
            "sheet_count": sheet_count,
            "base_line_count": len(lines),
            "phase_fiber_size": Q,
            "r54_triangle_components": len(r54_components),
            "intersecting_line_pairs": quotient_adjacent_counts.get(9, 0),
            "skew_line_pairs": quotient_skew_counts.get(0, 0),
            "all_identities_hold": all(identities.values()),
        },
        "bundle_law": {
            "total_space": "120 selector sheets = 40 W(3,3) lines * 3 qutrit phases",
            "same_line": "K3 phase fiber, pair overlap 54",
            "intersecting_lines": "complete K3,3 phase coupling, all 9 pairs overlap 12",
            "skew_lines": "one perfect matching of 3 phase pairs at overlap 4; six remaining pairs overlap 2",
            "quotient": "W(3,3) dual line-intersection graph SRG(40,12,2,4)",
        },
        "profiles": {
            "line_fiber_size_profile": {str(key): int(value) for key, value in sorted(line_fiber_profile.items())},
            "r54_component_size_profile": {str(key): int(value) for key, value in sorted(Counter(len(c) for c in r54_components).items())},
            "quotient_adjacent_r12_profile": {str(key): int(value) for key, value in sorted(quotient_adjacent_counts.items())},
            "quotient_skew_r12_profile": {str(key): int(value) for key, value in sorted(quotient_skew_counts.items())},
        },
        "sample_relation_profiles": dict(list(sorted(relation_profiles.items()))[:12]),
        "identities": identities,
        "theorem": theorem,
        "next_frontier": (
            "The skew-line perfect matchings are now the concrete relative-phase "
            "transport candidates.  The next test is whether their product "
            "around selector quadrangles gives the observed holonomy and whether "
            "a character twist on this qutrit bundle cancels it."
        ),
        "honesty_boundary": (
            "This identifies the finite qutrit phase-bundle structure.  It does "
            "not yet choose global phase labels or construct the correcting "
            "selector cochain."
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
