#!/usr/bin/env python3
"""
THEORY PART CXLV: PERFECT CORRELATIONS AND MEASUREMENT
======================================================

Investigating the correlation structure more carefully.

The maximally entangled state |Σ⟩ = (|00⟩+|11⟩+|22⟩+|33⟩)/2
gives PERFECT correlation when both parties measure in the 
COMPUTATIONAL BASIS, but we need to transform for other bases.
"""

import numpy as np

print("="*70)
print("PART CXLV: PERFECT CORRELATIONS IN WITTING BASES")
print("="*70)

omega = np.exp(2j * np.pi / 3)

# =====================================================
# BUILD WITTING STATES
# =====================================================

def build_witting_states():
    states = []
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        states.append(v)
    
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([0, 1, -omega**mu, omega**nu]) / np.sqrt(3))
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([1, 0, -omega**mu, -omega**nu]) / np.sqrt(3))
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([1, -omega**mu, 0, omega**nu]) / np.sqrt(3))
    for mu in [0, 1, 2]:
        for nu in [0, 1, 2]:
            states.append(np.array([1, omega**mu, omega**nu, 0]) / np.sqrt(3))
    
    return states

states = build_witting_states()

# Find all bases
def find_bases(states):
    n = len(states)
    adj = [[abs(np.vdot(states[i], states[j]))**2 < 1e-10 
            for j in range(n)] for i in range(n)]
    
    bases = []
    for i in range(n):
        neighbors_i = [j for j in range(n) if adj[i][j]]
        for j in neighbors_i:
            if j <= i: continue
            for k in neighbors_i:
                if k <= j or not adj[j][k]: continue
                for l in neighbors_i:
                    if l <= k or not adj[j][l] or not adj[k][l]: continue
                    bases.append(frozenset([i,j,k,l]))
    
    return list(set(bases))

bases = find_bases(states)
print(f"Found {len(bases)} orthonormal bases")

# =====================================================
# THE MAXIMALLY ENTANGLED STATE
# =====================================================

print("\n" + "="*70)
print("THE STANDARD ENTANGLED STATE")
print("="*70)

# The standard maximally entangled state
# |Σ⟩ = (|00⟩ + |11⟩ + |22⟩ + |33⟩)/2
# This is entangled in the COMPUTATIONAL basis

# Find the basis containing states 0,1,2,3
std_basis = frozenset([0, 1, 2, 3])
if std_basis in bases:
    print(f"Standard basis {{0,1,2,3}} is one of the 40 bases: YES")
else:
    print(f"Standard basis {{0,1,2,3}} is one of the 40 bases: NO")
    # Find which basis contains state 0
    for b in bases:
        if 0 in b:
            print(f"  Basis containing state 0: {sorted(b)}")

print("""
IMPORTANT OBSERVATION:
======================

The maximally entangled state |Σ⟩ = (|00⟩+|11⟩+|22⟩+|33⟩)/2
is defined in the COMPUTATIONAL basis {|0⟩,|1⟩,|2⟩,|3⟩}.

States 0,1,2,3 in our Witting construction ARE the computational basis!

So if BOTH parties measure in basis {0,1,2,3}, they get:
- Alice gets outcome i with probability 1/4
- Bob gets outcome i with probability 1/4
- They ALWAYS agree: P(same) = 1/4 + 1/4 + 1/4 + 1/4 = 1

But if Alice uses a DIFFERENT Witting basis, the correlations change.
""")

# =====================================================
# CORRELATION IN STANDARD BASIS
# =====================================================

print("\n" + "="*70)
print("CORRELATION IN STANDARD BASIS")
print("="*70)

# Define the entangled state as a vector in ℂ⁴ ⊗ ℂ⁴
Sigma = np.zeros((16,), dtype=complex)
Sigma[0*4 + 0] = 0.5  # |00⟩
Sigma[1*4 + 1] = 0.5  # |11⟩
Sigma[2*4 + 2] = 0.5  # |22⟩
Sigma[3*4 + 3] = 0.5  # |33⟩

def compute_correlation(basis_A, basis_B):
    """
    Compute P(i,j) when Alice measures in basis_A, Bob in basis_B.
    
    P(i,j) = |⟨ψ^A_i ⊗ ψ^B_j | Σ⟩|²
    """
    states_A = [states[idx] for idx in basis_A]
    states_B = [states[idx] for idx in basis_B]
    
    probs = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            proj = np.kron(states_A[i], states_B[j])
            probs[i, j] = abs(np.vdot(proj, Sigma))**2
    
    return probs

# Standard basis measurement
std_basis_list = [0, 1, 2, 3]
probs = compute_correlation(std_basis_list, std_basis_list)

print("Same-basis measurement in standard basis {0,1,2,3}:")
print("  Probability matrix P(i,j):")
for i in range(4):
    print(f"    [{', '.join(f'{p:.4f}' for p in probs[i])}]")
print(f"  P(same outcome): {np.trace(probs):.6f}")
print(f"  Expected: 1.0 (PERFECT correlation)")

# =====================================================
# GENERAL SAME-BASIS CORRELATION
# =====================================================

print("\n" + "="*70)
print("GENERAL SAME-BASIS CORRELATION")
print("="*70)

print("""
KEY PROPERTY:
=============

For |Σ⟩ = Σ_i |ii⟩/√4, if both measure in the SAME orthonormal basis,
they get perfectly correlated outcomes.

This is because |Σ⟩ is invariant under U ⊗ U* for any unitary U.

But wait - for SAME U on both sides (not U*), we need to think more carefully...
""")

# Check correlations for all 40 bases
same_basis_correlations = []
for b in bases:
    b_list = sorted(b)
    probs = compute_correlation(b_list, b_list)
    same_basis_correlations.append(np.trace(probs))

print(f"Same-basis correlation P(same outcome) for all 40 bases:")
print(f"  Min: {min(same_basis_correlations):.4f}")
print(f"  Max: {max(same_basis_correlations):.4f}")
print(f"  Mean: {np.mean(same_basis_correlations):.4f}")
print(f"  Unique values: {sorted(set(np.round(same_basis_correlations, 4)))}")

# =====================================================
# UNDERSTANDING THE CORRELATION STRUCTURE
# =====================================================

print("\n" + "="*70)
print("CORRELATION STRUCTURE ANALYSIS")
print("="*70)

print("""
OBSERVATION:
============

The correlation is NOT always 1.0 for same-basis measurements!

This is because our entangled state |Σ⟩ = (|00⟩+|11⟩+|22⟩+|33⟩)/2
is a SPECIFIC superposition in the computational basis.

For perfect correlation in a general basis B = {|b_0⟩, |b_1⟩, |b_2⟩, |b_3⟩},
the state should be expressible as Σ_i |b_i⟩|b_i⟩/2.

This requires |Σ⟩ to be symmetric under the basis transformation.
""")

# Analyze which bases give perfect correlation
perfect_corr_bases = [b for b, c in zip(bases, same_basis_correlations) if abs(c - 1.0) < 1e-10]
print(f"\nBases with perfect correlation (P=1.0):")
print(f"  Count: {len(perfect_corr_bases)}")
if perfect_corr_bases:
    for b in perfect_corr_bases[:5]:
        print(f"    {sorted(b)}")

# Analyze 0.5 correlation bases
half_corr_bases = [b for b, c in zip(bases, same_basis_correlations) if abs(c - 0.5) < 0.01]
print(f"\nBases with P(same) ≈ 0.5:")
print(f"  Count: {len(half_corr_bases)}")
if half_corr_bases:
    for b in half_corr_bases[:5]:
        print(f"    {sorted(b)}")

# =====================================================
# THE CORRECT ENTANGLED STATE
# =====================================================

print("\n" + "="*70)
print("CONSTRUCTING THE UNIVERSAL ENTANGLED STATE")
print("="*70)

print("""
For device-independent QKD, we need an entangled state that gives
perfect correlation in EVERY basis.

The solution: Use the unnormalized maximally entangled state
|Φ⟩ = Σᵢ |i⟩|i⟩ (sum over computational basis)

This state has the property:
  (U ⊗ I)|Φ⟩ = (I ⊗ Uᵀ)|Φ⟩

So if Alice applies U and Bob applies Uᵀ, they both transform
their marginals to the same basis → perfect correlation!

For SAME measurement (U = V), we need:
  ⟨Φ|(U† ⊗ V†)|ψ ⊗ φ⟩ where Alice gets |ψ⟩, Bob gets |φ⟩

Let's verify this properly...
""")

# The CORRECT protocol uses:
# - Alice measures in basis B = {|b_i⟩}
# - Bob measures in basis B* = {|b_i⟩*} (complex conjugate)
# This gives perfect correlation!

def compute_correlation_with_conjugate(basis):
    """
    Alice measures in basis, Bob measures in conjugate basis.
    This gives perfect correlation for |Φ⟩ = Σ|ii⟩
    """
    states_A = [states[idx] for idx in basis]
    states_B = [states[idx].conj() for idx in basis]  # Complex conjugate!
    
    # The maximally entangled state
    Phi = np.zeros(16, dtype=complex)
    for i in range(4):
        Phi[i*4 + i] = 1.0
    Phi = Phi / 2  # Normalize
    
    probs = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            proj = np.kron(states_A[i], states_B[j])
            probs[i, j] = abs(np.vdot(proj, Phi))**2
    
    return probs

# Test with a non-standard basis
test_basis = sorted(bases[1])
probs_conj = compute_correlation_with_conjugate(test_basis)

print(f"\nWith CONJUGATE basis for Bob (basis {test_basis}):")
print("  Probability matrix P(i,j):")
for i in range(4):
    print(f"    [{', '.join(f'{p:.4f}' for p in probs_conj[i])}]")
print(f"  P(same outcome): {np.trace(probs_conj):.6f}")

# Verify for all bases
conj_correlations = []
for b in bases:
    b_list = sorted(b)
    probs = compute_correlation_with_conjugate(b_list)
    conj_correlations.append(np.trace(probs))

print(f"\nConjugate-basis correlation for all 40 bases:")
print(f"  Min: {min(conj_correlations):.4f}")
print(f"  Max: {max(conj_correlations):.4f}")
print(f"  All perfect? {all(abs(c - 1.0) < 1e-10 for c in conj_correlations)}")

print("\n" + "="*70)
print("PART CXLV COMPLETE")
print("="*70)

print("""
KEY FINDING:
============

For the maximally entangled state |Φ⟩ = (Σ|ii⟩)/2:

✗ SAME basis measurement does NOT always give perfect correlation
  (Only works for bases where |b_i⟩ = |b_i⟩*)

✓ Alice in basis B, Bob in B* (conjugate) gives PERFECT correlation
  for ALL 40 Witting bases!

PROTOCOL CORRECTION:
====================

In the Witting QKD protocol:
1. Alice and Bob agree on 40 basis PAIRS (B, B*)
2. Alice measures in B, Bob measures in B*
3. Same-index outcomes are perfectly correlated

This uses the property: (U ⊗ Uᵀ)|Φ⟩ = |Φ⟩
where Uᵀ relates B to B*.

The security still follows from:
- Kochen-Specker obstruction (contextuality)
- Bell inequality violation
- Device-independent guarantees
""")
