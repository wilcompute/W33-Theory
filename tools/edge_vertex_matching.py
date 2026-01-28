#!/usr/bin/env python3
"""Find a perfect matching between W33 edges (240) and Witting vertices (40*6).

Each W33 edge connects two rays; each ray has 6 phase vertices. This is a
bipartite graph where each edge node connects to 12 vertex nodes (6+6).
We find a perfect matching to obtain an explicit bijection edge -> (ray, phase).
"""

from __future__ import annotations

import json
from collections import defaultdict, deque
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


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
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def build_edges(proj_points):
    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega_sym(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))
    return edges


# Hopcroft-Karp for bipartite matching


def hopcroft_karp(adj, n_left, n_right):
    """adj: list of lists; adj[u] gives list of v in right."""
    INF = 10**9
    pair_u = [-1] * n_left
    pair_v = [-1] * n_right
    dist = [0] * n_left

    def bfs():
        q = deque()
        for u in range(n_left):
            if pair_u[u] == -1:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        d_augment = INF
        while q:
            u = q.popleft()
            if dist[u] < d_augment:
                for v in adj[u]:
                    if pair_v[v] == -1:
                        d_augment = dist[u] + 1
                    elif dist[pair_v[v]] == INF:
                        dist[pair_v[v]] = dist[u] + 1
                        q.append(pair_v[v])
        return d_augment != INF

    def dfs(u):
        for v in adj[u]:
            if pair_v[v] == -1 or (dist[pair_v[v]] == dist[u] + 1 and dfs(pair_v[v])):
                pair_u[u] = v
                pair_v[v] = u
                return True
        dist[u] = 10**9
        return False

    matching = 0
    while bfs():
        for u in range(n_left):
            if pair_u[u] == -1 and dfs(u):
                matching += 1
    return matching, pair_u, pair_v


def main():
    proj_points = build_projective_points()
    edges = build_edges(proj_points)

    # Right side: vertices (ray, phase) -> index
    right_index = {}
    right_nodes = []
    for ray in range(40):
        for phase in range(6):
            idx = len(right_nodes)
            right_index[(ray, phase)] = idx
            right_nodes.append((ray, phase))

    # Build adjacency: each edge connects to 6 phases on each endpoint
    adj = [[] for _ in range(len(edges))]
    for e_idx, (i, j) in enumerate(edges):
        for phase in range(6):
            adj[e_idx].append(right_index[(i, phase)])
            adj[e_idx].append(right_index[(j, phase)])

    # Run matching
    matching, pair_u, pair_v = hopcroft_karp(adj, len(edges), len(right_nodes))

    print(f"Edges: {len(edges)}  Vertices: {len(right_nodes)}  Matching: {matching}")
    if matching != len(edges):
        print("No perfect matching found.")
        return

    # Build mapping edge -> (ray, phase)
    mapping = []
    for e_idx, v_idx in enumerate(pair_u):
        ray, phase = right_nodes[v_idx]
        mapping.append(
            {
                "edge_index": e_idx,
                "edge": edges[e_idx],
                "ray": ray,
                "phase": phase,
            }
        )

    # Check ray usage distribution
    ray_counts = defaultdict(int)
    for m in mapping:
        ray_counts[m["ray"]] += 1

    phase_counts = defaultdict(int)
    for m in mapping:
        phase_counts[(m["ray"], m["phase"])] += 1

    print(f"Ray usage min/max: {min(ray_counts.values())}/{max(ray_counts.values())}")
    print(
        f"Ray usage histogram: {dict(sorted((k, list(ray_counts.values()).count(k)) for k in set(ray_counts.values())))}"
    )
    ones = sum(1 for v in phase_counts.values() if v == 1)
    zeros = 40 * 6 - ones
    maxc = max(phase_counts.values())
    print(f"Ray-phase usage: ones={ones} zeros={zeros} max={maxc}")

    # Save mapping
    out = {
        "edges": len(edges),
        "vertices": len(right_nodes),
        "matching": matching,
        "mapping": mapping,
    }
    out_path = ROOT / "artifacts" / "edge_vertex_matching.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
