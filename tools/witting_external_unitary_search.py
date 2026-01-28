#!/usr/bin/env python3
"""Search for a unitary that maps Witting rays to the F3^4 grid rays.

Strategy:
1. Build source rays (Witting 40 rays).
2. Build target rays from F3^4 projective points: v = (w^a, w^b, w^c, w^d)/||.||
3. Enumerate orthonormal bases in each set (4-cliques of orthogonality).
4. For each basis pair (B_source, B_target), compute U = B_target * B_source^†.
5. Score U by how many source rays map to *some* target ray (up to phase).
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


def construct_f3_grid_rays():
    omega = np.exp(2j * np.pi / 3)
    rays = []
    F3 = [0, 1, 2]
    seen = set()
    for a in F3:
        for b in F3:
            for c in F3:
                for d in F3:
                    if a == b == c == d == 0:
                        continue
                    v = np.array([omega**a, omega**b, omega**c, omega**d], dtype=complex)
                    # projective normalization by first nonzero
                    idx = next(i for i, z in enumerate(v) if abs(z) > 1e-12)
                    v = v / v[idx]
                    key = tuple(np.round(v, 6))
                    if key in seen:
                        continue
                    seen.add(key)
                    v = v / np.linalg.norm(v)
                    rays.append(v)
    return rays


def orthonormal_bases(rays, tol=1e-8):
    n = len(rays)
    orth = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.vdot(rays[i], rays[j])) < tol:
                orth[i][j] = orth[j][i] = 1
    bases = set()
    for i in range(n):
        for j in range(i + 1, n):
            if not orth[i][j]:
                continue
            candidates = [k for k in range(n) if orth[i][k] and orth[j][k]]
            for k, l in combinations(candidates, 2):
                if orth[k][l] and orth[i][k] and orth[i][l] and orth[j][k] and orth[j][l]:
                    bases.add(tuple(sorted((i, j, k, l))))
    return sorted(bases)


def match_score(U, src_rays, tgt_rays, tol=1e-6):
    # precompute target rays for fast match
    score = 0
    for r in src_rays:
        v = U @ r
        # max overlap with any target ray
        overlaps = [abs(np.vdot(v, t)) for t in tgt_rays]
        if max(overlaps) > 1 - tol:
            score += 1
    return score


def main():
    src = construct_witting_40_rays()
    tgt = construct_f3_grid_rays()
    bases_src = orthonormal_bases(src)
    bases_tgt = orthonormal_bases(tgt)

    best = {"score": -1, "src_basis": None, "tgt_basis": None}
    score_hist = {}

    for b_src in bases_src:
        B_src = np.column_stack([src[i] for i in b_src])
        for b_tgt in bases_tgt:
            B_tgt = np.column_stack([tgt[i] for i in b_tgt])
            U = B_tgt @ np.conjugate(B_src).T
            score = match_score(U, src, tgt)
            score_hist[score] = score_hist.get(score, 0) + 1
            if score > best["score"]:
                best = {"score": score, "src_basis": b_src, "tgt_basis": b_tgt}
                if score == 40:
                    break
        if best["score"] == 40:
            break

    out = {
        "src_rays": len(src),
        "tgt_rays": len(tgt),
        "src_bases": len(bases_src),
        "tgt_bases": len(bases_tgt),
        "best": best,
        "score_hist": {str(k): v for k, v in sorted(score_hist.items())},
    }

    out_path = ROOT / "artifacts" / "witting_external_unitary_search.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_external_unitary_search.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# External Unitary Search (Witting → F3^4 Grid)\n\n")
        f.write(f"Source rays: **{len(src)}**\n")
        f.write(f"Target rays (naive ω‑grid): **{len(tgt)}**\n")
        f.write(f"Source bases: **{len(bases_src)}**\n")
        f.write(f"Target bases: **{len(bases_tgt)}**\n\n")
        f.write(f"Best score: **{best['score']} / 40**\n")
        f.write(f"Best source basis: **{best['src_basis']}**\n")
        f.write(f"Best target basis: **{best['tgt_basis']}**\n\n")
        f.write("## Score histogram\n\n")
        f.write("score | count\n")
        f.write("--- | ---\n")
        for k, v in sorted(score_hist.items()):
            f.write(f"{k} | {v}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
