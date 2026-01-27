#!/usr/bin/env python3
"""Witting Polytope to E8 via Realification.

Key insight from literature:
"Both configurations considered as 240 8D real vectors up to some
orthogonal transformation are equivalent with E8."

This tool:
1. Constructs the 240 Witting vertices in C^4
2. Realifies to R^8 (treating C^4 as R^8)
3. Compares to E8 root system
4. Searches for the orthogonal transformation
"""
from __future__ import annotations

import json
from collections import Counter
from itertools import product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def construct_witting_240():
    """Construct all 240 vertices of the Witting polytope.

    From the paper (Eq. 1):
    - 192 vertices: (0, +-omega^mu, +-omega^nu, +-omega^lambda) and permutations
    - 24 vertices: (+-i*omega^lambda*sqrt(3), 0, 0, 0) and permutations
    - Plus additional combinations

    omega = e^(2*pi*i/3) = (-1 + i*sqrt(3))/2
    """
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)

    vertices = []

    # Type 1: Permutations of (0, +-omega^mu, -+omega^nu, +-omega^lambda)
    for mu in range(3):
        for nu in range(3):
            for lam in range(3):
                # (0, +-omega^mu, -+omega^nu, +-omega^lambda)
                for s1, s2, s3 in product([1, -1], repeat=3):
                    v = np.array([0, s1*omega**mu, s2*omega**nu, s3*omega**lam], dtype=complex)
                    for perm in [(0,1,2,3), (1,0,2,3), (2,1,0,3), (3,1,2,0)]:
                        vp = v[list(perm)]
                        vertices.append(tuple(vp))

    # Type 2: (+-i*omega^lambda*sqrt(3), 0, 0, 0) and coordinate permutations
    for lam in range(3):
        for sign in [1, -1]:
            val = sign * 1j * (omega**lam) * sqrt3
            for pos in range(4):
                v = np.zeros(4, dtype=complex)
                v[pos] = val
                vertices.append(tuple(v))

    # Remove duplicates (up to machine precision)
    unique = []
    seen = set()
    for v in vertices:
        # Round for comparison
        key = tuple(round(x.real, 6) + 1j*round(x.imag, 6) for x in v)
        if key not in seen:
            seen.add(key)
            unique.append(np.array(v))

    return unique


def construct_witting_40_rays():
    """Construct the 40 Witting rays (projective classes).

    From the paper (Eq. 2a, 2b):
    - 4 basis states: (1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)
    - 36 states: 4 groups of 9 states each
    """
    omega = np.exp(2j * np.pi / 3)
    sqrt3 = np.sqrt(3)

    rays = []

    # 4 basis states (Eq. 2a)
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)

    # 36 states (Eq. 2b) - 4 groups of 9
    for mu in range(3):
        for nu in range(3):
            # Group 1: (1/sqrt3)(0, 1, -omega^mu, omega^nu)
            rays.append(np.array([0, 1, -omega**mu, omega**nu]) / sqrt3)
            # Group 2: (1/sqrt3)(1, 0, -omega^mu, -omega^nu)
            rays.append(np.array([1, 0, -omega**mu, -omega**nu]) / sqrt3)
            # Group 3: (1/sqrt3)(1, -omega^mu, 0, omega^nu)
            rays.append(np.array([1, -omega**mu, 0, omega**nu]) / sqrt3)
            # Group 4: (1/sqrt3)(1, omega^mu, omega^nu, 0)
            rays.append(np.array([1, omega**mu, omega**nu, 0]) / sqrt3)

    return rays


def realify(v):
    """Convert C^4 vector to R^8 vector."""
    result = np.zeros(8)
    for i in range(4):
        result[2*i] = v[i].real
        result[2*i + 1] = v[i].imag
    return result


def build_e8_roots():
    """Build E8 root system (240 roots in R^8)."""
    roots = []
    # Type 1: +-e_i +- e_j (112 roots)
    for i in range(8):
        for j in range(i+1, 8):
            for si in [1, -1]:
                for sj in [1, -1]:
                    r = [0]*8
                    r[i] = si
                    r[j] = sj
                    roots.append(tuple(r))
    # Type 2: (+-1/2, ..., +-1/2) with even minus signs (128 roots)
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            roots.append(tuple(s/2 for s in signs))
    return np.array(roots, dtype=float)


def compute_gram_matrix(vectors):
    """Compute Gram matrix (inner products) for a set of vectors."""
    n = len(vectors)
    gram = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            gram[i,j] = np.dot(vectors[i], vectors[j])
    return gram


def analyze_inner_products(gram):
    """Analyze the distribution of inner products."""
    n = gram.shape[0]
    ip_counts = Counter()
    for i in range(n):
        for j in range(i+1, n):
            val = round(gram[i,j], 4)
            ip_counts[val] += 1
    return dict(sorted(ip_counts.items()))


def main():
    print("Witting Polytope to E8 via Realification")
    print("=" * 55)

    # Construct Witting 40 rays
    rays_40 = construct_witting_40_rays()
    print(f"\nWitting 40 rays constructed: {len(rays_40)}")

    # Realify to R^8
    rays_40_real = [realify(r) for r in rays_40]
    print(f"Realified to R^8 vectors: {len(rays_40_real)}")

    # Check norms
    norms = [np.linalg.norm(r) for r in rays_40_real]
    print(f"Norms: min={min(norms):.4f}, max={max(norms):.4f}")

    # Normalize
    rays_40_normalized = [r / np.linalg.norm(r) for r in rays_40_real]

    # Compute Gram matrix for 40 rays
    gram_40 = compute_gram_matrix(rays_40_normalized)
    ip_dist_40 = analyze_inner_products(gram_40)
    print("\nInner product distribution (40 normalized rays):")
    for ip, count in ip_dist_40.items():
        print(f"  {ip}: {count} pairs")

    # Build E8 roots
    e8_roots = build_e8_roots()
    print(f"\nE8 roots: {len(e8_roots)}")

    # Normalize E8 roots
    e8_norms = [np.linalg.norm(r) for r in e8_roots]
    print(f"E8 norms: min={min(e8_norms):.4f}, max={max(e8_norms):.4f}")
    e8_normalized = [r / np.linalg.norm(r) for r in e8_roots]

    # Compute E8 Gram matrix
    gram_e8 = compute_gram_matrix(e8_normalized)
    ip_dist_e8 = analyze_inner_products(gram_e8)
    print("\nInner product distribution (240 normalized E8 roots):")
    for ip, count in ip_dist_e8.items():
        print(f"  {ip}: {count} pairs")

    # The key question: Can we find an orthogonal transformation O such that
    # O * Witting_vertices = E8_roots (up to permutation)?

    print("\n" + "=" * 55)
    print("COMPARISON: Witting 40 vs E8 240")
    print("=" * 55)

    # Compare cardinalities
    print(f"\nWitting rays: 40 (from 240 vertices / 6 phases)")
    print(f"E8 roots: 240 (or 120 root lines)")

    # The relationship: 240 Witting vertices -> 40 rays (6:1 phase quotient)
    # The relationship: 240 E8 roots -> 120 root lines (2:1 antipodal quotient)

    # Check if Witting inner products match a subset of E8
    print("\nWitting 40 inner products vs E8:")
    witting_ips = set(ip_dist_40.keys())
    e8_ips = set(ip_dist_e8.keys())
    print(f"  Witting IPs: {sorted(witting_ips)}")
    print(f"  E8 IPs: {sorted(e8_ips)}")
    print(f"  Intersection: {sorted(witting_ips & e8_ips)}")

    # The full 240 Witting vertices
    print("\n" + "=" * 55)
    print("FULL 240 WITTING VERTICES")
    print("=" * 55)

    # Construct via phase multiplication of the 40 rays
    omega = np.exp(2j * np.pi / 3)
    phases = [1, omega, omega**2, -1, -omega, -omega**2]

    vertices_240 = []
    for ray in rays_40:
        for phase in phases:
            vertices_240.append(phase * ray)

    print(f"240 Witting vertices (40 rays x 6 phases): {len(vertices_240)}")

    # Realify all 240
    verts_240_real = [realify(v) for v in vertices_240]

    # Normalize
    verts_240_normalized = [v / np.linalg.norm(v) for v in verts_240_real]

    # Compute Gram matrix
    gram_240 = compute_gram_matrix(verts_240_normalized)
    ip_dist_240 = analyze_inner_products(gram_240)

    print("\nInner product distribution (240 normalized Witting vertices):")
    for ip, count in ip_dist_240.items():
        print(f"  {ip}: {count} pairs")

    # Compare with E8
    print("\n" + "=" * 55)
    print("WITTING 240 vs E8 240 COMPARISON")
    print("=" * 55)

    witting_240_ips = set(ip_dist_240.keys())
    print(f"\nWitting 240 inner products: {sorted(witting_240_ips)}")
    print(f"E8 inner products: {sorted(e8_ips)}")

    # Check if they match
    if witting_240_ips == e8_ips:
        print("\nINNER PRODUCT SETS MATCH!")
        # Check counts
        counts_match = all(ip_dist_240.get(ip) == ip_dist_e8.get(ip) for ip in e8_ips)
        if counts_match:
            print("INNER PRODUCT DISTRIBUTIONS MATCH!")
            print("This strongly suggests an orthogonal equivalence!")
        else:
            print("Inner product counts differ:")
            for ip in sorted(e8_ips):
                w = ip_dist_240.get(ip, 0)
                e = ip_dist_e8.get(ip, 0)
                if w != e:
                    print(f"  {ip}: Witting={w}, E8={e}")
    else:
        print("\nInner product sets differ:")
        print(f"  Only in Witting: {sorted(witting_240_ips - e8_ips)}")
        print(f"  Only in E8: {sorted(e8_ips - witting_240_ips)}")

    # Save results
    results = {
        "witting_40": {
            "count": 40,
            "inner_products": {str(k): v for k, v in ip_dist_40.items()},
        },
        "witting_240": {
            "count": 240,
            "inner_products": {str(k): v for k, v in ip_dist_240.items()},
        },
        "e8": {
            "count": 240,
            "inner_products": {str(k): v for k, v in ip_dist_e8.items()},
        },
        "comparison": {
            "witting_240_ips_equal_e8": witting_240_ips == e8_ips,
        }
    }

    out_path = ROOT / "artifacts" / "witting_e8_realification.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2), encoding='utf-8')
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
