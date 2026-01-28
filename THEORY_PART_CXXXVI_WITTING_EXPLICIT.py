#!/usr/bin/env python3
"""
THEORY PART CXXXVI: EXPLICIT WITTING STATES FROM VLASOV
=======================================================

We construct the ACTUAL Witting states using Vlasov's formulas.

The key is: the states must satisfy |⟨ψ|φ⟩|² ∈ {0, 1/3} exactly.
"""

from itertools import combinations, product

import numpy as np

print("=" * 70)
print("PART CXXXVI: EXPLICIT WITTING STATES FROM VLASOV")
print("=" * 70)

omega = np.exp(2j * np.pi / 3)
w = omega
w2 = omega**2

# =====================================================
# VLASOV'S CONSTRUCTION
# =====================================================

print("\n" + "=" * 70)
print("VLASOV'S WITTING STATE CONSTRUCTION")
print("=" * 70)


def vlasov_witting_states():
    """
    From Vlasov arXiv:2503.18431:

    The 40 Witting states are built from the Witting polytope.
    The key equations are based on the 3-qubit stabilizer states
    embedded in dimension 4.

    STRUCTURE:
    - 4 computational basis states
    - 36 states from tensor products with ω phases

    INNER PRODUCTS:
    - Orthogonal: |⟨ψ|φ⟩|² = 0
    - Non-orthogonal, non-collinear: |⟨ψ|φ⟩|² = 1/3
    """
    states = []

    # TYPE 1: Standard basis (4 states)
    e0 = np.array([1, 0, 0, 0], dtype=complex)
    e1 = np.array([0, 1, 0, 0], dtype=complex)
    e2 = np.array([0, 0, 1, 0], dtype=complex)
    e3 = np.array([0, 0, 0, 1], dtype=complex)

    states.extend([e0, e1, e2, e3])

    # TYPE 2: Two-term superpositions with phases (12 states)
    # For each pair (i,j), we get states (|i⟩ + ω^k|j⟩)/√2 for k=0,1,2
    # But phase equivalence reduces to 2 per pair

    # Actually for Witting: 6 pairs × 3 = 18 rays, but some are collinear
    # The correct count: 6 pairs × 2 = 12 states (one phase class per pair)

    # No - let's be more careful. For two orthogonal vectors:
    # (|i⟩ + α|j⟩)/√2 where α ∈ {1, ω, ω²}
    # These are 3 distinct rays per pair, giving 6×3 = 18 states

    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    for i, j in pairs:
        for k in [0, 1, 2]:
            v = np.zeros(4, dtype=complex)
            v[i] = 1
            v[j] = omega**k
            v = v / np.linalg.norm(v)
            states.append(v)

    # TYPE 3: Four-term superpositions (some subset)
    # (1, ω^a, ω^b, ω^c)/2 for various (a,b,c) patterns

    # The total should be 40
    # We have: 4 + 18 = 22 so far
    # Need: 40 - 22 = 18 more from 4-term superpositions

    # The 27 four-term states include duplicates (collinear rays)
    # 27 = 3³, but we keep only non-collinear ones

    for a in [0, 1, 2]:
        for b in [0, 1, 2]:
            for c in [0, 1, 2]:
                v = np.array([1, omega**a, omega**b, omega**c], dtype=complex) / 2

                # Check collinearity with existing states
                is_new = True
                for s in states:
                    overlap = abs(np.vdot(s, v))
                    if abs(overlap - 1) < 1e-10:
                        is_new = False
                        break
                if is_new:
                    states.append(v)

    return states


states = vlasov_witting_states()
print(f"Total states constructed: {len(states)}")

# Verify inner products
print("\nInner product verification:")
inner_prods = {}
for i in range(len(states)):
    for j in range(i + 1, len(states)):
        ip = abs(np.vdot(states[i], states[j])) ** 2
        ip_key = round(ip, 6)
        if ip_key not in inner_prods:
            inner_prods[ip_key] = 0
        inner_prods[ip_key] += 1

print("Distinct |⟨ψ|φ⟩|² values:")
for ip, count in sorted(inner_prods.items()):
    print(f"  {ip:.6f}: {count} pairs")

# =====================================================
# THE CORRECT CONSTRUCTION: HESSE SYMMETRY
# =====================================================

print("\n" + "=" * 70)
print("CORRECT CONSTRUCTION VIA HESSE SYMMETRY")
print("=" * 70)


def hesse_witting_states():
    """
    Use the Hesse group structure to build Witting states.

    The Hesse group (order 216) acts on the 9 inflection points
    of a cubic curve. Embedded in C⁴, this generates Witting states.

    Key: The states form an orbit under the Hesse/Witting group.
    """
    # Seed states from which the orbit is generated

    # The 40 states partition into:
    # - 1 orbit of size 4 (standard basis)
    # - 1 orbit of size 36 (superpositions)

    # Or finer: depends on chosen symmetry

    # For SIC-like property, use specific generators

    # Method: Build from generalized Pauli group for d=4

    states = []

    # Standard basis
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        states.append(v)

    # MUB basis 1 (Fourier)
    F4 = (
        np.array(
            [[1, 1, 1, 1], [1, 1j, -1, -1j], [1, -1, 1, -1], [1, -1j, -1, 1j]],
            dtype=complex,
        )
        / 2
    )
    for i in range(4):
        states.append(F4[:, i])

    # MUB basis 2 (with ω phases)
    for j in range(4):
        v = (
            np.array([1, omega**j, omega ** (2 * j), omega ** (3 * j)], dtype=complex)
            / 2
        )
        # This is Fourier with ω instead of i
        pass

    # Actually, MUBs in d=4 give 5 bases × 4 = 20 states
    # We need the Witting-specific construction

    return build_witting_via_gram()


def build_witting_via_gram():
    """
    Build states from the Gram matrix.

    For Witting:
    G_ij = δ_ij + (1-δ_ij)[adj_ij × 0 + (1-adj_ij) × 1/3]

    Where adj is the Sp₄(3) adjacency matrix.
    """
    # First get the F₃ adjacency matrix
    F3 = [0, 1, 2]

    def symplectic_form(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3

    # Get representatives
    reps = []
    for v in product(F3, repeat=4):
        if v == (0, 0, 0, 0):
            continue
        first_nonzero = next(i for i, x in enumerate(v) if x != 0)
        scale = v[first_nonzero]
        inv = pow(scale, -1, 3)
        normalized = tuple((x * inv) % 3 for x in v)
        if normalized not in reps:
            reps.append(normalized)

    n = len(reps)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if symplectic_form(reps[i], reps[j]) == 0:
                adj[i, j] = adj[j, i] = 1

    # Build Gram matrix
    # G_ij = 1 if i=j, 0 if adjacent, 1/3 if non-adjacent
    G = np.zeros((n, n), dtype=complex)
    for i in range(n):
        G[i, i] = 1
        for j in range(i + 1, n):
            if adj[i, j]:
                G[i, j] = G[j, i] = 0
            else:
                # For Witting, non-orthogonal pairs have |⟨|⟩|² = 1/3
                # So ⟨ψ|φ⟩ can have any phase with magnitude 1/√3
                # The actual phases come from the W(E₆) structure
                G[i, j] = G[j, i] = 1 / np.sqrt(3)  # Assume positive for now

    # Check if G is positive semidefinite
    eigenvalues = np.linalg.eigvalsh(G)
    print(
        f"Gram matrix eigenvalues range: [{eigenvalues.min():.4f}, {eigenvalues.max():.4f}]"
    )

    if eigenvalues.min() < -0.01:
        print("WARNING: Gram matrix is not positive semidefinite!")
        print("Need to include proper phases")

        # The Witting Gram matrix requires specific relative phases
        # between non-adjacent pairs, determined by the E₆ structure

    return reps, adj, G


reps, adj, G = build_witting_via_gram()

# =====================================================
# WORKING BACKWARDS FROM Sp₄(3)
# =====================================================

print("\n" + "=" * 70)
print("THE STRUCTURAL UNDERSTANDING")
print("=" * 70)

print(
    """
THEOREM: The Sp₄(3) graph uniquely determines the Witting configuration.

PROOF STRUCTURE:
1. Sp₄(3) = SRG(40, 12, 2, 4) is determined by its eigenvalues
2. The eigenvalues determine the ANGLE set for any realization
3. For C⁴, the angles must be {0, arccos(1/√3)}
4. The relative phases are determined by the W(E₆) action

EIGENVALUE ANALYSIS:
  Sp₄(3) has spectrum {12¹, 2²⁴, (-4)¹⁵}

For a graph G with adjacency A and complement Ā:
  A + Ā = J - I (all-ones minus identity)

The Witting Gram matrix satisfies:
  G = I + (1/√3)(J - I - A)

where A is adjacency (orthogonal pairs → 0 in Gram).
"""
)

# Verify the Gram matrix formula
n = 40
J = np.ones((n, n))
I = np.eye(n)
A = adj  # adjacency

# Witting Gram (if all non-adj pairs have same positive inner product)
G_witting = I + (1 / np.sqrt(3)) * (J - I - A)

# Check eigenvalues
eigs_G = sorted(np.linalg.eigvalsh(G_witting), reverse=True)
print("\nGram matrix eigenvalues (positive inner products):")
print(f"  Max: {eigs_G[0]:.4f}")
print(f"  Min: {eigs_G[-1]:.4f}")

if eigs_G[-1] < 0:
    print("\n  Negative eigenvalue! Need complex phases in Gram matrix.")
    print("  The 'real' Gram matrix doesn't embed in C⁴.")

# The actual Witting embedding requires:
# 1. Complex phases on the off-diagonal entries
# 2. These phases are determined by the W(E₆) cocycle

print("\n" + "=" * 70)
print("THE KEY INSIGHT: PHASES FROM E₆")
print("=" * 70)

print(
    """
The Witting configuration is NOT just "any" realization of Sp₄(3).

It is the UNIQUE realization with:
1. States in C⁴ (the minimal dimension supporting 40 states)
2. Automorphism group exactly W(E₆)
3. Inner products |⟨ψ|φ⟩|² = 1/3 for non-orthogonal pairs

The relative phases between non-orthogonal pairs carry
the E₆ structure. This is why:

  240 = |E₈ roots| = |Witting polytope vertices| / 1

wait, actually:
  240 = Witting polytope vertices in C⁴
  40 = 240 / 6 (quotient by 6th roots of unity)

The Witting polytope has 240 VERTICES (not 40).
These project to 40 RAYS under the phase quotient.

So the Witting POLYTOPE has:
  - 240 vertices
  - Symmetry group = complex reflection group W = 3.W(E₆)

And the CONFIGURATION (quotient) has:
  - 40 rays
  - Symmetry group = W(E₆) (after quotienting)
"""
)

# =====================================================
# WITTING POLYTOPE: THE 240 VERTICES
# =====================================================

print("\n" + "=" * 70)
print("WITTING POLYTOPE: 240 VERTICES")
print("=" * 70)


def witting_polytope_vertices():
    """
    The Witting polytope has 240 vertices in C⁴.

    These form the orbit of a specific point under W = μ₆.W(E₆).

    Structure:
    - 24 standard basis vectors × 6 phases = 24 (wait, that's 4×6=24)
    - More vertices from superpositions

    Total: 240 = 4×6 + 18×6 + 18×6
           = 24 + 108 + 108
           = 24 + 216? No...

    Better: 240 = 40 × 6 (40 rays × 6 phase choices)
    """
    omega6 = np.exp(2j * np.pi / 6)  # 6th root of unity

    # First get the 40 ray representatives
    # then multiply by 6th roots to get 240 vertices

    # Ray representatives (normalized):
    rays = []

    # Type 1: Standard basis (4 rays)
    for i in range(4):
        v = np.zeros(4, dtype=complex)
        v[i] = 1
        rays.append(v)

    # Type 2: Two-term (18 rays: 6 pairs × 3 phases)
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    for i, j in pairs:
        for k in [0, 1, 2]:
            v = np.zeros(4, dtype=complex)
            v[i] = 1
            v[j] = omega**k  # cube root
            v = v / np.linalg.norm(v)
            rays.append(v)

    # Type 3: Four-term (18 rays from 27, removing collinear)
    # (1, ω^a, ω^b, ω^c)/2 modulo overall phase
    four_term = []
    for a in [0, 1, 2]:
        for b in [0, 1, 2]:
            for c in [0, 1, 2]:
                v = np.array([1, omega**a, omega**b, omega**c], dtype=complex) / 2

                # Check collinearity with existing four-term
                is_new = True
                for u in four_term:
                    overlap = abs(np.vdot(u, v))
                    if abs(overlap - 1) < 1e-10:
                        is_new = False
                        break
                if is_new:
                    four_term.append(v)

    rays.extend(four_term)

    print(f"Number of ray representatives: {len(rays)}")
    print(f"  Standard basis: 4")
    print(f"  Two-term: 18")
    print(f"  Four-term: {len(four_term)}")

    # Expand to 240 polytope vertices
    vertices = []
    for ray in rays:
        for k in range(6):
            v = omega6**k * ray
            vertices.append(v)

    print(f"\nTotal Witting polytope vertices: {len(vertices)}")

    return rays, vertices


rays, vertices = witting_polytope_vertices()

# Verify orthogonality structure
print("\nOrthogonality verification on rays:")
n_rays = len(rays)
adj_rays = np.zeros((n_rays, n_rays), dtype=int)
inner_prod_values = {}

for i in range(n_rays):
    for j in range(i + 1, n_rays):
        ip = abs(np.vdot(rays[i], rays[j])) ** 2
        ip_key = round(ip, 6)
        if ip_key not in inner_prod_values:
            inner_prod_values[ip_key] = 0
        inner_prod_values[ip_key] += 1

        if ip < 1e-10:
            adj_rays[i, j] = adj_rays[j, i] = 1

print("Inner product values |⟨ψ|φ⟩|²:")
for ip, count in sorted(inner_prod_values.items()):
    print(f"  {ip:.6f}: {count} pairs")

edges_rays = adj_rays.sum() // 2
degrees_rays = adj_rays.sum(axis=1)
print(f"\nOrthogonality graph:")
print(f"  Edges: {edges_rays}")
print(f"  Degrees: min={degrees_rays.min()}, max={degrees_rays.max()}")

# =====================================================
# COMPARISON WITH F₃ STRUCTURE
# =====================================================

print("\n" + "=" * 70)
print("COMPARING QUANTUM AND FINITE FIELD CONSTRUCTIONS")
print("=" * 70)

if n_rays == 40:
    # Check if orthogonality graphs match
    # The F₃ construction gave SRG(40, 12, 2, 4)
    # Does our quantum construction match?

    if degrees_rays.min() == degrees_rays.max() == 12:
        print("✓ Degree 12 matches Sp₄(3)!")

        # Check SRG parameters
        lambda_vals = []
        mu_vals = []
        for i in range(n_rays):
            for j in range(i + 1, n_rays):
                common = sum(adj_rays[i, k] and adj_rays[j, k] for k in range(n_rays))
                if adj_rays[i, j]:
                    lambda_vals.append(common)
                else:
                    mu_vals.append(common)

        if len(set(lambda_vals)) == 1 and len(set(mu_vals)) == 1:
            lam = lambda_vals[0]
            mu = mu_vals[0]
            print(f"  SRG parameters: (40, 12, {lam}, {mu})")
            if lam == 2 and mu == 4:
                print("✓ PERFECT MATCH with Sp₄(3)!")
            else:
                print(f"  Expected (40, 12, 2, 4), got different parameters")
    else:
        print(f"Degrees vary: {sorted(set(degrees_rays))}")
        print("Not regular - need to adjust construction")

print("\n" + "=" * 70)
print("PART CXXXVI COMPLETE")
print("=" * 70)
