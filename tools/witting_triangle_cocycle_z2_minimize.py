#!/usr/bin/env python3
"""Heuristic minimal-support representatives for Z2 cocycles.

We represent triangle cochains as bitmasks and reduce support by adding edge
coboundaries (columns of d1) greedily.
"""
from __future__ import annotations

import random
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


def build_nonorth_edges(rays, tol=1e-8):
    edges = []
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            if abs(np.vdot(rays[i], rays[j])) >= tol:
                edges.append((i, j))
    return edges


def build_triangles(edges, n):
    edge_set = set(edges)
    triangles = []
    for i in range(n):
        for j in range(i + 1, n):
            if (i, j) not in edge_set:
                continue
            for k in range(j + 1, n):
                if (i, k) in edge_set and (j, k) in edge_set:
                    triangles.append((i, j, k))
    return triangles


def phase_to_k(angle):
    return int(np.rint(angle / (np.pi / 6.0))) % 12


def greedy_reduce(v, cols, passes=3, seed=0):
    best = v
    best_w = v.bit_count()
    rng = random.Random(seed)
    cols_list = cols[:]
    for _ in range(passes):
        rng.shuffle(cols_list)
        cur = v
        improved = True
        while improved:
            improved = False
            for c in cols_list:
                w = (cur ^ c).bit_count()
                if w < cur.bit_count():
                    cur ^= c
                    improved = True
        if cur.bit_count() < best_w:
            best = cur
            best_w = cur.bit_count()
    return best


def multi_start_reduce(v, cols, seeds=20, passes=6):
    best = v
    best_w = v.bit_count()
    for s in range(seeds):
        cand = greedy_reduce(v, cols, passes=passes, seed=s)
        w = cand.bit_count()
        if w < best_w:
            best = cand
            best_w = w
    return best


def main():
    print("Z2 COCYCLE MIN-SUPPORT (HEURISTIC)")
    print("=" * 60)

    rays = construct_witting_40_rays()
    n = len(rays)
    edges = build_nonorth_edges(rays)
    triangles = build_triangles(edges, n)

    edge_index = {e: idx for idx, e in enumerate(edges)}

    # build column masks for each edge
    cols = [0] * len(edges)
    for t_idx, (i, j, k) in enumerate(triangles):
        for a, b in [(i, j), (j, k), (i, k)]:
            e = edge_index[(a, b) if a < b else (b, a)]
            cols[e] |= (1 << t_idx)

    # build z2_mag and z2_sign as bitmasks
    z2_mag = 0
    z2_sign = 0
    for t_idx, (i, j, k) in enumerate(triangles):
        ip = np.vdot(rays[i], rays[j]) * np.vdot(rays[j], rays[k]) * np.conjugate(np.vdot(rays[i], rays[k]))
        kp = phase_to_k(np.angle(ip))
        mag = 0 if kp in (1, 11) else 1
        sgn = 0 if kp in (1, 3) else 1
        if mag == 1:
            z2_mag |= (1 << t_idx)
        if sgn == 1:
            z2_sign |= (1 << t_idx)

    print(f"Initial mag support: {z2_mag.bit_count()}")
    print(f"Initial sign support: {z2_sign.bit_count()}")

    mag_red = multi_start_reduce(z2_mag, cols, seeds=30, passes=8)
    sign_red = multi_start_reduce(z2_sign, cols, seeds=30, passes=8)

    print(f"Reduced mag support: {mag_red.bit_count()}")
    print(f"Reduced sign support: {sign_red.bit_count()}")

    out_path = ROOT / "docs" / "witting_triangle_cocycle_z2_minimize.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Triangles: {len(triangles)}\n")
        f.write(f"Initial mag support: {z2_mag.bit_count()}\n")
        f.write(f"Reduced mag support: {mag_red.bit_count()}\n")
        f.write(f"Initial sign support: {z2_sign.bit_count()}\n")
        f.write(f"Reduced sign support: {sign_red.bit_count()}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
