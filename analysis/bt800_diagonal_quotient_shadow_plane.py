#!/usr/bin/env python3
"""
BT800 - The diagonal quotient and the shadow F4 split.

BT798-BT799 show that the residual carrier is the four common transversals of
a base skew-line pair.  BT800 identifies the module geometry:

  1. The base Q3 has four antipode pairs.  In a Gray-code labeling those pairs
     differ by 111, so quotienting by <111> gives four cosets.
  2. Those four cosets are exactly the four common transversals.
  3. The shadow endpoints on the transversals do not form a second Q3.  Instead
     their collinearity graph is K4,4 and their noncollinearity graph is K4+K4.
     The four shadow pairs are a perfect matching across the K4,4.

This is the geometric form of C2^3 = 1+2 becoming C2^4 = 2+2:
the fixed diagonal quotient gives one F4 plane, and the shadow endpoints give
the second F4 plane as a two-sheet K4/K4 split with a matching between sheets.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations, permutations, product
import json
from pathlib import Path

from bt787_rank4_incidence_r11_handle import compute_rank32
from bt798_residual_tetrahedral_carrier import common_transversals


ROOT = Path(__file__).resolve().parents[1]


def hamming_edges(words):
    return {
        tuple(sorted((a, b)))
        for a, b in combinations(words, 2)
        if sum(x != y for x, y in zip(a, b)) == 1
    }


def find_base_q3_labeling(geom, base_a, base_b):
    base0 = set(geom["line_sets"][base_a])
    base1 = set(geom["line_sets"][base_b])
    vertices = sorted(base0 | base1)
    cube_edges = set()
    antipode_pairs = []
    for a in base0:
        for b in base1:
            pair = tuple(sorted((a, b)))
            if geom["adj"][a][b]:
                antipode_pairs.append(pair)
            else:
                cube_edges.add(pair)

    words = list(product([0, 1], repeat=3))
    target_edges = hamming_edges(words)
    for perm in permutations(words):
        label = dict(zip(vertices, perm))
        image_edges = {tuple(sorted((label[a], label[b]))) for a, b in cube_edges}
        if image_edges != target_edges:
            continue
        if all(
            tuple(label[a][i] ^ label[b][i] for i in range(3)) == (1, 1, 1)
            for a, b in antipode_pairs
        ):
            return {
                "vertices": vertices,
                "labels": {str(v): list(label[v]) for v in vertices},
                "cube_edges": [list(e) for e in sorted(cube_edges)],
                "antipode_pairs": [list(e) for e in sorted(antipode_pairs)],
            }
    raise AssertionError("no Q3 labeling found")


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


def edge_count_inside(comp, edges):
    c = set(comp)
    return sum(1 for a, b in edges if a in c and b in c)


def is_complete_bipartite(parts, edges):
    a, b = [set(p) for p in parts]
    edge_set = {tuple(sorted(edge)) for edge in edges}
    expected = {tuple(sorted((x, y))) for x in a for y in b}
    return edge_set == expected


def main():
    rank32 = compute_rank32()
    geom = rank32["geometry"]
    base_a, base_b = geom["skew"][0]
    transversals = common_transversals(geom, base_a, base_b)
    q3 = find_base_q3_labeling(geom, base_a, base_b)

    transversal_by_base_pair = {
        tuple(row["base_points"]): row
        for row in transversals
    }
    quotient_rows = []
    labels = {int(k): tuple(v) for k, v in q3["labels"].items()}
    for pair in q3["antipode_pairs"]:
        a, b = pair
        xor = tuple(labels[a][i] ^ labels[b][i] for i in range(3))
        transversal = transversal_by_base_pair[tuple(pair)]
        quotient_rows.append({
            "base_antipode_pair": pair,
            "q3_labels": [list(labels[a]), list(labels[b])],
            "xor": list(xor),
            "transversal_line_id": transversal["line_id"],
            "transversal_points": list(transversal["points"]),
            "shadow_pair": list(transversal["shadow_points"]),
        })

    shadow_pairs = [tuple(row["shadow_points"]) for row in transversals]
    shadow_vertices = sorted({v for pair in shadow_pairs for v in pair})
    col_edges = [
        tuple(sorted((a, b)))
        for a, b in combinations(shadow_vertices, 2)
        if geom["adj"][a][b]
    ]
    noncol_edges = [
        tuple(sorted((a, b)))
        for a, b in combinations(shadow_vertices, 2)
        if not geom["adj"][a][b]
    ]
    col_adj, col_components = graph_components(shadow_vertices, col_edges)
    noncol_adj, noncol_components = graph_components(shadow_vertices, noncol_edges)
    noncol_component_edges = [edge_count_inside(comp, noncol_edges) for comp in noncol_components]

    matching_edges = {tuple(sorted(pair)) for pair in shadow_pairs}

    checks = {
        "base_q3_has_12_edges": len(q3["cube_edges"]) == 12,
        "base_q3_has_four_antipodes": len(q3["antipode_pairs"]) == 4,
        "all_antipodes_are_111": all(row["xor"] == [1, 1, 1] for row in quotient_rows),
        "antipode_cosets_equal_transversals": {
            tuple(row["base_antipode_pair"]) for row in quotient_rows
        } == {tuple(row["base_points"]) for row in transversals},
        "shadow_collinearity_is_K4_4": len(col_edges) == 16 and len(col_components) == 1,
        "shadow_noncollinearity_is_two_K4s": len(noncol_edges) == 12 and sorted(len(c) for c in noncol_components) == [4, 4] and noncol_component_edges == [6, 6],
        "shadow_collinearity_respects_two_sheet_split": is_complete_bipartite(noncol_components, col_edges),
        "shadow_pairs_are_perfect_matching_across_K4_4": len(matching_edges) == 4 and all(
            any(x in comp for x in edge) and not all(x in comp for x in edge)
            for edge in matching_edges
            for comp in [set(noncol_components[0])]
        ),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT800 check failed: {name}")

    out = {
        "theorem": "BT800 diagonal quotient and shadow F4 split",
        "base_skew_pair": [base_a, base_b],
        "base_q3": q3,
        "quotient_rows": quotient_rows,
        "shadow_plane": {
            "shadow_vertices": shadow_vertices,
            "shadow_pairs": [list(pair) for pair in shadow_pairs],
            "collinearity_edges": [list(edge) for edge in sorted(col_edges)],
            "noncollinearity_edges": [list(edge) for edge in sorted(noncol_edges)],
            "noncollinearity_components": [list(comp) for comp in noncol_components],
            "collinearity_structure": "K4,4 across the two noncollinearity K4 sheets",
            "shadow_pair_structure": "perfect matching across the K4,4 sheets",
        },
        "interpretation": {
            "base_quotient": "C2^3/<111> is the four antipode-coset set, and these cosets are the four common transversals",
            "shadow_split": "the added phase plane is a two-sheet K4/K4 shadow split, not another untwisted cube",
            "module_repair": "the geometry realizes 1+2 -> 2+2 by replacing the fixed cube diagonal with a matched shadow F4 sheet",
        },
        "checks": checks,
    }

    path = ROOT / "data" / "bt800_diagonal_quotient_shadow_plane.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT800 diagonal quotient / shadow F4 split")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
