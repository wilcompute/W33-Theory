#!/usr/bin/env python3
"""Search for cubic phase formulas mod 3 by family parameters.

We fit k (phase index mod 3) as a linear combination of all monomials
in (mu1, nu1, mu2, nu2) with total degree <= 3 over GF(3).
"""

from __future__ import annotations

import json
from collections import defaultdict
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


def phase_index_mod3(a):
    # use k mod 12 then reduce mod 3
    k = round(wrap_angle(a) / (np.pi / 6))
    return k % 3


def monomials(mu1, nu1, mu2, nu2):
    vars = [mu1, nu1, mu2, nu2]
    mons = []
    # exponents 0..2 with total degree <=3
    for e0 in range(3):
        for e1 in range(3):
            for e2 in range(3):
                for e3 in range(3):
                    deg = e0 + e1 + e2 + e3
                    if deg > 3:
                        continue
                    val = (
                        (vars[0] ** e0)
                        * (vars[1] ** e1)
                        * (vars[2] ** e2)
                        * (vars[3] ** e3)
                    )
                    mons.append(val % 3)
    return mons


def solve_mod3(samples):
    # Gaussian elimination mod 3
    M = []
    b = []
    for mu1, nu1, mu2, nu2, k in samples:
        M.append(monomials(mu1, nu1, mu2, nu2))
        b.append(k % 3)
    M = np.array(M, dtype=int)
    b = np.array(b, dtype=int)

    rows, cols = M.shape
    A = np.concatenate([M, b[:, None]], axis=1)
    r = 0
    pivots = [-1] * cols
    for c in range(cols):
        pivot = None
        for i in range(r, rows):
            if A[i, c] % 3 != 0:
                pivot = i
                break
        if pivot is None:
            continue
        A[[r, pivot]] = A[[pivot, r]]
        inv = 1 if A[r, c] == 1 else 2
        A[r, :] = (A[r, :] * inv) % 3
        for i in range(rows):
            if i != r and A[i, c] % 3 != 0:
                A[i, :] = (A[i, :] - A[i, c] * A[r, :]) % 3
        pivots[c] = r
        r += 1
    for i in range(rows):
        if all(A[i, c] % 3 == 0 for c in range(cols)) and A[i, cols] % 3 != 0:
            return None
    x = np.zeros(cols, dtype=int)
    for c in range(cols):
        if pivots[c] != -1:
            x[c] = A[pivots[c], cols] % 3
    return x.tolist()


def main():
    rays, labels = construct_witting_40_rays_with_labels()
    n = len(rays)

    samples_by_pair = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            fi, mu1, nu1 = labels[i]
            fj, mu2, nu2 = labels[j]
            if fi == "B" or fj == "B":
                continue
            ip = np.vdot(rays[i], rays[j])
            if abs(ip) < 1e-8:
                continue
            k = phase_index_mod3(np.angle(ip))
            key = tuple(sorted((fi, fj)))
            samples_by_pair[key].append((mu1, nu1, mu2, nu2, k))

    results = {}
    for key, samples in samples_by_pair.items():
        sol = solve_mod3(samples)
        results[str(key)] = {"samples": len(samples), "mod3_solution": sol}

    out_path = ROOT / "artifacts" / "witting_phase_cubic_formula_search.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_phase_cubic_formula_search.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Cubic Phase Formula Search (mod 3)\n\n")
        f.write(
            "Monomials: all exponents with total degree ≤ 3 in (mu1,nu1,mu2,nu2).\n\n"
        )
        f.write("family pair | samples | mod3 solution\n")
        f.write("--- | --- | ---\n")
        for key in sorted(results.keys()):
            r = results[key]
            f.write(f"{key} | {r['samples']} | {r['mod3_solution']}\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
