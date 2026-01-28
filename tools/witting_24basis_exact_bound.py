#!/usr/bin/env python3
"""Exact noncontextual bound for the 24-basis Witting KS subset.

Branch-and-bound over bases (not rays) to maximize satisfied bases.
"""
from __future__ import annotations

import json
from pathlib import Path
from itertools import combinations
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


def main():
    rays = construct_witting_40_rays()
    tetrads = find_tetrads(rays)
    subset_indices = load_24basis_subset()
    if not subset_indices:
        print("Missing 24-basis subset; aborting")
        return

    bases = [tetrads[i] for i in subset_indices]
    num_rays = len(rays)
    num_bases = len(bases)

    # Order bases by overlap (heuristic: highest-degree rays first)
    ray_degree = [0] * num_rays
    for b in bases:
        for r in b:
            ray_degree[r] += 1
    bases_order = sorted(range(num_bases), key=lambda i: -sum(ray_degree[r] for r in bases[i]))

    assign = [-1] * num_rays

    best = -1
    best_assign = None

    def base_status(base):
        vals = [assign[r] for r in base]
        ones = sum(v == 1 for v in vals)
        unassigned = sum(v == -1 for v in vals)
        if ones > 1:
            return "dead"
        if ones == 1 and unassigned == 0:
            return "sat"
        if ones == 0 and unassigned == 0:
            return "unsat"
        return "open"

    def backtrack(idx=0, sat_count=0):
        nonlocal best, best_assign

        # Upper bound: all remaining bases could be satisfied
        remaining = num_bases - idx
        if sat_count + remaining <= best:
            return

        if idx == num_bases:
            if sat_count > best:
                best = sat_count
                best_assign = assign.copy()
            return

        bi = bases_order[idx]
        base = bases[bi]

        status = base_status(base)
        if status == "dead":
            # cannot satisfy, skip
            backtrack(idx + 1, sat_count)
            return
        if status == "sat":
            backtrack(idx + 1, sat_count + 1)
            return
        if status == "unsat":
            backtrack(idx + 1, sat_count)
            return

        # open: we can try to satisfy it by choosing a ray as 1 and others 0
        # try each feasible choice
        for r in base:
            # set r=1, others in base=0
            if assign[r] not in (-1, 1):
                continue
            # check conflicts
            changed = []
            ok = True
            for rr in base:
                desired = 1 if rr == r else 0
                if assign[rr] == -1:
                    assign[rr] = desired
                    changed.append(rr)
                elif assign[rr] != desired:
                    ok = False
                    break
            if ok:
                backtrack(idx + 1, sat_count + 1)
            # undo
            for rr in changed:
                assign[rr] = -1

        # also allow it to be unsatisfied (leave assignments as-is)
        backtrack(idx + 1, sat_count)

    backtrack()

    print("Exact max satisfiable bases:", best, "/", num_bases)

    out_path = ROOT / "artifacts" / "witting_24basis_exact_bound.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps({"max_satisfied": best, "bases": num_bases}, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
