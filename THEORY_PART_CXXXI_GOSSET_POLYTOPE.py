#!/usr/bin/env python3
"""
THEORY PART CXXXI: THE GOSSET POLYTOPE AND E8

The Gosset polytope 4_21 is a uniform polytope in 8 dimensions with:
- 240 vertices (= E8 roots = Witting polytope vertices!)
- 6720 edges
- Symmetry group = W(E8) with order 696,729,600

The 240 vertices of Gosset ARE the E8 roots!

This connects:
E8 roots = Gosset 4_21 vertices = Witting polytope vertices

Let's explore the full descent:

E8 (240) → E7 (126) → E6 (72) → D5 (40) → D4 (24) → ...

And the corresponding polytopes:
Gosset 4_21 → Gosset 3_21 → Gosset 2_21 → ...
"""

import numpy as np
from itertools import combinations, product
from collections import defaultdict

def build_e8_roots():
    """Build all 240 E8 roots."""
    roots = []
    
    # Type 1: (±1, ±1, 0, 0, 0, 0, 0, 0) permutations - 112 roots
    for i in range(8):
        for j in range(i+1, 8):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    root = np.zeros(8)
                    root[i] = s1
                    root[j] = s2
                    roots.append(root)
    
    # Type 2: (±1/2)^8 with even number of minus signs - 128 roots
    for signs in product([1, -1], repeat=8):
        if sum(1 for s in signs if s == -1) % 2 == 0:
            root = np.array(signs) / 2
            roots.append(root)
    
    return np.array(roots)

def build_e7_roots(e8_roots):
    """
    E7 ⊂ E8: roots with x7 + x8 = 0 (in some conventions)
    Actually: E7 roots are E8 roots perpendicular to a fixed E8 root.
    
    E7 has 126 roots.
    """
    # E7 is the subsystem perpendicular to a fixed E8 root
    # Choose root r = (1,1,0,0,0,0,0,0)
    r = np.array([1, 1, 0, 0, 0, 0, 0, 0])
    
    e7_roots = []
    for root in e8_roots:
        if np.abs(np.dot(root, r)) < 1e-10:  # perpendicular to r
            e7_roots.append(root)
    
    return np.array(e7_roots)

def build_e6_roots(e8_roots):
    """
    E6 ⊂ E8: roots perpendicular to TWO independent roots.
    
    E6 has 72 roots.
    """
    r1 = np.array([1, 1, 0, 0, 0, 0, 0, 0])
    r2 = np.array([0, 0, 0, 0, 0, 0, 1, 1])
    
    e6_roots = []
    for root in e8_roots:
        if np.abs(np.dot(root, r1)) < 1e-10 and np.abs(np.dot(root, r2)) < 1e-10:
            e6_roots.append(root)
    
    return np.array(e6_roots)

def build_d5_roots():
    """
    D5 roots: (±1, ±1, 0, 0, 0) permutations in 5D.
    Total: C(5,2) * 4 = 10 * 4 = 40 roots.
    """
    roots = []
    for i in range(5):
        for j in range(i+1, 5):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    root = np.zeros(5)
                    root[i] = s1
                    root[j] = s2
                    roots.append(root)
    return np.array(roots)

def build_d4_roots():
    """D4 roots: 24 roots in 4D."""
    roots = []
    for i in range(4):
        for j in range(i+1, 4):
            for s1 in [1, -1]:
                for s2 in [1, -1]:
                    root = np.zeros(4)
                    root[i] = s1
                    root[j] = s2
                    roots.append(root)
    return np.array(roots)

def analyze_root_system_graph(roots, name, threshold=1.0):
    """
    Build graph where roots are adjacent if their inner product equals threshold.
    """
    n = len(roots)
    edges = []
    
    for i in range(n):
        for j in range(i+1, n):
            ip = np.dot(roots[i], roots[j])
            if np.abs(ip - threshold) < 1e-10:
                edges.append((i, j))
    
    # Build adjacency
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    
    degrees = [len(adj[i]) for i in range(n)]
    
    print(f"\n{name} graph (IP = {threshold}):")
    print(f"  Vertices: {n}")
    print(f"  Edges: {len(edges)}")
    print(f"  Degree: {set(degrees)}")
    
    if len(set(degrees)) == 1:
        k = degrees[0]
        
        # Check SRG parameters
        lambda_vals = set()
        for i, j in edges:
            lambda_vals.add(len(adj[i] & adj[j]))
        
        mu_vals = set()
        for i in range(n):
            for j in range(i+1, n):
                if j not in adj[i]:
                    mu_vals.add(len(adj[i] & adj[j]))
        
        print(f"  λ values: {lambda_vals}")
        print(f"  μ values: {mu_vals}")
        
        if len(lambda_vals) == 1 and len(mu_vals) == 1:
            print(f"  *** SRG({n}, {k}, {list(lambda_vals)[0]}, {list(mu_vals)[0]}) ***")
    
    return edges, adj

def explore_gosset_structure():
    """Explore the Gosset polytope and E8 root system."""
    print("="*70)
    print("GOSSET POLYTOPE AND ROOT SYSTEM HIERARCHY")
    print("="*70)
    
    e8_roots = build_e8_roots()
    print(f"\nE8: {len(e8_roots)} roots")
    
    e7_roots = build_e7_roots(e8_roots)
    print(f"E7: {len(e7_roots)} roots")
    
    e6_roots = build_e6_roots(e8_roots)
    print(f"E6: {len(e6_roots)} roots")
    
    d5_roots = build_d5_roots()
    print(f"D5: {len(d5_roots)} roots")
    
    d4_roots = build_d4_roots()
    print(f"D4: {len(d4_roots)} roots")
    
    print("\n" + "-"*50)
    print("ROOT SYSTEM INNER PRODUCT GRAPHS")
    print("-"*50)
    
    # Analyze D5 graph with IP = 1
    analyze_root_system_graph(d5_roots, "D5", threshold=1.0)
    
    # Analyze D5 graph with IP = -1
    analyze_root_system_graph(d5_roots, "D5", threshold=-1.0)
    
    # Analyze D4 graph
    analyze_root_system_graph(d4_roots, "D4", threshold=1.0)
    
    print("\n" + "-"*50)
    print("E8 INNER PRODUCTS")
    print("-"*50)
    
    # What inner products appear in E8?
    ip_counts = defaultdict(int)
    for i in range(len(e8_roots)):
        for j in range(i+1, len(e8_roots)):
            ip = np.dot(e8_roots[i], e8_roots[j])
            ip_counts[round(ip, 4)] += 1
    
    print("E8 root inner products:")
    for ip, count in sorted(ip_counts.items()):
        print(f"  {ip}: {count} pairs")
    
    return e8_roots, e7_roots, e6_roots, d5_roots, d4_roots

def the_gosset_adjacency():
    """
    The Gosset 4_21 polytope has 240 vertices (E8 roots).
    What is its edge structure?
    
    In the Gosset polytope, two vertices are adjacent iff
    their inner product is 1 (for unit-length roots).
    
    For E8 roots of squared length 2, adjacent means IP = 1.
    """
    print("\n" + "="*70)
    print("GOSSET 4_21 POLYTOPE EDGE STRUCTURE")
    print("="*70)
    
    e8_roots = build_e8_roots()
    
    # Count edges (IP = 1)
    edges = []
    for i in range(240):
        for j in range(i+1, 240):
            ip = np.dot(e8_roots[i], e8_roots[j])
            if np.abs(ip - 1) < 1e-10:
                edges.append((i, j))
    
    print(f"\nGosset 4_21 (E8 roots with IP = 1):")
    print(f"  Vertices: 240")
    print(f"  Edges: {len(edges)}")
    print(f"  Expected: 6720 (from polytope theory)")
    
    # Build adjacency
    adj = defaultdict(set)
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    
    degrees = [len(adj[i]) for i in range(240)]
    print(f"  Degree: {set(degrees)}")
    
    # This should be degree 56 (each E8 root has 56 neighbors in Gosset)
    
    # Compare with W33
    print("""
    
    GOSSET vs W33:
    ──────────────
    Gosset 4_21:
    - 240 vertices (E8 roots)
    - 6720 edges
    - Degree 56
    - Not strongly regular (various IP values)
    
    W33:
    - 40 vertices (Witting rays = E8/6)
    - 240 edges
    - Degree 12
    - Strongly regular SRG(40, 12, 2, 4)
    
    The 240 E8 roots quotient to 40 Witting rays.
    The Gosset adjacency does NOT directly become W33 adjacency!
    
    Instead:
    - W33 adjacency = orthogonality in C^4
    - Gosset adjacency = IP = 1 in R^8
    
    These are DIFFERENT relations, but both stem from E8.
    """)

def explore_24_cell():
    """
    The 24-cell is a 4D polytope with:
    - 24 vertices (D4 roots!)
    - 96 edges
    - Symmetry group W(D4) = 1152... wait, that's not right
    
    Actually W(D4) = 192, and the 24-cell symmetry is 1152.
    
    Hmm, W(D4) = 2^3 * 4! = 8 * 24 = 192? No...
    |W(D4)| = 2^3 * 4! = 192
    
    But 24-cell has symmetry group of order 1152 = 192 * 6.
    
    Let's verify our W33 stabilizer claim.
    """
    print("\n" + "="*70)
    print("THE 24-CELL AND D4")
    print("="*70)
    
    d4_roots = build_d4_roots()
    print(f"\nD4 roots: {len(d4_roots)}")
    
    # The 24-cell vertices can be:
    # Type 1: permutations of (±1, 0, 0, 0) - 8 vertices
    # Type 2: (±1/2, ±1/2, ±1/2, ±1/2) - 16 vertices
    # Total: 24 vertices
    
    # But D4 roots are (±1, ±1, 0, 0) permutations
    # That's 24 roots... same count but different!
    
    print("""
    CLARIFICATION:
    
    D4 root system: 24 roots of form (±1, ±1, 0, 0) permutations
    - These are NOT the 24-cell vertices!
    - |W(D4)| = 2^3 × 4!/2 = 8 × 12 = 192 (not 1152!)
    
    Wait, let me recalculate:
    |W(D_n)| = 2^{n-1} × n!
    |W(D4)| = 2^3 × 4! = 8 × 24 = 192
    
    But our stabilizer was 1296...
    |W(E6)|/40 = 51840/40 = 1296
    
    1296 = 2^4 × 3^4 = 16 × 81
    
    Hmm, 1296 is NOT |W(D4)| = 192.
    
    Let me check: 1296 = 6 × 216 = 6 × 6^3
    Or: 1296 = 1296... what factors?
    1296 = 2^4 × 81 = 16 × 81 = 16 × 3^4
    
    Compare to W(F4) = 1152 = 2^7 × 9 = 128 × 9
    
    Actually, the stabilizer in Aut(W33) of a vertex should be
    computed directly, not assumed to be W(D4).
    """)
    
    # Verify stabilizer
    print("\nRECALCULATING STABILIZER:")
    print(f"  |Aut(W33)| = |W(E6)| = 51840")
    print(f"  W33 vertices = 40")
    print(f"  If transitive: stabilizer = 51840/40 = {51840//40}")
    
    # What group has order 1296?
    # 1296 = 2^4 × 3^4
    # |W(B4)| = 2^4 × 4! = 16 × 24 = 384 (no)
    # |S_6| × 2 = 720 × 2 = 1440 (no)
    # 
    # Actually 1296 = 6^4 / 1 = 1296
    # Hmm, 1296 = 36^2... = (6^2)^2 = 6^4... no, 6^4 = 1296 yes!
    
    print(f"\n  1296 = 6^4 = {6**4}")
    print(f"  1296 = 2^4 × 3^4 = {2**4 * 3**4}")
    
    # Interesting: 1296 = |SL(2, F_9)| or related?
    # |SL(2, F_q)| = q(q-1)(q+1) = q^3 - q
    # |SL(2, F_9)| = 9 × 8 × 10 = 720 (no)
    # 
    # How about |Sp(2, F_9)|? 
    # |Sp(2n, F_q)| = q^{n^2} × prod (q^{2i} - 1)
    # |Sp(2, F_q)| = |SL(2, F_q)| = q^3 - q
    
    # 1296 appears in the ATLAS... 
    # It's the order of the group 3^4 : 2.A_4 or similar
    
    print("""
    THE STABILIZER 1296:
    
    The stabilizer of a vertex in Aut(W33) has order 1296.
    
    1296 = 2^4 × 3^4 = (2 × 3)^4 / (36/36) = hmm
    
    One description: The stabilizer is related to the 
    affine group AGL(2, F_3) or similar structure.
    
    AGL(2, F_3) = F_3^2 : GL(2, F_3)
    |GL(2, F_3)| = (9-1)(9-3) = 8 × 6 = 48
    |AGL(2, F_3)| = 9 × 48 = 432
    
    Hmm, 1296 = 3 × 432 = 3 × |AGL(2, F_3)|
    
    Or: 1296 = 27 × 48 = 27 × |GL(2, F_3)|
    
    Interesting: 27 appears again!
    """)

def d5_spinor_connection():
    """
    Explore the D5 spinor representation and its relation to 32.
    
    D5 has two half-spinor representations, each of dimension 16.
    Total spinor dimension: 32 = 16 + 16.
    
    72 (E6 roots) = 40 (D5 roots) + 32 (D5 spinor weights)
    """
    print("\n" + "="*70)
    print("D5 SPINORS AND THE 72 = 40 + 32 DECOMPOSITION")
    print("="*70)
    
    print("""
    D5 REPRESENTATION THEORY:
    
    D5 = SO(10) has:
    - Vector representation: dimension 10
    - Adjoint representation: dimension 45 (= 10 choose 2)
    - Root system: 40 roots
    
    Spinor representations:
    - Two half-spinors: Δ+ and Δ-, each dimension 16
    - Total spinor: dimension 32
    
    E6 BRANCHING:
    
    E6 → D5 branching:
    - E6 adjoint (78) → D5 adjoint (45) + D5 vector (10) + 2×spinor (32) + singlet
    
    Wait, that's: 45 + 10 + 32 + 1 = 88 ≠ 78
    
    Let me reconsider...
    
    E6 has 72 roots.
    D5 has 40 roots.
    
    Under D5 ⊂ E6:
    - 72 E6 roots = 40 D5 roots + 32 other weights
    
    The "32 other" are the weights of the D5 spinor appearing in E6!
    
    VERIFICATION:
    72 = 40 + 32 ✓
    
    This explains our earlier observation that 72 = 40 + 32
    in the context of W33 structure!
    """)
    
    # Build E6 roots and check decomposition
    e8_roots = build_e8_roots()
    
    # E6 ⊂ E8 with constraints
    r1 = np.array([1, 1, 0, 0, 0, 0, 0, 0])
    r2 = np.array([0, 0, 0, 0, 0, 0, 1, 1])
    
    e6_roots = []
    for root in e8_roots:
        if np.abs(np.dot(root, r1)) < 1e-10 and np.abs(np.dot(root, r2)) < 1e-10:
            e6_roots.append(root)
    
    print(f"\nE6 roots (embedded in E8): {len(e6_roots)}")
    
    # D5 ⊂ E6: add another constraint
    # D5 roots in first 5 coordinates (within the E6 constraint)
    
    # Actually, let's just count dimensions
    print("""
    THE DECOMPOSITION:
    
    E6 root system (72 roots)
         ↓
    D5 root system (40 roots) ⊕ D5 spinor weights (32)
    
    In W33/Witting context:
    - 40 vertices = D5 roots = Witting states
    - Each vertex has 27 non-neighbors (= 72 - 40 - some overlap structure)
    
    Hmm, 27 ≠ 32. Let me reconsider...
    
    The 27 non-neighbors per vertex is different from 32 spinor weights.
    
    Actually:
    - 40 W33 vertices total
    - For each vertex: 1 (self) + 12 (neighbors) + 27 (non-neighbors) = 40 ✓
    
    The 27 comes from [W(E6):W(D5)] = 27, not from spinor dimension.
    The 32 comes from D5 spinor in E6 ⊃ D5 embedding.
    
    Different 27 and 32!
    """)

def main():
    """Run all analyses."""
    explore_gosset_structure()
    the_gosset_adjacency()
    explore_24_cell()
    d5_spinor_connection()
    
    print("\n" + "="*70)
    print("SUMMARY: ROOT SYSTEMS AND W33")
    print("="*70)
    print("""
    THE EXCEPTIONAL HIERARCHY:
    
    E8 (240 roots)
    ├── Gosset 4_21 polytope (240 vertices)
    ├── W(E8) has order 696,729,600
    │
    └── E7 (126 roots)
        └── E6 (72 roots)
            ├── W(E6) = Aut(W33), order 51,840
            ├── Schläfli graph: 27 lines on cubic
            │
            └── D5 (40 roots) ← SAME COUNT AS W33!
                ├── W(D5), order 1,920
                ├── Index [W(E6):W(D5)] = 27
                │
                └── D4 (24 roots)
                    └── W(D4), order 192
    
    THE NUMBERS:
    ────────────
    240 = |E8 roots| = |Witting vertices| = |W33 edges|
    126 = |E7 roots|
    72 = |E6 roots| = 40 + 32 (D5 roots + spinor)
    51840 = |W(E6)| = |Aut(W33)|
    40 = |D5 roots| = |W33 vertices|
    27 = [W(E6):W(D5)] = W33 non-neighbors = lines on cubic
    24 = |D4 roots|
    1296 = 51840/40 = W33 vertex stabilizer = 2^4 × 3^4
    """)

if __name__ == "__main__":
    main()
