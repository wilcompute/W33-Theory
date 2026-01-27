#!/usr/bin/env python3
"""Check structural statistics of the explicit edge->root bijection.

Uses:
- artifacts/edge_to_e8_root.json (edge->root in simple-root basis)
- W33 edge adjacency (edges share a vertex)
- E8 inner product using Cartan matrix

Outputs:
- artifacts/edge_root_bijection_stats.json
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def build_w33_edges():
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
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i+1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))
    return edges


def cartan_e8():
    # E8 Cartan matrix in simple-root basis
    return [
        [ 2, -1,  0,  0,  0,  0,  0,  0],
        [-1,  2, -1,  0,  0,  0,  0,  0],
        [ 0, -1,  2, -1,  0,  0,  0, -1],
        [ 0,  0, -1,  2, -1,  0,  0,  0],
        [ 0,  0,  0, -1,  2, -1,  0,  0],
        [ 0,  0,  0,  0, -1,  2, -1,  0],
        [ 0,  0,  0,  0,  0, -1,  2,  0],
        [ 0,  0, -1,  0,  0,  0,  0,  2],
    ]


def ip_e8(r, s, C):
    # r,s are length-8 integer tuples in simple-root basis
    # inner product = r^T C s
    total = 0
    for i in range(8):
        for j in range(8):
            total += r[i] * C[i][j] * s[j]
    return total


def main():
    edge_to_root = json.loads((ROOT / "artifacts" / "edge_to_e8_root.json").read_text())
    edges = build_w33_edges()
    C = cartan_e8()

    # Normalize edge keys
    edge_map = {}
    for k, v in edge_to_root.items():
        # k like "(i, j)"
        i, j = k.strip("() ").split(",")
        e = tuple(sorted((int(i), int(j))))
        edge_map[e] = tuple(v)

    # adjacency: share a vertex
    edge_adj_ips = Counter()
    edge_nonadj_ips = Counter()

    edges_list = edges
    n = len(edges_list)

    for idx in range(n):
        e1 = edges_list[idx]
        r1 = edge_map[e1]
        s1 = set(e1)
        for jdx in range(idx + 1, n):
            e2 = edges_list[jdx]
            r2 = edge_map[e2]
            s2 = set(e2)
            ip = ip_e8(r1, r2, C)
            if s1 & s2:
                edge_adj_ips[ip] += 1
            else:
                edge_nonadj_ips[ip] += 1

    stats = {
        "adjacent_edge_ip_counts": dict(sorted(edge_adj_ips.items())),
        "nonadjacent_edge_ip_counts": dict(sorted(edge_nonadj_ips.items())),
    }

    out_path = ROOT / "artifacts" / "edge_root_bijection_stats.json"
    out_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print("Wrote", out_path)
    print("Adjacent IPs:", dict(sorted(edge_adj_ips.items())))
    print("Nonadjacent IPs:", dict(sorted(edge_nonadj_ips.items())))


if __name__ == "__main__":
    main()
