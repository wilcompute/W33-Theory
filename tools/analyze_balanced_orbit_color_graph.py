#!/usr/bin/env python3
"""Analyze Z3 phase coloring on the balanced 27-root graph."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def build_w33():
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

    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))

    return proj_points, edges


def main():
    points, edges = build_w33()
    edge_to_idx = {tuple(sorted(e)): i for i, e in enumerate(edges)}

    # Load balanced orbit id
    bias = json.loads((ROOT / "artifacts" / "su3_phase_orbit_bias.json").read_text())
    balanced_orbit = None
    for k, v in bias["orbit_sums"].items():
        if v == {"0": 9, "1": 9, "2": 9} or v == {0: 9, 1: 9, 2: 9}:
            balanced_orbit = int(k.split("_")[1])
    if balanced_orbit is None:
        print("No balanced orbit found")
        return

    # Edge->root map and orbit labels
    we6 = json.loads((ROOT / "artifacts" / "we6_orbit_labels.json").read_text())
    root_to_orbit = {eval(k): v for k, v in we6["mapping"].items()}
    edge_map = json.loads(
        (ROOT / "artifacts" / "explicit_bijection_decomposition.json").read_text()
    )
    edge_to_root_idx = {int(k): v for k, v in edge_map["edge_to_root_index"].items()}
    root_coords = [tuple(r) for r in edge_map["root_coords"]]

    # Z3 phase: f(x) = x4 (last coordinate) on normalized F3^4 point
    def phase(v):
        return v[3] % 3

    # Collect balanced edges and associated roots
    bal_edges = []
    roots = []
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info and info["orbit_size"] == 27 and info["orbit_id"] == balanced_orbit:
            bal_edges.append(e)
            roots.append(np.array([x / 2.0 for x in r], dtype=float))

    # Color each balanced edge by phase sum
    colors = []
    for i, j in bal_edges:
        c = (phase(points[i]) + phase(points[j])) % 3
        colors.append(int(c))

    color_counts = Counter(colors)

    # Build adjacency on balanced root graph (inner product 1)
    n = len(roots)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if abs(float(np.dot(roots[i], roots[j])) - 1.0) < 1e-6:
                adj[i, j] = adj[j, i] = 1

    # Count edges between colors
    color_edges = Counter()
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j] == 1:
                key = tuple(sorted((colors[i], colors[j])))
                color_edges[key] += 1

    # Internal adjacency per color class
    internal = Counter()
    for c in [0, 1, 2]:
        idx = [i for i in range(n) if colors[i] == c]
        count = 0
        for i, j in combinations(idx, 2):
            if adj[i, j] == 1:
                count += 1
        internal[c] = count

    results = {
        "balanced_orbit_id": balanced_orbit,
        "color_counts": dict(color_counts),
        "color_edge_counts": {str(k): v for k, v in sorted(color_edges.items())},
        "internal_edges_per_color": dict(internal),
    }

    out_path = ROOT / "artifacts" / "balanced_orbit_color_graph.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
