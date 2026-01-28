#!/usr/bin/env python3
"""
THEORY PART CXLIX: MUB SUBSETS IN THE WITTING CONFIGURATION
============================================================

The 40 Witting states form 40 orthonormal bases.
But they are NOT mutually unbiased bases (MUBs).

For MUBs in ℂ⁴: |⟨ψ|φ⟩|² = 1/4 for states from different bases
For Witting:    |⟨ψ|φ⟩|² = 1/3 for non-orthogonal pairs

Question: Can we find MUB SUBSETS within the Witting structure?
"""

from itertools import combinations

import numpy as np

print("=" * 70)
print("PART CXLIX: MUB SUBSETS IN THE WITTING CONFIGURATION")
print("=" * 70)

omega = np.exp(2j * np.pi / 3)

# =====================================================
# BUILD WITTING STATES AND BASES
# =====================================================


def build_witting_states():
    states = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        states.append(v)

    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([0, 1, -(omega**mu), omega**nu]) / np.sqrt(3))
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([1, 0, -(omega**mu), -(omega**nu)]) / np.sqrt(3))
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([1, -(omega**mu), 0, omega**nu]) / np.sqrt(3))
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([1, omega**mu, omega**nu, 0]) / np.sqrt(3))

    return states


def find_bases(states):
    n = len(states)
    adj = [
        [abs(np.vdot(states[i], states[j])) ** 2 < 1e-10 for j in range(n)]
        for i in range(n)
    ]

    bases = []
    for i in range(n):
        neighbors_i = [j for j in range(n) if adj[i][j]]
        for j in neighbors_i:
            if j <= i:
                continue
            for k in neighbors_i:
                if k <= j or not adj[j][k]:
                    continue
                for l in neighbors_i:
                    if l <= k or not adj[j][l] or not adj[k][l]:
                        continue
                    bases.append(frozenset([i, j, k, l]))

    return list(set(bases))


states = build_witting_states()
bases = find_bases(states)

print(f"Built {len(states)} Witting states")
print(f"Found {len(bases)} orthonormal bases")

# =====================================================
# MUB DEFINITION
# =====================================================

print("\n" + "=" * 70)
print("MUTUALLY UNBIASED BASES (MUBs)")
print("=" * 70)

print("""
DEFINITION:
===========

Two orthonormal bases B₁ = {|ψᵢ⟩} and B₂ = {|φⱼ⟩} in ℂᵈ are
MUTUALLY UNBIASED if:

    |⟨ψᵢ|φⱼ⟩|² = 1/d   for all i, j

For ℂ⁴ (d=4): MUB criterion is |⟨ψ|φ⟩|² = 1/4 = 0.25

WITTING CONFIGURATION:
======================

For non-orthogonal Witting states: |⟨ψ|φ⟩|² = 1/3 ≈ 0.333

So Witting bases are NOT mutually unbiased!

But can we find SUBSETS of bases that ARE mutually unbiased?
""")

# =====================================================
# CHECK PAIRWISE BASIS UNBIASEDNESS
# =====================================================

print("\n" + "=" * 70)
print("PAIRWISE BASIS ANALYSIS")
print("=" * 70)


def are_mub(basis1, basis2, tolerance=0.01):
    """Check if two bases are mutually unbiased (|⟨ψ|φ⟩|² = 1/4)"""
    for i in basis1:
        for j in basis2:
            ip_sq = abs(np.vdot(states[i], states[j])) ** 2
            if abs(ip_sq - 0.25) > tolerance:
                return False, ip_sq
    return True, 0.25


def inner_product_between_bases(basis1, basis2):
    """Get all inner products between two bases"""
    ips = []
    for i in basis1:
        for j in basis2:
            ips.append(abs(np.vdot(states[i], states[j])) ** 2)
    return ips


# Check what inner products appear between different bases
print("Inner products between different bases:")
ip_counts = {}
sample_pairs = 0
for i, b1 in enumerate(bases):
    for j, b2 in enumerate(bases):
        if j <= i:
            continue
        if b1 & b2:  # Bases share a state
            continue

        ips = inner_product_between_bases(b1, b2)
        for ip in ips:
            ip_rounded = round(ip, 4)
            ip_counts[ip_rounded] = ip_counts.get(ip_rounded, 0) + 1
        sample_pairs += 1

print(f"Sampled {sample_pairs} disjoint basis pairs")
print(f"Inner product values found:")
for ip, count in sorted(ip_counts.items()):
    print(f"  |⟨ψ|φ⟩|² = {ip:.4f}: {count} times")

# =====================================================
# SEARCH FOR MUB PAIRS
# =====================================================

print("\n" + "=" * 70)
print("SEARCHING FOR MUB PAIRS")
print("=" * 70)

# Check if ANY pair of bases is mutually unbiased
mub_pairs = []
almost_mub_pairs = []

for i, b1 in enumerate(bases):
    for j, b2 in enumerate(bases):
        if j <= i:
            continue
        if b1 & b2:  # Skip if bases share a state
            continue

        ips = inner_product_between_bases(b1, b2)
        min_ip = min(ips)
        max_ip = max(ips)

        if abs(min_ip - 0.25) < 0.01 and abs(max_ip - 0.25) < 0.01:
            mub_pairs.append((i, j))
        elif abs(min_ip - max_ip) < 0.01:  # Uniform but not 1/4
            almost_mub_pairs.append((i, j, min_ip))

print(f"Found {len(mub_pairs)} MUB pairs (|⟨ψ|φ⟩|² = 1/4)")
print(f"Found {len(almost_mub_pairs)} 'almost MUB' pairs (uniform but ≠ 1/4)")

if almost_mub_pairs:
    print("\n'Almost MUB' pairs (uniform inner products):")
    for i, j, ip in almost_mub_pairs[:10]:
        print(f"  Bases {sorted(bases[i])} and {sorted(bases[j])}: |⟨ψ|φ⟩|² = {ip:.4f}")

# =====================================================
# THE STANDARD MUBs IN ℂ⁴
# =====================================================

print("\n" + "=" * 70)
print("STANDARD MUBs IN ℂ⁴")
print("=" * 70)

print("""
In ℂ⁴, there exist 5 MUBs (the maximum possible for d=4):

B₀: Computational basis {|0⟩, |1⟩, |2⟩, |3⟩}

B₁-B₄: Constructed from tensor products of qubit MUBs

The standard construction uses ω₄ = e^{2πi/4} = i

These are DIFFERENT from the Witting configuration which uses ω₃ = e^{2πi/3}
""")

# Build standard MUBs for comparison
omega4 = np.exp(2j * np.pi / 4)  # = i

# Computational basis
mub_0 = [
    np.array([1, 0, 0, 0]),
    np.array([0, 1, 0, 0]),
    np.array([0, 0, 1, 0]),
    np.array([0, 0, 0, 1]),
]

# Fourier basis (tensor of Hadamard)
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
HH = np.kron(H, H)
mub_1 = [HH[:, i] for i in range(4)]


# Other MUBs from tensor products
def build_mub_4():
    """Build all 5 standard MUBs in ℂ⁴"""
    mubs = []

    # B0: Computational
    mubs.append(
        [
            np.array([1, 0, 0, 0], dtype=complex),
            np.array([0, 1, 0, 0], dtype=complex),
            np.array([0, 0, 1, 0], dtype=complex),
            np.array([0, 0, 0, 1], dtype=complex),
        ]
    )

    # B1-B4: From qubit tensor products with phases
    # Using the standard construction
    omega = np.exp(2j * np.pi / 4)  # i

    # B1
    b1 = []
    for a in [0, 1]:
        for b in [0, 1]:
            v = (
                np.array(
                    [1, omega ** (2 * a), omega ** (2 * b), omega ** (2 * (a + b))]
                )
                / 2
            )
            b1.append(v)
    mubs.append(b1)

    # B2
    b2 = []
    for a in [0, 1]:
        for b in [0, 1]:
            v = (
                np.array(
                    [
                        1,
                        omega ** (2 * a + 1),
                        omega ** (2 * b),
                        omega ** (2 * (a + b) + 1),
                    ]
                )
                / 2
            )
            b2.append(v)
    mubs.append(b2)

    # B3
    b3 = []
    for a in [0, 1]:
        for b in [0, 1]:
            v = (
                np.array(
                    [
                        1,
                        omega ** (2 * a),
                        omega ** (2 * b + 1),
                        omega ** (2 * (a + b) + 1),
                    ]
                )
                / 2
            )
            b3.append(v)
    mubs.append(b3)

    # B4
    b4 = []
    for a in [0, 1]:
        for b in [0, 1]:
            v = (
                np.array(
                    [
                        1,
                        omega ** (2 * a + 1),
                        omega ** (2 * b + 1),
                        omega ** (2 * (a + b)),
                    ]
                )
                / 2
            )
            b4.append(v)
    mubs.append(b4)

    return mubs


standard_mubs = build_mub_4()

print("Verifying standard MUBs:")
for i in range(5):
    for j in range(i + 1, 5):
        ips = []
        for v1 in standard_mubs[i]:
            for v2 in standard_mubs[j]:
                ips.append(abs(np.vdot(v1, v2)) ** 2)
        print(f"  B{i} vs B{j}: |⟨ψ|φ⟩|² = {set(np.round(ips, 4))}")

# =====================================================
# WITTING VS MUB COMPARISON
# =====================================================

print("\n" + "=" * 70)
print("WITTING CONFIGURATION VS STANDARD MUBs")
print("=" * 70)

print("""
COMPARISON:
===========

                    WITTING                    STANDARD MUBs
                    -------                    -------------
Dimension:          ℂ⁴                         ℂ⁴
States:             40                         20 (5 bases × 4)
Bases:              40                         5
Inner products:     0 or 1/3                   0 or 1/4
Root of unity:      ω₃ = e^{2πi/3}            ω₄ = e^{2πi/4} = i
Symmetry group:     W(E₆) (order 51840)       Unknown/smaller

KEY DIFFERENCE:
===============

MUBs optimize for UNIFORM sampling: each basis gives equal
information about any state from another basis.

Witting optimizes for CONTEXTUALITY: maximum Kochen-Specker
obstruction with equiangular states.

Different inner products (1/3 vs 1/4) serve different purposes!
""")

# =====================================================
# DO STANDARD MUBs APPEAR IN WITTING?
# =====================================================

print("\n" + "=" * 70)
print("DO STANDARD MUBs APPEAR IN WITTING?")
print("=" * 70)


# Check if any standard MUB state is (close to) a Witting state
def find_closest_witting(target):
    """Find the Witting state closest to target"""
    overlaps = [abs(np.vdot(target, s)) ** 2 for s in states]
    max_idx = np.argmax(overlaps)
    return max_idx, overlaps[max_idx]


print("Closest Witting states to standard MUB states:")
for mub_idx, mub in enumerate(standard_mubs):
    print(f"\n  MUB B{mub_idx}:")
    for v_idx, v in enumerate(mub):
        w_idx, overlap = find_closest_witting(v)
        print(f"    State {v_idx}: closest Witting is {w_idx}, overlap = {overlap:.4f}")

# =====================================================
# EMBEDDED 3D MUBs
# =====================================================

print("\n" + "=" * 70)
print("3D MUBs EMBEDDED IN WITTING?")
print("=" * 70)

print("""
In ℂ³, there exist 4 MUBs (maximum for d=3).
Inner product criterion: |⟨ψ|φ⟩|² = 1/3

This MATCHES the Witting non-orthogonal inner product!

Question: Do the Witting states restricted to any ℂ³ subspace
          contain a set of 4 MUBs?

The 12 neighbors of any vertex span a ℂ³ subspace perpendicular
to that vertex. Let's check if they contain 3D MUBs.
""")

# Get the 12 neighbors of vertex 0 (they span ℂ³)
neighbors = [j for j in range(40) if abs(np.vdot(states[0], states[j])) ** 2 < 1e-10]

# Project to ℂ³ (drop first coordinate which is 0 for all neighbors)
neighbor_states_3d = [states[n][1:4] for n in neighbors]

print(f"12 neighbors of |0⟩, projected to ℂ³:")
for i, s in enumerate(neighbor_states_3d[:5]):
    print(f"  State {neighbors[i]}: {s}")


# Find orthonormal bases within these 12 states
def find_3d_bases(states_3d, indices):
    """Find all orthonormal bases (size 3) among the 3D states"""
    n = len(states_3d)
    bases_3d = []
    for i in range(n):
        for j in range(i + 1, n):
            if abs(np.vdot(states_3d[i], states_3d[j])) ** 2 < 1e-10:
                for k in range(j + 1, n):
                    if (
                        abs(np.vdot(states_3d[i], states_3d[k])) ** 2 < 1e-10
                        and abs(np.vdot(states_3d[j], states_3d[k])) ** 2 < 1e-10
                    ):
                        bases_3d.append((indices[i], indices[j], indices[k]))
    return bases_3d


bases_in_3d = find_3d_bases(neighbor_states_3d, neighbors)
print(f"\nFound {len(bases_in_3d)} orthonormal bases in the ℂ³ subspace:")
for b in bases_in_3d:
    print(f"  {b}")

# Check if any pair of these 3D bases are MUBs (|⟨ψ|φ⟩|² = 1/3)
print("\nChecking for 3D MUB pairs:")
mub_3d_pairs = []
for i, b1 in enumerate(bases_in_3d):
    for j, b2 in enumerate(bases_in_3d):
        if j <= i:
            continue
        if set(b1) & set(b2):
            continue

        ips = []
        for idx1 in b1:
            for idx2 in b2:
                ip = abs(np.vdot(states[idx1], states[idx2])) ** 2
                ips.append(ip)

        if all(abs(ip - 1 / 3) < 0.01 for ip in ips):
            mub_3d_pairs.append((b1, b2))
            print(f"  MUB pair: {b1} and {b2}")

print(f"\nTotal 3D MUB pairs found: {len(mub_3d_pairs)}")

print("\n" + "=" * 70)
print("PART CXLIX COMPLETE")
print("=" * 70)

print("""
KEY FINDINGS:
=============

1. WITTING IS NOT A MUB SYSTEM
   - Non-orthogonal pairs have |⟨ψ|φ⟩|² = 1/3, not 1/4
   - No pairs of Witting bases are mutually unbiased

2. DIFFERENT DESIGN PRINCIPLES
   - MUBs: Uniform information gain (1/d inner products)
   - Witting: Maximum contextuality (equiangular tight frame)

3. 3D MUB STRUCTURE WITHIN WITTING
   - The 12 neighbors span ℂ³ with |⟨ψ|φ⟩|² = 1/3
   - This IS the 3D MUB criterion!
   - The 4 triangles ARE 4 MUBs in ℂ³

4. WITTING CONTAINS EMBEDDED 3D MUBs
   - At each vertex, the 12 neighbors form 4 MUBs in ℂ³
   - This is the MAXIMUM number of MUBs in dimension 3!
""")
