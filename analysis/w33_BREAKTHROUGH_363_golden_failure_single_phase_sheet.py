#!/usr/bin/env python3
"""BT363: the golden selector fails on one qutrit phase sheet.

BT361 identifies the 120 selector sheets as

    40 W(3,3) lines * 3 qutrit phases.

This verifier makes the draft golden-selector obstruction brutally simple:
the 108 unique failed quadrangles are exactly one of those 120 sheets.  The
864 ordered failures are that one sheet times the eight D4 orderings of each
square.

So the live obstruction is not distributed over the whole Z_min universe.  It
is a single selected line-phase sheet inside the ternary phase bundle.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (  # noqa: E402
    build_w33,
    generate_projective_symplectic_group,
    minimal_supports,
)
from analysis.w33_BREAKTHROUGH_360_selector_zmin_sheet_design import (  # noqa: E402
    selector_failure_edge_supports,
    sheet_orbit,
)
from analysis.w33_golden_failure_product_bijection import (  # noqa: E402
    failure_product_records,
)
from analysis.w33_golden_ordered_d4_torsor import (  # noqa: E402
    ordered_failure_cycles,
)


OUT = ROOT / "data" / "w33_BREAKTHROUGH_363_golden_failure_single_phase_sheet.json"

D4_ORDER = 8
Q = 3
G_NEG = 15


def anchor_line_for_sheet(sheet, edges, lines) -> int:
    line_to_index = {tuple(line): index for index, line in enumerate(lines)}
    point_frequency: Counter[int] = Counter()
    for support in sheet:
        for edge_id in support:
            for point in edges[edge_id]:
                point_frequency[point] += 1
    anchor = tuple(sorted(point for point, count in point_frequency.items() if count == 108))
    return line_to_index[anchor]


def ordered_supports(edges, edge_index) -> Counter[tuple[int, ...]]:
    support_counter: Counter[tuple[int, ...]] = Counter()
    for _cycle, points in ordered_failure_cycles():
        support = tuple(
            sorted(
                edge_index[tuple(sorted((left, right)))]
                for left, right in zip(points, points[1:] + points[:1])
            )
        )
        support_counter[support] += 1
    return support_counter


def build_payload() -> dict[str, Any]:
    points, edges, edge_index, lines, adjacency = build_w33()
    _x_supports, z_supports = minimal_supports(lines, edges, edge_index, adjacency)
    group = generate_projective_symplectic_group(points)

    failure_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, failure_sheet, edges, edge_index)
    sheet_set = set(sheets)
    records = failure_product_records()
    ordered_counter = ordered_supports(edges, edge_index)
    selected_anchor_line = anchor_line_for_sheet(failure_sheet, edges, lines)

    same_anchor_sheets = [
        sheet
        for sheet in sheets
        if anchor_line_for_sheet(sheet, edges, lines) == selected_anchor_line
    ]
    same_anchor_intersections = Counter(len(failure_sheet & sheet) for sheet in same_anchor_sheets)
    all_sheet_intersections = Counter(len(failure_sheet & sheet) for sheet in sheets)

    failure_supports_from_records = set()
    for quadrangle in records["failures"]:
        points_on_cycle = tuple(quadrangle.points)
        support = tuple(
            sorted(
                edge_index[tuple(sorted((left, right)))]
                for left, right in zip(points_on_cycle, points_on_cycle[1:] + points_on_cycle[:1])
            )
        )
        failure_supports_from_records.add(support)

    identities = {
        "failure_sheet_is_one_of_120_sheets": failure_sheet in sheet_set and len(sheets) == 120,
        "failure_sheet_has_108_supports": len(failure_sheet) == 108,
        "failure_sheet_is_subset_of_zmin": set(failure_sheet) <= z_supports,
        "draft_unique_failures_equal_failure_sheet": failure_supports_from_records == set(failure_sheet),
        "ordered_failures_are_failure_sheet_times_d4": ordered_counter == Counter({support: D4_ORDER for support in failure_sheet}),
        "selected_anchor_line_is_draft_anchor_line": selected_anchor_line == records["geometry"]["anchor_line"],
        "selected_anchor_has_three_phase_sheets": len(same_anchor_sheets) == Q,
        "same_anchor_phase_intersections_are_108_and_two_54s": same_anchor_intersections == Counter({108: 1, 54: 2}),
        "global_sheet_intersection_profile_matches_bt360": all_sheet_intersections == Counter({108: 1, 54: 2, 12: 36, 4: 27, 2: 54}),
        "failure_rate_is_one_sheet_over_zmin": len(failure_sheet) * G_NEG == len(z_supports),
        "ordered_failure_rate_is_one_sheet_with_d4": sum(ordered_counter.values()) == len(failure_sheet) * D4_ORDER == 864,
    }

    theorem = (
        "Golden Failure Single Phase-Sheet Theorem.  In the BT361 qutrit phase "
        "bundle, the draft golden-selector failure set is exactly one selected "
        "line-phase sheet: 108 minimal Z supports over the draft anchor line.  "
        "The 864 ordered failures are precisely those 108 supports times the "
        "D4 ordering torsor.  The obstruction rate 108/1620=1/15 is therefore "
        "one sheet of the 120-sheet selector design."
    )

    return {
        "part": "BT363",
        "title": "The golden obstruction is one selected qutrit phase sheet",
        "summary": {
            "sheet_count": len(sheets),
            "selected_sheet_supports": len(failure_sheet),
            "z_min_supports": len(z_supports),
            "selected_anchor_line": selected_anchor_line,
            "ordered_failures": sum(ordered_counter.values()),
            "all_identities_hold": all(identities.values()),
        },
        "single_sheet_law": {
            "selected_sheet": "one of 120 = 40 lines * 3 phases",
            "unique_failures": "108 = one selector sheet",
            "ordered_failures": "864 = 108 * |D4|",
            "rate": "108/1620 = 1/15",
            "same_anchor_fiber": "three phase sheets over the selected line; intersections 108,54,54",
        },
        "profiles": {
            "same_anchor_intersections": {str(key): int(value) for key, value in sorted(same_anchor_intersections.items())},
            "global_sheet_intersections": {str(key): int(value) for key, value in sorted(all_sheet_intersections.items())},
            "ordered_support_profile": {str(key): int(value) for key, value in sorted(Counter(ordered_counter.values()).items())},
        },
        "identities": identities,
        "theorem": theorem,
        "next_frontier": (
            "A flat correction should first be searched as a sheet-level "
            "2-cochain that flips the selected line-phase sheet.  Only after "
            "that succeeds should it be lifted to an edge-level transport "
            "1-cochain with locality constraints."
        ),
        "honesty_boundary": (
            "This identifies exactly where the draft selector fails.  It does "
            "not yet construct the edge-level corrected selector."
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
