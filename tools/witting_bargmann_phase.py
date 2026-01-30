#!/usr/bin/env python3
"""Compute Bargmann (Pancharatnam) phase on Witting tetrads.

For each orthonormal tetrad (basis) from Witting 40 rays,
compute phase of product <v1|v2><v2|v3><v3|v4><v4|v1>.
"""

from __future__ import annotations

import json
from itertools import combinations, permutations
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
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
    return rays


def orthogonal(v1, v2, tol=1e-8):
    return abs(np.vdot(v1, v2)) < tol


def find_tetrads(rays):
    n = len(rays)
    ortho = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if orthogonal(rays[i], rays[j]):
                ortho[i, j] = ortho[j, i] = True
    tetrads = []
    for a, b, c, d in combinations(range(n), 4):
        if (
            ortho[a, b]
            and ortho[a, c]
            and ortho[a, d]
            and ortho[b, c]
            and ortho[b, d]
            and ortho[c, d]
        ):
            tetrads.append((a, b, c, d))
    return tetrads


def bargmann_phase(v1, v2, v3, v4):
    prod = np.vdot(v1, v2) * np.vdot(v2, v3) * np.vdot(v3, v4) * np.vdot(v4, v1)
    # Normalize to unit complex (phase)
    if abs(prod) < 1e-12:
        return None
    return prod / abs(prod)


def main():
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)

    print("Witting Bargmann phase analysis")
    print("=" * 45)
    print(f"Rays: {len(rays)}")
    print(f"Tetrads: {len(tetrads)}")

    phases = []
    for tet in tetrads:
        # Use canonical order (sorted) and its cyclic permutations
        order = list(tet)
        v = [rays[i] for i in order]
        ph = bargmann_phase(v[0], v[1], v[2], v[3])
        if ph is not None:
            phases.append(ph)

    # Cluster phases by angle
    angles = [np.angle(p) for p in phases]
    # Round angles to 1e-3
    rounded = [round(a, 3) for a in angles]

    from collections import Counter

    counts = Counter(rounded)

    print("Phase distribution (radians, rounded to 1e-3):")
    for ang, count in sorted(counts.items()):
        print(f"  {ang}: {count}")

    result = {
        "tetrads": len(tetrads),
        "phases": {str(k): v for k, v in sorted(counts.items())},
    }

    out_path = ROOT / "artifacts" / "witting_bargmann_phase.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
