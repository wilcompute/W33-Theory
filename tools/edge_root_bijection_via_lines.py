#!/usr/bin/env python3
"""Construct explicit edge->root bijection via line-orbit duality.

Pipeline:
1) Build W33 from F3^4.
2) Extract 40 lines via common-neighbor rule (each edge determines a unique line).
3) Build line graph (lines adjacent if intersect).
4) Load E8 Coxeter-6 orbit graph from artifacts/e8_coxeter6_orbits.json.
5) Compute canonical isomorphism between line graph and orbit graph.
6) For each line, order its 6 edges canonically.
7) For each orbit, order its 6 roots canonically (via lex-min rotation + direction).
8) Map each edge to root by (line, position).

Outputs:
- artifacts/edge_to_e8_root.json
- artifacts/e8_root_to_edge.json
- artifacts/edge_root_bijection_summary.json
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

from sage.all import Graph

ROOT = Path(__file__).resolve().parents[1]


def build_w33_f3():
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]

    proj_points = []
    seen = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    n = len(proj_points)
    adj = [[0] * n for _ in range(n)]
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
                edges.append((i, j))

    return proj_points, adj, edges


def extract_lines(adj, edges):
    # Each edge has exactly two common neighbors; line = {i,j} U common_neighbors
    lines = set()
    edge_to_line = {}
    n = len(adj)
    for i, j in edges:
        common = [k for k in range(n) if adj[i][k] and adj[j][k]]
        if len(common) != 2:
            raise RuntimeError(f"Edge ({i},{j}) has {len(common)} common neighbors")
        line = tuple(sorted([i, j, common[0], common[1]]))
        lines.add(line)
        edge_to_line[(i, j)] = line

    lines = sorted(lines)
    line_index = {line: idx for idx, line in enumerate(lines)}
    # map edges to line index
    edge_to_line_idx = {e: line_index[line] for e, line in edge_to_line.items()}
    return lines, line_index, edge_to_line_idx


def build_line_graph(lines):
    # vertices: line indices
    edges = []
    for i, li in enumerate(lines):
        set_i = set(li)
        for j in range(i + 1, len(lines)):
            if set_i.intersection(lines[j]):
                edges.append((i, j))
    G = Graph(edges)
    G.add_vertices(range(len(lines)))
    return G


def load_orbit_graph():
    data = json.loads((ROOT / "artifacts" / "e8_coxeter6_orbits.json").read_text())
    orbit_edges = data["edges"]
    orbits = data["orbits"]
    G = Graph(orbit_edges)
    G.add_vertices(range(len(orbits)))
    return orbits, G


def canonical_label_map(G):
    # Return mapping old->canon and canon->old
    res = G.canonical_label(certificate=True)
    if isinstance(res, tuple) and len(res) == 2:
        Gc, lab = res
    else:
        # fallback: if certificate not returned
        Gc = res
        lab = G.canonical_labeling()
    inv = {v: k for k, v in lab.items()}
    return lab, inv


def map_orbit_to_line(G_orbit, G_line):
    lab_o, inv_o = canonical_label_map(G_orbit)
    lab_l, inv_l = canonical_label_map(G_line)

    # For each orbit vertex o, canon label = lab_o[o]
    # Find line vertex l with same canon label
    mapping = {o: inv_l[lab_o[o]] for o in G_orbit.vertices()}
    return mapping


def canonical_orbit_order(orbit):
    # orbit: list of roots as lists
    roots = [tuple(r) for r in orbit]
    # rotate so min root first
    min_root = min(roots)
    min_idx = roots.index(min_root)
    seq = roots[min_idx:] + roots[:min_idx]
    # reverse direction keeping same start
    rev = [seq[0]] + list(reversed(seq[1:]))
    return min(seq, rev)


def canonical_line_edge_order(line, points):
    # line: tuple of 4 point indices
    # points: list of coordinate tuples
    # order points by coordinate tuple
    ordered_pts = sorted(line, key=lambda idx: points[idx])
    # edges in lex order of ordered point indices
    edge_list = []
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = ordered_pts[i], ordered_pts[j]
            edge_list.append(tuple(sorted((a, b))))
    return edge_list


def main():
    points, adj, edges = build_w33_f3()
    lines, line_index, edge_to_line_idx = extract_lines(adj, edges)
    G_lines = build_line_graph(lines)

    orbits, G_orbit = load_orbit_graph()

    # Determine orbit -> line mapping via canonical isomorphism
    orbit_to_line = map_orbit_to_line(G_orbit, G_lines)

    # Build canonical root order for each orbit
    orbit_root_order = {o: canonical_orbit_order(orbits[o]) for o in range(len(orbits))}

    # Build canonical edge order for each line
    line_edge_order = {
        li: canonical_line_edge_order(lines[li], points) for li in range(len(lines))
    }

    # Build edge->root mapping
    edge_to_root = {}
    root_to_edge = {}

    # normalize edge list as sorted tuples
    edges_sorted = [tuple(sorted(e)) for e in edges]
    for e in edges_sorted:
        li = edge_to_line_idx[e]
        # find orbit whose mapped line is this line index
        # invert orbit_to_line
        # build once
    inv_orbit_to_line = {}
    for o, li in orbit_to_line.items():
        inv_orbit_to_line[li] = o

    for e in edges_sorted:
        li = edge_to_line_idx[e]
        o = inv_orbit_to_line[li]
        edge_order = line_edge_order[li]
        pos = edge_order.index(e)
        root = orbit_root_order[o][pos]
        edge_to_root[str(e)] = list(root)
        root_to_edge[str(root)] = list(e)

    # Sanity checks
    ok_bij = len(edge_to_root) == 240 and len(root_to_edge) == 240

    summary = {
        "edges": len(edge_to_root),
        "roots": len(root_to_edge),
        "bijective": ok_bij,
        "orbit_to_line": {str(k): int(v) for k, v in orbit_to_line.items()},
    }

    (ROOT / "artifacts" / "edge_to_e8_root.json").write_text(
        json.dumps(edge_to_root, indent=2), encoding="utf-8"
    )
    (ROOT / "artifacts" / "e8_root_to_edge.json").write_text(
        json.dumps(root_to_edge, indent=2), encoding="utf-8"
    )
    (ROOT / "artifacts" / "edge_root_bijection_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print("Wrote artifacts/edge_to_e8_root.json")
    print("Wrote artifacts/e8_root_to_edge.json")
    print("Wrote artifacts/edge_root_bijection_summary.json")
    print("Bijective:", ok_bij)


if __name__ == "__main__":
    main()
