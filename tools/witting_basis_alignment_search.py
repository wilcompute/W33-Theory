#!/usr/bin/env python3
"""Search for an orthonormal basis that aligns rays to cube-root grid form.

For each orthonormal 4-ray basis B, set U = B^† and test if U maps
all 40 rays to the canonical grid form:
  - basis rays: one nonzero entry of magnitude 1
  - non-basis rays: three nonzero entries of magnitude 1/sqrt(3)
    with phases in {1, w, w^2} up to global phase
We report the best score and if any basis achieves 40/40.
"""
from __future__ import annotations

import json
from itertools import combinations
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


def is_grid_ray(v, tol=1e-4):
    omega = np.exp(2j * np.pi / 3)
    roots = [1, omega, omega**2]

    # normalize by global phase (first nonzero)
    idx = None
    for i, z in enumerate(v):
        if abs(z) > tol:
            idx = i
            break
    if idx is None:
        return False
    v = v / v[idx]

    mags = [abs(z) for z in v]
    nz = [i for i, z in enumerate(v) if abs(z) > tol]
    if len(nz) == 1:
        # basis ray: magnitude ~1
        return abs(mags[nz[0]] - 1.0) < 1e-3

    if len(nz) != 3:
        return False
    # non-basis: all nonzeros magnitude ~1/sqrt(3)
    target = 1.0 / np.sqrt(3)
    if any(abs(mags[i] - target) > 1e-3 for i in nz):
        return False
    # phases near cube roots
    for i in nz:
        dists = [abs(v[i] - r) for r in roots]
        if min(dists) > 1e-3:
            return False
    return True


def main():
    rays = construct_witting_40_rays()
    n = len(rays)

    # orthogonality matrix
    orth = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.vdot(rays[i], rays[j])) < 1e-8:
                orth[i][j] = orth[j][i] = 1

    # enumerate orthonormal bases
    bases = set()
    for i in range(n):
        for j in range(i + 1, n):
            if not orth[i][j]:
                continue
            # candidates orthogonal to i and j
            candidates = [k for k in range(n) if orth[i][k] and orth[j][k]]
            for k, l in combinations(candidates, 2):
                if orth[k][l] and orth[i][k] and orth[i][l] and orth[j][k] and orth[j][l]:
                    base = tuple(sorted((i, j, k, l)))
                    bases.add(base)
    bases = sorted(bases)

    best = {"score": -1, "basis": None}
    score_hist = {}

    for base in bases:
        B = np.column_stack([rays[i] for i in base])
        U = np.conjugate(B).T
        score = 0
        for r in rays:
            v = U @ r
            if is_grid_ray(v):
                score += 1
        score_hist[score] = score_hist.get(score, 0) + 1
        if score > best["score"]:
            best = {"score": score, "basis": base}

    out = {
        "bases_found": len(bases),
        "best_score": best["score"],
        "best_basis": best["basis"],
        "score_hist": {str(k): v for k, v in sorted(score_hist.items())},
    }

    out_path = ROOT / "artifacts" / "witting_basis_alignment_search.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_basis_alignment_search.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Basis Alignment Search (Grid Form)\n\n")
        f.write(f"Orthogonal bases found: **{len(bases)}**\n\n")
        f.write(f"Best grid score: **{best['score']} / 40**\n")
        f.write(f"Best basis: **{best['basis']}**\n\n")
        f.write("## Score histogram\n\n")
        f.write("score | bases\n")
        f.write("--- | ---\n")
        for k, v in sorted(score_hist.items()):
            f.write(f"{k} | {v}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
