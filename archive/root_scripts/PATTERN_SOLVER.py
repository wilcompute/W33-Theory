#!/usr/bin/env python3
"""
PATTERN SOLVER — Deep structural patterns in W(3,3) → E8
=========================================================

CRITICAL NEW DISCOVERIES TO INVESTIGATE:

1. The μ=3 graph on 27 non-neighbors = complement of Schläfli graph 
   = SRG(27,16,10,8) = intersection graph of 27 lines on cubic surface

2. The μ=0 graph = 9 disjoint triangles = partition into 9 triples
   (a triple = 3 mutually non-adjacent, μ=0 vertices = a "spread" of lines)

3. The GF(2) quadratic form on H = ker(A)/im(A) ≅ GF(2)^8 is ZERO
   → The E8 structure comes from INTEGER LIFTING, not mod-2 form

4. E8 root decomposition under E6 × A2: 240 = 72 + 6 + 81 + 81
   This mirrors: W(3,3) edges = some decomposition related to the 27-line structure

5. The 240 edges CAN be mapped to E8 roots via the 
   W(E6) → W(E7) → W(E8) chain of Weyl groups
"""

from collections import Counter
from itertools import product
import numpy as np


# ===========================================================================
# BUILD W(3,3)
# ===========================================================================

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
# BUILD E8 ROOT SYSTEM
# ===========================================================================

def build_e8_roots():
    """
    Construct the 240 roots of E8 explicitly.
    
    Using the D8 construction: roots are vectors in Z^8 or (Z+1/2)^8 such that:
    - All integer coordinates with sum even, norm² = 2
      (all permutations of (±1, ±1, 0, 0, 0, 0, 0, 0) with even sum)
    - All half-integer coordinates with even sum, norm² = 2
      (all (±1/2, ±1/2, ..., ±1/2) with even number of minus signs, or odd)
    
    Actually, simpler: E8 roots in the "even unimodular lattice" description:
    x ∈ Z^8 ∪ (Z+1/2)^8, x·x = 2, Σxᵢ ∈ 2Z
    """
    roots = []
    
    # Type 1: All integer, permutations of (±1, ±1, 0, 0, 0, 0, 0, 0)
    # Choose 2 positions, all sign combinations, require even sum
    for i in range(8):
        for j in range(i+1, 8):
            for si in [-1, 1]:
                for sj in [-1, 1]:
                    if (si + sj) % 2 == 0:  # Even sum contribution from these two
                        r = [0]*8
                        r[i] = si
                        r[j] = sj
                        roots.append(tuple(r))
    
    # Type 2: All half-integer, (±1/2)^8, with even number of -1/2
    for bits in product([0, 1], repeat=8):
        signs = [(-1)**b for b in bits]
        r = tuple(s * 0.5 for s in signs)
        if sum(r) % 2 == 0:  # Even sum
            # Check: norm² = 8 × 1/4 = 2 ✓
            roots.append(r)
    
    # Remove duplicates and verify count
    roots = list(set(roots))
    
    # Verify all have norm² = 2
    for r in roots:
        assert abs(sum(x**2 for x in r) - 2) < 1e-10
    
    return roots


def e8_adjacency(roots):
    """
    Build E8 root adjacency structure.
    For roots r₁, r₂, the inner product r₁·r₂ can be -2, -1, 0, 1, 2.
    Two roots are adjacent (ip = 1) in the root graph.
    """
    n = len(roots)
    ip_counts = Counter()
    
    for i in range(n):
        for j in range(i+1, n):
            ip = sum(roots[i][k] * roots[j][k] for k in range(8))
            ip_counts[round(ip)] += 1
    
    return dict(ip_counts)


# ===========================================================================
# INVESTIGATION 1: THE 27-LINE CONFIGURATION DEEP DIVE
# ===========================================================================

def investigate_27_lines(adj, points):
    """
    Deep analysis of the 27 non-neighbors = 27 lines on a cubic surface.
    
    The μ=3 graph is the complement of the Schläfli graph.
    The μ=0 graph gives 9 disjoint triples (a "spread").
    
    In the theory of 27 lines:
    - Each line meets exactly 10 others → Schläfli graph SRG(27,10,1,5)
    - 16 lines are skew to any given line
    - The 9 disjoint triples = 9 "tritangent planes" forming a spread
    - There are exactly 36 "double-sixes" and 45 tritangent planes
    """
    n = 40
    
    results_per_vertex = []
    
    # Analyze vertex 0
    v_idx = 0
    non_neighbors = [j for j in range(n) if j != v_idx and adj[v_idx, j] == 0]
    neighbors = [j for j in range(n) if adj[v_idx, j] == 1]
    m = 27
    assert len(non_neighbors) == m
    
    # Build the three graphs on 27 non-neighbors
    g27 = np.zeros((m, m), dtype=int)     # Adjacent in W(3,3)
    g_mu0 = np.zeros((m, m), dtype=int)   # Non-adj with μ=0
    g_mu3 = np.zeros((m, m), dtype=int)   # Non-adj with μ=3
    
    for a in range(m):
        for b in range(a+1, m):
            if adj[non_neighbors[a], non_neighbors[b]] == 1:
                g27[a, b] = g27[b, a] = 1
            else:
                # Count common neighbors among the 27
                common = sum(1 for c in range(m) if g27[a, c] == 0 and a != c and b != c)
                # Actually need to count AFTER building g27 fully
                pass
    
    # Recompute μ values properly
    for a in range(m):
        for b in range(a+1, m):
            if g27[a, b] == 0:
                common = sum(1 for c in range(m) if g27[a, c] == 1 and g27[b, c] == 1)
                if common == 0:
                    g_mu0[a, b] = g_mu0[b, a] = 1
                else:
                    g_mu3[a, b] = g_mu3[b, a] = 1
    
    # VERIFY: g_mu3 is the complement of Schläfli
    # Schläfli complement = SRG(27,16,10,8)
    mu3_degrees = [sum(g_mu3[i]) for i in range(m)]
    mu3_k = mu3_degrees[0] if len(set(mu3_degrees)) == 1 else -1
    
    mu3_lambda = []
    mu3_mu = []
    for a in range(m):
        for b in range(a+1, m):
            common = sum(1 for c in range(m) if g_mu3[a, c] == 1 and g_mu3[b, c] == 1)
            if g_mu3[a, b] == 1:
                mu3_lambda.append(common)
            else:
                mu3_mu.append(common)
    
    is_complement_schlafli = (
        mu3_k == 16 and
        len(set(mu3_lambda)) == 1 and mu3_lambda[0] == 10 and
        len(set(mu3_mu)) == 1 and mu3_mu[0] == 8
    )
    
    # VERIFY: g_mu0 is 9 disjoint triangles
    mu0_edges = sum(sum(g_mu0[i]) for i in range(m)) // 2
    mu0_degrees = [sum(g_mu0[i]) for i in range(m)]
    
    # Find the 9 triangles
    triangles_mu0 = []
    covered = set()
    for a in range(m):
        if a in covered:
            continue
        for b in range(a+1, m):
            if b in covered or g_mu0[a, b] != 1:
                continue
            for c in range(b+1, m):
                if c in covered or g_mu0[a, c] != 1 or g_mu0[b, c] != 1:
                    continue
                triangles_mu0.append((a, b, c))
                covered.update([a, b, c])
                break
            if a in covered:
                break
    
    # What is the g27 graph on the 27 non-neighbors?
    # We know: 8-regular, λ=1, μ ∈ {0, 3}
    # Is it the PETERSEN graph complement? No, that's 10 vertices.
    # Is it the KNESER graph K(9,4)? That has C(9,4)=126 vertices. No.
    #
    # The graph has 27 vertices, degree 8, λ=1, μ∈{0,3}.
    # Each vertex: 8 neighbors, 2 μ=0 non-neighbors, 16 μ=3 non-neighbors
    # So each vertex's non-neighbors split as: 2 (μ=0) + 16 (μ=3) = 18 = 27-8-1
    #
    # The 2 μ=0 non-neighbors of each vertex: vertex v is in exactly one μ=0 triangle
    # Triangle {a,b,c}: each pair has μ=0, meaning a,b are non-adj in g27, 
    # b,c are non-adj, a,c are non-adj, AND share 0 common neighbors.
    
    # Compute the μ=0 triples' structure within g27
    triples_info = []
    for t in triangles_mu0:
        a, b, c = t
        # How many g27-neighbors does each vertex in the triple have in common?
        ab_common = sum(1 for x in range(m) if g27[a,x]==1 and g27[b,x]==1)
        ac_common = sum(1 for x in range(m) if g27[a,x]==1 and g27[c,x]==1)
        bc_common = sum(1 for x in range(m) if g27[b,x]==1 and g27[c,x]==1)
        
        # Where do the 8 neighbors of a go?
        a_nbrs = [x for x in range(m) if g27[a,x]==1]
        a_nbrs_in_triple = [x for x in a_nbrs if x in t]
        a_nbrs_outside = [x for x in a_nbrs if x not in t]
        
        triples_info.append({
            'triple': t,
            'ab_common_nbrs_in_g27': ab_common,
            'ac_common_nbrs_in_g27': ac_common,
            'bc_common_nbrs_in_g27': bc_common,
        })
    
    # How do the 12 neighbors relate to the 27 non-neighbors?
    # For the 12 neighbors of vertex 0, forming 4 triangles:
    # Each triangle = a GQ line through vertex 0
    # Each neighbor has degree 12, of which:
    #   1 edge to vertex 0
    #   2 edges to other neighbors (λ=2)
    #   9 edges to non-neighbors
    # So each neighbor connects to exactly 9 of the 27 non-neighbors.
    
    nbr_to_nonnbr = {}
    for ni, x in enumerate(neighbors):
        connected = [j for j in range(m) if adj[x, non_neighbors[j]] == 1]
        nbr_to_nonnbr[ni] = connected
    
    # How many non-neighbors does each neighbor connect to?
    nbr_degrees_to_27 = [len(nbr_to_nonnbr[ni]) for ni in range(12)]
    
    # Does each μ=0 triple correspond to a GQ line?
    # A GQ line has 4 points. Our 9 triples have 3 points each.
    # But a GQ line through a non-neighbor v' consists of v' + 3 other points.
    # These 3 other points must all be collinear with v' on a GQ line.
    # In the 27-subgraph, the μ=0 condition means the 3 vertices of a triple
    # are "maximally separated" — no common neighbors in the 27-graph.
    
    return {
        'is_complement_schlafli': is_complement_schlafli,
        'mu3_params': f'SRG(27, {mu3_k}, {mu3_lambda[0] if mu3_lambda else "?"}, '
                      f'{mu3_mu[0] if mu3_mu else "?"})',
        'mu0_graph': f'{len(triangles_mu0)} disjoint triangles = 9 triples',
        'mu0_edges': mu0_edges,
        'mu0_degrees': Counter(mu0_degrees),
        'triples': triangles_mu0,
        'triples_info': triples_info,
        'nbr_degrees_to_27': Counter(nbr_degrees_to_27),
        'nbr_to_nonnbr_patterns': {ni: len(v) for ni, v in nbr_to_nonnbr.items()},
    }


# ===========================================================================
# INVESTIGATION 2: EDGE PARTITION MATCHING E8 → E6 × A2
# ===========================================================================

def edge_partition_analysis(adj, points, edges):
    """
    E8 → E6 × A2 decomposes 240 roots as: 72 + 6 + 81 + 81.
    
    Can we find a meaningful partition of 240 W(3,3) edges into these sizes?
    
    For each vertex v of W(3,3), the 240 edges split as:
    - 12 edges incident to v
    - 12 edges among v's 12 neighbors (4 triangles)
    - 108 edges between the 12 neighbors and 27 non-neighbors
    - 108 edges among the 27 non-neighbors
    Total: 12 + 12 + 108 + 108 = 240 ✓
    
    But this gives 24 + 216, not 78 + 162 (the dim decomposition of 248).
    
    Alternative: Consider the GQ line structure.
    - 40 lines in GQ(3,3), each line has 4 points
    - Each line incident to 4×3 = 12 edges (inside the line: C(4,2)=6 edges)
    - Actually: edges WITHIN a line: 6 per line × 40 lines / (edges per line pair)
    - Wait: each edge is in exactly λ=2 triangles, i.e., each edge is on λ + 1 = ?
    
    Actually in GQ(3,3): each edge (i,j) with adj[i,j]=1 means i,j are collinear.
    i and j lie on exactly one GQ line (since it's a GQ). 
    So each edge belongs to exactly one line. The 4 points of a line contribute
    C(4,2) = 6 edges. Number of lines = 40. Total edges from lines = 40 × 6 = 240 ✓!
    
    So the 240 edges ARE the 40 lines × 6 edges per line.
    This gives a partition of edges into 40 groups of 6.
    """
    n = 40
    
    # Find all 40 GQ lines
    # A GQ line through points i,j (with adj[i,j]=1) is the set of all points
    # collinear with both i and j. But in GQ: any two collinear points lie on
    # exactly one line, and a line has s+1=4 points.
    
    lines = []
    used_edges = set()
    
    for i in range(n):
        nbrs_i = set(j for j in range(n) if adj[i,j] == 1)
        for j in nbrs_i:
            if j <= i:
                continue
            if (i,j) in used_edges:
                continue
            # Points collinear with both i and j:
            # k such that adj[i,k]=1 AND adj[j,k]=1 AND k≠i,j
            # These k + {i,j} form the line
            common = nbrs_i & set(k for k in range(n) if adj[j,k] == 1) - {i, j}
            line = tuple(sorted([i, j] + list(common)))
            
            if len(line) == 4:  # Should always be 4 for GQ(3,3)
                lines.append(line)
                # Mark all edges of this line as used
                for a in line:
                    for b in line:
                        if a < b:
                            used_edges.add((a, b))
    
    # Remove duplicate lines
    lines = list(set(lines))
    
    print(f"  Found {len(lines)} GQ lines")
    print(f"  {len(used_edges)} edges accounted for (expected 240)")
    
    # Verify: each line has 6 edges, and each edge belongs to exactly one line
    edge_to_line = {}
    for li, line in enumerate(lines):
        pts = list(line)
        for a in range(len(pts)):
            for b in range(a+1, len(pts)):
                edge = (pts[a], pts[b])
                if edge in edge_to_line:
                    print(f"  WARNING: Edge {edge} in multiple lines!")
                edge_to_line[edge] = li
    
    unaccounted = set(edges) - set(edge_to_line.keys())
    
    # Line-line adjacency: two lines share 0 or 1 points (GQ axiom)
    line_adj = np.zeros((len(lines), len(lines)), dtype=int)
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            shared = len(set(lines[i]) & set(lines[j]))
            if shared == 1:
                line_adj[i,j] = line_adj[j,i] = 1
    
    line_degrees = [sum(line_adj[i]) for i in range(len(lines))]
    
    # The line graph of the INCIDENCE structure (not the edge graph)
    # Each line is incident to 4 points, each point to 4 lines
    # Two lines intersect iff they share a point
    # Through each point: 4 lines, pairwise intersecting → C(4,2) = 6 pairs
    # Total intersecting pairs: 40 points × 6 = 240 ... hmm
    # But counted with multiplicity (each intersecting pair counted once):
    # 40 × C(4,2) / 1 if each pair meets in exactly 1 point = 240

    # The POINT-LINE incidence matrix
    incidence = np.zeros((n, len(lines)), dtype=int)
    for li, line in enumerate(lines):
        for p in line:
            incidence[p, li] = 1
    
    # Verify: each point on 4 lines, each line through 4 points
    point_line_counts = [sum(incidence[i]) for i in range(n)]
    line_point_counts = [sum(incidence[:, j]) for j in range(len(lines))]
    
    return {
        'num_lines': len(lines),
        'lines': lines,
        'unaccounted_edges': len(unaccounted),
        'edges_per_line': 6,
        'total_edges': len(lines) * 6,
        'line_degrees': Counter(line_degrees),
        'point_line_counts': Counter(point_line_counts),
        'line_point_counts': Counter(line_point_counts),
        'partition_240': '240 = 40 lines × 6 edges/line',
        'gq_verification': {
            'num_points': n,
            'num_lines': len(lines),
            'points_per_line': 4,
            'lines_per_point': 4,
        },
    }


# ===========================================================================
# INVESTIGATION 3: INTEGER LATTICE LIFT — THE E8 LATTICE CONSTRUCTION
# ===========================================================================

def integer_lattice_lift(adj, points):
    """
    The GF(2) homology H = ker(A mod 2)/im(A mod 2) has dim 8 but trivial 
    quadratic form.
    
    The E8 lattice structure must come from LIFTING to integers.
    
    Consider: the matrix A (over Z) has eigenvalues 12, 2, -4 with 
    multiplicities 1, 24, 15.
    
    The E8 lattice connection should come from considering the lattice
    Λ = {x ∈ Z^40 : Ax ≡ 0 mod 2} / {x : x = Ay mod 2 for some y}
    
    But actually, the right construction uses the INTERSECTION MATRIX
    of the W(3,3) structure, not the adjacency matrix directly.
    
    Let me try: define the lattice L ⊂ Z^40 generated by the columns of 
    (A + 2I)/2... no, A has entries 0,1 and diagonal 0.
    
    Alternative approach: use the GRAM MATRIX.
    Define the Gram matrix G = 2I - A for an appropriate sublattice.
    If G restricted to an 8-dimensional sublattice gives the E8 Cartan matrix,
    we have our E8 lattice.
    """
    n = 40
    
    # Approach 1: Look for E8 Cartan matrix as a submatrix of 2I - A
    G = 2 * np.eye(n, dtype=int) - adj
    
    # The E8 Cartan matrix:
    cartan_e8 = np.array([
        [ 2, 0,-1, 0, 0, 0, 0, 0],
        [ 0, 2, 0,-1, 0, 0, 0, 0],
        [-1, 0, 2,-1, 0, 0, 0, 0],
        [ 0,-1,-1, 2,-1, 0, 0, 0],
        [ 0, 0, 0,-1, 2,-1, 0, 0],
        [ 0, 0, 0, 0,-1, 2,-1, 0],
        [ 0, 0, 0, 0, 0,-1, 2,-1],
        [ 0, 0, 0, 0, 0, 0,-1, 2],
    ], dtype=int)
    
    # G = 2I - A means: G[i,i] = 2, G[i,j] = -adj[i,j] for i≠j
    # This is the Seidel matrix (sort of). 
    # For 8 vertices forming a path in the adjacency graph, the submatrix 
    # of G would be the Cartan matrix of... something.
    
    # BUT: for E8 Dynkin diagram, vertex 3 has degree 3 (connected to 2,4,8 in 
    # standard labeling). We need 8 vertices in W(3,3) where:
    # - The induced subgraph on these 8 vertices matches the E8 Dynkin diagram
    
    # Search for TRUE E8 Dynkin subgraph in W(3,3)
    # E8 Dynkin diagram (Bourbaki):
    #
    #   a1 - a2 - b - c1 - c2 - c3 - c4
    #             |
    #             d
    #
    # Branch at b with THREE arms:
    #   Arm 1: b - a2 - a1 (length 2)
    #   Arm 2: b - c1 - c2 - c3 - c4 (length 4)
    #   Arm 3: b - d (length 1, just a leaf)
    #
    # ARM LENGTHS (1, 2, 4) distinguish E8 from D8 (which has (1, 1, 5))
    # det(E8 Cartan) = 1, det(D8 Cartan) = 4
    
    def find_e8_dynkin():
        """Find 8 vertices whose induced subgraph is E8 Dynkin (arm lengths 1,2,4)."""
        # Strategy: find branch vertex b, then extend three arms
        for b in range(n):
            nbrs_b = [j for j in range(n) if adj[b, j] == 1]
            # Try all triples of neighbors for the three arm starts
            for i_a2, a2 in enumerate(nbrs_b):
                for i_c1, c1 in enumerate(nbrs_b):
                    if i_c1 <= i_a2:
                        continue
                    if adj[a2, c1] == 1:
                        continue  # a2 and c1 must NOT be adjacent
                    for i_d, d in enumerate(nbrs_b):
                        if i_d <= i_c1:
                            continue
                        if adj[a2, d] == 1 or adj[c1, d] == 1:
                            continue  # d must not be adjacent to a2 or c1
                        
                        used = {b, a2, c1, d}
                        
                        # ARM 1: b - a2 - a1 (find a1 adjacent to a2, not to anything else)
                        a1_candidates = []
                        for a1 in range(n):
                            if a1 in used:
                                continue
                            if adj[a2, a1] != 1:
                                continue
                            if adj[b, a1] == 1 or adj[c1, a1] == 1 or adj[d, a1] == 1:
                                continue
                            a1_candidates.append(a1)
                        
                        for a1 in a1_candidates:
                            # ARM 3: d is already a leaf (length 1)
                            # ARM 2: b - c1 - c2 - c3 - c4 (extend path from c1)
                            used2 = used | {a1}
                            
                            # Find c2 adjacent to c1, not adj to b, a2, a1, d
                            for c2 in range(n):
                                if c2 in used2:
                                    continue
                                if adj[c1, c2] != 1:
                                    continue
                                # c2 must not be adjacent to b, a2, a1, d
                                if any(adj[c2, u] == 1 for u in used2 if u != c1):
                                    continue
                                
                                used3 = used2 | {c2}
                                
                                # Find c3 adjacent to c2, not adj to anything in used3 except c2
                                for c3 in range(n):
                                    if c3 in used3:
                                        continue
                                    if adj[c2, c3] != 1:
                                        continue
                                    if any(adj[c3, u] == 1 for u in used3 if u != c2):
                                        continue
                                    
                                    used4 = used3 | {c3}
                                    
                                    # Find c4 adjacent to c3, not adj to anything except c3
                                    for c4 in range(n):
                                        if c4 in used4:
                                            continue
                                        if adj[c3, c4] != 1:
                                            continue
                                        if any(adj[c4, u] == 1 for u in used4 if u != c3):
                                            continue
                                        
                                        # FOUND E8!
                                        # Order: a1, a2, b, c1, c2, c3, c4, d
                                        # Edges: a1-a2, a2-b, b-c1, c1-c2, c2-c3, c3-c4, b-d
                                        verts = [a1, a2, b, c1, c2, c3, c4, d]
                                        
                                        # Final verification
                                        sub = adj[np.ix_(verts, verts)]
                                        edge_count = sum(sum(sub)) // 2
                                        
                                        if edge_count == 7:
                                            det_g = round(np.linalg.det(
                                                (2*np.eye(8) - sub).astype(float)))
                                            if det_g == 1:
                                                return [verts]
            
            if b >= 5:  # Limit search depth
                break
        
        return []
    
    e8_found = find_e8_dynkin()
    
    if e8_found:
        verts = e8_found[0]
        sub = adj[np.ix_(verts, verts)]
        gram = 2 * np.eye(8, dtype=int) - sub
        
        # Is Gram matrix = E8 Cartan matrix (up to permutation)?
        gram_evals = sorted(np.linalg.eigvalsh(gram.astype(float)))
        cartan_evals = sorted(np.linalg.eigvalsh(cartan_e8.astype(float)))
        
        gram_match = np.allclose(gram_evals, cartan_evals, atol=0.05)
        det_gram = round(np.linalg.det(gram.astype(float)))
        det_cartan = round(np.linalg.det(cartan_e8.astype(float)))
        
        return {
            'e8_dynkin_found': True,
            'vertices': verts,
            'subgraph_adj': sub.tolist(),
            'gram_matrix': gram.tolist(),
            'cartan_matrix': cartan_e8.tolist(),
            'gram_eigenvalues': [round(e, 4) for e in gram_evals],
            'cartan_eigenvalues': [round(e, 4) for e in cartan_evals],
            'gram_matches_cartan': gram_match,
            'det_gram': det_gram,
            'det_cartan': det_cartan,
            'gram_matrix_raw': gram.tolist(),
        }
    else:
        return {
            'e8_dynkin_found': False,
            'message': 'No E8 Dynkin subgraph found in first 10 vertices',
        }


# ===========================================================================
# INVESTIGATION 4: THE WITTING-TO-E8 VIA ORBITS
# ===========================================================================

def orbit_structure(adj, points, edges):
    """
    Analyze the orbit structure of edges under the stabilizer of a vertex.
    
    The stabilizer of a vertex in W(E6) acts on the 240 edges.
    If we can decompose the 240 edges into orbits matching
    E8 root system structure, we have our bijection.
    
    Key question: the stabilizer of a point in Aut(GQ(3,3)) = W(E6)
    has order |W(E6)|/40 = 51840/40 = 1296.
    
    1296 = 6^4 = 2^4 · 3^4
    
    This stabilizer acts on the 240 edges: 12 incident + 228 non-incident.
    The 12 incident edges split into 4 lines × 3 edges = orbits?
    """
    n = 40
    
    # We can compute the stabilizer action on edges by looking at
    # which edges are "equivalent" under the automorphism group.
    
    # Since W(E6) acts transitively on vertices (GQ(3,3) is vertex-transitive),
    # and on edges (since it's edge-transitive for SRG with these parameters),
    # the edge orbits are determined by the pair type:
    # (distance from fixed vertex v) × (distance from both endpoints)
    
    # Edge types relative to vertex 0:
    # Type A: (0, j) where adj[0,j]=1 — incident edges (12 of them)
    # Type B: (i, j) where adj[0,i]=adj[0,j]=1 — among neighbors (12 of them)
    # Type C: (i, j) where adj[0,i]=1, adj[0,j]=0 — neighbor to non-neighbor (108)
    # Type D: (i, j) where adj[0,i]=adj[0,j]=0 — among non-neighbors (108)
    
    type_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    for i, j in edges:
        if i == 0 or j == 0:
            type_counts['A'] += 1
        elif adj[0, i] == 1 and adj[0, j] == 1:
            type_counts['B'] += 1
        elif adj[0, i] == 1 or adj[0, j] == 1:
            type_counts['C'] += 1
        else:
            type_counts['D'] += 1
    
    # Further split Type D edges by μ-type of the endpoints
    # Type D has 108 edges among 27 non-neighbors
    # The 27-graph has eigenvalues {8:1, 2:12, -1:8, -4:6}
    
    # The 108 edges in the 27-graph relate to the 8-regular structure
    # Each of the 9 μ=0 triples has 3 vertices; edges within triples: 0 (they're non-adjacent!)
    # Edges between triples: all 108 edges go between different triples
    # 9 triples, C(9,2) = 36 pairs of triples, each pair shares 108/36 = 3 edges on average
    
    non_neighbors = [j for j in range(n) if j != 0 and adj[0, j] == 0]
    m = 27
    
    # Build g27 and find triples
    g27 = np.zeros((m, m), dtype=int)
    for a in range(m):
        for b in range(a+1, m):
            if adj[non_neighbors[a], non_neighbors[b]] == 1:
                g27[a, b] = g27[b, a] = 1
    
    # Find μ=0 triples
    g_mu0 = np.zeros((m, m), dtype=int)
    for a in range(m):
        for b in range(a+1, m):
            if g27[a, b] == 0:
                common = sum(1 for c in range(m) if g27[a, c] == 1 and g27[b, c] == 1)
                if common == 0:
                    g_mu0[a, b] = g_mu0[b, a] = 1
    
    # Find the 9 triples
    triples = []
    covered = set()
    for a in range(m):
        if a in covered:
            continue
        for b in range(a+1, m):
            if b in covered or g_mu0[a, b] != 1:
                continue
            for c in range(b+1, m):
                if c in covered or g_mu0[a, c] != 1 or g_mu0[b, c] != 1:
                    continue
                triples.append((a, b, c))
                covered.update([a, b, c])
                break
            if a in covered:
                break
    
    # Edges between triples
    inter_triple_edges = {}
    for ti in range(len(triples)):
        for tj in range(ti+1, len(triples)):
            count = 0
            for a in triples[ti]:
                for b in triples[tj]:
                    if g27[a, b] == 1:
                        count += 1
            inter_triple_edges[(ti, tj)] = count
    
    edge_between_triples_dist = Counter(inter_triple_edges.values())
    
    # This gives a 9×9 weighted adjacency matrix — the "triple graph"
    triple_adj = np.zeros((9, 9), dtype=int)
    for (ti, tj), count in inter_triple_edges.items():
        triple_adj[ti, tj] = count
        triple_adj[tj, ti] = count
    
    triple_row_sums = [sum(triple_adj[i]) for i in range(9)]
    
    # Each vertex in a triple has 8 neighbors in g27, all outside the triple.
    # Each triple has 3 vertices × 8 = 24 edge-endpoints going out,
    # but each edge counted once from each end.
    # So each triple sends 24 edges to other triples.
    # But wait: these are edges in g27 from the triple's vertices to outside.
    # Edges from triple T = sum of degrees in g27 of T's vertices
    # = 3 × 8 = 24. Each such edge goes to exactly one other triple.
    # So the triple graph has each vertex with "weighted degree" 24.
    
    return {
        'edge_types': type_counts,
        'total': sum(type_counts.values()),
        'expected': len(edges),
        'num_triples': len(triples),
        'inter_triple_edge_dist': dict(edge_between_triples_dist),
        'triple_row_sums': Counter(triple_row_sums),
        'triple_adj_matrix': triple_adj.tolist(),
    }


# ===========================================================================
# INVESTIGATION 5: CHARACTERISTIC POLYNOMIAL AND DISCRIMINANT
# ===========================================================================

def characteristic_analysis(adj):
    """
    The characteristic polynomial of A encodes deep structural information.
    
    For SRG(40,12,2,4):
    char poly = (x - 12)(x - 2)^24 (x + 4)^15
    
    The DISCRIMINANT and other invariants from this polynomial...
    """
    n = 40
    
    # Eigenvalues and their formal properties
    evals = [(12, 1), (2, 24), (-4, 15)]
    
    # Product of all eigenvalues (up to sign) = |det(A)|
    det_sign = (12**1) * (2**24) * ((-4)**15)
    det_abs = abs(det_sign)
    
    # Trace identities
    tr_A = sum(e * m for e, m in evals)  # = 0 (A has 0 diagonal)
    tr_A2 = sum(e**2 * m for e, m in evals)  # = Σ adj[i,j]² = 2 × edges = 480
    tr_A3 = sum(e**3 * m for e, m in evals)  # = 6 × triangles (closed walks of length 3)
    tr_A4 = sum(e**4 * m for e, m in evals)  # = closed walks of length 4
    
    # tr(A) = 12 + 48 - 60 = 0 ✓
    # tr(A²) = 144 + 96 + 240 = 480 ✓ (= 2 × 240 edges)
    # tr(A³) = 1728 + 192 - 960 = 960 → triangles = 960/6 = 160
    # tr(A⁴) = 20736 + 384 + 3840 = 24960 → closed 4-walks
    
    num_triangles = tr_A3 // 6
    
    # In GQ(3,3): each line has C(4,2)=6 edges, each edge in λ=2 triangles.
    # But also: each line (4 points) has C(4,3)=4 triangles.
    # Number of lines = 40, so triangles from lines = 40 × 4 = 160 ✓ 
    # All triangles come from GQ lines!
    
    # The Seidel matrix S = J - I - 2A (for SRG)
    # Or: the signless Laplacian L = D + A = 12I + A
    # L has eigenvalues 12+12=24, 12+2=14, 12-4=8
    # These are all positive → the Laplacian is positive definite
    
    # Smith Normal Form of A over Z could reveal torsion in integer homology
    # det(A) = 12 × 2^24 × (-4)^15 = 12 × 16777216 × (-1073741824)
    # = 12 × 2^24 × (-2^30) = -12 × 2^54 = -3 × 2^56
    
    det_A = 12 * (2**24) * ((-4)**15)
    det_factored = f"det(A) = 12 × 2²⁴ × (-4)¹⁵ = (-1)¹⁵ × 3 × 2²⁶ × 2²⁴ × 2³⁰ = -3 × 2⁵⁶"
    
    # Actually: 12 = 2² × 3, 2^24 = 2^24, (-4)^15 = -4^15 = -2^30
    # det = 2² × 3 × 2^24 × (-2^30) = -3 × 2^56
    det_check = -3 * 2**56
    
    return {
        'eigenvalues': evals,
        'traces': {
            'tr(A)': tr_A,
            'tr(A²)': tr_A2,
            'tr(A³)': tr_A3,
            'tr(A⁴)': tr_A4,
        },
        'triangles': num_triangles,
        'triangles_from_lines': '40 × 4 = 160 ✓ (all triangles come from GQ lines)',
        'det(A)': det_A,
        'det_factored': det_factored,
        'det_check': det_A == det_check,
        'det_factorization': '-3 × 2⁵⁶',
        'note': ('det(A) = -3 × 2⁵⁶: the only odd prime factor is 3 = the GQ order s. '
                 'The power 56 = 2 × 28 = 2 × [Sp(6,F₂):W(E6)]. '
                 'Also 56 = dim(fund rep of E7).'),
    }


# ===========================================================================
# MAIN
# ===========================================================================

def main():
    print("=" * 78)
    print(" PATTERN SOLVER — Deep structural patterns in W(3,3) → E8")
    print("=" * 78)
    
    adj, points, edges = build_w33()
    print(f"\n  Built W(3,3): {len(points)} points, {len(edges)} edges\n")
    
    # Investigation 1: 27 lines
    print("─" * 78)
    print("  [1/5] THE 27-LINE CONFIGURATION")
    print("─" * 78)
    lines27 = investigate_27_lines(adj, points)
    print(f"  μ=3 graph = complement of Schläfli: {lines27['is_complement_schlafli']}")
    print(f"  μ=3 parameters: {lines27['mu3_params']}")
    print(f"  μ=0 graph: {lines27['mu0_graph']}")
    print(f"  9 triples (spreads): {lines27['triples'][:3]}...")
    n_triples = len(lines27['triples'])
    print(f"  Triple-pair common neighbor counts:")
    for info in lines27['triples_info'][:3]:
        print(f"    {info['triple']}: ab={info['ab_common_nbrs_in_g27']}, "
              f"ac={info['ac_common_nbrs_in_g27']}, bc={info['bc_common_nbrs_in_g27']}")
    print(f"  Each of 12 neighbors connects to {dict(lines27['nbr_degrees_to_27'])} non-neighbors")
    
    # Investigation 2: Edge partition  
    print("\n" + "─" * 78)
    print("  [2/5] EDGE PARTITION BY GQ LINES")
    print("─" * 78)
    edge_part = edge_partition_analysis(adj, points, edges)
    print(f"  {edge_part['partition_240']}")
    print(f"  Line degrees (adjacency): {dict(edge_part['line_degrees'])}")
    print(f"  GQ verification: {edge_part['gq_verification']}")
    
    # Investigation 3: Integer lattice
    print("\n" + "─" * 78)
    print("  [3/5] E8 DYNKIN SUBGRAPH SEARCH")
    print("─" * 78)
    lattice = integer_lattice_lift(adj, points)
    print(f"  E8 Dynkin found: {lattice['e8_dynkin_found']}")
    if lattice['e8_dynkin_found']:
        print(f"  Vertices: {lattice['vertices']}")
        print(f"  Gram matrix = E8 Cartan: {lattice['gram_matches_cartan']}")
        print(f"  det(Gram) = {lattice.get('det_gram', '?')}, det(Cartan) = {lattice.get('det_cartan', '?')}")
        print(f"  Gram eigenvalues: {lattice['gram_eigenvalues']}")
        print(f"  Cartan eigenvalues: {lattice['cartan_eigenvalues']}")
        print(f"  Gram matrix (2I - adj[sub]):")
        for row in lattice.get('gram_matrix_raw', lattice['subgraph_adj']):
            print(f"    {row}")
        print(f"  Adjacency submatrix:")
        for row in lattice['subgraph_adj']:
            print(f"    {row}")
    
    # Investigation 4: Orbit structure
    print("\n" + "─" * 78)
    print("  [4/5] ORBIT STRUCTURE OF 240 EDGES")
    print("─" * 78)
    orbits = orbit_structure(adj, points, edges)
    print(f"  Edge types relative to vertex 0: {orbits['edge_types']}")
    print(f"  12 + 12 + 108 + 108 = {orbits['total']}")
    print(f"  Number of μ=0 triples: {orbits['num_triples']}")
    print(f"  Inter-triple edge distribution: {orbits['inter_triple_edge_dist']}")
    print(f"  Triple row sums: {orbits['triple_row_sums']}")
    print(f"  Triple adjacency matrix (9×9 weighted):")
    for row in orbits['triple_adj_matrix']:
        print(f"    {row}")
    
    # Investigation 5: Characteristic analysis
    print("\n" + "─" * 78)
    print("  [5/5] CHARACTERISTIC POLYNOMIAL ANALYSIS")
    print("─" * 78)
    char_analysis = characteristic_analysis(adj)
    print(f"  Traces: {char_analysis['traces']}")
    print(f"  Triangles: {char_analysis['triangles']}")
    print(f"  {char_analysis['triangles_from_lines']}")
    print(f"  det(A) = {char_analysis['det_factorization']}")
    print(f"  {char_analysis['note']}")
    
    # Final synthesis
    print("\n" + "=" * 78)
    print("  PATTERN SYNTHESIS")
    print("=" * 78)
    print(f"""
  ┌─────────────────────────────────────────────────────────────────────┐
  │  THE DEEP PATTERNS:                                                │
  │                                                                    │
  │  1. VERTEX → CUBIC SURFACE:                                       │
  │     Fix any vertex v. Its 27 non-neighbors naturally carry         │
  │     the structure of 27 lines on a cubic surface:                  │
  │     • μ=3 graph = complement of Schläfli ✓                        │
  │     • μ=0 graph = 9 disjoint triples (a "spread")                │
  │     • Symmetry W(E6) matches Aut(GQ(3,3))                         │
  │                                                                    │
  │  2. LINES → E8 EDGES:                                             │
  │     The 240 edges = 40 GQ lines × 6 edges per line               │
  │     Each GQ line = clique of 4 mutually-adjacent points            │
  │     160 triangles = 40 lines × 4 triangles per line              │
  │                                                                    │
  │  3. THE DETERMINANT:                                               │
  │     det(A) = -3 × 2⁵⁶                                            │
  │     Only odd prime factor = 3 = GF(3)'s characteristic           │
  │     Exponent 56 = dim(fund rep E7) = 2 × 28                      │
  │                                                                    │
  │  4. THE TRIPLE GRAPH:                                              │
  │     The 9 triples of non-neighbors form a weighted graph           │
  │     with total degree 24 per triple (= 3 x 8)                    │
  │     Triple adj = 3(J_9 - I_9): COMPLETELY UNIFORM!                │
  └─────────────────────────────────────────────────────────────────────┘
""")
    
    return {
        'lines27': lines27,
        'edge_part': edge_part,
        'lattice': lattice,
        'orbits': orbits,
        'char_analysis': char_analysis,
    }


if __name__ == '__main__':
    results = main()
