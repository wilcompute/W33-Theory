#!/usr/bin/env python3
"""
MATCHING_TO_ROOTS — Can 40×3×2 be mapped to 120+120 E8 roots?
================================================================

PROVEN STRUCTURE:
  240 W(3,3) edges = 40 GQ lines × 3 matchings × 2 edges per matching

QUESTION: Does this structure match the E8 root structure?

E8 ROOT DECOMPOSITION under E6 × A2 (SU(3)):
  248 = (78,1) + (1,8) + (27,3) + (27̄,3̄)
  
  Roots only (dim 240):
  240 = 72 + 6 + 81 + 81
      = (E6 adj roots) + (A2 adj roots) + (27 × 3) + (27̄ × 3̄)
  
  The factor of 3 in (27,3) is the 3 of SU(3) = the 3 of GF(3)!
  The 81 = 27 × 3 means each of the 27-dimensional worth of roots
  comes in 3 copies labeled by elements of GF(3).

OUR STRUCTURE:
  240 = 40 × 3 × 2
  
  • 40 GQ lines ↔ 40 points (self-dual GQ)
  • 3 matchings per line ↔ 3 elements of GF(3) ↔ 3 of SU(3)
  • 2 edges per matching ↔ ±α (root vs negative root)

COMPATIBILITY CHECK:
  40 × 3 = 120 (matching-line pairs)
  120 positive E8 roots: 36 + 3 + 81 = 120 (from E6 + A2 + mixed)
  
  But 40 ≠ 36 + 3 and 3 isn't playing the same role in both decompositions.
  
  Alternative: 40 = 27 + 12 + 1
  Through each vertex: 12 neighbors + 27 non-neighbors + self = 40
  And: 27 × 3 = 81, 12 × 3 = 36, 1 × 3 = 3
  So: 40 × 3 = 120 = (27 + 12 + 1) × 3 = 81 + 36 + 3 ✓
  
  This MATCHES: 120 = 81(mixed) + 36(E6/2) + 3(A2/2)!!!
  
  ButWait: E6 positive roots = 36 = 72/2? Yes! And A2 positive = 3 = 6/2!
  
  SO: 120 positive E8 roots = 36 + 3 + 81
                             = (E6+)/2 + (A2+)/2 + (27 × 3)
                             = 12 × 3 + 1 × 3 + 27 × 3
                             = (12 + 1 + 27) × 3
                             = 40 × 3
                             
  WAIT — this means 120 = 40 × 3 IS the correct decomposition!
  36 + 3 + 81 = 120 = 40 × 3 says that:
  - 12 lines (through a fixed vertex) × 3 matchings = 36 (E6 positive roots)
  - 1 "self-line" × 3 matchings = 3 (A2 positive roots)
  - 27 lines (through non-neighbors) × 3 matchings = 81 (mixed)
  
  But GQ has 40 lines, not 40 = 12 + 1 + 27!
  Actually 40 lines decompose relative to a fixed VERTEX (not LINE):
  - 4 lines through the vertex (the vertex lies on 4 GQ lines)
  - 36 other lines
  
  Hmm, that doesn't give 12 + 1 + 27 either.
  
  Let me count differently. Lines through each POINT:
  Each point lies on 4 lines. There are 40 points and 40 lines.
  The point-line incidence: 40 × 4 = 160 flags
  Check: 40 lines × 4 points/line = 160 ✓
  
  OK so the decomposition 40 = 12 + 1 + 27 was for VERTICES, not lines.
  
  But: 40 × 3 = 120 = (12+1+27) × 3 is still a numerical identity.
  It means:
    120 positive roots = 40 matching-line pairs
    and 40 = the number of both points AND lines of GQ(3,3)
    and 120 = 40 × 3 = 40 × |GF(3)*| where GF(3)* = {1, 2} (units)
    
  WAIT: 40 × 3 = 120, but 40 × |GF(3)*| = 40 × 2 = 80 ≠ 120.
  No, the 3 matchings are labeled by ALL of GF(3) = {0, 1, 2}, not just units.
  
  The key numerical check: 
    40 × 3 = 120 (matching-line pairs) = positive roots
    40 × 3 × 2 = 240 (edges) = all roots
  
  This is not just numerology — it's STRUCTURAL:
    Each matching-line pair (L, m) where L is a line and m ∈ GF(3)
    is a matching of 2 disjoint edges on L.
    The two edges in the matching correspond to α and -α.
    The 3 matchings correspond to the 3 colors of SU(3).
    
    This is a FUNCTION: edges → roots (up to choosing signs).
    
  Can we make this explicit? Let me compute.
"""

from collections import Counter
from itertools import product
import numpy as np


def build_w33():
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


def find_gq_lines(adj, n):
    """Find all 40 GQ lines (each a clique of 4 mutually adjacent points)."""
    lines = []
    used_edges = set()
    for i in range(n):
        nbrs_i = set(j for j in range(n) if adj[i,j] == 1)
        for j in nbrs_i:
            if j <= i:
                continue
            if (i,j) in used_edges:
                continue
            common = nbrs_i & set(k for k in range(n) if adj[j,k] == 1) - {i, j}
            line = tuple(sorted([i, j] + list(common)))
            if len(line) == 4:
                lines.append(line)
                for a in range(len(line)):
                    for b in range(a+1, len(line)):
                        used_edges.add((line[a], line[b]))
    return list(set(lines))


def matching_decomposition(lines):
    """
    For each line (K₄ on 4 points), find the 3 perfect matchings.
    
    A perfect matching of K₄ = a partition of 4 vertices into 2 pairs.
    There are exactly 3 such partitions:
      M₀ = {{a,b}, {c,d}}
      M₁ = {{a,c}, {b,d}}
      M₂ = {{a,d}, {b,c}}
    
    Label these by GF(3) = {0, 1, 2}.
    Each matching contributes 2 edges to the total 6 edges of K₄.
    """
    all_labeled_edges = {}  # edge → (line_idx, matching_idx, pair_idx)
    
    for li, line in enumerate(lines):
        p = list(line)
        matchings = [
            [(p[0], p[1]), (p[2], p[3])],
            [(p[0], p[2]), (p[1], p[3])],
            [(p[0], p[3]), (p[1], p[2])],
        ]
        for mi, matching in enumerate(matchings):
            for pi, pair in enumerate(matching):
                edge = tuple(sorted(pair))
                all_labeled_edges[edge] = (li, mi, pi)
    
    return all_labeled_edges


def analyze_matching_structure(adj, edges, lines, labeled_edges):
    """
    Investigate the structure of the 3-coloring induced by matchings.
    
    Each edge has a color ∈ {0, 1, 2} = GF(3) (its matching index).
    Color class c = all edges with matching index c.
    Each class has 40 × 2 = 80 edges.
    
    Questions:
    1. Are the 3 color classes isomorphic as graphs on 40 vertices?
    2. What is the degree of each vertex in each color class?
    3. Do the color classes have special spectral properties?
    """
    n = 40
    
    # Build the 3 color class adjacency matrices
    color_adj = [np.zeros((n, n), dtype=int) for _ in range(3)]
    
    for edge, (li, mi, pi) in labeled_edges.items():
        i, j = edge
        color_adj[mi][i, j] = 1
        color_adj[mi][j, i] = 1
    
    # Analyze each color class
    color_results = []
    for c in range(3):
        degrees = [sum(color_adj[c][i]) for i in range(n)]
        evals = sorted([round(e, 4) for e in np.linalg.eigvalsh(color_adj[c].astype(float))], reverse=True)
        eval_rounded = [round(e) for e in evals]
        
        # Edge count
        edge_count = sum(degrees) // 2
        
        color_results.append({
            'color': c,
            'edges': edge_count,
            'degree_dist': Counter(degrees),
            'is_regular': len(set(degrees)) == 1,
            'degree': degrees[0] if len(set(degrees)) == 1 else f"varies: {dict(Counter(degrees))}",
            'eigenvalues': Counter(eval_rounded),
        })
    
    # Pairwise intersections of color classes
    # Color c₁ ∩ c₂: edges that share a vertex
    for c1 in range(3):
        for c2 in range(c1+1, 3):
            product_mat = (color_adj[c1] @ color_adj[c2])
            # product_mat[i][j] = number of paths i→k→j where i-k has color c1 and k-j has color c2
    
    # The SUM of all 3 color class matrices should equal the adjacency matrix
    total = sum(color_adj)
    matches_adj = np.array_equal(total, adj)
    
    # The product color_adj[c1] × color_adj[c2] tells us about paths
    # colored (c1, c2): how do colors interact?
    
    return {
        'color_results': color_results,
        'sum_equals_adj': matches_adj,
        '3_coloring_verified': matches_adj and all(cr['edges'] == 80 for cr in color_results),
    }


def analyze_matching_as_roots(adj, lines, labeled_edges):
    """
    Test whether the matching structure naturally produces a root system.
    
    Key idea: if we assign each matching-line pair (L, m) a "root vector"
    based on the W(3,3) structure, do these vectors form an E8 root system?
    
    Define for each line L through points {a,b,c,d}:
    The characteristic vector χ_L = e_a + e_b + e_c + e_d ∈ Z^40
    
    For each matching M on L:
    M = {{a,b}, {c,d}}: define ψ_M = e_a + e_b - e_c - e_d ∈ Z^40
    (positive for one pair, negative for the other)
    
    OR: ψ_M = (e_a + e_b) - (e_c + e_d) = "difference of pairs"
    
    This gives 120 vectors (40 lines × 3 matchings).
    With signs: ±ψ_M gives 240 vectors.
    
    Question: do these 240 vectors form a root system?
    """
    n = 40
    
    # Compute matching vectors
    matching_vectors = []  # Each entry: (line_idx, match_idx, vector)
    
    for li, line in enumerate(lines):
        p = list(line)
        matchings = [
            (set([p[0], p[1]]), set([p[2], p[3]])),
            (set([p[0], p[2]]), set([p[1], p[3]])),
            (set([p[0], p[3]]), set([p[1], p[2]])),
        ]
        for mi, (pos_pair, neg_pair) in enumerate(matchings):
            vec = np.zeros(n, dtype=int)
            for v in pos_pair:
                vec[v] = 1
            for v in neg_pair:
                vec[v] = -1
            matching_vectors.append((li, mi, vec))
    
    # Compute inner product matrix
    # ψ_M1 · ψ_M2 using standard inner product in R^40
    m = len(matching_vectors)
    ip_counts = Counter()
    
    for i in range(m):
        for j in range(i+1, m):
            ip = int(matching_vectors[i][2] @ matching_vectors[j][2])
            ip_counts[ip] += 1
    
    # Self inner products
    self_norms = Counter()
    for i in range(m):
        norm_sq = int(matching_vectors[i][2] @ matching_vectors[i][2])
        self_norms[norm_sq] += 1
    
    # Also include negative vectors to get full 240
    all_vecs = []
    for li, mi, vec in matching_vectors:
        all_vecs.append(vec)
        all_vecs.append(-vec)
    
    full_ip_counts = Counter()
    for i in range(len(all_vecs)):
        for j in range(i+1, len(all_vecs)):
            ip = int(all_vecs[i] @ all_vecs[j])
            full_ip_counts[ip] += 1
    
    # For a root system, we need:
    # 1. All roots have the same norm² (= 2 for simply-laced)
    # 2. Inner products between distinct roots ∈ {-2, -1, 0, 1, 2}
    # 3. 2(α·β)/(β·β) ∈ Z for all pairs
    
    is_root_system = (
        len(self_norms) == 1 and 
        all(ip in [-4, -3, -2, -1, 0, 1, 2, 3, 4] for ip in full_ip_counts.keys())
    )
    
    # The norms
    norm_val = list(self_norms.keys())[0] if len(self_norms) == 1 else None
    
    # If norm² = 4, we can rescale by √2 to get norm² = 2
    # Then inner products get divided by 2
    
    return {
        'num_matching_vectors': m,
        'self_norms': dict(self_norms),
        'norm_value': norm_val,
        'ip_distribution_120': dict(ip_counts),
        'ip_distribution_240': dict(full_ip_counts),
        'is_root_system': is_root_system,
        'note': f'All matching vectors have norm² = {norm_val}' if norm_val else 'Mixed norms!',
    }


def main():
    print("=" * 78)
    print(" MATCHING_TO_ROOTS — Can 40x3x2 map to E8 roots?")
    print("=" * 78)
    
    adj, points, edges = build_w33()
    n = 40
    print(f"\n  Built W(3,3): {n} points, {len(edges)} edges")
    
    lines = find_gq_lines(adj, n)
    labeled = matching_decomposition(lines)
    print(f"  Found {len(lines)} GQ lines, {len(labeled)} labeled edges")
    
    # 3-coloring analysis
    print("\n" + "-" * 78)
    print("  [1/2] 3-COLORING BY MATCHINGS")
    print("-" * 78)
    
    colors = analyze_matching_structure(adj, edges, lines, labeled)
    print(f"  Sum of 3 color classes = adjacency matrix: {colors['sum_equals_adj']}")
    print(f"  3-coloring verified (each class = 80 edges): {colors['3_coloring_verified']}")
    
    for cr in colors['color_results']:
        print(f"\n  Color {cr['color']}:")
        print(f"    Edges: {cr['edges']}")
        print(f"    Regular: {cr['is_regular']}, degree: {cr['degree']}")
        print(f"    Eigenvalues: {dict(cr['eigenvalues'])}")
    
    # Root system test
    print("\n" + "-" * 78)
    print("  [2/2] MATCHING VECTORS AS ROOT SYSTEM?")
    print("-" * 78)
    
    root_test = analyze_matching_as_roots(adj, lines, labeled)
    print(f"  Number of matching vectors: {root_test['num_matching_vectors']}")
    print(f"  {root_test['note']}")
    print(f"  Inner products (120 positive): {root_test['ip_distribution_120']}")
    print(f"  Inner products (240 = ±): {root_test['ip_distribution_240']}")
    print(f"  Is root system? {root_test['is_root_system']}")
    
    # Key analysis
    norm = root_test['norm_value']
    if norm:
        print(f"\n  If we rescale by 1/sqrt({norm//2}), norm² → 2")
        print(f"  Then inner products get divided by {norm//2}")
        scaled_ip = {k: v for k, v in root_test['ip_distribution_240'].items()}
        
        # Check if inner products / (norm/2) are always integers
        scale = norm // 2
        normalized_ip = {}
        for ip, count in root_test['ip_distribution_240'].items():
            if ip % scale == 0:
                normalized_ip[ip // scale] = count
            else:
                normalized_ip[f'{ip}/{scale}'] = count
        print(f"  Normalized inner products: {normalized_ip}")
    
    # The 80 edges per color class 
    # Compare: 80 = dim of adjoint of SO(16) minus something?
    # 80 = 8 × 10 = rank(E8) × 10
    # 80 = 40 × 2 (2 edges per matching per line)
    # 80 edges form a 4-regular graph on 40 vertices (each vertex on 4 edges per color)
    #   because: each vertex is on 4 lines × 1 matching per line = 4 edges per color
    #   Wait: for a fixed color c, each vertex v participates in how many edges?
    #   v is on 4 lines. Each line has 1 matching of color c.
    #   In matching c of a line, is v always in one of the 2 pairs? Yes!
    #   So v participates in exactly 4 edges of color c.
    #   4 × 40 / 2 = 80 ✓
    
    print(f"""
  ┌─────────────────────────────────────────────────────────────────────┐
  │  MATCHING STRUCTURE ANALYSIS:                                      │
  │                                                                    │
  │  240 = 40 × 3 × 2:                                               │
  │  • 40 GQ lines, each a K₄ on 4 points                            │
  │  • 3 perfect matchings per K₄ (labeled by GF(3))                 │  
  │  • 2 edges per matching (paired by the matching)                  │
  │                                                                    │
  │  Each color class (80 edges) is 4-REGULAR on 40 vertices          │  
  │  because each point lies on 4 lines × 1 matching/line = 4 edges  │
  │                                                                    │
  │  The 3 color classes partition the adjacency matrix:              │
  │  A = A₀ + A₁ + A₂  where each Aᵢ has degree 4                   │
  │  Note: 4 + 4 + 4 = 12 = k ✓                                     │
  │                                                                    │
  │  This is a PARTITION INTO 3 SPANNING 4-REGULAR SUBGRAPHS!        │
  │  A 3-edge-coloring or 3-factorization of W(3,3).                 │
  │                                                                    │
  │  The matching vectors ψ_M ∈ Z⁴⁰ have norm² = 4.                 │
  │  After rescaling by 1/√2, they have norm² = 2.                   │
  │  But their inner products need to be checked for root system      │
  │  conditions.                                                       │
  └─────────────────────────────────────────────────────────────────────┘
""")


if __name__ == '__main__':
    main()
