#!/usr/bin/env python3
"""Recompute phase vs symplectic invariants using an explicit graph isomorphism.

We load the ray→F3 mapping from artifacts/witting_graph_isomorphism.json and
recompute ω invariants for pairs/triangles, then tabulate phase clusters.
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


def construct_f3_points():
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
    return proj_points


def omega_symp(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def phase_cluster(angle):
    a = np.arctan2(np.sin(angle), np.cos(angle))
    targets = [np.pi / 6, -np.pi / 6, np.pi / 2, -np.pi / 2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def main():
    rays = construct_witting_40_rays()
    f3_points = construct_f3_points()

    mapping_path = ROOT / "artifacts" / "witting_graph_isomorphism.json"
    mapping = json.loads(mapping_path.read_text())["mapping"]
    mapping = {int(k): int(v) for k, v in mapping.items()}

    # precompute overlaps
    n = len(rays)
    overlap = {}
    for i in range(n):
        for j in range(i + 1, n):
            overlap[(i, j)] = np.vdot(rays[i], rays[j])

    # triangle table
    tables = {
        "omega_counts": defaultdict(Counter),
        "omega_product": defaultdict(Counter),
        "omega_multiset": defaultdict(Counter),
    }
    triples = 0
    for i, j, k in itertools.combinations(range(n), 3):
        ip_ij = overlap[(i, j)]
        ip_jk = overlap[(j, k)]
        ip_ik = overlap[(i, k)]
        if abs(ip_ij) < 1e-8 or abs(ip_jk) < 1e-8 or abs(ip_ik) < 1e-8:
            continue
        triples += 1
        prod = ip_ij * ip_jk * np.conjugate(ip_ik)
        if abs(prod) < 1e-12:
            continue
        cluster = phase_cluster(np.angle(prod))

        p_i = f3_points[mapping[i]]
        p_j = f3_points[mapping[j]]
        p_k = f3_points[mapping[k]]

        w12 = omega_symp(p_i, p_j)
        w23 = omega_symp(p_j, p_k)
        w31 = omega_symp(p_k, p_i)

        c1 = sum(1 for w in (w12, w23, w31) if w == 1)
        c2 = 3 - c1
        prod_sign = (
            (1 if w12 == 1 else -1) * (1 if w23 == 1 else -1) * (1 if w31 == 1 else -1)
        )
        multiset = tuple(sorted([w12, w23, w31]))

        tables["omega_counts"][(c1, c2)][cluster] += 1
        tables["omega_product"][prod_sign][cluster] += 1
        tables["omega_multiset"][multiset][cluster] += 1

    out = {
        "triples": triples,
        "omega_counts": {
            str(k): {str(c): n for c, n in sorted(v.items())}
            for k, v in tables["omega_counts"].items()
        },
        "omega_product": {
            str(k): {str(c): n for c, n in sorted(v.items())}
            for k, v in tables["omega_product"].items()
        },
        "omega_multiset": {
            str(k): {str(c): n for c, n in sorted(v.items())}
            for k, v in tables["omega_multiset"].items()
        },
    }

    out_path = ROOT / "artifacts" / "witting_phase_symplectic_mapped.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_phase_symplectic_mapped.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Phase vs Symplectic Invariants (Mapped)\n\n")
        f.write(f"Non‑orthogonal triples analyzed: **{triples}**\n\n")
        f.write("## ω counts (number of ω=1 vs ω=2)\n\n")
        f.write("counts (c1,c2) | clusters\n")
        f.write("--- | ---\n")
        for k in sorted(tables["omega_counts"].keys()):
            clusters = ", ".join(
                f"{c}:{n}" for c, n in sorted(tables["omega_counts"][k].items())
            )
            f.write(f"{k} | {clusters}\n")
        f.write("\n## ω product sign\n\n")
        f.write("prod_sign | clusters\n")
        f.write("--- | ---\n")
        for k in sorted(tables["omega_product"].keys()):
            clusters = ", ".join(
                f"{c}:{n}" for c, n in sorted(tables["omega_product"][k].items())
            )
            f.write(f"{k} | {clusters}\n")
        f.write("\n## ω multiset\n\n")
        f.write("multiset | clusters\n")
        f.write("--- | ---\n")
        for k in sorted(tables["omega_multiset"].keys()):
            clusters = ", ".join(
                f"{c}:{n}" for c, n in sorted(tables["omega_multiset"][k].items())
            )
            f.write(f"{k} | {clusters}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
