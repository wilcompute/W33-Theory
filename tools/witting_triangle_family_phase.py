#!/usr/bin/env python3
"""Triangle phase distribution by family composition.

We classify each non-orthogonal triangle by the multiset of family labels
(B, F0..F3) and tabulate the Pancharatnam phase cluster (±pi/6, ±pi/2).
"""

from __future__ import annotations

import itertools
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


def phase_cluster(angle):
    a = wrap_angle(angle)
    targets = [np.pi / 6, -np.pi / 6, np.pi / 2, -np.pi / 2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def main():
    rays, labels = construct_witting_40_rays_with_labels()
    n = len(rays)

    table = defaultdict(Counter)
    total = 0
    for i, j, k in itertools.combinations(range(n), 3):
        ip_ij = np.vdot(rays[i], rays[j])
        ip_jk = np.vdot(rays[j], rays[k])
        ip_ik = np.vdot(rays[i], rays[k])
        if abs(ip_ij) < 1e-8 or abs(ip_jk) < 1e-8 or abs(ip_ik) < 1e-8:
            continue
        prod = ip_ij * ip_jk * np.conjugate(ip_ik)
        if abs(prod) < 1e-12:
            continue
        total += 1
        ph = phase_cluster(np.angle(prod))
        fams = sorted([labels[i][0], labels[j][0], labels[k][0]])
        key = tuple(fams)
        table[key][ph] += 1

    # keep top patterns by total count
    totals = sorted(
        [(k, sum(v.values())) for k, v in table.items()], key=lambda x: -x[1]
    )
    top = totals[:12]

    out = {
        "triples": total,
        "top_patterns": [
            {
                "pattern": list(k),
                "total": t,
                "clusters": {str(p): n for p, n in sorted(table[k].items())},
            }
            for k, t in top
        ],
    }

    out_path = ROOT / "artifacts" / "witting_triangle_family_phase.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_triangle_family_phase.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Triangle Phase by Family Composition\n\n")
        f.write(f"Non‑orthogonal triangles: **{total}**\n\n")
        f.write("## Top family patterns\n\n")
        f.write("pattern | total | clusters\n")
        f.write("--- | --- | ---\n")
        for item in out["top_patterns"]:
            pat = item["pattern"]
            total_c = item["total"]
            clusters = ", ".join(f"{k}:{v}" for k, v in item["clusters"].items())
            f.write(f"{pat} | {total_c} | {clusters}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
