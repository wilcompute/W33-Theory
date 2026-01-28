#!/usr/bin/env python3
"""Compute Pancharatnam (Bargmann) phase for non-orthogonal triangles in Witting 40 rays.

Observed quantization clusters at ±π/6 and ±π/2.
We compute phase of <a|b><b|c><c|a> for all triples where all overlaps are nonzero.
"""
from __future__ import annotations

import json
import itertools
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def phase_triangle(a, b, c):
    prod = np.vdot(a, b) * np.vdot(b, c) * np.vdot(c, a)
    if abs(prod) < 1e-12:
        return None
    return prod / abs(prod)


def main():
    rays = construct_witting_40_rays()
    n = len(rays)

    phases = []
    for i, j, k in itertools.combinations(range(n), 3):
        # require all overlaps nonzero
        if abs(np.vdot(rays[i], rays[j])) < 1e-8:
            continue
        if abs(np.vdot(rays[j], rays[k])) < 1e-8:
            continue
        if abs(np.vdot(rays[k], rays[i])) < 1e-8:
            continue
        ph = phase_triangle(rays[i], rays[j], rays[k])
        if ph is not None:
            phases.append(np.angle(ph))

    # Cluster phases around observed quantization targets: ±pi/6, ±pi/2
    clusters = Counter()
    for ang in phases:
        # wrap to (-pi, pi]
        a = np.arctan2(np.sin(ang), np.cos(ang))
        targets = [np.pi/6, -np.pi/6, np.pi/2, -np.pi/2]
        nearest = min(targets, key=lambda t: abs(a - t))
        clusters[round(float(nearest), 6)] += 1

    raw_counts = Counter(round(float(np.arctan2(np.sin(a), np.cos(a))), 6) for a in phases)

    print("Witting Pancharatnam triangle phases")
    print("=" * 45)
    print(f"Triples analyzed: {len(phases)}")
    print("Nearest cluster counts (targets: ±pi/6, ±pi/2):")
    for k, v in sorted(clusters.items()):
        print(f"  {k}: {v}")

    out_path = ROOT / "artifacts" / "witting_pancharatnam_triangles.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(
            {
                "triples": len(phases),
                "clusters": {str(k): v for k, v in sorted(clusters.items())},
                "raw_phase_counts": {str(k): v for k, v in sorted(raw_counts.items())},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
