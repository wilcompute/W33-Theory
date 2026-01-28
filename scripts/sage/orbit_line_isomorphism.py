#!/usr/bin/env sage
"""Compute isomorphism between Coxeter-6 orbit graph and W33 point/line graph."""
from __future__ import annotations

import json
from itertools import product
from sage.all import Graph


def build_projective_points():
    F3 = [0, 1, 2]
    proj_points = []
    seen = set()
    for v in product(F3, repeat=4):
        if all(x == 0 for x in v):
            continue
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            proj_points.append(v)
    return proj_points


def omega_sym(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build_edges(points):
    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega_sym(points[i], points[j]) == 0:
                edges.append((i, j))
    return edges


def build_lines_from_edges(edges):
    adj = [[0]*40 for _ in range(40)]
    for i, j in edges:
        adj[i][j] = adj[j][i] = 1

    lines = set()
    for i, j in edges:
        common = [k for k in range(40) if adj[i][k] and adj[j][k]]
        if len(common) == 2:
            line = tuple(sorted([i, j, common[0], common[1]]))
            lines.add(line)
    return sorted(lines)


def line_graph(lines):
    n = len(lines)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if set(lines[i]) & set(lines[j]):
                edges.append((i, j))
    return Graph(edges)


def first_isomorphism(G1, G2):
    iso_iter = G1.isomorphisms(G2)
    try:
        return next(iso_iter)
    except StopIteration:
        return None


def main():
    data = json.loads(open('artifacts/e8_coxeter6_orbits.json').read())
    orbit_edges = data['edges']
    G_orbit = Graph(orbit_edges)

    points = build_projective_points()
    w33_edges = build_edges(points)
    G_point = Graph(w33_edges)

    lines = build_lines_from_edges(w33_edges)
    G_line = line_graph(lines)

    print(f"Orbit graph vertices: {G_orbit.num_verts()}, edges: {G_orbit.num_edges()}")
    print(f"Point graph vertices: {G_point.num_verts()}, edges: {G_point.num_edges()}")
    print(f"Line graph vertices: {G_line.num_verts()}, edges: {G_line.num_edges()}")

    iso_point = G_orbit.is_isomorphic(G_point)
    iso_line = G_orbit.is_isomorphic(G_line)
    print(f"Isomorphic to point graph: {iso_point}")
    print(f"Isomorphic to line graph: {iso_line}")

    mapping = None
    target = None
    if iso_point:
        mapping = first_isomorphism(G_orbit, G_point)
        target = 'point'
    elif iso_line:
        mapping = first_isomorphism(G_orbit, G_line)
        target = 'line'
    else:
        raise RuntimeError("Orbit graph not isomorphic to point or line graph")

    if mapping is None:
        raise RuntimeError("Failed to compute isomorphism mapping")

    out = {
        "orbit_to_index": {int(k): int(v) for k, v in mapping.items()},
        "target": target,
    }
    with open('artifacts/orbit_graph_isomorphism.json', 'w') as f:
        json.dump(out, f, indent=2)
    print("Wrote artifacts/orbit_graph_isomorphism.json")


if __name__ == '__main__':
    main()
