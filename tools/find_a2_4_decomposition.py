#!/usr/bin/env python3
"""Find an A2^4 decomposition inside E8 and compare to 27-orbits.

We search for four mutually orthogonal A2 subsystems (each 6 roots),
then summarize how these roots intersect the six 27-orbits.
"""

from __future__ import annotations

import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def build_e8_roots():
    roots = []
    # type 1
    for i in range(8):
        for j in range(i + 1, 8):
            for si in (1, -1):
                for sj in (1, -1):
                    r = [0.0] * 8
                    r[i] = float(si)
                    r[j] = float(sj)
                    roots.append(tuple(r))
    # type 2
    for bits in range(256):
        signs = [1 if (bits >> k) & 1 else -1 for k in range(8)]
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(0.5 * s for s in signs))
    return roots


def dot(r1, r2):
    return sum(a * b for a, b in zip(r1, r2))


def negate(r):
    return tuple(-x for x in r)


def load_we6_orbits(roots):
    path = ROOT / "artifacts" / "we6_orbit_labels.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    mapping = {eval(k): v for k, v in data["mapping"].items()}
    # Map each root index to orbit id
    root_orbit = {}
    for idx, r in enumerate(roots):
        r_key = tuple(int(round(2 * x)) for x in r)
        info = mapping.get(r_key)
        if info:
            root_orbit[idx] = (info["orbit_id"], info["orbit_size"])
    return root_orbit


def build_a2_subsystems(roots):
    idx = {r: i for i, r in enumerate(roots)}
    a2_sets = {}

    for i, j in combinations(range(len(roots)), 2):
        if dot(roots[i], roots[j]) != -1:
            continue
        rsum = tuple(roots[i][k] + roots[j][k] for k in range(8))
        if rsum not in idx:
            continue
        k = idx[rsum]
        # Build full A2 root system: ±alpha, ±beta, ±(alpha+beta)
        indices = sorted(
            {
                i,
                j,
                k,
                idx[negate(roots[i])],
                idx[negate(roots[j])],
                idx[negate(roots[k])],
            }
        )
        if len(indices) != 6:
            continue
        key = tuple(indices)
        a2_sets[key] = indices

    return list(a2_sets.values())


def a2_orthogonal(a2a, a2b, roots):
    for i in a2a:
        for j in a2b:
            if dot(roots[i], roots[j]) != 0:
                return False
    return True


def find_a2_4(roots, a2_list):
    # Build adjacency list of orthogonal A2s
    n = len(a2_list)
    orth = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if a2_orthogonal(a2_list[i], a2_list[j], roots):
                orth[i].add(j)
                orth[j].add(i)

    # Find cliques of size 4
    solutions = []
    for a in range(n):
        cand_b = orth[a]
        for b in cand_b:
            if b <= a:
                continue
            cand_c = cand_b & orth[b]
            for c in cand_c:
                if c <= b:
                    continue
                cand_d = cand_c & orth[c]
                for d in cand_d:
                    if d <= c:
                        continue
                    solutions.append([a, b, c, d])
                    if len(solutions) >= 5:
                        return solutions
    return solutions


def summarize_alignment(roots, a2_list, solution, root_orbit):
    # Build orbit -> roots set
    orbit_sets = defaultdict(set)
    if root_orbit:
        for idx, (oid, osz) in root_orbit.items():
            if osz == 27:
                orbit_sets[oid].add(idx)

    # A2 intersections with 27-orbits
    a2_orbit_hits = []
    for a2_idx in solution:
        a2 = set(a2_list[a2_idx])
        hits = {}
        for oid, oset in orbit_sets.items():
            inter = a2 & oset
            if inter:
                hits[oid] = len(inter)
        a2_orbit_hits.append(hits)

    # Count A2 subsystems fully contained in any 27-orbit
    full_in_orbit = defaultdict(int)
    if orbit_sets:
        for a2_idx in solution:
            a2 = set(a2_list[a2_idx])
            for oid, oset in orbit_sets.items():
                if a2.issubset(oset):
                    full_in_orbit[oid] += 1

    return {
        "a2_orbit_hits": a2_orbit_hits,
        "a2_full_in_27_orbit": dict(full_in_orbit),
    }


def main():
    roots = build_e8_roots()
    root_orbit = load_we6_orbits(roots)

    a2_list = build_a2_subsystems(roots)
    print(f"Found {len(a2_list)} A2 subsystems")

    solutions = find_a2_4(roots, a2_list)
    if not solutions:
        print("No A2^4 decomposition found")
        return

    # Use first solution
    sol = solutions[0]
    a2_indices = [a2_list[i] for i in sol]

    alignment = summarize_alignment(roots, a2_list, sol, root_orbit)

    results = {
        "a2_count": len(a2_list),
        "a2_4_solution_indices": sol,
        "a2_4_solution": a2_indices,
        "alignment_with_27_orbits": alignment,
    }

    out_path = ROOT / "artifacts" / "a2_4_decomposition.json"
    out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    print("A2^4 solution indices:", sol)
    print("Alignment:", alignment)


if __name__ == "__main__":
    main()
