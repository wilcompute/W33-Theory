from __future__ import annotations

import json
import math
import os
from dataclasses import asdict
from datetime import datetime
from itertools import permutations
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from lib.permutation_group import Perm, PermutationGroup
from lib.simplicial_homology import betti_numbers_via_primes
from lib.w33_io import (W33DataPaths, load_w33_lines, load_w33_rays,
                        simplices_from_lines)


def ray_equiv(a: np.ndarray, b: np.ndarray, *, rtol=1e-6, atol=1e-8) -> bool:
    """Check whether a and b are the same projective ray: a ≈ λ b for |λ|=1."""

    # Find a nonzero coordinate to estimate λ.
    idx = None
    for i in range(len(a)):
        if abs(b[i]) > 1e-12:
            idx = i
            break
    if idx is None:
        return False

    lam = a[idx] / b[idx]
    if abs(lam) < 1e-12:
        return False
    lam /= abs(lam)
    return np.allclose(a, lam * b, rtol=rtol, atol=atol)


def canonical_ray_key(
    v: np.ndarray, *, eps: float = 1e-12, ndigits: int = 10
) -> Tuple[float, ...]:
    """Canonicalize a ray up to global phase by dividing by first nonzero entry."""

    idx = None
    for i in range(len(v)):
        if abs(v[i]) > eps:
            idx = i
            break
    if idx is None:
        return tuple([0.0] * (2 * len(v)))

    w = v / v[idx]
    out: List[float] = []
    for z in w:
        out.append(round(float(np.real(z)), ndigits))
        out.append(round(float(np.imag(z)), ndigits))
    return tuple(out)


def build_ray_index(V: np.ndarray) -> Dict[Tuple[float, ...], List[int]]:
    idx: Dict[Tuple[float, ...], List[int]] = {}
    for i in range(V.shape[0]):
        k = canonical_ray_key(V[i])
        idx.setdefault(k, []).append(i)
    return idx


def induced_point_permutation_from_unitary(
    V: np.ndarray,
    U: np.ndarray,
    *,
    ray_index: Dict[Tuple[float, ...], List[int]] | None = None,
) -> Perm | None:
    """If U sends the set of rays to itself, return the induced permutation of point ids."""

    V_new = (U @ V.T).T
    n = V.shape[0]

    if ray_index is None:
        ray_index = build_ray_index(V)

    mapping = [-1] * n
    used = set()

    for p in range(n):
        v = V_new[p]
        found = None
        cand = ray_index.get(canonical_ray_key(v), [])
        # If key collides, disambiguate via exact ray_equiv
        for q in cand:
            if q in used:
                continue
            if ray_equiv(v, V[q]):
                found = q
                break
        if found is None:
            return None
        mapping[p] = found
        used.add(found)

    return tuple(mapping)


def coordinate_permutation_generators(V: np.ndarray) -> List[Perm]:
    """Build point permutations induced by permuting the C^4 coordinates.

    This yields a subgroup ≤ S_40 that is guaranteed to preserve the ray-realization.
    """

    gens: List[Perm] = []
    ray_index = build_ray_index(V)
    for perm in permutations(range(4)):
        P = np.zeros((4, 4), dtype=np.complex128)
        for i, j in enumerate(perm):
            P[i, j] = 1.0
        p = induced_point_permutation_from_unitary(V, P, ray_index=ray_index)
        if p is not None and p not in gens:
            gens.append(p)

    return gens


def monomial_z12_generators(
    V: np.ndarray,
    *,
    root_order: int = 12,
    sample_points: int = 6,
    max_generators: int = 40,
    progress_every: int = 2000,
) -> List[Perm]:
    """Search for ray-automorphisms among monomial unitaries: U = D P.

    - P is a 4x4 permutation matrix.
    - D is diagonal with entries in the `root_order` roots of unity.
    - Overall global phase is irrelevant, so we fix D[0,0] = 1 to reduce search.

    This is a concrete, group-theory flavored way to look for the subgroup of the
    ray-realization automorphism group coming from Z_12 phase structure.
    """

    roots = [np.exp(2j * np.pi * k / root_order) for k in range(root_order)]
    n = V.shape[0]
    # deterministic sample to prune candidates quickly
    sample = list(range(min(n, sample_points)))

    ray_index = build_ray_index(V)

    gens: List[Perm] = []

    checked = 0

    for perm in permutations(range(4)):
        P = np.zeros((4, 4), dtype=np.complex128)
        for i, j in enumerate(perm):
            P[i, j] = 1.0

        for k1 in range(root_order):
            for k2 in range(root_order):
                for k3 in range(root_order):
                    D = np.diag([1.0 + 0j, roots[k1], roots[k2], roots[k3]]).astype(
                        np.complex128
                    )
                    U = D @ P

                    checked += 1
                    if checked % progress_every == 0:
                        print(
                            f"  checked {checked} monomial candidates; generators={len(gens)}"
                        )

                    # fast prune: check a small sample maps to *some* ray
                    V_new = (U @ V.T).T
                    ok = True
                    for p in sample:
                        v = V_new[p]
                        cand = ray_index.get(canonical_ray_key(v), [])
                        if not any(ray_equiv(v, V[q]) for q in cand):
                            ok = False
                            break
                    if not ok:
                        continue

                    perm_pts = induced_point_permutation_from_unitary(
                        V, U, ray_index=ray_index
                    )
                    if perm_pts is None:
                        continue
                    if perm_pts not in gens:
                        gens.append(perm_pts)
                        if len(gens) >= max_generators:
                            return gens

    return gens


def main() -> int:
    paths = W33DataPaths.from_this_file(__file__)

    lines = load_w33_lines(paths)
    simplices = simplices_from_lines(lines)

    topo = betti_numbers_via_primes(simplices)

    print("=" * 90)
    print("W33 GROUP + ALGEBRAIC TOPOLOGY WORKBENCH")
    print("=" * 90)
    print("\nSimplicial complex (line-K4 flag complex):")
    for k in sorted(simplices.keys()):
        print(f"  dim {k}: {len(simplices[k])} simplices")

    print("\nHomology (estimated over Q via multi-prime ranks):")
    for k in sorted(topo.betti_estimate.keys()):
        print(f"  beta_{k} = {topo.betti_estimate[k]}")
    print(f"  Euler characteristic chi = {topo.euler_characteristic}")

    # Group theory: start with ray-realization automorphisms we can concretely detect.
    V = load_w33_rays(paths)
    coord_gens = coordinate_permutation_generators(V)
    mono_gens = monomial_z12_generators(V, root_order=12, sample_points=10)

    print("\nRay-realization automorphisms (search):")
    print(f"  coordinate-only generators found: {len(coord_gens)}")
    print(f"  Z12-monomial generators found: {len(mono_gens)}")

    gens_all = list(coord_gens)
    for g in mono_gens:
        if g not in gens_all:
            gens_all.append(g)

    line_orbits: List[List[int]] = []
    if gens_all:
        G = PermutationGroup(n=40, generators=tuple(gens_all))
        elements = G.closure(max_size=20000)
        group_order = len(elements)
        print(f"  detected subgroup size (capped at 20000): {group_order}")
        orbs = G.orbits(list(range(40)), max_size=20000)
        print(f"  point orbits: {len(orbs)}")
        print(f"  orbit sizes: {[len(o) for o in orbs]}")

        # Action on lines (treat each line as a 4-set of points)
        line_sets = [tuple(sorted(L)) for L in lines]
        line_index = {L: i for i, L in enumerate(line_sets)}

        def act_on_line(g: Perm, L: Tuple[int, int, int, int]) -> int:
            img = tuple(sorted(g[x] for x in L))
            return line_index[img]

        unassigned = set(range(len(lines)))
        while unassigned:
            seed = next(iter(unassigned))
            orbit = set()
            for g in elements:
                orbit.add(act_on_line(g, line_sets[seed]))
            for x in orbit:
                unassigned.discard(x)
            line_orbits.append(sorted(orbit))

        print(f"  line orbits: {len(line_orbits)}")
        print(f"  line orbit sizes: {[len(o) for o in line_orbits]}")
    else:
        elements = []
        group_order = 0
        orbs = [[i] for i in range(40)]

    out = {
        "timestamp": datetime.now().isoformat(),
        "topology": {
            "simplex_counts": {str(k): len(v) for k, v in simplices.items()},
            "euler_characteristic": topo.euler_characteristic,
            "betti_estimate": topo.betti_estimate,
            "betti_by_prime": topo.betti_by_prime,
            "primes": topo.primes,
        },
        "group": {
            "coordinate_perm_generators": len(coord_gens),
            "z12_monomial_generators": len(mono_gens),
            "ray_auto_subgroup_size_capped": len(elements),
            "ray_auto_subgroup_order": group_order,
            "point_orbits": [o for o in orbs],
            "line_orbits": [o for o in line_orbits],
        },
    }

    data_dir = paths.data_root
    data_dir.mkdir(parents=True, exist_ok=True)
    out_json = data_dir / "w33_group_topology_results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=int)

    print("\nSaved:")
    print(f"  {out_json}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
