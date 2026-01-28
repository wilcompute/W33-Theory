#!/usr/bin/env python3
"""Tabulate pair-phase classes by ray family labels.

Families:
  B  : basis rays (4)
  F0 : (0,1,-w^mu,w^nu)/sqrt3
  F1 : (1,0,-w^mu,-w^nu)/sqrt3
  F2 : (1,-w^mu,0,w^nu)/sqrt3
  F3 : (1,w^mu,w^nu,0)/sqrt3

We compute phase classes (rounded to pi/6 grid) for non-orthogonal pairs
and tabulate by (family_i, family_j).
"""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_40_rays_with_labels():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    labels = []

    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
        labels.append(("B", -1, -1))

    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            labels.append(("F0", mu, nu))
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            labels.append(("F1", mu, nu))
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
            labels.append(("F2", mu, nu))
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
            labels.append(("F3", mu, nu))

    return rays, labels


def wrap_angle(a):
    return np.arctan2(np.sin(a), np.cos(a))


def phase_class(a):
    return round(float(wrap_angle(a)), 6)


def main():
    rays, labels = construct_witting_40_rays_with_labels()
    n = len(rays)

    table = defaultdict(Counter)
    for i in range(n):
        for j in range(i + 1, n):
            ip = np.vdot(rays[i], rays[j])
            if abs(ip) < 1e-8:
                continue
            ph = phase_class(np.angle(ip))
            fi = labels[i][0]
            fj = labels[j][0]
            key = tuple(sorted((fi, fj)))
            table[key][ph] += 1

    out = {
        "pairs_nonorth": sum(sum(c.values()) for c in table.values()),
        "table": {
            str(k): {str(p): n for p, n in sorted(v.items())} for k, v in table.items()
        },
    }

    out_path = ROOT / "artifacts" / "witting_pair_phase_family_table.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_pair_phase_family_table.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Pair‑Phase Classes by Ray Family\n\n")
        f.write(f"Non‑orthogonal pairs: **{out['pairs_nonorth']}**\n\n")
        for key in sorted(table.keys()):
            f.write(f"## {key}\n\n")
            f.write("phase (rad) | count\n")
            f.write("--- | ---\n")
            for p, cnt in sorted(table[key].items()):
                f.write(f"{p} | {cnt}\n")
            f.write("\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
