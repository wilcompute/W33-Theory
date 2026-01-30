#!/usr/bin/env python3
"""Random U(4) search to maximize grid-score of Witting rays.

Grid-score: number of rays that, after U, become "grid form":
  - 1 nonzero (magnitude ~1), or
  - 3 nonzero (magnitude ~1/sqrt(3)),
with phases in {1, w, w^2} up to global phase.
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
    # normalize phases
    d = np.diag(r)
    q = q * (d / np.abs(d))
    return q


def is_grid_ray(v, tol=1e-2):
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
        return abs(mags[nz[0]] - 1.0) < 5e-2
    if len(nz) != 3:
        return False
    target = 1.0 / np.sqrt(3)
    if any(abs(mags[i] - target) > 5e-2 for i in nz):
        return False
    for i in nz:
        dists = [abs(v[i] - r) for r in roots]
        if min(dists) > 5e-2:
            return False
    return True


def score_unitary(U, rays):
    score = 0
    for r in rays:
        v = U @ r
        if is_grid_ray(v):
            score += 1
    return score


def main():
    rays = construct_witting_40_rays()
    trials = 2000
    best_score = -1
    best_U = None
    hist = {}

    for _ in range(trials):
        U = random_unitary()
        score = score_unitary(U, rays)
        hist[score] = hist.get(score, 0) + 1
        if score > best_score:
            best_score = score
            best_U = U

    best_serialized = None
    if best_U is not None:
        best_serialized = [
            [{"re": float(x.real), "im": float(x.imag)} for x in row]
            for row in np.round(best_U, 6)
        ]

    out = {
        "trials": trials,
        "best_score": best_score,
        "hist": {str(k): v for k, v in sorted(hist.items())},
        "best_U": best_serialized,
    }

    out_path = ROOT / "artifacts" / "witting_unitary_grid_score_search.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_unitary_grid_score_search.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Random U(4) Grid‑Score Search\n\n")
        f.write(f"Trials: **{trials}**\n")
        f.write(f"Best score: **{best_score} / 40**\n\n")
        f.write("## Score histogram\n\n")
        f.write("score | count\n")
        f.write("--- | ---\n")
        for k, v in sorted(hist.items()):
            f.write(f"{k} | {v}\n")
        f.write("\n## Best U (rounded)\n\n")
        f.write("```text\n")
        if best_U is not None:
            for row in np.round(best_U, 6):
                f.write(" ".join(f"{x.real:+.6f}{x.imag:+.6f}j" for x in row) + "\n")
        f.write("```\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
