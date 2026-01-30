#!/usr/bin/env python3
"""Generate a step-by-step lab script for the 24-basis KS test.

Includes basis order, MZI schedule link, waveplate degrees, and expected KS bound.
"""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    labels = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
        labels.append(f"e{i}")
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -(omega**mu), omega**nu]) / sqrt3)
            labels.append(f"(0,1,-w^{mu},w^{nu})/sqrt3")
            rays.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / sqrt3)
            labels.append(f"(1,0,-w^{mu},-w^{nu})/sqrt3")
            rays.append(np.array([1, -(omega**mu), 0, omega**nu]) / sqrt3)
            labels.append(f"(1,-w^{mu},0,w^{nu})/sqrt3")
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
            labels.append(f"(1,w^{mu},w^{nu},0)/sqrt3")
    return rays, labels


def orthogonal(v1, v2, tol=1e-8):
    return abs(np.vdot(v1, v2)) < tol


def find_tetrads(rays):
    n = len(rays)
    ortho = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            if orthogonal(rays[i], rays[j]):
                ortho[i, j] = ortho[j, i] = True
    tetrads = []
    for a, b, c, d in combinations(range(n), 4):
        if (
            ortho[a, b]
            and ortho[a, c]
            and ortho[a, d]
            and ortho[b, c]
            and ortho[b, d]
            and ortho[c, d]
        ):
            tetrads.append((a, b, c, d))
    return tetrads


def main():
    rays, labels = construct_witting_40_rays()
    tetrads = find_tetrads(rays)

    subset_path = ROOT / "artifacts" / "witting_ks_reduce_bases.json"
    if not subset_path.exists():
        print("Missing artifacts/witting_ks_reduce_bases.json")
        return

    indices = json.loads(subset_path.read_text()).get("bases", [])
    bases = [tetrads[i] for i in indices]

    bound_path = ROOT / "artifacts" / "witting_24basis_exact_bound.json"
    bound = 23
    if bound_path.exists():
        bound = json.loads(bound_path.read_text()).get("max_satisfied", 23)

    md_path = DOCS / "witting_24basis_labscript.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# 24‑Basis KS Lab Script\n\n")
        f.write("## Required inputs\n")
        f.write("- MZI schedule: docs/witting_24basis_mzi_schedule.md\n")
        f.write(
            "- Waveplate schedule (deg): docs/witting_24basis_waveplates_deg.md\n\n"
        )
        f.write("## Target inequality\n")
        f.write(f"Noncontextual bound: **{bound} / 24**\n")
        f.write("Quantum prediction: **24 / 24**\n\n")
        f.write("## Measurement steps\n\n")
        for bi, base in enumerate(bases):
            f.write(f"### Basis B{bi:02d}\n")
            f.write(f"Rays: {list(base)}\n\n")
            f.write("Prepare basis via MZI or waveplates, then measure counts\n")
            f.write("for the four designated outcomes.\n\n")
            for r in base:
                f.write(f"- r{r}: {labels[r]}\n")
            f.write("\n")
        f.write("## Scoring\n")
        f.write(
            "For each basis, mark satisfied if exactly one designated outcome occurs.\n"
        )
        f.write("Sum S across 24 bases and compare to bound.\n")

    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
