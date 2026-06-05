#!/usr/bin/env python3
"""BT364: the Z20 correction is an anchor-bipartition edge lift.

MCCXLVI solved the golden-selector obstruction as a GF(2) transport-edge
cochain and lifted it to a Z20 half-period phase.  BT363 then showed the
failure set is one qutrit phase sheet.

This verifier identifies the displayed 54-edge Z20 correction geometrically.
Relative to the anchor line, the four anchor points split into

    unselected side {0,1}  |  selected side {2,3}.

For each of the 27 bridge lines, the correction selects exactly the two
transport edges from the bridge line to the endpoint lines at the selected
side.  Therefore every active K2,2 failure quadrangle, which crosses the
anchor bipartition, contains exactly one selected edge.  Passing quadrangles
contain an even number of selected edges.
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

from analysis.w33_golden_failure_product_bijection import (  # noqa: E402
    endpoint_line_for_bridge,
    failure_product_records,
    intersect_point,
)
from analysis.w33_golden_selector_z20_cochain_lift import (  # noqa: E402
    build_transport_edges,
    build_unique_quadrangles,
    load_selector_data,
    solve_gf2,
)


OUT = ROOT / "data" / "w33_BREAKTHROUGH_364_z20_anchor_bipartition_lift.json"

Q = 3
SELECTED_SIDE = (2, 3)
UNSELECTED_SIDE = (0, 1)


def selected_solution_edges() -> tuple[set[tuple[int, int, int]], dict[str, Any]]:
    lines, sigma = load_selector_data()
    transport_edges, edge_index = build_transport_edges(lines)
    quadrangles = build_unique_quadrangles(lines, sigma, edge_index)
    solution = solve_gf2([(quadrangle.edge_mask, quadrangle.rhs) for quadrangle in quadrangles], len(transport_edges))
    selected = {transport_edges[index] for index in solution["support"]}
    return selected, {
        "lines": lines,
        "sigma": sigma,
        "transport_edges": transport_edges,
        "edge_index": edge_index,
        "quadrangles": quadrangles,
        "solution": solution,
    }


def expected_anchor_bipartition_edges(records: dict[str, Any]) -> set[tuple[int, int, int]]:
    geometry = records["geometry"]
    line_points = geometry["line_points"]
    expected = set()
    for bridge_line in geometry["bridge_lines"]:
        for anchor_point in SELECTED_SIDE:
            endpoint_line = endpoint_line_for_bridge(geometry, anchor_point, bridge_line)
            point = intersect_point(line_points, endpoint_line, bridge_line)
            left, right = sorted((endpoint_line, bridge_line))
            expected.add((point, left, right))
    return expected


def quadrangle_selected_edge_count(quadrangle, selected_edges: set[tuple[int, int, int]]) -> int:
    points = quadrangle.points
    lines = quadrangle.lines
    count = 0
    for index in range(4):
        point = points[index]
        left, right = sorted((lines[index], lines[(index + 1) % 4]))
        if (point, left, right) in selected_edges:
            count += 1
    return count


def build_payload() -> dict[str, Any]:
    selected_edges, solver_data = selected_solution_edges()
    records = failure_product_records()
    expected_edges = expected_anchor_bipartition_edges(records)
    quadrangles = solver_data["quadrangles"]

    active_pairs = {tuple(pair) for pair in records["active_pairs"]}
    inactive_pairs = {tuple(pair) for pair in records["inactive_pairs"]}
    selected_side = set(SELECTED_SIDE)
    unselected_side = set(UNSELECTED_SIDE)
    cross_pairs = {
        tuple(sorted((left, right)))
        for left in selected_side
        for right in unselected_side
    }

    selected_count_profile_by_holonomy: Counter[tuple[int, int]] = Counter()
    active_pair_parity_profile: Counter[tuple[str, int]] = Counter()
    failure_product_parity_errors = []

    geometry = records["geometry"]
    anchor_set = set(geometry["anchor_points"])

    for quadrangle in quadrangles:
        selected_count = quadrangle_selected_edge_count(quadrangle, selected_edges)
        selected_count_profile_by_holonomy[(quadrangle.holonomy, selected_count)] += 1

    for quadrangle in records["failures"]:
        anchor_pair = tuple(sorted(set(quadrangle.points) & anchor_set))
        selected_count = quadrangle_selected_edge_count(quadrangle, selected_edges)
        pair_type = "cross" if anchor_pair in cross_pairs else "noncross"
        active_pair_parity_profile[(pair_type, selected_count)] += 1
        if anchor_pair not in active_pairs or selected_count != 1:
            failure_product_parity_errors.append((quadrangle.lines, quadrangle.points, anchor_pair, selected_count))

    all_anchor_pairs = {
        tuple(sorted((left, right)))
        for left in geometry["anchor_points"]
        for right in geometry["anchor_points"]
        if left < right
    }

    identities = {
        "gf2_solution_is_consistent": bool(solver_data["solution"]["consistent"]),
        "selected_edge_count_is_2q3": len(selected_edges) == 2 * Q**3 == 54,
        "expected_anchor_bipartition_edge_count_is_2q3": len(expected_edges) == 2 * Q**3 == 54,
        "selected_edges_equal_anchor_bipartition_edges": selected_edges == expected_edges,
        "active_pairs_are_exactly_cross_pairs": active_pairs == cross_pairs,
        "inactive_pairs_are_exactly_same_side_pairs": inactive_pairs == all_anchor_pairs - cross_pairs,
        "every_failure_has_one_selected_edge": active_pair_parity_profile == Counter({("cross", 1): 108}),
        "no_failure_product_parity_errors": not failure_product_parity_errors,
        "passing_quadrangles_have_even_selected_edge_count": all(
            count % 2 == 0
            for (holonomy, count), total in selected_count_profile_by_holonomy.items()
            if holonomy == 1 and total
        ),
        "failing_quadrangles_have_odd_selected_edge_count": all(
            count % 2 == 1
            for (holonomy, count), total in selected_count_profile_by_holonomy.items()
            if holonomy == -1 and total
        ),
        "full_selected_count_profile_matches_solver": selected_count_profile_by_holonomy
        == Counter({(1, 0): 864, (1, 2): 621, (1, 4): 27, (-1, 1): 108}),
    }

    theorem = (
        "Z20 Anchor-Bipartition Lift Theorem.  The deterministic gauge-fixed "
        "MCCXLVI correction is exactly the 54-edge set obtained by choosing one "
        "side {2,3} of the anchor-line K4 and selecting, for every bridge line, "
        "the two bridge-to-endpoint transport edges on that side.  The golden "
        "failure pairs are precisely the K2,2 cross-pairs between {0,1} and "
        "{2,3}, so each failed quadrangle receives odd Z20 half-period parity "
        "and every passing quadrangle receives even parity."
    )

    return {
        "part": "BT364",
        "title": "The Z20 correction is an anchor-bipartition edge lift",
        "summary": {
            "selected_edge_count": len(selected_edges),
            "bridge_line_count": len(records["geometry"]["bridge_lines"]),
            "selected_side": list(SELECTED_SIDE),
            "unselected_side": list(UNSELECTED_SIDE),
            "unique_failures": len(records["failures"]),
            "all_identities_hold": all(identities.values()),
        },
        "edge_lift_law": {
            "selected_edges": "54 = 2 * 27 bridge-to-endpoint transport edges",
            "anchor_split": "{0,1} | {2,3}",
            "active_pairs": "K2,2 cross-pairs between the two sides",
            "correction_phase": "Z20 half-period 10 on selected edges, 0 elsewhere",
            "parity": "failed quadrangles have one selected edge; passing quadrangles have 0, 2, or 4",
        },
        "profiles": {
            "selected_count_by_holonomy": {str(key): int(value) for key, value in sorted(selected_count_profile_by_holonomy.items())},
            "failure_pair_parity": {str(key): int(value) for key, value in sorted(active_pair_parity_profile.items())},
            "selected_sigma_profile": {
                str(key): int(value)
                for key, value in sorted(
                    Counter(solver_data["sigma"][edge] for edge in selected_edges).items()
                )
            },
        },
        "identities": identities,
        "theorem": theorem,
        "honesty_boundary": (
            "This identifies one deterministic gauge-fixed edge lift of the "
            "single-sheet correction.  The GF(2) solution space has 40 line-phase "
            "gauge freedoms, so this is a canonical displayed representative, "
            "not a uniqueness theorem for all cochain lifts."
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
