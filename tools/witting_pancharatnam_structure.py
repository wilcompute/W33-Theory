#!/usr/bin/env python3
"""Analyze structure of Pancharatnam phase clusters for Witting rays.

We classify non-orthogonal ray triples by:
  - basis_count: number of basis rays (3 zeros) in the triple
  - overlap pattern: sorted tuple of |<ri|rj>|^2 for the three pairs
Then we tabulate phase cluster counts for targets ±pi/6 and ±pi/2.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict
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


def basis_count(ray):
    # basis rays have 3 zeros
    return sum(1 for x in ray if abs(x) < 1e-12)


def phase_cluster(angle):
    a = np.arctan2(np.sin(angle), np.cos(angle))
    targets = [np.pi / 6, -np.pi / 6, np.pi / 2, -np.pi / 2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def main():
    rays = construct_witting_40_rays()
    n = len(rays)

    # Precompute overlaps
    overlap = {}
    for i in range(n):
        for j in range(i + 1, n):
            ip = np.vdot(rays[i], rays[j])
            overlap[(i, j)] = ip

    basis_flags = [1 if basis_count(r) == 3 else 0 for r in rays]

    by_basis = defaultdict(Counter)
    by_pattern = defaultdict(Counter)
    total_clusters = Counter()

    triples = 0
    for i, j, k in itertools.combinations(range(n), 3):
        # require all overlaps nonzero
        ip_ij = overlap[(i, j)]
        ip_jk = overlap[(j, k)]
        ip_ik = overlap[(i, k)]
        if abs(ip_ij) < 1e-8 or abs(ip_jk) < 1e-8 or abs(ip_ik) < 1e-8:
            continue

        triples += 1
        prod = ip_ij * ip_jk * ip_ik.conjugate()
        if abs(prod) < 1e-12:
            continue
        ang = np.angle(prod)
        cluster = phase_cluster(ang)
        total_clusters[cluster] += 1

        bcount = basis_flags[i] + basis_flags[j] + basis_flags[k]
        by_basis[bcount][cluster] += 1

        mags = sorted(
            [
                round(float(abs(ip_ij) ** 2), 6),
                round(float(abs(ip_jk) ** 2), 6),
                round(float(abs(ip_ik) ** 2), 6),
            ]
        )
        by_pattern[tuple(mags)][cluster] += 1

    # Summarize top overlap patterns
    pattern_totals = {k: sum(v.values()) for k, v in by_pattern.items()}
    top_patterns = sorted(pattern_totals.items(), key=lambda kv: -kv[1])[:10]

    out = {
        "triples": triples,
        "clusters": {str(k): v for k, v in sorted(total_clusters.items())},
        "by_basis": {
            str(k): {str(c): n for c, n in sorted(v.items())}
            for k, v in by_basis.items()
        },
        "by_pattern_top": [
            {
                "pattern": list(pat),
                "total": total,
                "clusters": {str(c): n for c, n in sorted(by_pattern[pat].items())},
            }
            for pat, total in top_patterns
        ],
    }

    out_path = ROOT / "artifacts" / "witting_pancharatnam_structure.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_pancharatnam_structure.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting Pancharatnam Phase Structure\n\n")
        f.write(f"Non‑orthogonal triples analyzed: **{triples}**\n\n")
        f.write("## Cluster counts (targets ±π/6, ±π/2)\n\n")
        f.write("cluster (rad) | count\n")
        f.write("--- | ---\n")
        for c, ncount in sorted(total_clusters.items()):
            f.write(f"{c} | {ncount}\n")
        f.write("\n## By basis‑ray count\n\n")
        f.write("basis rays in triple | clusters\n")
        f.write("--- | ---\n")
        for bcount in sorted(by_basis.keys()):
            clusters = ", ".join(
                f"{c}:{n}" for c, n in sorted(by_basis[bcount].items())
            )
            f.write(f"{bcount} | {clusters}\n")
        f.write("\n## Top overlap‑magnitude patterns\n\n")
        f.write("pattern (|<ri|rj>|²) | total | cluster counts\n")
        f.write("--- | --- | ---\n")
        for item in out["by_pattern_top"]:
            pat = item["pattern"]
            total = item["total"]
            clusters = ", ".join(f"{k}:{v}" for k, v in item["clusters"].items())
            f.write(f"{pat} | {total} | {clusters}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
