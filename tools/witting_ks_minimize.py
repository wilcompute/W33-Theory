#!/usr/bin/env python3
"""Heuristic search for smaller KS-uncolorable subsets of the Witting 40 rays.

We repeatedly try greedy deletions in random order, keeping a ray removed
if the induced configuration remains KS-uncolorable.
"""

from __future__ import annotations

import itertools
import random
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
    for a, b, c, d in itertools.combinations(range(n), 4):
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


def ks_satisfiable(num_rays, bases, ray_subset):
    """Return True if there exists a 0/1 assignment with exactly one 1 per base."""
    # Filter bases to those fully contained in subset
    subset_set = set(ray_subset)
    bases = [b for b in bases if all(r in subset_set for r in b)]
    if not bases:
        return True

    # Remap rays to 0..k-1
    mapping = {r: i for i, r in enumerate(sorted(subset_set))}
    bases_mapped = [tuple(mapping[r] for r in b) for b in bases]
    num_rays = len(mapping)

    ray_bases = [[] for _ in range(num_rays)]
    for bi, base in enumerate(bases_mapped):
        for r in base:
            ray_bases[r].append(bi)

    assign = [-1] * num_rays
    base_ones = [0] * len(bases_mapped)
    base_unassigned = [4] * len(bases_mapped)

    order = sorted(range(num_rays), key=lambda r: -len(ray_bases[r]))

    def propagate(ray, val):
        for bi in ray_bases[ray]:
            base_unassigned[bi] -= 1
            if val == 1:
                base_ones[bi] += 1
                if base_ones[bi] > 1:
                    return False
            if base_ones[bi] + base_unassigned[bi] < 1:
                return False
        return True

    def undo(ray, val):
        for bi in ray_bases[ray]:
            base_unassigned[bi] += 1
            if val == 1:
                base_ones[bi] -= 1

    def forced_zeros():
        forced = []
        for bi, base in enumerate(bases_mapped):
            if base_ones[bi] == 1:
                for r in base:
                    if assign[r] == -1:
                        forced.append(r)
        return forced

    def backtrack(idx=0):
        if idx == num_rays:
            return all(base_ones[bi] == 1 for bi in range(len(bases_mapped)))

        ray = order[idx]
        if assign[ray] != -1:
            return backtrack(idx + 1)

        for val in (1, 0):
            assign[ray] = val
            ok = propagate(ray, val)
            if ok:
                forced = forced_zeros()
                stack = []
                consistent = True
                for r in forced:
                    if assign[r] == -1:
                        assign[r] = 0
                        stack.append(r)
                        if not propagate(r, 0):
                            consistent = False
                            break
                    elif assign[r] == 1:
                        consistent = False
                        break
                if consistent and backtrack(idx + 1):
                    return True
                for r in reversed(stack):
                    undo(r, 0)
                    assign[r] = -1
            undo(ray, val)
            assign[ray] = -1
        return False

    return backtrack()


def greedy_minimize(rays, bases, seed, max_steps=200):
    rng = random.Random(seed)
    current = set(range(len(rays)))

    improved = True
    while improved and len(current) > 4:
        improved = False
        order = list(current)
        rng.shuffle(order)
        for r in order:
            trial = set(current)
            trial.remove(r)
            if not ks_satisfiable(len(rays), bases, trial):
                current = trial
                improved = True
        if len(current) <= 10:
            break
    return current


def main():
    rays = construct_witting_40_rays()
    bases = find_tetrads(rays)

    print("Witting KS minimization")
    print("=" * 35)
    print(f"Rays: {len(rays)}")
    print(f"Bases: {len(bases)}")

    best = set(range(len(rays)))
    for seed in range(30):
        subset = greedy_minimize(rays, bases, seed)
        if len(subset) < len(best):
            best = subset
            print(f"New best size: {len(best)} (seed {seed})")

    # Verify best is uncolorable
    unsat = not ks_satisfiable(len(rays), bases, best)
    print(f"Best size: {len(best)}; uncolorable: {unsat}")

    out_path = ROOT / "artifacts" / "witting_ks_minimize.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        '{"best_size": %d, "subset": %s}\n' % (len(best), sorted(best)),
        encoding="utf-8",
    )
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
