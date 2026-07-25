#!/usr/bin/env python3
"""
BIJECTION SOLVER — Can we construct 240 edges ↔ 240 E8 roots?
===============================================================

We have PROVEN:
  - E8 Dynkin diagram exists as induced subgraph of W(3,3) [PATTERN_SOLVER]
  - Gram matrix (2I - adj[sub]) = E8 Cartan matrix, det = 1 [PATTERN_SOLVER]
  - 8 vertices [7, 1, 0, 13, 24, 28, 37, 16] in W(3,3) form E8

NEW APPROACH TO BIJECTION:
  1. The 8 simple roots of E8 sit at 8 W(3,3) vertices
  2. Generate ALL 240 E8 roots via Weyl reflections of simple roots
  3. Each root is a Z-linear combination of simple roots (Dynkin coordinates)
  4. Map back to W(3,3) via the vertex assignment
  5. Check if the resulting 240 objects match the 240 edges

The key insight: roots in Dynkin coordinates have specific structure:
  - Positive roots: non-negative integer coordinates
  - 120 positive + 120 negative = 240 total
  - The highest root θ = [2,3,4,5,6,4,2,3] (in Dynkin coordinates for E8)
  - All positive roots' Dynkin coordinates are known explicitly

But the matching cannot be literal (roots are vectors, edges are pairs).
The question is: what FUNCTION maps an edge (i,j) to an E8 root vector?

HYPOTHESIS: The function uses the characteristic vectors.
For edge (i,j), define χ_{ij} = e_i + e_j ∈ Z^40.
Project χ_{ij} onto the 8-dimensional E8 sublattice spanned by the 
8 simple root vertices. If this projection gives the E8 roots, we win.
"""

from collections import Counter
from itertools import product
import numpy as np


def build_w33():
    """Build W(3,3) = GQ(3,3) = SRG(40,12,2,4)."""
    F3 = [0, 1, 2]
    raw = [v for v in product(F3, repeat=4) if any(x != 0 for x in v)]
    
    points = []
    seen = set()
    for v in raw:
        v = list(v)
        for i in range(4):
            if v[i] != 0:
                inv = 2 if v[i] == 2 else 1
                v = tuple((x * inv) % 3 for x in v)
                break
        if v not in seen:
            seen.add(v)
            points.append(v)
    
    assert len(points) == 40
    
    def omega(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3
    
    n = 40
    adj = np.zeros((n, n), dtype=int)
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            if omega(points[i], points[j]) == 0:
                adj[i,j] = adj[j,i] = 1
                edges.append((i, j))
    
    return adj, points, edges


# ===========================================================================
# E8 ROOT SYSTEM CONSTRUCTION
# ===========================================================================

def e8_simple_roots():
    """
    E8 simple roots in the standard basis of R^8.
    Convention matching the Cartan matrix:
    
    C_{ij} = 2(α_i · α_j)/(α_j · α_j)
    
    For simply-laced E8: C_{ij} = 2(α_i · α_j)/2 = α_i · α_j
    (since all roots have norm² = 2).
    """
    # Standard E8 simple roots (Bourbaki ordering):
    # α₁ = ( 1,-1, 0, 0, 0, 0, 0, 0)
    # α₂ = ( 0, 1,-1, 0, 0, 0, 0, 0)
    # α₃ = ( 0, 0, 1,-1, 0, 0, 0, 0)
    # α₄ = ( 0, 0, 0, 1,-1, 0, 0, 0)
    # α₅ = ( 0, 0, 0, 0, 1,-1, 0, 0)
    # α₆ = ( 0, 0, 0, 0, 0, 1,-1, 0)
    # α₇ = ( 0, 0, 0, 0, 0, 1, 1, 0)
    # α₈ = (-1/2,-1/2,-1/2,-1/2,-1/2,-1/2,-1/2, 1/2)
    #
    # Wait, this gives the conventional Cartan matrix. Let me use the ordering
    # that matches our found Dynkin diagram:
    #
    # Our vertices: a1=7, a2=1, BRANCH=0, c1=13, c2=24, c3=28, c4=37, d=16
    # Order in Gram matrix: [a1, a2, b, c1, c2, c3, c4, d]
    # 
    # Dynkin edges: a1-a2, a2-b, b-c1, c1-c2, c2-c3, c3-c4, b-d
    # Branch at b (index 2 in our 8-vertex list)
    
    # Use standard E8 with branch at α₃:
    # Path: α₁-α₂-α₃-α₄-α₅-α₆-α₇ with α₈ branching from α₃
    # This matches our layout: a1-a2-b-c1-c2-c3-c4 with d from b
    
    alpha = np.zeros((8, 8))
    alpha[0] = [1, -1, 0, 0, 0, 0, 0, 0]
    alpha[1] = [0, 1, -1, 0, 0, 0, 0, 0]
    alpha[2] = [0, 0, 1, -1, 0, 0, 0, 0]
    alpha[3] = [0, 0, 0, 1, -1, 0, 0, 0]
    alpha[4] = [0, 0, 0, 0, 1, -1, 0, 0]
    alpha[5] = [0, 0, 0, 0, 0, 1, -1, 0]
    alpha[6] = [0, 0, 0, 0, 0, 1, 1, 0]
    alpha[7] = [-0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, 0.5]
    
    # Verify Cartan matrix
    C = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            C[i, j] = 2 * np.dot(alpha[i], alpha[j]) / np.dot(alpha[j], alpha[j])
    
    return alpha, C


def generate_all_roots(simple_roots):
    """Generate all 240 E8 roots via Weyl reflections of simple roots."""
    roots = set()
    
    def to_tuple(v):
        return tuple(round(x * 2) / 2 for x in v)
    
    def reflect(v, alpha):
        """Reflect v in the hyperplane perpendicular to alpha."""
        return v - 2 * np.dot(v, alpha) / np.dot(alpha, alpha) * alpha
    
    # Start with simple roots and their negatives
    frontier = []
    for i in range(8):
        r = to_tuple(simple_roots[i])
        if r not in roots:
            roots.add(r)
            frontier.append(simple_roots[i].copy())
        r_neg = to_tuple(-simple_roots[i])
        if r_neg not in roots:
            roots.add(r_neg)
            frontier.append(-simple_roots[i].copy())
    
    # Iterate: apply all reflections to all known roots
    while frontier:
        new_frontier = []
        for root in frontier:
            for i in range(8):
                reflected = reflect(root, simple_roots[i])
                r_tuple = to_tuple(reflected)
                if r_tuple not in roots:
                    roots.add(r_tuple)
                    new_frontier.append(reflected)
        frontier = new_frontier
    
    return [np.array(r) for r in roots]


def roots_in_dynkin_basis(roots, simple_roots):
    """
    Express each root in the basis of simple roots (Dynkin coordinates).
    
    If r = Σ cᵢ αᵢ, then the Dynkin coordinates are (c₁, ..., c₈).
    For a root r: cᵢ = 2(r · αᵢ)/|αᵢ|² using Cartan matrix.
    Actually: r = C⁻¹ · (2 r·α₁/|α₁|², ..., 2 r·α₈/|α₈|²)
    """
    # Build the matrix of simple roots (rows)
    S = np.array([simple_roots[i] for i in range(8)])
    # Roots matrix
    R = np.array(roots)
    
    # For each root r, solve S^T c = r for c (Dynkin coordinates)
    # Or equivalently: c = (S^T)^{-1} r = (S^{-1})^T r
    S_inv = np.linalg.inv(S)
    
    dynkin_coords = []
    for root in roots:
        c = S_inv @ root
        dynkin_coords.append(tuple(round(x) for x in c))
    
    return dynkin_coords


# ===========================================================================
# INVESTIGATION: THE EDGE → ROOT MAPPING
# ===========================================================================

def investigate_bijection(adj, edges, e8_verts):
    """
    Try to construct a bijection between 240 edges and 240 E8 roots.
    
    Approach 1: Projection method
    - The 8 E8 vertices span an 8D sublattice of R^40
    - Project each edge characteristic vector onto this sublattice
    
    Approach 2: Distance method
    - Map each edge (i,j) based on graph distances from the 8 E8 vertices
    
    Approach 3: Combinatorial encoding
    - Each edge determines a binary "profile" relative to the 8 E8 vertices
    """
    n = 40
    
    # E8 vertex indices in W(3,3): a1=7, a2=1, b=0, c1=13, c2=24, c3=28, c4=37, d=16
    # (From our Dynkin subgraph search)
    
    # Approach 2: Distance profiles
    # For each vertex v, compute graph distance from each of the 8 E8 vertices
    # Then for each edge (i,j), combine the profiles somehow
    
    # First: compute all-pairs shortest distances
    from collections import deque
    
    dist = np.full((n, n), -1, dtype=int)
    for start in range(n):
        dist[start, start] = 0
        q = deque([start])
        while q:
            u = q.popleft()
            for v in range(n):
                if adj[u, v] == 1 and dist[start, v] == -1:
                    dist[start, v] = dist[start, u] + 1
                    q.append(v)
    
    # SRG(40,12,2,4) has diameter 2 (every pair at distance 1 or 2)
    max_dist = dist.max()
    
    # Profile of each vertex relative to E8 vertices
    # profile(v) = (d(v, e8[0]), d(v, e8[1]), ..., d(v, e8[7]))
    profiles = {}
    for v in range(n):
        prof = tuple(dist[v, e8_verts[i]] for i in range(8))
        profiles[v] = prof
    
    # Profile of each edge (i,j): combine the two endpoint profiles
    # Option A: (profile(i), profile(j)) sorted
    # Option B: profile(i) + profile(j) (elementwise)
    # Option C: |profile(i) - profile(j)| (elementwise)
    
    edge_profile_sum = {}
    edge_profile_diff = {}
    edge_profile_pair = {}
    
    for idx, (i, j) in enumerate(edges):
        pi = np.array(profiles[i])
        pj = np.array(profiles[j])
        
        s = tuple((pi + pj).tolist())
        d = tuple(sorted([tuple(pi.tolist()), tuple(pj.tolist())]))
        
        edge_profile_sum[idx] = s
        edge_profile_pair[idx] = d
    
    # How many distinct sum-profiles?
    sum_profile_dist = Counter(edge_profile_sum.values())
    pair_profile_dist = Counter(edge_profile_pair.values())
    
    # Approach 3: Adjacency to E8 vertices
    # For each vertex v, compute which of the 8 E8 vertices it's adjacent to
    # adj_prof(v) = (adj[v, e8[0]], ..., adj[v, e8[7]]) ∈ {0,1}^8
    
    adj_profiles = {}
    for v in range(n):
        prof = tuple(adj[v, e8_verts[i]] for i in range(8))
        adj_profiles[v] = prof
    
    adj_profile_dist = Counter(adj_profiles.values())
    
    # Edge adjacency profile: for each edge (i,j), combine the adj profiles
    edge_adj_sum = {}
    for idx, (i, j) in enumerate(edges):
        s = tuple(a + b for a, b in zip(adj_profiles[i], adj_profiles[j]))
        edge_adj_sum[idx] = s
    
    edge_adj_dist = Counter(edge_adj_sum.values())
    
    # Key question: are there 240 distinct edge profiles?
    
    return {
        'diameter': int(max_dist),
        'num_distinct_sum_profiles': len(sum_profile_dist),
        'num_distinct_pair_profiles': len(pair_profile_dist),
        'num_distinct_adj_profiles': len(adj_profile_dist),
        'num_distinct_edge_adj_profiles': len(edge_adj_dist),
        'adj_profile_distribution': dict(adj_profile_dist),
        'edge_adj_distribution': dict(edge_adj_dist),
        'sum_profiles_sample': dict(list(sum_profile_dist.items())[:10]),
    }


# ===========================================================================
# E8 ROOT STRUCTURE ANALYSIS
# ===========================================================================

def analyze_e8_structure(roots, simple_roots):
    """
    Analyze the E8 root system internal structure.
    
    In particular: how do E8 roots decompose under E6 × A2?
    This decomposition should match the W(3,3) local structure:
    - 27 non-neighbors ↔ 27 of E6
    - 3 from GF(3) ↔ 3 of A2
    """
    n_roots = len(roots)
    
    # Inner product matrix
    ip_counts = Counter()
    for i in range(n_roots):
        for j in range(i+1, n_roots):
            ip = round(np.dot(roots[i], roots[j]))
            ip_counts[ip] += 1
    
    # Count roots by norm (should all be 2)
    norms = Counter(round(np.dot(r, r)) for r in roots)
    
    # Positive roots (those where first nonzero coordinate is positive)
    positive = []
    negative = []
    for r in roots:
        for x in r:
            if abs(x) > 1e-10:
                if x > 0:
                    positive.append(r)
                else:
                    negative.append(r)
                break
    
    # Dynkin coordinates of positive roots
    dynkin = roots_in_dynkin_basis(positive, simple_roots)
    
    # Highest root: the one with largest sum of Dynkin coordinates
    max_height = max(sum(d) for d in dynkin)
    highest = [d for d in dynkin if sum(d) == max_height]
    
    # E8 → E6 × A2 decomposition
    # E8 simple roots: α₁,...,α₈
    # E6 simple roots: α₁,...,α₆ (first 6)
    # A2 simple roots: α₇, α₈
    # But this depends on the Dynkin diagram labeling...
    #
    # For our labeling (branch at α₃):
    # Arm 1 (length 2): α₁ - α₂ - α₃
    # Arm 2 (length 4): α₃ - α₄ - α₅ - α₆ - α₇
    # Arm 3 (length 1): α₃ - α₈
    #
    # E6 is obtained by removing α₈ (the leaf on arm 3)
    # Then the remaining E7 Dynkin is: α₁-α₂-α₃-α₄-α₅-α₆-α₇
    # Removing α₇ from E7 gives E6: α₁-α₂-α₃-α₄-α₅-α₆
    # And A2 from α₇, α₈
    
    # E6 roots: those expressible using only α₁,...,α₆ (Dynkin coords 7,8 = 0)
    e6_roots = [d for d in dynkin if d[6] == 0 and d[7] == 0]
    
    # A2 roots: those expressible using only α₇, α₈ (Dynkin coords 1-6 = 0)
    a2_roots = [d for d in dynkin if all(d[i] == 0 for i in range(6))]
    
    # Mixed roots (involving both E6 and A2 directions)
    mixed_roots = [d for d in dynkin if d not in e6_roots and d not in a2_roots]
    
    return {
        'total_roots': n_roots,
        'inner_products': dict(ip_counts),
        'norms': dict(norms),
        'positive_roots': len(positive),
        'negative_roots': len(negative),
        'highest_root': highest[0] if highest else None,
        'max_height': max_height,
        'e6_positive_roots': len(e6_roots),
        'a2_positive_roots': len(a2_roots),
        'mixed_positive_roots': len(mixed_roots),
        'decomposition': f'{len(e6_roots)} + {len(a2_roots)} + {len(mixed_roots)} = {len(dynkin)}',
        'expected': '36 + 3 + 81 = 120 (positive roots: E6(36) + A2(3) + mixed(81))',
    }


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    print("=" * 78)
    print(" BIJECTION SOLVER — The 240 edge ↔ E8 root correspondence")
    print("=" * 78)
    
    adj, points, edges = build_w33()
    print(f"\n  Built W(3,3): {len(points)} points, {len(edges)} edges")
    
    # E8 Dynkin vertices found by PATTERN_SOLVER:
    # a1=7, a2=1, BRANCH=0, c1=13, c2=24, c3=28, c4=37, d=16
    e8_verts = [7, 1, 0, 13, 24, 28, 37, 16]
    
    # Verify these form E8 Dynkin
    sub = adj[np.ix_(e8_verts, e8_verts)]
    gram = 2 * np.eye(8, dtype=int) - sub
    det_gram = round(np.linalg.det(gram.astype(float)))
    print(f"  E8 Dynkin verified: det(Gram) = {det_gram}")
    
    # Build E8 root system
    print("\n" + "─" * 78)
    print("  [1/3] E8 ROOT SYSTEM")
    print("─" * 78)
    simple_roots, cartan = e8_simple_roots()
    
    # Check our Cartan matrix matches
    our_cartan = gram
    print(f"  Our Cartan from W(3,3):")
    for row in our_cartan:
        print(f"    {list(row)}")
    print(f"  Standard Cartan:")
    for row in cartan.astype(int):
        print(f"    {list(row)}")
    
    # Are they the same (up to permutation)?
    our_det = round(np.linalg.det(our_cartan.astype(float)))
    std_det = round(np.linalg.det(cartan))
    print(f"  det(our) = {our_det}, det(std) = {std_det}")
    
    all_roots = generate_all_roots(simple_roots)
    print(f"  Generated {len(all_roots)} E8 roots")
    
    e8_analysis = analyze_e8_structure(all_roots, simple_roots)
    print(f"  Inner product distribution: {e8_analysis['inner_products']}")
    print(f"  Highest root (Dynkin coords): {e8_analysis['highest_root']}")
    print(f"  E8 → E6 × A2 decomposition (positive roots):")
    print(f"    {e8_analysis['decomposition']}")
    print(f"    Expected: {e8_analysis['expected']}")
    
    # Investigate bijection
    print("\n" + "─" * 78)
    print("  [2/3] EDGE-ROOT BIJECTION INVESTIGATION")
    print("─" * 78)
    bij = investigate_bijection(adj, edges, e8_verts)
    print(f"  Graph diameter: {bij['diameter']}")
    print(f"  Distinct vertex adjacency profiles: {bij['num_distinct_adj_profiles']}")
    print(f"  Adjacency profile distribution:")
    for prof, count in sorted(bij['adj_profile_distribution'].items(), key=lambda x: -x[1]):
        print(f"    {prof}: {count} vertices")
    print(f"  Distinct edge adjacency sum-profiles: {bij['num_distinct_edge_adj_profiles']}")
    print(f"  Edge adj profile distribution:")
    for prof, count in sorted(bij['edge_adj_distribution'].items(), key=lambda x: -x[1]):
        print(f"    {prof}: {count} edges")
    print(f"  Distinct edge distance sum-profiles: {bij['num_distinct_sum_profiles']}")
    print(f"  Distinct edge distance pair-profiles: {bij['num_distinct_pair_profiles']}")
    
    # Summary
    print("\n" + "─" * 78)
    print("  [3/3] BIJECTION FEASIBILITY ANALYSIS")
    print("─" * 78)
    
    # Can the 240 edges be distinguished by their E8-vertex profiles?
    if bij['num_distinct_pair_profiles'] >= 240:
        print("  ✓ Edge pair-profiles DISTINGUISH all 240 edges!")
        print("  → A bijection via distance profiles is possible")
    else:
        print(f"  ✗ Only {bij['num_distinct_pair_profiles']} distinct pair-profiles")
        print(f"    (need 240 for a profile-based bijection)")
    
    if bij['num_distinct_edge_adj_profiles'] >= 240:
        print("  ✓ Edge adj-profiles DISTINGUISH all 240 edges!")
    else:
        print(f"  ✗ Only {bij['num_distinct_edge_adj_profiles']} distinct adj-profiles")
    
    print(f"""
  ┌─────────────────────────────────────────────────────────────────────┐
  │  KEY INSIGHT:                                                      │
  │                                                                    │
  │  The E8 Cartan matrix sits INSIDE W(3,3) as 2I - adj[sub].       │
  │  This means E8's simple root system is encoded in the graph.       │
  │                                                                    │
  │  The 240 edges of W(3,3) = 40 GQ lines × 6 edges/line.           │
  │  The 240 E8 roots = 120 positive + 120 negative.                  │
  │                                                                    │
  │  The natural INVOLUTION on edges: reverse orientation (i,j)↔(j,i) │
  │  matches the root negation: α ↔ -α.                               │
  │  So 120 pairs of ±edges ↔ 120 pairs of ±roots.                    │
  │                                                                    │
  │  The bijection may factor through:                                 │
  │  240 edges → 40 line orbits × 6 edges/orbit                      │
  │  240 roots → (72 E6 + 6 A2 + 81+81 mixed)                       │
  │            → (different decomposition needed)                      │
  └─────────────────────────────────────────────────────────────────────┘
""")
    
    return {
        'e8_analysis': e8_analysis,
        'bijection': bij,
    }


if __name__ == '__main__':
    results = main()
