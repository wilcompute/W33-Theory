#!/usr/bin/env python3
"""
BT798 - The residual 48-packet is four tetrahedra.

BT788 found that the actual 480 action carrier is not ten free 48-orbits.
The residual compressed packet has micro-orbit sizes:

    16 + 16 + 8 + 8 = 48.

BT798 identifies that residual packet.  On directed W33 edges it is the full
directed edge set of four disjoint K4 components.  Those four K4 components
are not abstract cliques: they are exactly the four common transversal lines of
the base skew-line pair.  On triangle-corners the residual packet is the full
corner set of the same four transversal lines:

    4 * |E_dir(K4)| = 4 * 12 = 48
    4 * (4 triangles in K4) * 3 corners = 48.

Each K4 contains one base antipode pair and one shadow antipode pair.  This is
the finite carrier of the diagonal kill: a cube antipode bit is not discarded;
it is completed into a tetrahedral phase packet.
"""
from __future__ import annotations

from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path

from bt787_rank4_incidence_r11_handle import compute_rank32
from bt788_action_480_orbit_compression import (
    build_directed_edges,
    build_triangle_corners,
    directed_edge_transform,
    orbit_decomposition,
    point_item_perms,
    stabilizer_point_perms,
    triangle_corner_transform,
)


ROOT = Path(__file__).resolve().parents[1]


def residual_micro_orbits(orbits):
    residual = [i for i, orbit in enumerate(orbits) if len(orbit) in (8, 16)]
    profile = Counter(len(orbits[i]) for i in residual)
    assert profile == Counter({8: 2, 16: 2})
    return residual


def build_residual_edge_graph(directed_edges, edge_orbits, residual):
    directed = []
    undirected = set()
    for micro in residual:
        for idx in edge_orbits[micro]:
            edge = directed_edges[idx]
            directed.append(edge)
            undirected.add(tuple(sorted(edge)))

    vertices = sorted({v for edge in undirected for v in edge})
    adj = {v: set() for v in vertices}
    for a, b in undirected:
        adj[a].add(b)
        adj[b].add(a)
    return directed, undirected, vertices, adj


def components(adj):
    seen = set()
    comps = []
    for start in sorted(adj):
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
    return comps


def is_clique(comp, adj):
    return all(b in adj[a] for a, b in combinations(comp, 2))


def classify_edge_micro_orbits(directed_edges, edge_orbits, residual, base_union, shadow_vertices):
    classes = {}
    for micro in residual:
        items = [directed_edges[idx] for idx in edge_orbits[micro]]
        size = len(items)
        base_hits_per_edge = [int(a in base_union) + int(b in base_union) for a, b in items]
        if size == 8 and all(h == 2 for h in base_hits_per_edge):
            label = "base_antipode_matching_directed"
        elif size == 8 and all(h == 0 for h in base_hits_per_edge):
            label = "shadow_antipode_matching_directed"
        elif size == 16 and all((a in base_union and b in shadow_vertices) for a, b in items):
            label = "base_to_shadow_cross_edges"
        elif size == 16 and all((a in shadow_vertices and b in base_union) for a, b in items):
            label = "shadow_to_base_cross_edges"
        else:
            raise AssertionError(f"unclassified residual micro-orbit {micro}: {items}")
        classes[label] = {
            "micro_orbit": micro,
            "size": size,
            "representative": list(items[0]),
        }
    return classes


def triangle_corners_from_components(comps):
    corners = set()
    for comp in comps:
        for tri in combinations(comp, 3):
            tri = tuple(sorted(tri))
            for marked in tri:
                corners.add((tri, marked))
    return corners


def common_transversals(geom, base_a, base_b):
    out = []
    base0 = geom["line_sets"][base_a]
    base1 = geom["line_sets"][base_b]
    for line_id, line in enumerate(geom["line_sets"]):
        if line_id in (base_a, base_b):
            continue
        if line & base0 and line & base1:
            out.append({
                "line_id": line_id,
                "points": tuple(sorted(line)),
                "base_points": tuple(sorted(line & (base0 | base1))),
                "shadow_points": tuple(sorted(line - (base0 | base1))),
            })
    return out


def classify_triangle_micro_orbits(triangle_corners, triangle_orbits, residual, base_union, comp_of):
    classes = {}
    for micro in residual:
        items = [triangle_corners[idx] for idx in triangle_orbits[micro]]
        base_vertices_profile = Counter(sum(1 for v in tri if v in base_union) for tri, _ in items)
        marked_profile = Counter("base" if marked in base_union else "shadow" for _, marked in items)
        comp_profile = Counter(comp_of[marked] for _, marked in items)
        key = (
            len(items),
            tuple(sorted(base_vertices_profile.items())),
            tuple(sorted(marked_profile.items())),
        )
        classes[str(micro)] = {
            "size": len(items),
            "representative": [list(items[0][0]), items[0][1]],
            "base_vertices_in_triangle_profile": dict(base_vertices_profile),
            "marked_vertex_profile": dict(marked_profile),
            "component_profile": {str(k): v for k, v in sorted(comp_profile.items())},
            "classification_key": str(key),
        }
    return classes


def main():
    rank32 = compute_rank32()
    geom = rank32["geometry"]
    base_a, base_b = geom["skew"][0]
    base_union = set(geom["line_sets"][base_a] | geom["line_sets"][base_b])

    _, stabilizer = stabilizer_point_perms()
    directed_edges = build_directed_edges(geom)
    edge_perms = point_item_perms(directed_edges, stabilizer, directed_edge_transform)
    edge_orbits = orbit_decomposition(directed_edges, edge_perms)
    edge_residual = residual_micro_orbits(edge_orbits)

    directed, undirected, vertices, adj = build_residual_edge_graph(directed_edges, edge_orbits, edge_residual)
    comps = components(adj)
    shadow_vertices = set(vertices) - base_union

    triangle_corners = build_triangle_corners(geom)
    triangle_perms = point_item_perms(triangle_corners, stabilizer, triangle_corner_transform)
    triangle_orbits = orbit_decomposition(triangle_corners, triangle_perms)
    triangle_residual = residual_micro_orbits(triangle_orbits)
    residual_triangle_items = {
        triangle_corners[idx]
        for micro in triangle_residual
        for idx in triangle_orbits[micro]
    }
    k4_triangle_items = triangle_corners_from_components(comps)

    comp_of = {v: i for i, comp in enumerate(comps) for v in comp}
    edge_classes = classify_edge_micro_orbits(
        directed_edges,
        edge_orbits,
        edge_residual,
        base_union,
        shadow_vertices,
    )
    triangle_classes = classify_triangle_micro_orbits(
        triangle_corners,
        triangle_orbits,
        triangle_residual,
        base_union,
        comp_of,
    )
    transversals = common_transversals(geom, base_a, base_b)
    transversal_points = {row["points"] for row in transversals}

    component_rows = []
    for i, comp in enumerate(comps):
        comp_edges = [edge for edge in undirected if edge[0] in comp and edge[1] in comp]
        component_rows.append({
            "component": i,
            "vertices": list(comp),
            "base_vertices": sorted(set(comp) & base_union),
            "shadow_vertices": sorted(set(comp) & shadow_vertices),
            "undirected_edges": [list(edge) for edge in sorted(comp_edges)],
            "directed_edge_count": 2 * len(comp_edges),
            "triangle_corner_count": 4 * 3,
        })

    checks = {
        "residual_edge_micro_orbits_are_16_16_8_8": Counter(len(edge_orbits[i]) for i in edge_residual) == Counter({16: 2, 8: 2}),
        "residual_triangle_micro_orbits_are_16_16_8_8": Counter(len(triangle_orbits[i]) for i in triangle_residual) == Counter({16: 2, 8: 2}),
        "directed_residual_count_is_48": len(directed) == 48,
        "undirected_residual_edges_are_24": len(undirected) == 24,
        "residual_vertices_are_16": len(vertices) == 16,
        "four_components": len(comps) == 4,
        "every_component_is_K4": all(len(comp) == 4 and is_clique(comp, adj) for comp in comps),
        "components_are_common_transversal_lines": set(comps) == transversal_points,
        "there_are_four_common_transversals": len(transversals) == 4,
        "each_component_has_two_base_two_shadow": all(
            len(set(comp) & base_union) == 2 and len(set(comp) & shadow_vertices) == 2
            for comp in comps
        ),
        "triangle_residual_is_same_four_K4_corner_set": residual_triangle_items == k4_triangle_items,
        "edge_classes_complete": set(edge_classes) == {
            "base_antipode_matching_directed",
            "shadow_antipode_matching_directed",
            "base_to_shadow_cross_edges",
            "shadow_to_base_cross_edges",
        },
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT798 check failed: {name}")

    out = {
        "theorem": "BT798 residual 48-packet is four tetrahedra",
        "base_skew_pair": [base_a, base_b],
        "base_union": sorted(base_union),
        "residual_edge_micro_orbits": edge_residual,
        "residual_triangle_micro_orbits": triangle_residual,
        "edge_micro_orbit_classes": edge_classes,
        "component_rows": component_rows,
        "common_transversal_lines": [
            {
                "line_id": row["line_id"],
                "points": list(row["points"]),
                "base_points": list(row["base_points"]),
                "shadow_points": list(row["shadow_points"]),
            }
            for row in transversals
        ],
        "triangle_micro_orbit_classes": triangle_classes,
        "carrier_identities": {
            "directed_edges": "4 * |E_dir(K4)| = 4 * 12 = 48",
            "triangle_corners": "4 * C(4,3) * 3 = 4 * 4 * 3 = 48",
            "transversal_lines": "the four K4 components are the four common transversals of the base skew pair",
            "torus_unit": "each K4 contributes 4 vertices * 3 outgoing directions = 12",
        },
        "interpretation": {
            "diagonal_kill": "the cube antipode bit is completed into the four common transversal lines",
            "BT788_refinement": "the unique 16+16+8+8 residual compressed packet is a four-tetrahedra carrier",
            "BT789_link": "one K4 is the local 4*3 toroidal unit before normalization by 12",
        },
        "checks": checks,
    }

    path = ROOT / "data" / "bt798_residual_tetrahedral_carrier.json"
    path.parent.mkdir(exist_ok=True)
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print("BT798 residual tetrahedral carrier")
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
