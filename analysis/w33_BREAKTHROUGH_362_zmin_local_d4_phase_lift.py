#!/usr/bin/env python3
"""BT362: local D4 phase lift of every minimal Z support.

BT360 showed each minimal Z support lies in eight selector sheets.  BT361
identified those sheets globally as a qutrit phase bundle over the 40 W(3,3)
lines.  This verifier proves the local refinement:

    every Z_min support sees exactly 4 boundary lines * 2 phases.

For a Z logical quadrangle, the eight incident selector sheets are not spread
through the 120-sheet space.  They sit precisely over the four boundary lines
of the quadrangle, with exactly two of the three qutrit phases present over
each boundary line.  The missing phases on opposite skew boundary lines are
paired by the BT361 skew-line phase matching for every quadrangle.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
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
from analysis.w33_golden_selector_z20_cochain_lift import (  # noqa: E402
    build_transport_edges,
    build_unique_quadrangles,
    load_selector_data,
)


OUT = ROOT / "data" / "w33_BREAKTHROUGH_362_zmin_local_d4_phase_lift.json"

Q = 3
D4_ORDER = 8


def anchor_line_for_sheet(sheet, edges, lines) -> int:
    line_to_index = {tuple(line): index for index, line in enumerate(lines)}
    point_frequency: Counter[int] = Counter()
    for support in sheet:
        for edge_id in support:
            for point in edges[edge_id]:
                point_frequency[point] += 1
    anchor = tuple(sorted(point for point, count in point_frequency.items() if count == 108))
    return line_to_index[anchor]


def build_payload() -> dict[str, Any]:
    points, edges, edge_index, lines, adjacency = build_w33()
    _x_supports, z_supports = minimal_supports(lines, edges, edge_index, adjacency)
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)

    sheet_anchor = [anchor_line_for_sheet(sheet, edges, lines) for sheet in sheets]
    fibers: dict[int, list[int]] = defaultdict(list)
    for sheet_index, line_index in enumerate(sheet_anchor):
        fibers[line_index].append(sheet_index)
    for line_index in fibers:
        fibers[line_index].sort()

    sheet_intersections = [[0] * len(sheets) for _ in sheets]
    for left in range(len(sheets)):
        for right in range(len(sheets)):
            sheet_intersections[left][right] = len(sheets[left] & sheets[right])

    incident_sheets: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for sheet_index, sheet in enumerate(sheets):
        for support in sheet:
            incident_sheets[support].append(sheet_index)

    edge_to_line = {}
    for line_index, line in enumerate(lines):
        for left, right in combinations(line, 2):
            edge_to_line[edge_index[tuple(sorted((left, right)))]] = line_index

    local_profiles: Counter[tuple[tuple[int, int], ...]] = Counter()
    off_boundary_count_profile: Counter[int] = Counter()
    missing_phase_count_profile: Counter[int] = Counter()
    bad_supports = []

    for support in z_supports:
        boundary_lines = {edge_to_line[edge_id] for edge_id in support}
        anchors = Counter(sheet_anchor[sheet_index] for sheet_index in incident_sheets[support])
        local_profiles[tuple(sorted(Counter(anchors.values()).items()))] += 1
        off_boundary_count_profile[sum(value for line, value in anchors.items() if line not in boundary_lines)] += 1
        missing_phase_count_profile[
            sum(len(set(fibers[line]) - set(incident_sheets[support])) for line in boundary_lines)
        ] += 1
        if set(anchors) != boundary_lines or Counter(anchors.values()) != Counter({2: 4}):
            bad_supports.append((support, tuple(sorted(boundary_lines)), dict(anchors)))

    selector_lines, sigma = load_selector_data()
    _transport_edges, transport_edge_index = build_transport_edges(selector_lines)
    quadrangles = build_unique_quadrangles(selector_lines, sigma, transport_edge_index)
    holonomy_profile = Counter(q.holonomy for q in quadrangles)
    opposite_missing_match_profile: Counter[tuple[int, int, int]] = Counter()

    for quadrangle in quadrangles:
        points_on_cycle = tuple(quadrangle.points)
        support = tuple(
            sorted(
                edge_index[tuple(sorted((left, right)))]
                for left, right in zip(points_on_cycle, points_on_cycle[1:] + points_on_cycle[:1])
            )
        )
        incident = set(incident_sheets[support])
        missing = {}
        for line_index in quadrangle.lines:
            missing_phase = list(set(fibers[line_index]) - incident)
            if len(missing_phase) != 1:
                raise AssertionError("expected exactly one missing phase per boundary line")
            missing[line_index] = missing_phase[0]

        line0, line1, line2, line3 = quadrangle.lines
        opposite_overlaps = (
            sheet_intersections[missing[line0]][missing[line2]],
            sheet_intersections[missing[line1]][missing[line3]],
        )
        opposite_missing_match_profile[(quadrangle.holonomy, *opposite_overlaps)] += 1

    identities = {
        "every_zmin_support_has_8_incident_sheets": Counter(len(v) for v in incident_sheets.values()) == Counter({D4_ORDER: 1620}),
        "incident_sheet_supports_cover_all_zmin": set(incident_sheets) == z_supports,
        "local_lift_is_four_lines_times_two_phases": not bad_supports and local_profiles == Counter({((2, 4),): 1620}),
        "no_incident_sheets_off_boundary_lines": off_boundary_count_profile == Counter({0: 1620}),
        "one_missing_phase_per_boundary_line": missing_phase_count_profile == Counter({4: 1620}),
        "selector_quadrangle_count_and_holonomy_profile": len(quadrangles) == 1620 and holonomy_profile == Counter({1: 1512, -1: 108}),
        "opposite_missing_phases_are_skew_matched_for_all_quadrangles": opposite_missing_match_profile == Counter({(1, 4, 4): 1512, (-1, 4, 4): 108}),
        "phase_fibers_are_qutrits": Counter(len(fiber) for fiber in fibers.values()) == Counter({Q: 40}),
    }

    theorem = (
        "Z-Min Local D4 Phase-Lift Theorem.  Every minimal Z logical support "
        "is incident with exactly eight selector sheets, and those eight are "
        "precisely two qutrit phases over each of the four boundary lines.  "
        "No off-boundary sheet occurs.  The one missing phase over each boundary "
        "line is paired with the opposite missing phase by the BT361 skew-line "
        "matching for both flat and failing golden-selector quadrangles."
    )

    return {
        "part": "BT362",
        "title": "Every Z-min support has a local 4-lines times 2-phases lift",
        "summary": {
            "z_min_supports": len(z_supports),
            "selector_quadrangles": len(quadrangles),
            "incident_sheets_per_support": D4_ORDER,
            "boundary_lines_per_support": 4,
            "phases_present_per_boundary_line": 2,
            "all_identities_hold": all(identities.values()),
        },
        "local_lift": {
            "incident_sheet_law": "8 = 4 boundary lines * 2 present qutrit phases",
            "missing_phase_law": "one missing phase over each boundary line",
            "opposite_pair_law": "opposite missing phases are overlap-4 matched for all quadrangles",
            "holonomy_boundary": "this local law is common to 1512 flat and 108 failing selector quadrangles",
        },
        "profiles": {
            "local_anchor_count_profile": {str(key): int(value) for key, value in sorted(local_profiles.items(), key=lambda item: str(item[0]))},
            "off_boundary_count_profile": {str(key): int(value) for key, value in sorted(off_boundary_count_profile.items())},
            "missing_phase_count_profile": {str(key): int(value) for key, value in sorted(missing_phase_count_profile.items())},
            "opposite_missing_match_profile": {str(key): int(value) for key, value in sorted(opposite_missing_match_profile.items())},
        },
        "identities": identities,
        "theorem": theorem,
        "next_frontier": (
            "Because the opposite missing-phase rule is shared by good and bad "
            "quadrangles, the golden obstruction must live in the cyclic order "
            "of the four binary phase choices around the support, not in a "
            "single opposite-pair mismatch."
        ),
        "honesty_boundary": (
            "This proves the local incidence and missing-phase law.  It does "
            "not yet identify the cyclic binary invariant that separates the "
            "108 failing quadrangles from the 1512 flat quadrangles."
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
