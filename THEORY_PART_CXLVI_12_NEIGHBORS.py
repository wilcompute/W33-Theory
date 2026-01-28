#!/usr/bin/env python3
"""
THEORY PART CXLVI: THE 12-NEIGHBOR SUBGRAPH
============================================

We've analyzed the 27 non-neighbors (tripartite 9+9+9 structure).
Now let's examine the 12 NEIGHBORS of any vertex in Sp₄(3).

What graph do they form?
"""

from itertools import combinations

import numpy as np

print("=" * 70)
print("PART CXLVI: THE 12-NEIGHBOR SUBGRAPH")
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


def inner_product_sq(i, j):
    return abs(np.vdot(states[i], states[j])) ** 2


# Build adjacency matrix (orthogonality graph = Sp₄(3))
adj = [[inner_product_sq(i, j) < 1e-10 for j in range(40)] for i in range(40)]

# =====================================================
# ANALYZE THE 12 NEIGHBORS
# =====================================================

print("\n" + "=" * 70)
print("THE INDUCED SUBGRAPH ON 12 NEIGHBORS")
print("=" * 70)

vertex = 0
neighbors = [j for j in range(40) if adj[vertex][j]]
non_neighbors = [j for j in range(40) if j != vertex and not adj[vertex][j]]

print(f"Chosen vertex: {vertex} (state |0⟩)")
print(f"Neighbors ({len(neighbors)}): {neighbors}")

# Build induced subgraph on neighbors
n_n = len(neighbors)
induced_adj = [
    [adj[neighbors[i]][neighbors[j]] for j in range(n_n)] for i in range(n_n)
]

# Basic statistics
edge_count = sum(sum(row) for row in induced_adj) // 2
degrees = [sum(row) for row in induced_adj]

print(f"\nInduced subgraph on 12 neighbors:")
print(f"  Vertices: {n_n}")
print(f"  Edges: {edge_count}")
print(f"  Degree sequence: {sorted(degrees)}")
print(f"  Is regular? {len(set(degrees)) == 1}")

if len(set(degrees)) == 1:
    k = degrees[0]
    print(f"  Regular of degree: {k}")

# =====================================================
# IDENTIFY THE GRAPH
# =====================================================

print("\n" + "=" * 70)
print("GRAPH IDENTIFICATION")
print("=" * 70)


# Check for SRG parameters
def compute_srg_params(adj_matrix, n):
    """Compute λ and μ if graph is SRG"""
    degrees = [sum(row) for row in adj_matrix]
    if len(set(degrees)) != 1:
        return None
    k = degrees[0]

    lambda_counts = []
    mu_counts = []

    for i in range(n):
        for j in range(i + 1, n):
            common = sum(adj_matrix[i][l] and adj_matrix[j][l] for l in range(n))
            if adj_matrix[i][j]:
                lambda_counts.append(common)
            else:
                mu_counts.append(common)

    lam = lambda_counts[0] if lambda_counts and len(set(lambda_counts)) == 1 else None
    mu = mu_counts[0] if mu_counts and len(set(mu_counts)) == 1 else None

    return (n, k, lam, mu) if lam is not None and mu is not None else None


params = compute_srg_params(induced_adj, n_n)
if params:
    print(f"SRG parameters: {params}")
else:
    # Get the actual values
    degrees = [sum(row) for row in induced_adj]
    k = degrees[0] if len(set(degrees)) == 1 else "varies"

    lambda_counts = set()
    mu_counts = set()
    for i in range(n_n):
        for j in range(i + 1, n_n):
            common = sum(induced_adj[i][l] and induced_adj[j][l] for l in range(n_n))
            if induced_adj[i][j]:
                lambda_counts.add(common)
            else:
                mu_counts.add(common)

    print(f"Graph statistics:")
    print(f"  n = {n_n}")
    print(f"  k = {k}")
    print(f"  λ values (adjacent pairs): {sorted(lambda_counts)}")
    print(f"  μ values (non-adjacent pairs): {sorted(mu_counts)}")

# =====================================================
# SPECTRUM ANALYSIS
# =====================================================

print("\n" + "=" * 70)
print("SPECTRUM ANALYSIS")
print("=" * 70)

adj_matrix = np.array(induced_adj, dtype=float)
eigenvalues = np.linalg.eigvalsh(adj_matrix)
eigenvalues = np.round(eigenvalues, 6)

print("Eigenvalues:")
for e in sorted(set(eigenvalues), reverse=True):
    mult = sum(1 for x in eigenvalues if abs(x - e) < 0.001)
    print(f"  {e:8.4f} with multiplicity {mult}")

# =====================================================
# WHICH STATES ARE THE NEIGHBORS?
# =====================================================

print("\n" + "=" * 70)
print("STRUCTURE OF THE 12 NEIGHBORS")
print("=" * 70)

# Group classification
group_0 = [0, 1, 2, 3]  # Basis states
group_1 = list(range(4, 13))  # (0, 1, -ω^μ, ω^ν)/√3
group_2 = list(range(13, 22))  # (1, 0, -ω^μ, -ω^ν)/√3
group_3 = list(range(22, 31))  # (1, -ω^μ, 0, ω^ν)/√3
group_4 = list(range(31, 40))  # (1, ω^μ, ω^ν, 0)/√3

n_in_g0 = len(set(neighbors) & set(group_0))
n_in_g1 = len(set(neighbors) & set(group_1))
n_in_g2 = len(set(neighbors) & set(group_2))
n_in_g3 = len(set(neighbors) & set(group_3))
n_in_g4 = len(set(neighbors) & set(group_4))

print(f"Neighbors of |0⟩ by Vlasov group:")
print(f"  Group 0 (basis states): {n_in_g0}")
print(f"  Group 1 ((0,1,-ω^μ,ω^ν)/√3): {n_in_g1}")
print(f"  Group 2 ((1,0,-ω^μ,-ω^ν)/√3): {n_in_g2}")
print(f"  Group 3 ((1,-ω^μ,0,ω^ν)/√3): {n_in_g3}")
print(f"  Group 4 ((1,ω^μ,ω^ν,0)/√3): {n_in_g4}")

print(f"\nThe 12 neighbors are: {neighbors}")
print(f"  From Group 0: {sorted(set(neighbors) & set(group_0))}")
print(f"  From Group 1: {sorted(set(neighbors) & set(group_1))}")

# =====================================================
# GEOMETRIC INTERPRETATION
# =====================================================

print("\n" + "=" * 70)
print("GEOMETRIC INTERPRETATION")
print("=" * 70)

print("""
ANALYSIS:
=========

The 12 neighbors of |0⟩ = (1,0,0,0) are:
- States {1, 2, 3}: the other 3 basis states
- States 4-12: all 9 states of form (0, 1, -ω^μ, ω^ν)/√3

These are EXACTLY the states with first component = 0!

In quantum terms:
  ⟨0|ψ⟩ = 0 ⟺ ψ orthogonal to |0⟩ ⟺ first component is 0

The 12 neighbors span the 3-dimensional subspace ℂ³ ⊂ ℂ⁴
perpendicular to |0⟩.
""")

# Verify: all neighbors have first component 0
print("Verification - first component of each neighbor:")
for idx in neighbors:
    first_comp = states[idx][0]
    print(f"  State {idx}: first component = {first_comp:.4f}")

# =====================================================
# THE INDUCED GRAPH STRUCTURE
# =====================================================

print("\n" + "=" * 70)
print("INDUCED GRAPH STRUCTURE")
print("=" * 70)

# The 12 neighbors are: {1,2,3} ∪ {4,5,6,7,8,9,10,11,12}
# Let's see the adjacency pattern

# States 1,2,3 (basis states in ℂ³)
basis_neighbors = [1, 2, 3]
superposition_neighbors = list(range(4, 13))

# Check adjacencies within basis states
print("Adjacencies among basis states {1,2,3}:")
for i in basis_neighbors:
    for j in basis_neighbors:
        if i < j:
            orth = adj[i][j]
            print(f"  |{i}⟩ ⊥ |{j}⟩? {orth}")

# Check adjacencies between basis and superposition
print("\nAdjacencies between basis and superpositions:")
for i in basis_neighbors:
    adj_count = sum(adj[i][j] for j in superposition_neighbors)
    print(f"  |{i}⟩ adjacent to {adj_count} superposition states")

# Check adjacencies within superpositions
print("\nAdjacencies within superposition states (Group 1):")
sup_edges = sum(
    1
    for i in superposition_neighbors
    for j in superposition_neighbors
    if i < j and adj[i][j]
)
print(f"  Edges among 9 superposition states: {sup_edges}")

# =====================================================
# IDENTIFY KNOWN GRAPHS
# =====================================================

print("\n" + "=" * 70)
print("GRAPH IDENTIFICATION")
print("=" * 70)

# Count triangles
triangles = 0
for i in range(n_n):
    for j in range(i + 1, n_n):
        if induced_adj[i][j]:
            for k in range(j + 1, n_n):
                if induced_adj[i][k] and induced_adj[j][k]:
                    triangles += 1

print(f"Triangle count: {triangles}")

# Count 4-cycles (if any)
four_cycles = 0
for i in range(n_n):
    for j in range(i + 1, n_n):
        if not induced_adj[i][j]:  # i,j non-adjacent
            common = [k for k in range(n_n) if induced_adj[i][k] and induced_adj[j][k]]
            four_cycles += len(common) * (len(common) - 1) // 2

print(f"4-cycles (through non-adjacent pairs): {four_cycles}")

# Chromatic number estimate
print(f"\nMaximum clique size estimate:")
max_clique = 0
for size in range(n_n, 0, -1):
    found = False
    for clique in combinations(range(n_n), size):
        if all(
            induced_adj[clique[i]][clique[j]]
            for i in range(size)
            for j in range(i + 1, size)
        ):
            max_clique = size
            found = True
            print(f"  Found {size}-clique: {[neighbors[c] for c in clique]}")
            break
    if found:
        break

# Maximum independent set
print(f"\nMaximum independent set:")
max_indep = 0
for size in range(n_n, 0, -1):
    found = False
    for indep in combinations(range(n_n), size):
        if all(
            not induced_adj[indep[i]][indep[j]]
            for i in range(size)
            for j in range(i + 1, size)
        ):
            max_indep = size
            found = True
            print(f"  Found {size}-independent set: {[neighbors[c] for c in indep]}")
            break
    if found:
        break

# =====================================================
# COMPARISON TO KNOWN GRAPHS
# =====================================================

print("\n" + "=" * 70)
print("COMPARISON TO KNOWN GRAPHS ON 12 VERTICES")
print("=" * 70)

print("""
CANDIDATE GRAPHS:
=================

1. PALEY GRAPH P(11): Has 11 vertices, not 12. Ruled out.

2. ICOSAHEDRON GRAPH: 12 vertices, 30 edges, regular degree 5.
   Check: Our graph has {edge_count} edges.

3. CUBOCTAHEDRON GRAPH: 12 vertices, 24 edges, regular degree 4.
   Check: Our graph has {edge_count} edges.

4. COMPLEMENT OF ABOVE: Would have different parameters.

5. LINE GRAPH L(K₄): 6 vertices. Ruled out.

6. PETERSEN GRAPH: 10 vertices. Ruled out.

7. 3×4 GRID GRAPH: 12 vertices, 17 edges. Check our count.

8. K₃,₃,₃,₃ (complete 4-partite): 12 vertices, but different structure.
""".format(edge_count=edge_count))

# Specific checks
if edge_count == 30:
    print("Edge count matches ICOSAHEDRON (30 edges)")
elif edge_count == 24:
    print("Edge count matches CUBOCTAHEDRON (24 edges)")
elif edge_count == 36:
    print("Edge count matches K₃×K₄ or similar (36 edges)")
else:
    print(f"Edge count {edge_count} - checking other possibilities...")

# =====================================================
# THE ACTUAL STRUCTURE
# =====================================================

print("\n" + "=" * 70)
print("THE ACTUAL STRUCTURE")
print("=" * 70)

# Detailed adjacency matrix visualization
print("Adjacency matrix (12×12):")
print("     " + " ".join(f"{neighbors[j]:2d}" for j in range(n_n)))
for i in range(n_n):
    row = "".join("1 " if induced_adj[i][j] else ". " for j in range(n_n))
    print(f"{neighbors[i]:2d}   {row}")

# Partition into blocks
block_0 = [i for i, n in enumerate(neighbors) if n in [1, 2, 3]]
block_1 = [i for i, n in enumerate(neighbors) if n in range(4, 13)]

print(f"\nBlock structure:")
print(f"  Block 0 (basis states 1,2,3): indices {block_0}")
print(f"  Block 1 (superpositions 4-12): indices {block_1}")

# Count inter-block and intra-block edges
intra_0 = sum(1 for i in block_0 for j in block_0 if i < j and induced_adj[i][j])
intra_1 = sum(1 for i in block_1 for j in block_1 if i < j and induced_adj[i][j])
inter = sum(1 for i in block_0 for j in block_1 if induced_adj[i][j])

print(f"  Edges within Block 0: {intra_0}")
print(f"  Edges within Block 1: {intra_1}")
print(f"  Edges between blocks: {inter}")
print(f"  Total: {intra_0 + intra_1 + inter}")

print("\n" + "=" * 70)
print("PART CXLVI COMPLETE")
print("=" * 70)

print(f"""
KEY FINDINGS:
=============

1. The 12 neighbors of vertex 0 form a graph with:
   - {n_n} vertices
   - {edge_count} edges
   - Degree sequence: {sorted(degrees)}

2. The neighbors consist of:
   - 3 basis states: |1⟩, |2⟩, |3⟩
   - 9 superpositions: (0, 1, -ω^μ, ω^ν)/√3

3. All neighbors have first component = 0
   (They span the ℂ³ perpendicular to |0⟩)

4. Block structure:
   - {intra_0} edges within basis block
   - {intra_1} edges within superposition block
   - {inter} edges between blocks
""")
