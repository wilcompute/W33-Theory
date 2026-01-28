#!/usr/bin/env python3
"""Check KS uncolorability for the Witting 40-ray configuration.

We seek a 0/1 assignment to 40 rays such that each tetrad (basis)
contains exactly one '1'. If no assignment exists, configuration is
KS-uncolorable (state-independent contextuality).
"""

from __future__ import annotations

import itertools
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


def ks_satisfiable(num_rays, bases):
    # For each base, exactly one 1.
    ray_bases = [[] for _ in range(num_rays)]
    for bi, base in enumerate(bases):
        for r in base:
            ray_bases[r].append(bi)

    # Assignment: -1 unassigned, 0 or 1
    assign = [-1] * num_rays
    base_ones = [0] * len(bases)
    base_unassigned = [4] * len(bases)

    # Order rays by degree
    order = sorted(range(num_rays), key=lambda r: -len(ray_bases[r]))

    def propagate(ray, val):
        # Update bases containing ray
        for bi in ray_bases[ray]:
            base_unassigned[bi] -= 1
            if val == 1:
                base_ones[bi] += 1
                # If more than one 1, fail
                if base_ones[bi] > 1:
                    return False
            # If no slots left for a 1, fail
            if base_ones[bi] + base_unassigned[bi] < 1:
                return False
        return True

    def undo(ray, val):
        for bi in ray_bases[ray]:
            base_unassigned[bi] += 1
            if val == 1:
                base_ones[bi] -= 1

    def forced_zeros():
        # If a base already has a 1, all other rays in that base must be 0
        forced = []
        for bi, base in enumerate(bases):
            if base_ones[bi] == 1:
                for r in base:
                    if assign[r] == -1:
                        forced.append(r)
        return forced

    def backtrack(idx=0):
        if idx == num_rays:
            # Check all bases have exactly one 1
            return all(base_ones[bi] == 1 for bi in range(len(bases)))

        ray = order[idx]
        if assign[ray] != -1:
            return backtrack(idx + 1)

        # Try 1 then 0 (heuristic)
        for val in (1, 0):
            assign[ray] = val
            ok = propagate(ray, val)
            if ok:
                # Force zeros if needed
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
                # undo forced
                for r in reversed(stack):
                    undo(r, 0)
                    assign[r] = -1
            # undo
            undo(ray, val)
            assign[ray] = -1
        return False

    return backtrack()


def main():
    rays = construct_witting_40_rays()
    bases = find_tetrads(rays)

    print("Witting KS uncolorability check")
    print("=" * 45)
    print(f"Rays: {len(rays)}")
    print(f"Bases: {len(bases)}")

    sat = ks_satisfiable(len(rays), bases)
    print(f"Satisfiable 0/1 assignment: {sat}")

    out_path = ROOT / "artifacts" / "witting_ks_uncolorable.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        '{"satisfiable": %s}\n' % ("true" if sat else "false"),
        encoding="utf-8",
    )
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
