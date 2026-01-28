#!/usr/bin/env python3
"""
THEORY PART CXXXVIII: THE EXPLICIT 40 WITTING STATES
====================================================

From Vlasov arXiv:2503.18431, Equation (2):

The 40 Witting states consist of:
- 4 standard basis states: (1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1)
- 36 superposition states in 4 groups of 9 each:
  Group 1: (0, 1, -ω^μ, ω^ν)/√3
  Group 2: (1, 0, -ω^μ, -ω^ν)/√3
  Group 3: (1, -ω^μ, 0, ω^ν)/√3
  Group 4: (1, ω^μ, ω^ν, 0)/√3

where μ,ν ∈ {0,1,2} and ω = e^{2πi/3}.
"""

from itertools import product

import numpy as np

print("=" * 70)
print("PART CXXXVIII: THE EXPLICIT 40 WITTING STATES (FROM VLASOV)")
print("=" * 70)

omega = np.exp(2j * np.pi / 3)  # Cube root of unity


def build_vlasov_witting_states():
    """
    Build the 40 Witting states using Vlasov's explicit formulas.
    """
    states = []
    labels = []

    # TYPE 1: Standard basis (4 states)
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        states.append(v)
        labels.append(f"e{i}")

    # TYPE 2: 36 superposition states
    # Group 1: (0, 1, -ω^μ, ω^ν)/√3
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            v = np.array([0, 1, -(omega**mu), omega**nu], dtype=complex) / np.sqrt(3)
            states.append(v)
            labels.append(f"G1({mu},{nu})")

    # Group 2: (1, 0, -ω^μ, -ω^ν)/√3
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            v = np.array([1, 0, -(omega**mu), -(omega**nu)], dtype=complex) / np.sqrt(3)
            states.append(v)
            labels.append(f"G2({mu},{nu})")

    # Group 3: (1, -ω^μ, 0, ω^ν)/√3
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            v = np.array([1, -(omega**mu), 0, omega**nu], dtype=complex) / np.sqrt(3)
            states.append(v)
            labels.append(f"G3({mu},{nu})")

    # Group 4: (1, ω^μ, ω^ν, 0)/√3
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            v = np.array([1, omega**mu, omega**nu, 0], dtype=complex) / np.sqrt(3)
            states.append(v)
            labels.append(f"G4({mu},{nu})")

    return states, labels


states, labels = build_vlasov_witting_states()
print(f"Number of states: {len(states)}")
print(f"  Standard basis: 4")
print(f"  Superpositions: 36 (4 groups × 9)")

# =====================================================
# VERIFY INNER PRODUCTS
# =====================================================

print("\n" + "=" * 70)
print("INNER PRODUCT VERIFICATION")
print("=" * 70)

n = len(states)
inner_prods = {}
for i in range(n):
    for j in range(i + 1, n):
        ip = round(abs(np.vdot(states[i], states[j])) ** 2, 10)
        if ip not in inner_prods:
            inner_prods[ip] = []
        inner_prods[ip].append((i, j))

print("Distinct |⟨ψ|φ⟩|² values:")
for ip in sorted(inner_prods.keys()):
    count = len(inner_prods[ip])
    print(f"  {ip:.10f}: {count} pairs")

# Verify we have exactly {0, 1/3}
expected_values = {0.0, round(1 / 3, 10)}
actual_values = set(inner_prods.keys())

if actual_values == expected_values or actual_values == {0.0, round(1 / 3, 10)}:
    print("\n✓ CONFIRMED: |⟨ψ|φ⟩|² ∈ {0, 1/3} exactly!")
else:
    print(f"\nActual values: {actual_values}")
    print(f"Expected: {expected_values}")

# =====================================================
# VERIFY ORTHOGONALITY GRAPH = Sp₄(3)
# =====================================================

print("\n" + "=" * 70)
print("ORTHOGONALITY GRAPH VERIFICATION")
print("=" * 70)

# Build adjacency matrix
adj = np.zeros((n, n), dtype=int)
for i in range(n):
    for j in range(i + 1, n):
        ip = abs(np.vdot(states[i], states[j])) ** 2
        if ip < 1e-10:  # Orthogonal
            adj[i, j] = adj[j, i] = 1

edges = adj.sum() // 2
degrees = adj.sum(axis=1)

print(f"Number of edges (orthogonal pairs): {edges}")
print(f"Degrees: min={degrees.min()}, max={degrees.max()}")

if degrees.min() == degrees.max():
    k = degrees[0]
    print(f"Graph is {k}-regular ✓")

    # Check SRG parameters
    lam_vals, mu_vals = [], []
    for i in range(n):
        for j in range(i + 1, n):
            common = sum(adj[i, l] and adj[j, l] for l in range(n))
            if adj[i, j]:
                lam_vals.append(common)
            else:
                mu_vals.append(common)

    if len(set(lam_vals)) == 1 and len(set(mu_vals)) == 1:
        lam = lam_vals[0]
        mu = mu_vals[0]
        print(f"\nSRG parameters: ({n}, {k}, {lam}, {mu})")

        if (n, k, lam, mu) == (40, 12, 2, 4):
            print("✓ PERFECT MATCH: Orthogonality graph = Sp₄(3)!")
        else:
            print(f"Expected: (40, 12, 2, 4)")

# =====================================================
# VERIFY SPECTRUM
# =====================================================

print("\n" + "=" * 70)
print("SPECTRUM VERIFICATION")
print("=" * 70)

eigenvalues = np.linalg.eigvalsh(adj)
eigenvalues = sorted(eigenvalues, reverse=True)

from collections import Counter

rounded_eigs = [round(e, 4) for e in eigenvalues]
spectrum = Counter(rounded_eigs)

print("Eigenvalues with multiplicities:")
for ev in sorted(spectrum.keys(), reverse=True):
    print(f"  {ev:8.4f}^{spectrum[ev]}")

print("\nExpected for Sp₄(3):")
print("  12.0000^1")
print("   2.0000^24")
print("  -4.0000^15")

# =====================================================
# FIND THE 40 ORTHONORMAL BASES (LINES OF GQ(3,3))
# =====================================================

print("\n" + "=" * 70)
print("40 ORTHONORMAL BASES (LINES OF GQ(3,3))")
print("=" * 70)


def find_maximal_cliques(adj, n):
    """Find all 4-cliques (orthonormal bases) in the orthogonality graph"""
    cliques = []
    for i in range(n):
        neighbors_i = [j for j in range(n) if adj[i, j]]
        for j in neighbors_i:
            if j <= i:
                continue
            for k in neighbors_i:
                if k <= j or not adj[j, k]:
                    continue
                for l in neighbors_i:
                    if l <= k or not adj[j, l] or not adj[k, l]:
                        continue
                    cliques.append(tuple(sorted([i, j, k, l])))
    return list(set(cliques))


bases = find_maximal_cliques(adj, n)
print(f"Number of orthonormal bases found: {len(bases)}")

if len(bases) == 40:
    print("✓ Exactly 40 bases - confirms GQ(3,3) structure!")

    # Verify each state is in exactly 4 bases
    state_counts = [0] * n
    for basis in bases:
        for idx in basis:
            state_counts[idx] += 1

    if min(state_counts) == max(state_counts) == 4:
        print("✓ Each state in exactly 4 bases!")

# =====================================================
# DISPLAY SOME BASES
# =====================================================

print("\n" + "=" * 70)
print("SAMPLE BASES")
print("=" * 70)

print("First 5 bases (by state indices):")
for i, basis in enumerate(sorted(bases)[:5]):
    basis_labels = [labels[j] for j in basis]
    print(f"  Basis {i+1}: {basis} = {basis_labels}")

# =====================================================
# VERIFY STATES ARE NORMALIZED
# =====================================================

print("\n" + "=" * 70)
print("NORMALIZATION CHECK")
print("=" * 70)

norms = [np.linalg.norm(s) for s in states]
print(f"Norms: min={min(norms):.10f}, max={max(norms):.10f}")
print(
    "✓ All states normalized to 1"
    if abs(min(norms) - 1) < 1e-10
    else "WARNING: Normalization issue"
)

# =====================================================
# THE STRUCTURE SUMMARY
# =====================================================

print("\n" + "=" * 70)
print("STRUCTURE SUMMARY")
print("=" * 70)

print(
    """
THE WITTING CONFIGURATION:
==========================

40 quantum states in ℂ⁴ with:
- 4 standard basis states: |e₀⟩, |e₁⟩, |e₂⟩, |e₃⟩
- 36 superposition states with cube root phases ω = e^{2πi/3}

Inner products:
- |⟨ψ|φ⟩|² = 0 for orthogonal pairs (240 pairs)
- |⟨ψ|φ⟩|² = 1/3 for non-orthogonal pairs (540 pairs)

Orthogonality graph: Sp₄(3) = SRG(40, 12, 2, 4)

GQ(3,3) structure:
- 40 points (states)
- 40 lines (orthonormal bases)
- Each point on 4 lines
- Each line has 4 points

Automorphism group: W(E₆) with |W(E₆)| = 51840
"""
)

# =====================================================
# NAMING CONVENTION
# =====================================================

print("\n" + "=" * 70)
print("NAMING CONVENTION (FINALIZED)")
print("=" * 70)

print(
    """
PRIMARY NAME: Sp₄(3)
====================

The graph is the symplectic polar graph Sp₄(3) = SRG(40, 12, 2, 4).

QUANTUM REALIZATION: "Witting configuration"
=============================================

The Witting configuration is the unique realization of Sp₄(3) in ℂ⁴
with inner products |⟨ψ|φ⟩|² ∈ {0, 1/3}.

The 40 Witting states form:
- An equiangular tight frame
- The vertices of GQ(3,3) (self-dual generalized quadrangle)
- The quotient of the 240-vertex Witting polytope by 6th roots of unity

NAMING CONVENTIONS:
- Use "Sp₄(3)" for the abstract graph
- Use "Witting graph" or "Witting configuration" for the quantum realization
- Use "GQ(3,3)" when emphasizing incidence geometry

RETIRED: "W33" - the informal name is now replaced by standard notation.
"""
)

print("\n" + "=" * 70)
print("PART CXXXVIII COMPLETE")
print("=" * 70)
