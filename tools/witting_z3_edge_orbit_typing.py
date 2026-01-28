#!/usr/bin/env python3
"""Type monomial edge orbits by family-pair and basis involvement.

We assign each orbit a signature: distribution over family-pair blocks and
basis involvement (BB/BN/NN), to interpret the 12 orbits (8x27, 4x81).
"""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict, deque
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


def canonical_key(ray, tol=1e-6):
    idx = None
    for i, z in enumerate(ray):
        if abs(z) > tol:
            idx = i
            break
    if idx is None:
        return None
    ray_n = ray / ray[idx]
    key = tuple((round(float(z.real), 6), round(float(z.imag), 6)) for z in ray_n)
    return key


def build_monomial_group(rays):
    omega = np.exp(2j * np.pi / 3)
    phases = [0, 1, 2]
    ray_key = [canonical_key(r) for r in rays]
    key_to_idx = {k: i for i, k in enumerate(ray_key)}
    elements = []
    for perm in itertools.permutations(range(4)):
        for a0, a1, a2, a3 in itertools.product(phases, repeat=4):
            phase_vec = np.array(
                [omega**a0, omega**a1, omega**a2, omega**a3], dtype=complex
            )
            mapping = []
            valid = True
            for r in rays:
                v = r[list(perm)] * phase_vec
                key = canonical_key(v)
                if key not in key_to_idx:
                    valid = False
                    break
                mapping.append(key_to_idx[key])
            if valid:
                elements.append(mapping)
    return elements


def build_nonorth_edges(rays, tol=1e-8):
    edges = []
    for i in range(len(rays)):
        for j in range(i + 1, len(rays)):
            if abs(np.vdot(rays[i], rays[j])) >= tol:
                edges.append((i, j))
    return edges


def ray_family(idx):
    if idx < 4:
        return ("B", None, None)
    t = idx - 4
    pair = t // 4
    fam = t % 4
    mu = pair // 3
    nu = pair % 3
    return (f"F{fam}", mu, nu)


def orbit_decomposition(edge_maps, m):
    seen = set()
    orbits = []
    for e_idx in range(m):
        if e_idx in seen:
            continue
        orb = set()
        queue = deque([e_idx])
        seen.add(e_idx)
        while queue:
            cur = queue.popleft()
            orb.add(cur)
            for emap in edge_maps:
                nxt = emap[cur]
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        orbits.append(sorted(orb))
    return orbits


def main():
    print("EDGE ORBIT TYPING")
    print("=" * 60)
    rays = construct_witting_40_rays()
    edges = build_nonorth_edges(rays)
    edge_index = {e: idx for idx, e in enumerate(edges)}

    group = build_monomial_group(rays)
    edge_maps = []
    for g in group:
        emap = []
        for i, j in edges:
            a, b = g[i], g[j]
            if a > b:
                a, b = b, a
            emap.append(edge_index[(a, b)])
        edge_maps.append(emap)

    orbits = orbit_decomposition(edge_maps, len(edges))
    sizes = [len(o) for o in orbits]
    print(f"Orbits: {len(orbits)} sizes={sorted(sizes)}")

    out_path = ROOT / "docs" / "witting_z3_edge_orbit_typing.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Orbits: {len(orbits)} sizes={sorted(sizes)}\n")
        for idx, orb in enumerate(orbits):
            fam_dist = Counter()
            bb = Counter()
            for e in orb:
                i, j = edges[e]
                fi, _, _ = ray_family(i)
                fj, _, _ = ray_family(j)
                key = tuple(sorted((fi, fj)))
                fam_dist[key] += 1
                bi = i < 4
                bj = j < 4
                bkey = "BB" if bi and bj else "BN" if (bi or bj) else "NN"
                bb[bkey] += 1
            f.write(f"Orbit {idx} size {len(orb)}\n")
            f.write(f"  family pairs: {dict(fam_dist)}\n")
            f.write(f"  basis types: {dict(bb)}\n")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
