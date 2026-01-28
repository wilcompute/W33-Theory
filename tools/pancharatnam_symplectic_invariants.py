#!/usr/bin/env python3
"""Analyze Pancharatnam phase clusters vs symplectic invariants on F3^4.

We map each Witting ray to an F3^4 projective point by normalizing the ray
so its first nonzero entry is 1, then reading entries as cube‑root exponents.
Then, for each non‑orthogonal triangle, we compute:
  - phase cluster (±pi/6, ±pi/2)
  - ω12, ω23, ω31 in F3 (map to signs ±1)
  - counts of ω=1 vs ω=2
  - product sign of ω's
We tabulate contingency tables to see if phase cluster is predicted by any
simple symplectic invariant.
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


def f3_point_from_ray(ray, tol=1e-6):
    omega = np.exp(2j * np.pi / 3)
    roots = [1, omega, omega**2]

    # normalize by first nonzero entry
    idx = None
    for i, z in enumerate(ray):
        if abs(z) > tol:
            idx = i
            break
    if idx is None:
        raise ValueError("zero ray?")
    ray_n = ray / ray[idx]

    # rotate so first entry is closest cube root
    roots = [1, omega, omega**2]
    z0 = ray_n[idx]
    nearest = min(roots, key=lambda r: abs(z0 - r))
    factor = nearest / z0
    ray_n = ray_n * factor

    # square to remove overall sign ambiguity (−ω^k -> ω^{2k})
    ray_n = ray_n**2

    coords = []
    for z in ray_n:
        if abs(z) < tol:
            coords.append(0)
        else:
            # match to nearest cube root
            dists = [abs(z - r) for r in roots]
            k = int(np.argmin(dists))
            if dists[k] > 1e-3:
                # unexpected phase (should not happen after normalization)
                raise ValueError(f"unexpected phase {z}")
            coords.append(k)  # exponent 0,1,2
    return tuple(coords)


def omega_symp(x, y):
    return (x[0] * y[2] - x[2] * y[0] + x[1] * y[3] - x[3] * y[1]) % 3


def phase_cluster(angle):
    a = np.arctan2(np.sin(angle), np.cos(angle))
    targets = [np.pi / 6, -np.pi / 6, np.pi / 2, -np.pi / 2]
    nearest = min(targets, key=lambda t: abs(a - t))
    return round(float(nearest), 6)


def main():
    rays = construct_witting_40_rays()
    n = len(rays)

    # map rays to F3^4 points
    f3_pts = [f3_point_from_ray(r) for r in rays]

    # precompute overlaps
    overlap = {}
    for i in range(n):
        for j in range(i + 1, n):
            overlap[(i, j)] = np.vdot(rays[i], rays[j])

    tables = {
        "omega_counts": defaultdict(Counter),  # (c1,c2) -> cluster
        "omega_product": defaultdict(Counter),  # prod_sign -> cluster
        "omega_multiset": defaultdict(Counter),  # multiset -> cluster
    }

    triples = 0
    for i, j, k in itertools.combinations(range(n), 3):
        ip_ij = overlap[(i, j)]
        ip_jk = overlap[(j, k)]
        ip_ik = overlap[(i, k)]
        if abs(ip_ij) < 1e-8 or abs(ip_jk) < 1e-8 or abs(ip_ik) < 1e-8:
            continue

        triples += 1
        prod = ip_ij * ip_jk * ip_ik.conjugate()
        if abs(prod) < 1e-12:
            continue
        cluster = phase_cluster(np.angle(prod))

        w12 = omega_symp(f3_pts[i], f3_pts[j])
        w23 = omega_symp(f3_pts[j], f3_pts[k])
        w31 = omega_symp(f3_pts[k], f3_pts[i])

        # map ω=1->+1, ω=2->-1
        def sgn(w):
            return 1 if w == 1 else -1

        c1 = sum(1 for w in (w12, w23, w31) if w == 1)
        c2 = 3 - c1
        prod_sign = sgn(w12) * sgn(w23) * sgn(w31)
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

    out_path = ROOT / "artifacts" / "pancharatnam_symplectic_invariants.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "pancharatnam_symplectic_invariants.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Pancharatnam Phase vs Symplectic Invariants (F3^4)\n\n")
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
