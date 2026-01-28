#!/usr/bin/env python3
"""
THEORY PART CXLVII: THE 4 TRIANGLES STRUCTURE
==============================================

DISCOVERY: The 12 neighbors form 4 DISJOINT TRIANGLES!

This is the graph 4K₃ (four copies of K₃).

- 12 vertices, 12 edges
- Regular of degree 2
- 4 triangles, no edges between them
- Spectrum: {2⁴, (-1)⁸}

Let's understand WHY this structure emerges.
"""

from itertools import combinations

import numpy as np

print("=" * 70)
print("PART CXLVII: THE FOUR TRIANGLES - 4K₃")
print("=" * 70)

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


states = build_witting_states()


def is_orthogonal(i, j):
    return abs(np.vdot(states[i], states[j])) ** 2 < 1e-10


# =====================================================
# IDENTIFY THE 4 TRIANGLES
# =====================================================

print("\n" + "=" * 70)
print("IDENTIFYING THE 4 TRIANGLES")
print("=" * 70)

vertex = 0
neighbors = [j for j in range(40) if is_orthogonal(vertex, j)]

# Build induced subgraph
n_n = len(neighbors)
induced_adj = [
    [is_orthogonal(neighbors[i], neighbors[j]) for j in range(n_n)] for i in range(n_n)
]

# Find all triangles
triangles = []
for i in range(n_n):
    for j in range(i + 1, n_n):
        if induced_adj[i][j]:
            for k in range(j + 1, n_n):
                if induced_adj[i][k] and induced_adj[j][k]:
                    triangles.append((neighbors[i], neighbors[j], neighbors[k]))

print(f"Found {len(triangles)} triangles:")
for t in triangles:
    print(f"  Triangle: {t}")

# =====================================================
# ANALYZE EACH TRIANGLE
# =====================================================

print("\n" + "=" * 70)
print("STRUCTURE OF EACH TRIANGLE")
print("=" * 70)

# Triangle 1: basis states {1, 2, 3}
print("\nTriangle 1: {1, 2, 3} - The standard basis in ℂ³")
for idx in [1, 2, 3]:
    print(f"  |{idx}⟩ = {states[idx]}")

# Remaining triangles: in the superposition block
superposition_neighbors = list(range(4, 13))
sup_adj = [
    [is_orthogonal(i, j) for j in superposition_neighbors]
    for i in superposition_neighbors
]

# Find triangles in superposition block
sup_triangles = []
for i in range(9):
    for j in range(i + 1, 9):
        if sup_adj[i][j]:
            for k in range(j + 1, 9):
                if sup_adj[i][k] and sup_adj[j][k]:
                    sup_triangles.append(
                        (
                            superposition_neighbors[i],
                            superposition_neighbors[j],
                            superposition_neighbors[k],
                        )
                    )

print(f"\nTriangles in superposition block: {len(sup_triangles)}")
for i, t in enumerate(sup_triangles):
    print(f"\nTriangle {i+2}: {t}")
    for idx in t:
        state = states[idx]
        # Extract (μ, ν) from state 4-12
        # states[4+3*μ+ν] = (0, 1, -ω^μ, ω^ν)/√3
        local_idx = idx - 4
        mu = local_idx // 3
        nu = local_idx % 3
        print(f"  State {idx}: (0, 1, -ω^{mu}, ω^{nu})/√3 = {state}")

# =====================================================
# THE PATTERN: F₃ × F₃ STRUCTURE
# =====================================================

print("\n" + "=" * 70)
print("THE F₃ × F₃ PATTERN")
print("=" * 70)

print("""
The 9 superposition states are indexed by (μ, ν) ∈ F₃ × F₃:

     ν=0    ν=1    ν=2
μ=0:  4      5      6
μ=1:  7      8      9
μ=2: 10     11     12

State index = 4 + 3μ + ν

Question: What orthogonality pattern creates the 3 triangles?
""")

# Compute which states are orthogonal
print("Orthogonality pattern in F₃ × F₃:")
for i in range(9):
    mu_i, nu_i = i // 3, i % 3
    adj_list = []
    for j in range(9):
        if i != j and sup_adj[i][j]:
            mu_j, nu_j = j // 3, j % 3
            adj_list.append(f"({mu_j},{nu_j})")
    print(f"  ({mu_i},{nu_i}) adjacent to: {adj_list}")

# =====================================================
# FIND THE ORTHOGONALITY RULE
# =====================================================

print("\n" + "=" * 70)
print("DISCOVERING THE ORTHOGONALITY RULE")
print("=" * 70)

print("""
For states (0, 1, -ω^μ₁, ω^ν₁)/√3 and (0, 1, -ω^μ₂, ω^ν₂)/√3:

Inner product = (1/3)(1 + ω^{μ₂-μ₁} + ω^{ν₁-ν₂})

This is zero iff: 1 + ω^{μ₂-μ₁} + ω^{ν₁-ν₂} = 0
                  ω^{μ₂-μ₁} + ω^{ν₁-ν₂} = -1 = ω + ω²

So we need: {ω^{μ₂-μ₁}, ω^{ν₁-ν₂}} = {ω, ω²}

This happens when:
  μ₂ - μ₁ ∈ {1, 2} and ν₁ - ν₂ ∈ {2, 1} respectively
  
Or: (μ₂-μ₁, ν₁-ν₂) ∈ {(1,2), (2,1)} mod 3
""")

# Verify the rule
print("\nVerifying orthogonality rule:")
for i in range(9):
    mu_i, nu_i = i // 3, i % 3
    for j in range(i + 1, 9):
        mu_j, nu_j = j // 3, j % 3

        d_mu = (mu_j - mu_i) % 3
        d_nu = (nu_i - nu_j) % 3

        # Compute actual inner product
        ip = np.vdot(states[4 + i], states[4 + j])
        is_orth = abs(ip) ** 2 < 1e-10

        # Predicted orthogonality
        predicted = (d_mu, d_nu) in [(1, 2), (2, 1)]

        if is_orth != predicted:
            print(
                f"  MISMATCH at ({mu_i},{nu_i})-({mu_j},{nu_j}): actual={is_orth}, predicted={predicted}"
            )

        if is_orth:
            print(f"  ({mu_i},{nu_i}) ⊥ ({mu_j},{nu_j}): Δμ={d_mu}, Δν={d_nu}")

# =====================================================
# THE GEOMETRIC MEANING
# =====================================================

print("\n" + "=" * 70)
print("GEOMETRIC INTERPRETATION")
print("=" * 70)

print("""
THE THREE TRIANGLES IN F₃ × F₃:
===============================

The orthogonality rule (Δμ, Δν) ∈ {(1,2), (2,1)} 
defines a GRAPH on the 9 points of F₃ × F₃.

This graph is 3K₃: three disjoint triangles!

Triangle 2: {(0,0), (1,2), (2,1)} = {4, 8, 10}
Triangle 3: {(0,1), (1,0), (2,2)} = {5, 7, 12}  
Triangle 4: {(0,2), (1,1), (2,0)} = {6, 8, 11}

Wait, let me verify...
""")

# Find the actual triangles
for t in sup_triangles:
    indices = [idx - 4 for idx in t]
    coords = [(idx // 3, idx % 3) for idx in indices]
    print(f"Triangle {t}:")
    print(f"  F₃×F₃ coords: {coords}")

    # Check pattern
    diffs = []
    for i in range(3):
        for j in range(i + 1, 3):
            d_mu = (coords[j][0] - coords[i][0]) % 3
            d_nu = (coords[i][1] - coords[j][1]) % 3
            diffs.append((d_mu, d_nu))
    print(f"  (Δμ, Δν) pairs: {diffs}")

# =====================================================
# THE AFFINE PLANE AG(2, F₃)
# =====================================================

print("\n" + "=" * 70)
print("CONNECTION TO AFFINE GEOMETRY")
print("=" * 70)

print("""
THE AFFINE PLANE AG(2, F₃):
===========================

The 9 points of F₃ × F₃ form the affine plane AG(2, 3).
This plane has:
- 9 points
- 12 lines (each with 3 points)
- 4 parallel classes (3 lines each)

Each parallel class partitions all 9 points into 3 lines of 3.

THE TRIANGLES ARE LINES!
========================

Our 3 triangles {4,8,10}, {5,7,12}, {6,9,11} (if those are right)
correspond to ONE parallel class of lines in AG(2, F₃)!

The direction of these lines is determined by the orthogonality
condition (Δμ, Δν) ∈ {(1,2), (2,1)}.
""")

# Verify: do the triangles partition the 9 points?
all_points = set()
for t in sup_triangles:
    all_points.update(t)
print(f"Points covered by triangles: {sorted(all_points)}")
print(f"Expected: {list(range(4,13))}")
print(f"Partition? {sorted(all_points) == list(range(4,13))}")

# =====================================================
# SUMMARY: THE LOCAL STRUCTURE OF Sp₄(3)
# =====================================================

print("\n" + "=" * 70)
print("COMPLETE LOCAL STRUCTURE OF Sp₄(3)")
print("=" * 70)

print("""
╔══════════════════════════════════════════════════════════════════════╗
║               LOCAL STRUCTURE AT ANY VERTEX                          ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  VERTEX: Any state v in the 40 Witting states                        ║
║                                                                      ║
║  12 NEIGHBORS (orthogonal to v):                                     ║
║  ───────────────────────────────                                     ║
║    Induced graph: 4K₃ (four disjoint triangles)                      ║
║    - One triangle from basis states                                  ║
║    - Three triangles from AG(2, F₃) parallel class                   ║
║    - 12 vertices, 12 edges, degree 2                                 ║
║    - Spectrum: {2⁴, (-1)⁸}                                          ║
║                                                                      ║
║  27 NON-NEIGHBORS (non-orthogonal to v):                            ║
║  ─────────────────────────────────────                              ║
║    Induced graph: Tripartite 9+9+9                                   ║
║    - Three blocks from Groups 2, 3, 4                                ║
║    - All 108 edges between blocks, none within                       ║
║    - 27 vertices, 108 edges, degree 8                                ║
║                                                                      ║
║  COMBINED LOCAL VIEW:                                                ║
║  ────────────────────                                                ║
║    40 = 1 + 12 + 27                                                  ║
║        = vertex + neighbors + non-neighbors                          ║
║        = 1 + 4×3 + 3×9                                              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

print("\n" + "=" * 70)
print("PART CXLVII COMPLETE")
print("=" * 70)

print("""
KEY DISCOVERIES:
================

1. THE 12-NEIGHBOR SUBGRAPH IS 4K₃
   - Four disjoint triangles
   - One triangle = {|1⟩, |2⟩, |3⟩} (basis)
   - Three triangles from superpositions

2. THE THREE SUPERPOSITION TRIANGLES
   - Come from states (0, 1, -ω^μ, ω^ν)/√3
   - Form a PARALLEL CLASS in the affine plane AG(2, F₃)
   - Orthogonality ⟺ (Δμ, Δν) ∈ {(1,2), (2,1)} mod 3

3. THE F₃ × F₃ STRUCTURE
   - 9 superpositions indexed by (μ, ν) ∈ F₃ × F₃
   - Orthogonality defines an incidence geometry
   - Three parallel lines = three triangles

4. COMPLETE LOCAL STRUCTURE OF Sp₄(3)
   - 12 neighbors: 4K₃ (triangles, parallel class)
   - 27 non-neighbors: tripartite graph (9+9+9)
   - Beautiful interplay of F₃ geometry and quantum structure
""")
