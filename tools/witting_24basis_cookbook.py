#!/usr/bin/env python3
"""Generate a photonic cookbook for the 24-basis KS subset of the Witting 40 rays.

Outputs:
- docs/witting_24basis_cookbook.md
- docs/witting_24basis_vectors.csv
- docs/witting_24basis_subset.json

Also computes a heuristic noncontextual bound: max number of bases that can be
satisfied by any 0/1 assignment (exactly one "1" per basis) found by local search.
"""
from __future__ import annotations

import json
import random
from pathlib import Path
from itertools import combinations

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)


def construct_witting_40_rays():
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)
    rays = []
    labels = []

    # 4 basis states
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)
        labels.append(f"e{i}")

    # 36 states in 4 groups of 9
    for mu in range(3):
        for nu in range(3):
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            labels.append(f"(0,1,-w^{mu},w^{nu})/sqrt3")

            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            labels.append(f"(1,0,-w^{mu},-w^{nu})/sqrt3")

            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
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
        if (ortho[a, b] and ortho[a, c] and ortho[a, d] and
                ortho[b, c] and ortho[b, d] and ortho[c, d]):
            tetrads.append((a, b, c, d))
    return tetrads


def load_24basis_subset():
    path = ROOT / "artifacts" / "witting_ks_reduce_bases.json"
    if path.exists():
        data = json.loads(path.read_text())
        return data.get("bases", [])
    return []


def load_exact_bound():
    path = ROOT / "artifacts" / "witting_24basis_exact_bound.json"
    if path.exists():
        data = json.loads(path.read_text())
        return data.get("max_satisfied")
    return None


def bases_satisfied(assign, bases):
    count = 0
    for base in bases:
        s = assign[base[0]] + assign[base[1]] + assign[base[2]] + assign[base[3]]
        if s == 1:
            count += 1
    return count


def heuristic_max_satisfied(num_rays, bases, iters=200, flips=50):
    best = 0
    best_assign = None
    rng = random.Random(0)

    for _ in range(iters):
        assign = [rng.randint(0, 1) for _ in range(num_rays)]
        score = bases_satisfied(assign, bases)
        improved = True

        while improved:
            improved = False
            for _ in range(flips):
                i = rng.randrange(num_rays)
                assign[i] ^= 1
                new_score = bases_satisfied(assign, bases)
                if new_score >= score:
                    score = new_score
                    improved = True
                else:
                    assign[i] ^= 1

        if score > best:
            best = score
            best_assign = assign.copy()

    return best, best_assign


def main():
    rays, labels = construct_witting_40_rays()
    tetrads = find_tetrads(rays)

    subset_indices = load_24basis_subset()
    if not subset_indices:
        print("No 24-basis subset found in artifacts; aborting.")
        return

    bases_24 = [tetrads[i] for i in subset_indices]

    # Heuristic classical bound
    max_sat, assignment = heuristic_max_satisfied(len(rays), bases_24)
    exact_bound = load_exact_bound()

    # Save vectors CSV
    csv_path = DOCS / "witting_24basis_vectors.csv"
    with csv_path.open("w", encoding="utf-8") as f:
        f.write("ray_index,label,v0,v1,v2,v3\n")
        for i, v in enumerate(rays):
            f.write(
                f"{i},\"{labels[i]}\",{v[0]},{v[1]},{v[2]},{v[3]}\n"
            )

    # Save subset JSON
    subset_path = DOCS / "witting_24basis_subset.json"
    subset_path.write_text(
        json.dumps(
            {
                "bases": [list(map(int, b)) for b in bases_24],
                "ray_labels": labels,
                "heuristic_max_satisfied_bases": int(max_sat),
                "exact_max_satisfied_bases": int(exact_bound) if exact_bound is not None else None,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # Markdown cookbook
    md_path = DOCS / "witting_24basis_cookbook.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Witting 24‑Basis KS Cookbook\n\n")
        f.write("This file lists a 24‑basis subset (out of 40) that remains KS‑uncolorable.\n")
        if exact_bound is not None:
            f.write("It also includes the exact noncontextual bound.\n\n")
            f.write("## Exact noncontextual bound\n")
            f.write(f"- Max bases satisfiable by any 0/1 assignment: **{exact_bound} / {len(bases_24)}**\n\n")
        else:
            f.write("It also includes a heuristic noncontextual bound from local search.\n\n")
            f.write("## Heuristic noncontextual bound\n")
            f.write(f"- Best bases satisfiable found: **{max_sat} / {len(bases_24)}**\n\n")
        f.write("## Ray index map\n")
        for i, lab in enumerate(labels):
            f.write(f"- r{i}: {lab}\n")
        f.write("\n## 24 bases\n")
        for bi, base in enumerate(bases_24):
            f.write(f"**B{bi:02d}**: {list(map(int, base))}\n\n")

    print(f"Wrote {md_path}")
    print(f"Wrote {csv_path}")
    print(f"Wrote {subset_path}")


if __name__ == "__main__":
    main()
