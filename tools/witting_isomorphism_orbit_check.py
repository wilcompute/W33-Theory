#!/usr/bin/env python3
"""Check uniqueness class of the graph isomorphism under Aut(W33).

We use the monomial symmetry subgroup (order 243) as a tractable proxy
for Aut(W33) to test whether the phase law is invariant under symmetries.
"""
from __future__ import annotations

import json
import itertools
from collections import Counter
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
            phase_vec = np.array([omega**a0, omega**a1, omega**a2, omega**a3], dtype=complex)
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


def load_mapping():
    path = ROOT / "artifacts" / "witting_graph_isomorphism.json"
    data = json.loads(path.read_text())
    mapping = {int(k): int(v) for k, v in data["mapping"].items()}
    return mapping


def main():
    rays = construct_witting_40_rays()
    group = build_monomial_group(rays)
    base_map = load_mapping()

    # treat mapping as a 40-vector; apply symmetry to ray labels
    # new mapping = base_map ∘ g^{-1}
    def apply_map(g):
        inv = [0]*40
        for i, gi in enumerate(g):
            inv[gi] = i
        return {i: base_map[inv[i]] for i in range(40)}

    # count distinct mappings under the monomial group
    maps = {}
    for g in group:
        m = apply_map(g)
        key = tuple(m[i] for i in range(40))
        maps[key] = 1

    out = {
        "monomial_group": len(group),
        "distinct_maps": len(maps),
    }

    out_path = ROOT / "artifacts" / "witting_isomorphism_orbit_check.json"
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    md_path = ROOT / "docs" / "witting_isomorphism_orbit_check.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Isomorphism Orbit Check (Monomial Subgroup)\n\n")
        f.write(f"Monomial group size: **{len(group)}**\n")
        f.write(f"Distinct mappings from base isomorphism: **{len(maps)}**\n")
    print(f"Wrote {out_path}")
    print(f"Wrote {md_path}")


if __name__ == "__main__":
    main()
