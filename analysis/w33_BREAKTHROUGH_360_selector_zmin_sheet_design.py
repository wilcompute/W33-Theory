#!/usr/bin/env python3
"""BT360: the selector failures form a 120-sheet Z-min design.

BT359 proves the golden-selector obstruction count equals

    864 = 27 * |Stab_Sp(Z_min)|.

This verifier goes below the count.  It converts the 108 unique failed
selector line cycles into the actual edge supports of the canonical W(3,3)
CSS code and proves they are minimal Z logical supports.  Then it moves that
108-support sheet by PSp(4,3).

The result is a clean incidence design:

    120 sheets * 108 supports = 1620 Z_min supports * 8 sheets/support.

So the D4 factor is visible twice: as the eight orderings of a square and as
the eight selector sheets incident with each minimal Z logical support.
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_BREAKTHROUGH_357_minimal_logical_orbit_stabilizers import (  # noqa: E402
    act_support,
    build_w33,
    generate_projective_symplectic_group,
    minimal_supports,
)
from analysis.w33_golden_failure_product_bijection import (  # noqa: E402
    failure_product_records,
)
from analysis.w33_golden_ordered_d4_torsor import (  # noqa: E402
    ordered_failure_cycles,
)


OUT = ROOT / "data" / "w33_BREAKTHROUGH_360_selector_zmin_sheet_design.json"

Q = 3
D4_ORDER = 8
G_NEG = 15


def selector_failure_edge_supports(edges, edge_index) -> set[tuple[int, ...]]:
    records = failure_product_records()
    supports: set[tuple[int, ...]] = set()
    for quadrangle in records["failures"]:
        support = []
        points = tuple(quadrangle.points)
        for left, right in zip(points, points[1:] + points[:1]):
            support.append(edge_index[tuple(sorted((left, right)))])
        supports.add(tuple(sorted(support)))
    return supports


def ordered_failure_support_profile(edges, edge_index) -> Counter[int]:
    profile: Counter[tuple[int, ...]] = Counter()
    for _cycle, points in ordered_failure_cycles():
        support = []
        for left, right in zip(points, points[1:] + points[:1]):
            support.append(edge_index[tuple(sorted((left, right)))])
        profile[tuple(sorted(support))] += 1
    return Counter(profile.values())


def sheet_orbit(group, base_sheet, edges, edge_index) -> list[frozenset[tuple[int, ...]]]:
    seen: set[frozenset[tuple[int, ...]]] = set()
    sheets: list[frozenset[tuple[int, ...]]] = []
    for element in group:
        image = frozenset(act_support(element, support, edges, edge_index) for support in base_sheet)
        if image not in seen:
            seen.add(image)
            sheets.append(image)
    return sheets


def point_edge_profiles(sheet, edges) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    edge_frequency = Counter(edge_id for support in sheet for edge_id in support)
    point_frequency: Counter[int] = Counter()
    for support in sheet:
        for edge_id in support:
            for point in edges[edge_id]:
                point_frequency[point] += 1
    edge_profile = tuple(sorted(Counter(edge_frequency.values()).items()))
    point_profile = tuple(sorted(Counter(point_frequency.values()).items()))
    return edge_profile, point_profile


def build_payload() -> dict[str, Any]:
    points, edges, edge_index, lines, adjacency = build_w33()
    _x_supports, z_supports = minimal_supports(lines, edges, edge_index, adjacency)
    group = generate_projective_symplectic_group(points)
    base_sheet = frozenset(selector_failure_edge_supports(edges, edge_index))

    ordered_profile = ordered_failure_support_profile(edges, edge_index)
    setwise_stabilizer = sum(
        1
        for element in group
        if frozenset(act_support(element, support, edges, edge_index) for support in base_sheet) == base_sheet
    )
    sheets = sheet_orbit(group, base_sheet, edges, edge_index)

    incidence: Counter[tuple[int, ...]] = Counter()
    for sheet in sheets:
        for support in sheet:
            incidence[support] += 1

    base_intersections = Counter(len(base_sheet & sheet) for sheet in sheets)
    edge_profile_types: Counter[tuple[tuple[int, int], ...]] = Counter()
    point_profile_types: Counter[tuple[tuple[int, int], ...]] = Counter()
    for sheet in sheets:
        edge_profile, point_profile = point_edge_profiles(sheet, edges)
        edge_profile_types[edge_profile] += 1
        point_profile_types[point_profile] += 1

    support_orbit = {act_support(element, next(iter(base_sheet)), edges, edge_index) for element in group}

    identities = {
        "base_sheet_has_108_supports": len(base_sheet) == 108,
        "base_sheet_is_subset_of_zmin": set(base_sheet) <= z_supports,
        "ordered_failures_are_d4_over_base_sheet": ordered_profile == Counter({D4_ORDER: 108}),
        "psp_group_order_is_25920": len(group) == 25_920,
        "setwise_stabilizer_is_216": setwise_stabilizer == 216 == D4_ORDER * Q**3,
        "sheet_orbit_has_120_sheets": len(sheets) == 120 == math.factorial(5),
        "all_sheets_have_108_supports": Counter(len(sheet) for sheet in sheets) == Counter({108: 120}),
        "sheet_orbit_stabilizer_identity": len(group) == len(sheets) * setwise_stabilizer,
        "sheet_incidence_covers_all_zmin": set(incidence) == z_supports,
        "each_zmin_support_lies_in_8_sheets": Counter(incidence.values()) == Counter({D4_ORDER: 1620}),
        "total_incidence_is_flatness_loop_carrier": sum(incidence.values()) == 12_960 == 120 * 108 == 1620 * D4_ORDER,
        "single_failed_support_orbit_is_all_zmin": support_orbit == z_supports,
        "base_intersection_profile_matches_selector_scheme": base_intersections == Counter({108: 1, 54: 2, 12: 36, 4: 27, 2: 54}),
        "edge_profiles_are_sheet_invariant": edge_profile_types == Counter({((1, 108), (6, 36), (27, 4)): 120}),
        "point_profiles_are_sheet_invariant": point_profile_types == Counter({((12, 36), (108, 4)): 120}),
        "failure_rate_is_one_g_sheet": 108 * 120 == 864 * G_NEG,
    }

    theorem = (
        "Selector Z-Min Sheet Design Theorem.  The 108 unique golden-selector "
        "failure supports are actual minimal Z logical supports.  Their orbit "
        "under PSp(4,3) is a 120-sheet design with sheet stabilizer 216=8*27.  "
        "Every one of the 1620 minimal Z supports lies in exactly eight sheets, "
        "so 120*108 = 1620*8 = 12960.  The square D4 factor is therefore both "
        "the ordering torsor of one failed quadrangle and the incidence "
        "multiplicity of the global selector-sheet design."
    )

    return {
        "part": "BT360",
        "title": "Golden selector failures form a 120-sheet Z-min design",
        "summary": {
            "base_sheet_supports": len(base_sheet),
            "z_min_supports": len(z_supports),
            "projective_group_order": len(group),
            "setwise_stabilizer": setwise_stabilizer,
            "sheet_count": len(sheets),
            "incidence_total": sum(incidence.values()),
            "all_identities_hold": all(identities.values()),
        },
        "design_parameters": {
            "base_sheet": "108 minimal Z supports",
            "sheet_orbit": "120 = 5! sheets",
            "setwise_stabilizer": "216 = 8 * 27",
            "z_min_universe": "1620 supports",
            "z_min_sheet_multiplicity": "8 = |D4|",
            "incidence_identity": "120 * 108 = 1620 * 8 = 12960",
        },
        "profiles": {
            "ordered_failure_support_profile": {str(key): int(value) for key, value in sorted(ordered_profile.items())},
            "base_sheet_intersections": {str(key): int(value) for key, value in sorted(base_intersections.items())},
            "edge_profile": "108 edges used once, 36 edges used six times, 4 edges used 27 times",
            "point_profile": "36 points used 12 times, 4 anchor points used 108 times",
        },
        "identities": identities,
        "theorem": theorem,
        "next_frontier": (
            "Search for the hidden association scheme on the 120 selector sheets. "
            "The base-intersection profile {108,54,12,4,2} is structured enough "
            "to support a signed section or character twist, which is the likely "
            "route to canceling the golden holonomy obstruction."
        ),
        "honesty_boundary": (
            "This proves the finite sheet design and incidence multiplicities.  "
            "It does not yet produce a corrected flat selector cochain."
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
