#!/usr/bin/env python3
"""Structured U(4) search via local random perturbations (annealing).

We try to maximize a "grid-score" for Witting rays under a unitary U.
Score = number of rays that map into grid form (tolerant).
We run hill-climb/anneal starting from random U.
"""

from __future__ import annotations

import json
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


def random_unitary():
    z = (np.random.randn(4, 4) + 1j * np.random.randn(4, 4)) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    q = q * (d / np.abs(d))
    return q


def is_grid_ray(v, tol_mag=5e-2, tol_phase=5e-2):
    omega = np.exp(2j * np.pi / 3)
    roots = [1, omega, omega**2]
    # normalize by global phase (first nonzero)
    idx = None
    for i, z in enumerate(v):
        if abs(z) > tol_mag:
            idx = i
            break
    if idx is None:
        return False
    v = v / v[idx]

    mags = [abs(z) for z in v]
    nz = [i for i, z in enumerate(v) if abs(z) > tol_mag]
    if len(nz) == 1:
        return abs(mags[nz[0]] - 1.0) < tol_mag
    if len(nz) != 3:
        return False
    target = 1.0 / np.sqrt(3)
    if any(abs(mags[i] - target) > tol_mag for i in nz):
        return False
    for i in nz:
        dists = [abs(v[i] - r) for r in roots]
        if min(dists) > tol_phase:
            return False
    return True


def score_unitary(U, rays, tol_mag=5e-2, tol_phase=5e-2):
    score = 0
    for r in rays:
        v = U @ r
        if is_grid_ray(v, tol_mag=tol_mag, tol_phase=tol_phase):
            score += 1
    return score


def perturb_unitary(U, eps=0.05):
    # random skew-Hermitian perturbation, reunitarize via QR
    A = np.random.randn(4, 4) + 1j * np.random.randn(4, 4)
    K = A - A.conjugate().T
    M = U + eps * (K @ U)
    q, r = np.linalg.qr(M)
    d = np.diag(r)
    q = q * (d / np.abs(d))
    return q


def main():
    rays = construct_witting_40_rays()
    steps = 5000
    eps = 0.08

    # two tolerance settings
    settings = [(5e-2, 5e-2), (8e-2, 8e-2)]
    best = {str(s): {"score": -1, "U": None} for s in settings}

    U = random_unitary()
    scores = {str(s): score_unitary(U, rays, *s) for s in settings}

    for step in range(steps):
        U_new = perturb_unitary(U, eps=eps)
        scores_new = {str(s): score_unitary(U_new, rays, *s) for s in settings}

        # accept if improves strict score or probabilistically
        if scores_new[str(settings[0])] >= scores[str(settings[0])]:
            U = U_new
            scores = scores_new
        else:
            # small random acceptance
            if np.random.rand() < 0.05:
                U = U_new
                scores = scores_new

        for s in settings:
            key = str(s)
            if scores[key] > best[key]["score"]:
                best[key] = {"score": scores[key], "U": U}

    out = {
        "steps": steps,
        "settings": [str(s) for s in settings],
        "best_scores": {k: v["score"] for k, v in best.items()},
        "best_U": {
            k: (
                [
                    [{"re": float(x.real), "im": float(x.imag)} for x in row]
                    for row in np.round(v["U"], 6)
                ]
                if v["U"] is not None
                else None
            )
            for k, v in best.items()
        },
    }

    out_path = ROOT / "artifacts" / "witting_unitary_grid_anneal.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_unitary_grid_anneal.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Structured U(4) Anneal Search (Grid‑Score)\n\n")
        f.write(f"Steps: **{steps}**\n\n")
        for s in settings:
            key = str(s)
            f.write(f"## Tolerances {key}\n\n")
            f.write(f"Best score: **{best[key]['score']} / 40**\n\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
