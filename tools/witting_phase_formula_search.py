#!/usr/bin/env python3
"""Search for simple linear phase formulas by ray family parameters.

For each family pair (Fα, Fβ), we try to fit:
    k ≡ a*mu1 + b*nu1 + c*mu2 + d*nu2 + e (mod 12)
where k is the phase index (angle / (pi/6)) mod 12.
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


def phase_index(a):
    # map to nearest multiple of pi/6 in Z12
    k = round(wrap_angle(a) / (np.pi / 6))
    return k % 12


def fit_linear_formula(samples):
    """Try all coefficients in Z12 for linear formula."""
    # samples: list of (mu1, nu1, mu2, nu2, k)
    best = None
    for a in range(12):
        for b in range(12):
            for c in range(12):
                for d in range(12):
                    for e in range(12):
                        ok = True
                        for mu1, nu1, mu2, nu2, k in samples:
                            pred = (a * mu1 + b * nu1 + c * mu2 + d * nu2 + e) % 12
                            if pred != k:
                                ok = False
                                break
                        if ok:
                            return (a, b, c, d, e)
    return best


def main():
    rays, labels = construct_witting_40_rays_with_labels()
    n = len(rays)

    # collect samples by family pair
    samples = defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            fi, mu1, nu1 = labels[i]
            fj, mu2, nu2 = labels[j]
            if fi == "B" or fj == "B":
                continue
            ip = np.vdot(rays[i], rays[j])
            if abs(ip) < 1e-8:
                continue
            k = phase_index(np.angle(ip))
            key = tuple(sorted((fi, fj)))
            samples[key].append((mu1, nu1, mu2, nu2, k))

    results = {}
    for key, samp in samples.items():
        coef = fit_linear_formula(samp)
        results[str(key)] = {"samples": len(samp), "formula": coef}

    out_path = ROOT / "artifacts" / "witting_phase_formula_search.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_phase_formula_search.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Linear Phase Formula Search (F‑Families)\n\n")
        f.write("We search for k ≡ a*mu1 + b*nu1 + c*mu2 + d*nu2 + e (mod 12).\n\n")
        f.write("family pair | samples | formula (a,b,c,d,e)\n")
        f.write("--- | --- | ---\n")
        for key in sorted(results.keys()):
            samp = results[key]["samples"]
            coef = results[key]["formula"]
            f.write(f"{key} | {samp} | {coef}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
