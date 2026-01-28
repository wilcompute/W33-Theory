#!/usr/bin/env python3
"""Build a canonical edge->root bijection using Coxeter-6 orbits and matching.

Orbits correspond to W33 vertices (via orbit->F3 mapping). Each orbit has 6 roots
ordered by the Coxeter-6 cycle. We perform a deterministic perfect matching
between edges and (vertex,phase) pairs, then map to roots.
"""
from __future__ import annotations

import json
from collections import deque
from itertools import product
from pathlib import Path

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
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def build_edges(points):
    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega_sym(points[i], points[j]) == 0:
                edges.append((i, j))
    return edges


# Hopcroft-Karp for bipartite matching

def hopcroft_karp(adj, n_left, n_right):
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
    # Load Coxeter-6 orbits
    orbit_data = json.loads((ROOT / 'artifacts' / 'e8_coxeter6_orbits.json').read_text())
    orbits = orbit_data['orbits']  # list of 40 orbits, each 6 roots (simple-root coords)

    # Load orbit -> F3 point mapping
    f3_map = json.loads((ROOT / 'artifacts' / 'e8_orbit_to_f3_point.json').read_text())
    orbit_to_f3 = {int(k): tuple(v) for k, v in f3_map['mapping'].items()}

    # Build W33 points and edges
    points = build_projective_points()
    point_to_idx = {tuple(p): i for i, p in enumerate(points)}
    edges = build_edges(points)

    # Map orbits to vertex indices
    orbit_to_vertex = {orb: point_to_idx[orbit_to_f3[orb]] for orb in orbit_to_f3}

    # Build right side nodes: (vertex, phase)
    right_index = {}
    right_nodes = []
    for v in range(40):
        for phase in range(6):
            idx = len(right_nodes)
            right_index[(v, phase)] = idx
            right_nodes.append((v, phase))

    # Build adjacency: each edge connects to all 6 phases of each endpoint
    adj = [[] for _ in range(len(edges))]
    for e_idx, (i, j) in enumerate(edges):
        for phase in range(6):
            adj[e_idx].append(right_index[(i, phase)])
            adj[e_idx].append(right_index[(j, phase)])

    # Deterministic matching
    matching, pair_u, pair_v = hopcroft_karp(adj, len(edges), len(right_nodes))
    if matching != len(edges):
        raise RuntimeError("No perfect matching found")

    # Build edge->root mapping
    edge_to_root = []
    for e_idx, v_idx in enumerate(pair_u):
        v, phase = right_nodes[v_idx]
        # find which orbit corresponds to this vertex
        orb = next(k for k, vv in orbit_to_vertex.items() if vv == v)
        root = orbits[orb][phase]  # use phase index as orbit order
        edge_to_root.append({
            'edge_index': e_idx,
            'edge': edges[e_idx],
            'vertex': v,
            'orbit': orb,
            'phase': phase,
            'root': root,
        })

    out = {
        'edges': len(edges),
        'orbits': len(orbits),
        'edge_to_root': edge_to_root,
    }
    out_path = ROOT / 'artifacts' / 'edge_root_canonical_orbit_bijection.json'
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
