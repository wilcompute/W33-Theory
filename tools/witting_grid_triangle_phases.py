#!/usr/bin/env python3
"""Triangle phase distribution for the naive F3^4 omega-grid rays.

This tests whether the naive grid rays are unitarily equivalent to the Witting rays
by comparing Pancharatnam phase clustering.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_f3_grid_rays():
    omega = np.exp(2j * np.pi / 3)
    rays = []
    F3 = [0, 1, 2]
    seen = set()
    for a in F3:
        for b in F3:
            for c in F3:
                for d in F3:
                    if a == b == c == d == 0:
                        continue
                    v = np.array(
                        [omega**a, omega**b, omega**c, omega**d], dtype=complex
                    )
                    idx = next(i for i, z in enumerate(v) if abs(z) > 1e-12)
                    v = v / v[idx]
                    key = tuple(np.round(v, 6))
                    if key in seen:
                        continue
                    seen.add(key)
                    v = v / np.linalg.norm(v)
                    rays.append(v)
    return rays


def wrap_angle(a):
    return np.arctan2(np.sin(a), np.cos(a))


def phase_cluster(a):
    a = wrap_angle(a)
    targets = [np.pi / 6, -np.pi / 6, np.pi / 2, -np.pi / 2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def main():
    rays = construct_f3_grid_rays()
    n = len(rays)

    # check orthonormal bases count
    orth = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.vdot(rays[i], rays[j])) < 1e-8:
                orth[i][j] = orth[j][i] = 1

    bases = 0
    for i in range(n):
        for j in range(i + 1, n):
            if not orth[i][j]:
                continue
            candidates = [k for k in range(n) if orth[i][k] and orth[j][k]]
            for k, l in itertools.combinations(candidates, 2):
                if orth[k][l]:
                    bases += 1
    bases //= 6  # each basis counted 6 times

    clusters = Counter()
    triples = 0
    for i, j, k in itertools.combinations(range(n), 3):
        ip_ij = np.vdot(rays[i], rays[j])
        ip_jk = np.vdot(rays[j], rays[k])
        ip_ik = np.vdot(rays[i], rays[k])
        if abs(ip_ij) < 1e-8 or abs(ip_jk) < 1e-8 or abs(ip_ik) < 1e-8:
            continue
        triples += 1
        prod = ip_ij * ip_jk * np.conjugate(ip_ik)
        if abs(prod) < 1e-12:
            continue
        clusters[phase_cluster(np.angle(prod))] += 1

    out = {
        "rays": n,
        "bases": bases,
        "triples": triples,
        "clusters": {str(k): v for k, v in sorted(clusters.items())},
    }

    out_path = ROOT / "artifacts" / "witting_grid_triangle_phases.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_grid_triangle_phases.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Naive F3^4 Grid Triangle Phases\n\n")
        f.write(f"Grid rays: **{n}**\n")
        f.write(f"Orthonormal bases: **{bases}**\n")
        f.write(f"Non‑orthogonal triples: **{triples}**\n\n")
        f.write("cluster (rad) | count\n")
        f.write("--- | ---\n")
        for k, v in sorted(clusters.items()):
            f.write(f"{k} | {v}\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
