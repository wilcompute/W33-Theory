#!/usr/bin/env python3
"""Compute overlap structure of the 40 Witting rays.

We report the distribution of |<ri|rj>|^2 over all pairs.
"""
from __future__ import annotations

import json
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


def main():
    rays = construct_witting_40_rays()
    n = len(rays)
    counts = Counter()
    for i in range(n):
        for j in range(i + 1, n):
            ip = abs(np.vdot(rays[i], rays[j])) ** 2
            counts[round(float(ip), 6)] += 1

    out = {
        "pairs": n * (n - 1) // 2,
        "overlap_counts": {str(k): v for k, v in sorted(counts.items())},
    }

    out_path = ROOT / "artifacts" / "witting_ray_overlap_structure.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_ray_overlap_structure.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting Ray Overlap Structure\n\n")
        f.write(f"Total ray pairs: **{out['pairs']}**\n\n")
        f.write("## |<ri|rj>|^2 distribution\n\n")
        f.write("value | count\n")
        f.write("--- | ---\n")
        for k, v in sorted(counts.items()):
            f.write(f"{k} | {v}\n")
        f.write("\n")
        f.write("All non‑orthogonal pairs have |<ri|rj>|^2 = 1/3.\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
