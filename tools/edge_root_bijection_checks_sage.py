#!/usr/bin/env python3
"""Sage: check edge->root bijection statistics using E8 bilinear form.

Uses artifacts/edge_to_e8_root.json (root coordinates in Sage simple-root basis).
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import product
from pathlib import Path

from sage.all import RootSystem

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
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if omega(proj_points[i], proj_points[j]) == 0:
                edges.append((i, j))
    return edges


def main():
    edge_to_root = json.loads((ROOT / "artifacts" / "edge_to_e8_root.json").read_text())
    edges = build_w33_edges()

    # Build E8 root lattice and Cartan matrix (Gram in simple-root basis)
    R = RootSystem(["E", 8]).root_lattice()
    C = R.cartan_type().cartan_matrix()

    # map edge->root element
    edge_map = {}
    for k, v in edge_to_root.items():
        i, j = k.strip("() ").split(",")
        e = tuple(sorted((int(i), int(j))))
        coeffs = list(map(int, v))
        edge_map[e] = coeffs

    adj_ips = Counter()
    nonadj_ips = Counter()

    # build edge adjacency list (share a vertex)
    edge_adj = {e: [] for e in edges}
    for idx in range(len(edges)):
        e1 = edges[idx]
        s1 = set(e1)
        for jdx in range(idx + 1, len(edges)):
            e2 = edges[jdx]
            if s1 & set(e2):
                edge_adj[e1].append(e2)
                edge_adj[e2].append(e1)

    n = len(edges)
    for idx in range(n):
        e1 = edges[idx]
        r1 = edge_map[e1]
        s1 = set(e1)
        for jdx in range(idx + 1, n):
            e2 = edges[jdx]
            r2 = edge_map[e2]
            s2 = set(e2)
            # inner product in simple-root basis: r^T C s
            ip = int(sum(r1[i] * C[i, j] * r2[j] for i in range(8) for j in range(8)))
            if s1 & s2:
                adj_ips[ip] += 1
            else:
                nonadj_ips[ip] += 1

    # Per-edge adjacent inner-product counts
    per_edge_ip_counts = []
    for e1 in edges:
        r1 = edge_map[e1]
        counts = Counter()
        for e2 in edge_adj[e1]:
            r2 = edge_map[e2]
            ip = int(sum(r1[i] * C[i, j] * r2[j] for i in range(8) for j in range(8)))
            counts[ip] += 1
        per_edge_ip_counts.append(tuple(sorted(counts.items())))

    per_edge_dist = Counter(per_edge_ip_counts)

    stats = {
        "adjacent_edge_ip_counts": dict(sorted(adj_ips.items())),
        "nonadjacent_edge_ip_counts": dict(sorted(nonadj_ips.items())),
        "per_edge_adjacent_ip_profile_counts": {
            str(k): v for k, v in per_edge_dist.items()
        },
    }

    out_path = ROOT / "artifacts" / "edge_root_bijection_stats_sage.json"
    out_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print("Wrote", out_path)
    print("Adjacent IPs:", dict(sorted(adj_ips.items())))
    print("Nonadjacent IPs:", dict(sorted(nonadj_ips.items())))
    print("Per-edge adjacent IP profile classes:", len(per_edge_dist))


if __name__ == "__main__":
    main()
