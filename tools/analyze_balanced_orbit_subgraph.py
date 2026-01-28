#!/usr/bin/env python3
"""Analyze the induced line-graph structure on the balanced 27-edge orbit."""

from __future__ import annotations

import json
from collections import Counter, deque
from itertools import product
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

    # Load root labels and edge->root map
    we6 = json.loads((ROOT / "artifacts" / "we6_orbit_labels.json").read_text())
    root_to_orbit = {eval(k): v for k, v in we6["mapping"].items()}
    edge_map = json.loads(
        (ROOT / "artifacts" / "explicit_bijection_decomposition.json").read_text()
    )
    edge_to_root_idx = {int(k): v for k, v in edge_map["edge_to_root_index"].items()}
    root_coords = [tuple(r) for r in edge_map["root_coords"]]

    # Balanced edge indices
    balanced_indices = []
    for e in edges:
        eidx = edge_to_idx[tuple(sorted(e))]
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        info = root_to_orbit.get(r)
        if info and info["orbit_size"] == 27 and info["orbit_id"] == balanced_orbit:
            balanced_indices.append(eidx)

    # Build induced line-graph on these 27 edges
    n = len(balanced_indices)
    idx_to_edge = [edges[i] for i in balanced_indices]
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        a, b = idx_to_edge[i]
        for j in range(i + 1, n):
            c, d = idx_to_edge[j]
            if a == c or a == d or b == c or b == d:
                adj[i, j] = adj[j, i] = 1

    degrees = adj.sum(axis=1)
    degree_dist = Counter(int(d) for d in degrees)

    # Connected components
    seen = set()
    comps = []
    for i in range(n):
        if i in seen:
            continue
        comp = {i}
        dq = deque([i])
        seen.add(i)
        while dq:
            u = dq.popleft()
            for v in np.where(adj[u] == 1)[0]:
                if v not in seen:
                    seen.add(v)
                    comp.add(v)
                    dq.append(v)
        comps.append(sorted(comp))

    # Classify edges by shell (relative to v0=0)
    v0 = 0
    # Build adjacency for shell split
    # We only need H12/H27 for this fixed base
    # Rebuild adjacency quickly
    F3 = [0, 1, 2]
    vectors = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]
    proj_points = []
    seen2 = set()
    for v in vectors:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 1 if v[i] == 1 else 2
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen2:
            seen2.add(v)
            proj_points.append(v)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj_w33 = [[0] * 40 for _ in range(40)]
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj_w33[i][j] = adj_w33[j][i] = 1

    H12 = {j for j in range(40) if adj_w33[v0][j] == 1}
    H27 = {j for j in range(40) if j != v0 and adj_w33[v0][j] == 0}

    # Root type for each balanced edge
    edge_root_type = {}
    for i, eidx in enumerate(balanced_indices):
        ridx = edge_to_root_idx[eidx]
        r = root_coords[ridx]
        has_odd = any(abs(x) % 2 == 1 for x in r)
        edge_root_type[i] = "half" if has_odd else "integral"

    comp_summaries = []
    for comp in comps:
        shell_counts = Counter()
        root_counts = Counter()
        comp_degrees = []
        comp_edges = []
        for local_idx in comp:
            a, b = idx_to_edge[local_idx]
            if a in H27 and b in H27:
                shell_counts["H27-H27"] += 1
            elif (a in H12 and b in H27) or (a in H27 and b in H12):
                shell_counts["H12-H27"] += 1
            elif a in H12 and b in H12:
                shell_counts["H12-H12"] += 1
            elif a == v0 or b == v0:
                shell_counts["v0"] += 1
            else:
                shell_counts["other"] += 1
            root_counts[edge_root_type[local_idx]] += 1
            comp_degrees.append(int(degrees[local_idx]))
            comp_edges.append((a, b, points[a], points[b], edge_root_type[local_idx]))
        # If component is tiny, record its internal adjacency
        comp_adj = None
        if len(comp) <= 4:
            comp_list = [int(x) for x in comp]
            comp_adj = [[int(adj[i, j]) for j in comp_list] for i in comp_list]
        comp_summaries.append(
            {
                "size": len(comp),
                "shell_counts": dict(shell_counts),
                "root_types": dict(root_counts),
                "degree_dist": dict(Counter(comp_degrees)),
                "adjacency": comp_adj,
                "edges": comp_edges if len(comp) <= 3 else None,
                "nodes": comp_list if len(comp) <= 3 else None,
            }
        )

    # Spectrum
    eigvals = np.linalg.eigvalsh(adj)
    eigvals_rounded = [round(x, 6) for x in eigvals]
    eigval_counts = Counter(eigvals_rounded)

    results = {
        "balanced_orbit_id": balanced_orbit,
        "edge_count": n,
        "degree_distribution": dict(sorted(degree_dist.items())),
        "component_sizes": sorted([len(c) for c in comps], reverse=True),
        "component_summaries": comp_summaries,
        "spectrum_counts": {str(k): v for k, v in sorted(eigval_counts.items())},
    }

    out_path = ROOT / "artifacts" / "balanced_orbit_subgraph.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(results)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
