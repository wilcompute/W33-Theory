#!/usr/bin/env python3
"""Search for quadratic phase formulas by family parameters.

We attempt to fit k (phase index in Z12) as:
  k ≡ sum_i c_i * m_i  (mod 12)
with monomials:
  1, mu1, nu1, mu2, nu2, mu1*nu1, mu2*nu2,
  mu1*mu2, nu1*nu2, mu1*nu2, nu1*mu2

We solve mod 3 by linear algebra over GF(3),
and mod 4 by meet-in-the-middle, then combine via CRT.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
import itertools

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
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            labels.append(("F0", mu, nu))
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            labels.append(("F1", mu, nu))
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            labels.append(("F2", mu, nu))
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)
            labels.append(("F3", mu, nu))

    return rays, labels


def wrap_angle(a):
    return np.arctan2(np.sin(a), np.cos(a))


def phase_index(a):
    k = round(wrap_angle(a) / (np.pi / 6))
    return k % 12


def monomials(mu1, nu1, mu2, nu2):
    return [
        1,
        mu1, nu1, mu2, nu2,
        mu1*nu1, mu2*nu2,
        mu1*mu2, nu1*nu2,
        mu1*nu2, nu1*mu2,
    ]


def solve_mod3(samples):
    # Gaussian elimination mod 3
    M = []
    b = []
    for mu1, nu1, mu2, nu2, k in samples:
        M.append([m % 3 for m in monomials(mu1, nu1, mu2, nu2)])
        b.append(k % 3)
    M = np.array(M, dtype=int)
    b = np.array(b, dtype=int)

    rows, cols = M.shape
    A = np.concatenate([M, b[:, None]], axis=1)
    r = 0
    pivots = [-1] * cols
    for c in range(cols):
        # find pivot
        pivot = None
        for i in range(r, rows):
            if A[i, c] % 3 != 0:
                pivot = i
                break
        if pivot is None:
            continue
        # swap
        A[[r, pivot]] = A[[pivot, r]]
        inv = 1 if A[r, c] == 1 else 2  # inverse mod 3
        A[r, :] = (A[r, :] * inv) % 3
        for i in range(rows):
            if i != r and A[i, c] % 3 != 0:
                A[i, :] = (A[i, :] - A[i, c] * A[r, :]) % 3
        pivots[c] = r
        r += 1
    # check consistency
    for i in range(rows):
        if all(A[i, c] % 3 == 0 for c in range(cols)) and A[i, cols] % 3 != 0:
            return None  # no solution
    # extract one solution (free vars = 0)
    x = np.zeros(cols, dtype=int)
    for c in range(cols):
        if pivots[c] != -1:
            x[c] = A[pivots[c], cols] % 3
    return x.tolist()


def solve_mod4(samples):
    # meet-in-the-middle over 11 coefficients
    mon_len = 11
    left_idx = list(range(5))
    right_idx = list(range(5, mon_len))

    # build matrix of monomials mod 4
    M = []
    b = []
    for mu1, nu1, mu2, nu2, k in samples:
        M.append([m % 4 for m in monomials(mu1, nu1, mu2, nu2)])
        b.append(k % 4)
    M = np.array(M, dtype=int)
    b = np.array(b, dtype=int)

    # precompute right sums
    right_map = {}
    for coeffs in itertools.product(range(4), repeat=len(right_idx)):
        s = (M[:, right_idx] @ np.array(coeffs, dtype=int)) % 4
        right_map[tuple(s.tolist())] = coeffs

    for coeffs_left in itertools.product(range(4), repeat=len(left_idx)):
        s_left = (M[:, left_idx] @ np.array(coeffs_left, dtype=int)) % 4
        needed = (b - s_left) % 4
        key = tuple(needed.tolist())
        if key in right_map:
            coeffs_right = right_map[key]
            # assemble full
            coeffs = [0]*mon_len
            for i, c in zip(left_idx, coeffs_left):
                coeffs[i] = c
            for i, c in zip(right_idx, coeffs_right):
                coeffs[i] = c
            return coeffs
    return None


def crt_mod12(a3, a4):
    # find x in 0..11 with x≡a3 mod3 and x≡a4 mod4
    for x in range(12):
        if x % 3 == a3 % 3 and x % 4 == a4 % 4:
            return x
    return None


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
            k = phase_index(np.angle(ip))
            key = tuple(sorted((fi, fj)))
            samples_by_pair[key].append((mu1, nu1, mu2, nu2, k))

    results = {}
    for key, samples in samples_by_pair.items():
        sol3 = solve_mod3(samples)
        sol4 = solve_mod4(samples)
        sol12 = None
        if sol3 is not None and sol4 is not None:
            sol12 = [crt_mod12(a3, a4) for a3, a4 in zip(sol3, sol4)]
        results[str(key)] = {
            "samples": len(samples),
            "mod3": sol3,
            "mod4": sol4,
            "mod12": sol12,
        }

    out_path = ROOT / "artifacts" / "witting_phase_quadratic_formula_search.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_phase_quadratic_formula_search.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Quadratic Phase Formula Search\n\n")
        f.write("Monomials: 1, mu1, nu1, mu2, nu2, mu1*nu1, mu2*nu2, mu1*mu2, nu1*nu2, mu1*nu2, nu1*mu2\n\n")
        f.write("family pair | samples | mod3 | mod4 | mod12\n")
        f.write("--- | --- | --- | --- | ---\n")
        for key in sorted(results.keys()):
            r = results[key]
            f.write(f"{key} | {r['samples']} | {r['mod3']} | {r['mod4']} | {r['mod12']}\n")

    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
