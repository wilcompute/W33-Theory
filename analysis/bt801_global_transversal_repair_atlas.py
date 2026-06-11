#!/usr/bin/env python3
"""
BT801 - Global transversal repair atlas.

BT800 proved the diagonal quotient / shadow split for one base cube chart.
BT801 globalizes it to all 540 skew-line charts of W(3,3).

For every skew line pair:
  * there are exactly four common transversals;
  * the four base antipode pairs are exactly the base intersections of those
    transversals, so Q3/<111> is the transversal tetrad;
  * the eight shadow endpoints split as collinearity K4,4 and
    noncollinearity K4 + K4;
  * the four shadow pairs are a perfect matching across the two K4 sheets.

The global count is 540 * 4 = 2160 chart-transversal slots, the same cardinal
level as the rectangle/antipode-slot boundary, but now with the structural
shadow split attached.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path

from bt787_rank4_incidence_r11_handle import build_geometry


ROOT = Path(__file__).resolve().parents[1]


def graph_components(vertices, edges):
    adj = {v: set() for v in vertices}
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    seen = set()
    comps = []
    for start in vertices:
        if start in seen:
            continue
        q = deque([start])
        seen.add(start)
        comp = []
        while q:
            x = q.popleft()
            comp.append(x)
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    q.append(y)
        comps.append(tuple(sorted(comp)))
    return adj, comps


def is_complete_bipartite(parts, edges):
    if len(parts) != 2:
        return False
    a, b = [set(p) for p in parts]
    edge_set = {tuple(sorted(edge)) for edge in edges}
    expected = {tuple(sorted((x, y))) for x in a for y in b}
    return edge_set == expected


def analyze_chart(geom, chart_index, pair):
    line_sets = geom["line_sets"]
    adj = geom["adj"]
    a, b = pair
    base0 = line_sets[a]
    base1 = line_sets[b]
    base_union = base0 | base1

    antipode_pairs = {
        tuple(sorted((x, y)))
        for x in base0 for y in base1
        if adj[x][y]
    }
    cube_edges = {
        tuple(sorted((x, y)))
        for x in base0 for y in base1
        if not adj[x][y]
    }
    transversals = []
    for line_id, line in enumerate(line_sets):
        if line_id in pair:
            continue
        if line & base0 and line & base1:
            transversals.append({
                "line_id": line_id,
                "points": tuple(sorted(line)),
                "base_pair": tuple(sorted(line & base_union)),
                "shadow_pair": tuple(sorted(line - base_union)),
            })

    shadow_pairs = {row["shadow_pair"] for row in transversals}
    shadow_vertices = sorted({v for pair0 in shadow_pairs for v in pair0})
    col_edges = {
        tuple(sorted((x, y)))
        for x, y in combinations(shadow_vertices, 2)
        if adj[x][y]
    }
    noncol_edges = {
        tuple(sorted((x, y)))
        for x, y in combinations(shadow_vertices, 2)
        if not adj[x][y]
    }
    _, col_components = graph_components(shadow_vertices, col_edges)
    _, noncol_components = graph_components(shadow_vertices, noncol_edges)

    noncol_component_edge_counts = []
    for comp in noncol_components:
        c = set(comp)
        noncol_component_edge_counts.append(sum(1 for x, y in noncol_edges if x in c and y in c))

    matching_across = all(
        (edge[0] in set(noncol_components[0])) != (edge[1] in set(noncol_components[0]))
        for edge in shadow_pairs
    ) if len(noncol_components) == 2 else False

    checks = {
        "four_transversals": len(transversals) == 4,
        "cube_edges_are_Q3_count": len(cube_edges) == 12,
        "four_antipode_pairs": len(antipode_pairs) == 4,
        "antipodes_equal_transversal_base_pairs": antipode_pairs == {row["base_pair"] for row in transversals},
        "shadow_vertices_are_8": len(shadow_vertices) == 8,
        "shadow_collinearity_K4_4": len(col_edges) == 16 and len(col_components) == 1 and is_complete_bipartite(noncol_components, col_edges),
        "shadow_noncollinearity_two_K4": len(noncol_edges) == 12 and sorted(len(c) for c in noncol_components) == [4, 4] and sorted(noncol_component_edge_counts) == [6, 6],
        "shadow_pairs_matching_across_sheets": len(shadow_pairs) == 4 and matching_across,
    }
    if not all(checks.values()):
        raise AssertionError(f"chart {chart_index} failed: {checks}")

    return {
        "chart_index": chart_index,
        "skew_pair": [a, b],
        "transversal_line_ids": [row["line_id"] for row in transversals],
        "antipode_pairs": [list(pair0) for pair0 in sorted(antipode_pairs)],
        "shadow_pairs": [list(pair0) for pair0 in sorted(shadow_pairs)],
        "shadow_noncollinearity_components": [list(comp) for comp in noncol_components],
    }


def main():
    geom = build_geometry()
    rows = []
    transversal_slot_counts = Counter()
    shadow_component_profiles = Counter()
    for chart_index, pair in enumerate(geom["skew"]):
        row = analyze_chart(geom, chart_index, pair)
        rows.append(row)
        transversal_slot_counts.update(row["transversal_line_ids"])
        shadow_component_profiles[tuple(sorted(len(c) for c in row["shadow_noncollinearity_components"]))] += 1

    checks = {
        "all_540_charts_verified": len(rows) == 540,
        "global_chart_transversal_slots": sum(transversal_slot_counts.values()) == 2160,
        "each_chart_has_four_transversals": all(len(row["transversal_line_ids"]) == 4 for row in rows),
        "each_line_is_transversal_for_54_charts": set(transversal_slot_counts.values()) == {54},
        "all_shadow_splits_are_4_4": shadow_component_profiles == Counter({(4, 4): 540}),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT801 check failed: {name}")

    out = {
        "theorem": "BT801 global transversal repair atlas",
        "chart_count": len(rows),
        "global_chart_transversal_slots": sum(transversal_slot_counts.values()),
        "transversal_slot_count_per_line_profile": {
            str(k): v for k, v in sorted(Counter(transversal_slot_counts.values()).items())
        },
        "shadow_component_profile": {
            str(k): v for k, v in sorted(shadow_component_profiles.items())
        },
        "sample_charts": rows[:8],
        "interpretation": {
            "atlas_law": "every one of the 540 cube charts carries the same diagonal quotient and matched shadow split",
            "slot_count": "540*4=2160 chart-transversal slots; each W33 line appears as transversal in 54 charts",
            "repair_carrier": "the common-transversal tetrad is the global carrier of the C2^3/<111> repair",
        },
        "checks": checks,
    }

    path = ROOT / "data" / "bt801_global_transversal_repair_atlas.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT801 global transversal repair atlas")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
