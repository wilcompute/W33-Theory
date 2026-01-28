#!/usr/bin/env python3
"""
THEORY PART CLI: WHAT DO ADJACENT VERTICES SHARE?
==================================================

Surprising finding: No two vertices share any BASES (triangles).
But adjacent vertices MUST share states! Let's investigate.
"""

from collections import defaultdict
from itertools import combinations

import numpy as np

print("=" * 70)
print("PART CLI: THE SHARING STRUCTURE")
print("=" * 70)

omega = np.exp(2j * np.pi / 3)


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


def get_neighbors(v):
    return set(j for j in range(40) if j != v and is_orthogonal(v, j))


# =====================================================
# ADJACENT VS NON-ADJACENT SHARING
# =====================================================

print("\n" + "=" * 70)
print("WHAT DO VERTICES SHARE?")
print("=" * 70)

# Classify pairs
adjacent_pairs = []
non_adjacent_pairs = []

for i in range(40):
    for j in range(i + 1, 40):
        if is_orthogonal(i, j):
            adjacent_pairs.append((i, j))
        else:
            non_adjacent_pairs.append((i, j))

print(f"Adjacent pairs: {len(adjacent_pairs)}")
print(f"Non-adjacent pairs: {len(non_adjacent_pairs)}")

# =====================================================
# SHARED STATES (NOT BASES)
# =====================================================

print("\n" + "-" * 50)
print("SHARED STATES between vertices")
print("-" * 50)


def count_shared_neighbors(v1, v2):
    """Count states that are neighbors of BOTH v1 and v2"""
    n1 = get_neighbors(v1)
    n2 = get_neighbors(v2)
    return len(n1 & n2)


# Adjacent pairs
adj_shared = defaultdict(list)
for i, j in adjacent_pairs:
    shared = count_shared_neighbors(i, j)
    adj_shared[shared].append((i, j))

print("\nAdjacent vertices - shared neighbor counts:")
for count in sorted(adj_shared.keys()):
    print(f"  {count} shared neighbors: {len(adj_shared[count])} pairs")

# Non-adjacent pairs
nonadj_shared = defaultdict(list)
for i, j in non_adjacent_pairs:
    shared = count_shared_neighbors(i, j)
    nonadj_shared[shared].append((i, j))

print("\nNon-adjacent vertices - shared neighbor counts:")
for count in sorted(nonadj_shared.keys()):
    print(f"  {count} shared neighbors: {len(nonadj_shared[count])} pairs")

# =====================================================
# THE SRG PARAMETER λ = 2
# =====================================================

print("\n" + "=" * 70)
print("THE SRG PARAMETER λ = 2")
print("=" * 70)

print(
    """
From SRG(40, 12, 2, 4):
- λ = 2: Adjacent vertices share exactly 2 common neighbors
- μ = 4: Non-adjacent vertices share exactly 4 common neighbors

These 2 (or 4) shared states are the intersection of the
two ℂ³ subspaces at the adjacent (or non-adjacent) vertices!
"""
)

# Verify
print("Verification:")
print(
    f"  All adjacent pairs share exactly 2 neighbors: {set(adj_shared.keys()) == {2}}"
)
print(
    f"  All non-adjacent pairs share exactly 4 neighbors: {set(nonadj_shared.keys()) == {4}}"
)

# =====================================================
# GEOMETRIC INTERPRETATION
# =====================================================

print("\n" + "=" * 70)
print("GEOMETRIC INTERPRETATION")
print("=" * 70)

print(
    """
When two vertices v₁ ⊥ v₂ (adjacent in Sp₄(3)):
- v₁ spans a ℂ¹ subspace
- Neighbors of v₁ span v₁^⊥ ≅ ℂ³
- Similarly, neighbors of v₂ span v₂^⊥ ≅ ℂ³
- The intersection (v₁^⊥ ∩ v₂^⊥) = {v₁, v₂}^⊥ ≅ ℂ²!
- This ℂ² contains exactly 2 orthogonal states in our configuration

When two vertices v₁ ⟂̸ v₂ (non-adjacent):
- The intersection v₁^⊥ ∩ v₂^⊥ is larger
- Contains exactly 4 states (μ = 4)
"""
)

# =====================================================
# DETAILED LOOK AT SHARED STATES
# =====================================================

print("\n" + "=" * 70)
print("DETAILED: ADJACENT PAIR (0, 1)")
print("=" * 70)

n0 = get_neighbors(0)
n1 = get_neighbors(1)
shared_01 = n0 & n1

print(f"Neighbors of 0: {sorted(n0)}")
print(f"Neighbors of 1: {sorted(n1)}")
print(f"Shared: {sorted(shared_01)}")

# Are the 2 shared states orthogonal?
shared_list = list(shared_01)
if len(shared_list) == 2:
    ip = abs(np.vdot(states[shared_list[0]], states[shared_list[1]])) ** 2
    print(f"\nInner product |⟨{shared_list[0]}|{shared_list[1]}⟩|² = {ip:.6f}")
    print(f"The 2 shared states are orthogonal: {ip < 0.001}")

print("\n" + "-" * 50)
print("DETAILED: NON-ADJACENT PAIR (0, 4)")
print("-" * 50)

n4 = get_neighbors(4)
shared_04 = n0 & n4

print(f"Neighbors of 0: {sorted(n0)}")
print(f"Neighbors of 4: {sorted(n4)}")
print(f"Shared: {sorted(shared_04)}")

# Check inner products among the 4 shared states
print("\nInner products among the 4 shared states:")
shared_list = sorted(shared_04)
for i, s1 in enumerate(shared_list):
    for j, s2 in enumerate(shared_list):
        if j > i:
            ip = abs(np.vdot(states[s1], states[s2])) ** 2
            orth = "⊥" if ip < 0.001 else ""
            print(f"  |⟨{s1}|{s2}⟩|² = {ip:.4f} {orth}")

# =====================================================
# STRUCTURE AMONG 4 SHARED STATES
# =====================================================

print("\n" + "=" * 70)
print("WHAT STRUCTURE DO 4 SHARED STATES FORM?")
print("=" * 70)


# For non-adjacent pairs, check the graph structure of 4 shared states
def check_shared_structure(v1, v2):
    shared = sorted(get_neighbors(v1) & get_neighbors(v2))
    if len(shared) != 4:
        return None

    # Count edges among 4 states
    edges = []
    for i, s1 in enumerate(shared):
        for j, s2 in enumerate(shared):
            if j > i and is_orthogonal(s1, s2):
                edges.append((s1, s2))

    return shared, edges


# Analyze a few non-adjacent pairs
sample_pairs = [(0, 4), (0, 13), (1, 5), (2, 6)]
print("Sample non-adjacent pairs:")
for v1, v2 in sample_pairs:
    if not is_orthogonal(v1, v2):
        shared, edges = check_shared_structure(v1, v2)
        print(f"\n  Pair ({v1}, {v2}):")
        print(f"    Shared states: {shared}")
        print(f"    Edges among them: {edges}")
        print(f"    Edge count: {len(edges)}")

# Count how many edges on average
edge_counts = defaultdict(int)
for v1, v2 in non_adjacent_pairs:
    _, edges = check_shared_structure(v1, v2)
    edge_counts[len(edges)] += 1

print("\nEdge count distribution among 4 shared states:")
for count in sorted(edge_counts.keys()):
    print(f"  {count} edges: {edge_counts[count]} pairs")

print(
    """
INTERPRETATION:
- 2 edges among 4 states = P₄ (path) or 2K₂ (matching)
- 4 edges = C₄ (cycle) or K₄-e (almost complete)
- 0 edges = independent set (no orthogonalities)
"""
)

# =====================================================
# WHICH GRAPHS APPEAR?
# =====================================================

print("\n" + "=" * 70)
print("IDENTIFYING THE INDUCED SUBGRAPH")
print("=" * 70)


def describe_graph_on_4(shared):
    """Describe the orthogonality graph on 4 states"""
    adj = [[is_orthogonal(shared[i], shared[j]) for j in range(4)] for i in range(4)]
    edges = sum(sum(row) for row in adj) // 2

    # Compute degree sequence
    degrees = sorted([sum(adj[i]) for i in range(4)], reverse=True)

    if edges == 0:
        return "Empty (4 isolated)", degrees
    elif edges == 1:
        return "K₂ + 2K₁", degrees
    elif edges == 2:
        if degrees == [1, 1, 1, 1]:
            return "2K₂ (matching)", degrees
        else:
            return "P₃ + K₁", degrees
    elif edges == 3:
        if degrees == [2, 2, 1, 1]:
            return "P₄ (path)", degrees
        else:
            return "K₃ + K₁", degrees
    elif edges == 4:
        if degrees == [2, 2, 2, 2]:
            return "C₄ (cycle)", degrees
        elif degrees == [3, 1, 1, 1]:
            return "K₁,₃ (star)", degrees
        else:
            return "K₄ - e", degrees
    elif edges == 5:
        return "K₄ - e", degrees
    elif edges == 6:
        return "K₄ (complete)", degrees
    else:
        return f"Unknown ({edges} edges)", degrees


graph_types = defaultdict(list)
for v1, v2 in non_adjacent_pairs:
    shared = sorted(get_neighbors(v1) & get_neighbors(v2))
    gtype, degrees = describe_graph_on_4(shared)
    graph_types[gtype].append((v1, v2))

print("Graph types appearing among 4 shared states:")
for gtype in sorted(graph_types.keys()):
    print(f"  {gtype}: {len(graph_types[gtype])} pairs")

# =====================================================
# THE 2 SHARED STATES FOR ADJACENT PAIRS
# =====================================================

print("\n" + "=" * 70)
print("THE 2 SHARED STATES FOR ADJACENT PAIRS")
print("=" * 70)

# Are they always orthogonal or never orthogonal?
orthogonal_count = 0
for v1, v2 in adjacent_pairs:
    shared = sorted(get_neighbors(v1) & get_neighbors(v2))
    if len(shared) == 2:
        if is_orthogonal(shared[0], shared[1]):
            orthogonal_count += 1

print(
    f"Adjacent pairs where 2 shared states are orthogonal: {orthogonal_count}/{len(adjacent_pairs)}"
)

print("\n" + "=" * 70)
print("PART CLI COMPLETE")
print("=" * 70)

print(
    """
SUMMARY OF SHARING STRUCTURE:
=============================

1. NO BASES ARE SHARED
   - All 40 MUB systems are distinct
   - 780 pairs share 0 bases (triangles)

2. STATES ARE SHARED (SRG PARAMETERS)
   - Adjacent vertices share exactly 2 neighbors (λ = 2)
   - Non-adjacent vertices share exactly 4 neighbors (μ = 4)

3. GEOMETRIC MEANING
   - 2 shared neighbors = ℂ² intersection of perpendicular spaces
   - 4 shared neighbors = larger intersection when not orthogonal

4. SUBGRAPH STRUCTURE
   - The 4 shared states for non-adjacent pairs form specific graphs
   - This constrains the global structure of Witting

IMPLICATION: While bases aren't shared, the FABRIC of
individual states is intricately woven between the 40 MUB systems.
"""
)
