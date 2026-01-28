#!/usr/bin/env python3
"""Test projective F3^4 mapping of Witting rays and symplectic orthogonality.

We map each ray to an F3^4 projective point by finding a global phase factor
that makes entries closest to {0, 1, w, w^2}. Then we test:
  - whether every ray maps cleanly
  - whether symplectic orthogonality matches ray orthogonality
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


def omega_symp(x, y):
    return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3


def best_f3_point(ray, tol=1e-6):
    omega = np.exp(2j * np.pi / 3)
    roots = [1, omega, omega**2]
    # try 6th roots of unity as global phase
    phases = [np.exp(1j * np.pi * k / 3) for k in range(6)]
    best = None
    best_err = 1e9
    for phase in phases:
        v = ray * phase
        # normalize by first nonzero to be nearest cube root
        idx = None
        for i, z in enumerate(v):
            if abs(z) > tol:
                idx = i
                break
        if idx is None:
            continue
        z0 = v[idx]
        nearest = min(roots, key=lambda r: abs(z0 - r))
        v = v * (nearest / z0)
        # map entries to nearest root
        coords = []
        err = 0.0
        for z in v:
            if abs(z) < tol:
                coords.append(0)
                continue
            dists = [abs(z - r) for r in roots]
            k = int(np.argmin(dists))
            err += dists[k]
            coords.append(k)
        if err < best_err:
            best_err = err
            best = coords
    if best is None:
        return None, None
    # normalize projectively: first nonzero to 1
    coords = best
    for i, x in enumerate(coords):
        if x != 0:
            inv = 1 if x == 1 else 2  # inverse in F3
            coords = [(c * inv) % 3 for c in coords]
            break
    return tuple(coords), best_err


def main():
    rays = construct_witting_40_rays()
    n = len(rays)

    f3_points = []
    err_stats = []
    for r in rays:
        pt, err = best_f3_point(r)
        f3_points.append(pt)
        err_stats.append(err)

    err_max = max(err_stats)
    err_nonzero = sum(1 for e in err_stats if e > 1e-6)

    # Build orthogonality matrices
    ray_orth = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.vdot(rays[i], rays[j])) < 1e-8:
                ray_orth[i][j] = ray_orth[j][i] = 1

    symp_orth = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega_symp(f3_points[i], f3_points[j]) == 0:
                symp_orth[i][j] = symp_orth[j][i] = 1

    # Confusion matrix
    tp = tn = fp = fn = 0
    for i in range(n):
        for j in range(i + 1, n):
            r = ray_orth[i][j]
            s = symp_orth[i][j]
            if r == 1 and s == 1:
                tp += 1
            elif r == 0 and s == 0:
                tn += 1
            elif r == 0 and s == 1:
                fp += 1
            elif r == 1 and s == 0:
                fn += 1

    out = {
        "rays": n,
        "max_fit_error": err_max,
        "nonzero_fit_errors": err_nonzero,
        "orth_confusion": {"tp": tp, "tn": tn, "fp": fp, "fn": fn},
    }

    out_path = ROOT / "artifacts" / "witting_f3_projective_map_test.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_f3_projective_map_test.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting Ray -> F3^4 Projective Map Test\n\n")
        f.write(f"Rays: **{n}**\n\n")
        f.write(f"Max fit error: **{err_max:.6e}**\n")
        f.write(f"Nonzero fit errors: **{err_nonzero}**\n\n")
        f.write("## Orthogonality match (ray inner product vs symplectic ω)\n\n")
        f.write("tp | tn | fp | fn\n")
        f.write("--- | --- | --- | ---\n")
        f.write(f"{tp} | {tn} | {fp} | {fn}\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
