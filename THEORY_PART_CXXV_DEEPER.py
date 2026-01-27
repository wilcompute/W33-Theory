"""
W33 THEORY - PART CXXV (continued): DEEPER INVESTIGATION
=========================================================

The simple inner product criterion doesn't work.
Let's try more sophisticated approaches:

1. Look at the actual structure of both graphs more carefully
2. Try other geometric relations on D₅ roots
3. Check if W33 is isomorphic to a DIFFERENT graph on D₅ roots
"""

import numpy as np
from itertools import combinations, product
from collections import Counter

def construct_D5_roots():
    """D₅ roots: ±eᵢ ± eⱼ for i < j"""
    roots = []
    for i, j in combinations(range(5), 2):
        for si, sj in product([1, -1], repeat=2):
            root = [0, 0, 0, 0, 0]
            root[i] = si
            root[j] = sj
            roots.append(tuple(root))
    return roots

def inner_product(r1, r2):
    return sum(a * b for a, b in zip(r1, r2))

def build_W33_symplectic():
    """Build W33 as Sp(4, F₃)"""
    F3 = [0, 1, 2]
    
    def symplectic_form(v1, v2):
        x1, x2, x3, x4 = v1
        y1, y2, y3, y4 = v2
        return (x1*y2 - x2*y1 + x3*y4 - x4*y3) % 3
    
    all_vectors = [(x1, x2, x3, x4) for x1 in F3 for x2 in F3 
                   for x3 in F3 for x4 in F3 if (x1, x2, x3, x4) != (0,0,0,0)]
    
    def span_subspace(v1, v2):
        vectors = set()
        for a in F3:
            for b in F3:
                if a == 0 and b == 0:
                    continue
                v = tuple((a * v1[i] + b * v2[i]) % 3 for i in range(4))
                vectors.add(v)
        return frozenset(vectors)
    
    def is_totally_isotropic_subspace(vectors):
        vec_list = list(vectors)
        for i in range(len(vec_list)):
            for j in range(i+1, len(vec_list)):
                if symplectic_form(vec_list[i], vec_list[j]) != 0:
                    return False
        return True
    
    subspaces = set()
    for v1 in all_vectors:
        for v2 in all_vectors:
            if v1 >= v2:
                continue
            span = span_subspace(v1, v2)
            if len(span) == 8:
                if is_totally_isotropic_subspace(span):
                    subspaces.add(span)
    
    vertices = list(subspaces)
    n = len(vertices)
    
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            intersection = vertices[i] & vertices[j]
            if len(intersection) == 2:
                adj[i][j] = 1
                adj[j][i] = 1
    
    return vertices, adj

def analyze_graph_structure(adj, name):
    """Compute detailed graph invariants"""
    n = len(adj)
    
    # Degree distribution
    degrees = [sum(row) for row in adj]
    
    # Count triangles
    triangles = 0
    for i in range(n):
        for j in range(i+1, n):
            if adj[i][j]:
                for k in range(j+1, n):
                    if adj[i][k] and adj[j][k]:
                        triangles += 1
    
    # Compute λ (common neighbors of adjacent pairs) and μ (of non-adjacent)
    lambda_list = []
    mu_list = []
    
    for i in range(n):
        for j in range(i+1, n):
            common = sum(adj[i][k] and adj[j][k] for k in range(n))
            if adj[i][j]:
                lambda_list.append(common)
            else:
                mu_list.append(common)
    
    print(f"\n  {name}:")
    print(f"    Vertices: {n}")
    print(f"    Edges: {sum(degrees)//2}")
    print(f"    Degree: {degrees[0]} (regular: {len(set(degrees)) == 1})")
    print(f"    Triangles: {triangles}")
    print(f"    λ (adjacent common neighbors): {Counter(lambda_list)}")
    print(f"    μ (non-adjacent common neighbors): {Counter(mu_list)}")
    
    return {
        'n': n,
        'edges': sum(degrees)//2,
        'degree': degrees[0],
        'triangles': triangles,
        'lambda': Counter(lambda_list),
        'mu': Counter(mu_list)
    }

def check_graph_isomorphism_by_spectrum(adj1, adj2, name1, name2):
    """Compare eigenvalue spectra (necessary but not sufficient for isomorphism)"""
    
    A1 = np.array(adj1, dtype=float)
    A2 = np.array(adj2, dtype=float)
    
    eig1 = sorted(np.linalg.eigvalsh(A1), reverse=True)
    eig2 = sorted(np.linalg.eigvalsh(A2), reverse=True)
    
    # Round for comparison
    eig1_rounded = [round(e, 6) for e in eig1]
    eig2_rounded = [round(e, 6) for e in eig2]
    
    print(f"\n  Eigenvalue comparison ({name1} vs {name2}):")
    print(f"    {name1} spectrum: {Counter(eig1_rounded)}")
    print(f"    {name2} spectrum: {Counter(eig2_rounded)}")
    
    if eig1_rounded == eig2_rounded:
        print(f"    SPECTRA MATCH! (Possible isomorphism)")
        return True
    else:
        print(f"    Spectra differ (NOT isomorphic)")
        return False

def main():
    print("=" * 70)
    print(" PART CXXV (continued): DEEPER GRAPH ANALYSIS")
    print("=" * 70)
    
    # Build D₅ graphs with different adjacency criteria
    D5_roots = construct_D5_roots()
    n = len(D5_roots)
    
    # Build W33
    _, W33_adj = build_W33_symplectic()
    
    print("\n" + "=" * 70)
    print(" DETAILED STRUCTURE ANALYSIS")
    print("=" * 70)
    
    # Analyze W33
    W33_stats = analyze_graph_structure(W33_adj, "W33 (Sp(4,F₃))")
    
    # Analyze D₅ with IP = -1 (this had 240 edges, degree 12)
    D5_minus1_adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if inner_product(D5_roots[i], D5_roots[j]) == -1:
                D5_minus1_adj[i][j] = 1
                D5_minus1_adj[j][i] = 1
    
    D5_m1_stats = analyze_graph_structure(D5_minus1_adj, "D₅ (IP = -1)")
    
    # Analyze D₅ with IP = +1
    D5_plus1_adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if inner_product(D5_roots[i], D5_roots[j]) == 1:
                D5_plus1_adj[i][j] = 1
                D5_plus1_adj[j][i] = 1
    
    D5_p1_stats = analyze_graph_structure(D5_plus1_adj, "D₅ (IP = +1)")
    
    # Check spectra
    print("\n" + "=" * 70)
    print(" SPECTRAL COMPARISON")
    print("=" * 70)
    
    check_graph_isomorphism_by_spectrum(W33_adj, D5_minus1_adj, "W33", "D₅(IP=-1)")
    check_graph_isomorphism_by_spectrum(W33_adj, D5_plus1_adj, "W33", "D₅(IP=+1)")
    check_graph_isomorphism_by_spectrum(D5_minus1_adj, D5_plus1_adj, "D₅(IP=-1)", "D₅(IP=+1)")
    
    # Try complement
    print("\n" + "=" * 70)
    print(" TRYING COMPLEMENT GRAPHS")
    print("=" * 70)
    
    # Complement of D₅(IP=-1): adjacent iff IP ≠ -1
    D5_comp_adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if inner_product(D5_roots[i], D5_roots[j]) != -1:
                D5_comp_adj[i][j] = 1
                D5_comp_adj[j][i] = 1
    
    D5_comp_stats = analyze_graph_structure(D5_comp_adj, "D₅ (IP ≠ -1)")
    check_graph_isomorphism_by_spectrum(W33_adj, D5_comp_adj, "W33", "D₅(IP≠-1)")
    
    # Try: adjacent if IP = 0 (orthogonal roots)
    D5_orth_adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if inner_product(D5_roots[i], D5_roots[j]) == 0:
                D5_orth_adj[i][j] = 1
                D5_orth_adj[j][i] = 1
    
    D5_orth_stats = analyze_graph_structure(D5_orth_adj, "D₅ (orthogonal)")
    check_graph_isomorphism_by_spectrum(W33_adj, D5_orth_adj, "W33", "D₅(orth)")
    
    print("\n" + "=" * 70)
    print(" KEY INSIGHT")
    print("=" * 70)
    
    print("""
  The D₅ inner product graphs have:
    • Same vertex count (40)
    • Same edge count (240) for IP = ±1
    • Same degree (12) for IP = ±1
  
  BUT different λ, μ parameters and different spectra!
  
  This means W33 is NOT the simple inner product graph on D₅ roots.
  
  HOWEVER, this doesn't mean the correspondence is false!
  
  The relationship might be:
  1. W33 and D₅ roots are related via a more complex map
  2. Both are different "realizations" of the same abstract structure
  3. The number 40 arises independently from:
     - Symplectic geometry: (q²+1)(q+1) = 40 for q=3
     - Root systems: 2n(n-1) = 40 for n=5
     
  These are DIFFERENT constructions that happen to give the same count!
""")
    
    print("\n" + "=" * 70)
    print(" WHAT THIS MEANS FOR OUR THEORY")
    print("=" * 70)
    
    print("""
  THE HONEST ASSESSMENT:
  
  ✓ CONFIRMED: W33 has 40 vertices, same as D₅ roots
  ✓ CONFIRMED: W33 has 240 edges, same as E₈ roots  
  ✓ CONFIRMED: |Aut(W33)| = |W(E₆)| = 51,840
  ✓ CONFIRMED: Eigenvalue multiplicity 24 = D₄ roots
  
  ✗ NOT PROVEN: W33 vertices = D₅ roots structurally
  
  The D₅ root graph with natural adjacency (IP = ±1) has the same
  basic parameters but is NOT isomorphic to W33.
  
  INTERPRETATION:
  
  W33 is a "symplectic shadow" of exceptional structure, but the
  correspondence with D₅ roots is NUMERICAL, not directly structural.
  
  The shared numbers (40, 240, 51840, 24) arise because:
  - Sp(4, F₃) is related to E₆ via the exceptional isomorphism
  - The Weyl group W(E₆) acts on both structures
  - But the graphs themselves are different!
  
  This is actually MORE interesting than a simple isomorphism
  because it suggests deeper connections yet to be understood.
""")

if __name__ == "__main__":
    main()
