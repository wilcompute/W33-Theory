#!/usr/bin/env python3
"""Compute Bargmann phase on W33 K4 cliques using a C^4 embedding.

We embed F3^4 projective points into C^4 via omega^x mapping
and compute Bargmann invariant for each 4-clique (line) in W33.
"""
from __future__ import annotations

import json
import itertools
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_w33():
    F3 = [0, 1, 2]
    vectors = [v for v in itertools.product(F3, repeat=4) if any(x != 0 for x in v)]

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

    n = len(proj_points)

    def omega(x, y):
        return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3

    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if omega(proj_points[i], proj_points[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    return proj_points, adj


def embed_rays(proj_points):
    omega = np.exp(2j * np.pi / 3)
    rays = []
    for p in proj_points:
        v = np.array([omega ** x for x in p], dtype=complex)
        v = v / np.linalg.norm(v)
        rays.append(v)
    return rays


def bargmann_phase(v1, v2, v3, v4):
    prod = np.vdot(v1, v2) * np.vdot(v2, v3) * np.vdot(v3, v4) * np.vdot(v4, v1)
    if abs(prod) < 1e-12:
        return None
    return prod / abs(prod)


def find_k4s(adj):
    n = adj.shape[0]
    k4s = []
    for a, b, c, d in itertools.combinations(range(n), 4):
        if (adj[a, b] and adj[a, c] and adj[a, d] and
                adj[b, c] and adj[b, d] and adj[c, d]):
            k4s.append((a, b, c, d))
    return k4s


def main():
    proj_points, adj = construct_w33()
    rays = embed_rays(proj_points)

    k4s = find_k4s(adj)

    print("W33 K4 Bargmann phase")
    print("=" * 40)
    print(f"Vertices: {len(proj_points)}")
    print(f"K4 cliques: {len(k4s)}")

    phases = []
    for k4 in k4s:
        # Use canonical order (sorted)
        a, b, c, d = k4
        ph = bargmann_phase(rays[a], rays[b], rays[c], rays[d])
        if ph is not None:
            phases.append(ph)

    angles = [round(float(np.angle(p)), 6) for p in phases]
    from collections import Counter
    counts = Counter(angles)

    print("Phase distribution (radians):")
    for ang, count in sorted(counts.items()):
        print(f"  {ang}: {count}")

    result = {
        "k4_count": len(k4s),
        "phase_distribution": {str(k): v for k, v in sorted(counts.items())},
    }

    out_path = ROOT / "artifacts" / "w33_k4_bargmann_phase.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
