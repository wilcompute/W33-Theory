
#!/usr/bin/env sage
"""
Construct W33 = SRG(40, 12, 2, 4) from Sp(4, F_3)
"""

print("=" * 60)
print("CONSTRUCTING W33 FROM Sp(4, F_3)")
print("=" * 60)

# =====================================================
# METHOD 1: Direct SRG construction (if available)
# =====================================================
print("\nMETHOD 1: Built-in SRG construction")
print("-" * 40)

try:
    # SageMath has built-in strongly regular graphs
    from sage.graphs.strongly_regular_db import strongly_regular_graph
    
    # SRG(40, 12, 2, 4) - this is our W33!
    G = strongly_regular_graph(40, 12, 2, 4)
    print(f"Graph constructed: {G}")
    print(f"  Vertices: {G.order()}")
    print(f"  Edges: {G.size()}")
    print(f"  Is strongly regular: {G.is_strongly_regular()}")
    
    # Get parameters
    params = G.is_strongly_regular(parameters=True)
    print(f"  Parameters (v,k,λ,μ): {params}")
    
except Exception as e:
    print(f"Method 1 failed: {e}")
    G = None

# =====================================================
# METHOD 2: Symplectic construction from Sp(4, F_3)
# =====================================================
print("\nMETHOD 2: Symplectic construction from Sp(4, F_3)")
print("-" * 40)

try:
    from sage.all import *
    
    # The finite field F_3
    F3 = GF(3)
    print(f"Field: F_3 = {list(F3)}")
    
    # The 4-dimensional vector space over F_3
    V = VectorSpace(F3, 4)
    print(f"Vector space: F_3^4 has {V.cardinality()} elements")
    
    # The symplectic form: omega(u, v) = u_1*v_2 - u_2*v_1 + u_3*v_4 - u_4*v_3
    def symplectic_form(u, v):
        return u[0]*v[1] - u[1]*v[0] + u[2]*v[3] - u[3]*v[2]
    
    # A vector is isotropic if omega(v, v) = 0 (always true for symplectic)
    # A 1-dimensional subspace (line) is isotropic if all its vectors are
    
    # Get all nonzero vectors
    nonzero_vecs = [v for v in V if v != V.zero()]
    print(f"Nonzero vectors: {len(nonzero_vecs)}")
    
    # Group vectors by the lines they span
    # Two vectors span the same line if one is a nonzero scalar multiple of the other
    lines = []
    used = set()
    
    for v in nonzero_vecs:
        v_tuple = tuple(v)
        if v_tuple not in used:
            line = set()
            for scalar in F3:
                if scalar != 0:
                    sv = scalar * v
                    line.add(tuple(sv))
                    used.add(tuple(sv))
            lines.append(frozenset(line))
    
    print(f"Total 1-dimensional subspaces (lines): {len(lines)}")
    
    # Check which lines are isotropic
    # An isotropic line is one where all vectors satisfy omega(v, v) = 0
    # For a symplectic form, omega(v, v) = 0 for all v (antisymmetric)
    # But the relevant condition for our graph is different...
    
    # Actually, for the symplectic graph, two lines are adjacent if
    # their span is a 2-dimensional isotropic subspace
    
    # A 2-dimensional subspace is isotropic if omega(u, v) = 0 for all u, v in it
    
    def is_isotropic_pair(v1, v2):
        """Check if span(v1, v2) is isotropic"""
        return symplectic_form(v1, v2) == 0
    
    # Build adjacency: two lines are adjacent if they span an isotropic 2-space
    line_list = list(lines)
    n = len(line_list)
    
    adj_matrix = matrix(ZZ, n, n, 0)
    
    for i in range(n):
        for j in range(i+1, n):
            # Get representative vectors from each line
            v1 = vector(F3, list(list(line_list[i])[0]))
            v2 = vector(F3, list(list(line_list[j])[0]))
            
            if is_isotropic_pair(v1, v2):
                adj_matrix[i, j] = 1
                adj_matrix[j, i] = 1
    
    # Create graph from adjacency matrix
    G_symplectic = Graph(adj_matrix)
    
    print(f"\nSymplectic graph constructed:")
    print(f"  Vertices: {G_symplectic.order()}")
    print(f"  Edges: {G_symplectic.size()}")
    
    # Check if strongly regular
    srg_params = G_symplectic.is_strongly_regular(parameters=True)
    if srg_params:
        print(f"  Is strongly regular: Yes")
        print(f"  Parameters (v,k,λ,μ): {srg_params}")
    else:
        print(f"  Is strongly regular: No")
    
except Exception as e:
    print(f"Method 2 failed: {e}")
    import traceback
    traceback.print_exc()

# =====================================================
# METHOD 3: Using Sage's built-in symplectic graph
# =====================================================
print("\nMETHOD 3: Sage's SymplecticGraph function")
print("-" * 40)

try:
    from sage.graphs.graph_generators import graphs
    
    # SymplecticGraph(d, q) gives the graph on 1-dim subspaces of F_q^(2d)
    # adjacent if orthogonal under symplectic form
    
    # For d=2, q=3: gives graph on F_3^4
    G_sage_symp = graphs.SymplecticGraph(2, 3)
    
    print(f"Symplectic graph Sp(2,3):")
    print(f"  Vertices: {G_sage_symp.order()}")
    print(f"  Edges: {G_sage_symp.size()}")
    
    srg_params = G_sage_symp.is_strongly_regular(parameters=True)
    if srg_params:
        print(f"  Is strongly regular: Yes")
        print(f"  Parameters: {srg_params}")
    
except Exception as e:
    print(f"Method 3 failed: {e}")

# =====================================================
# COMPUTE EIGENVALUES
# =====================================================
print("\n" + "=" * 60)
print("EIGENVALUE ANALYSIS")
print("=" * 60)

try:
    if G is not None:
        A = G.adjacency_matrix()
        eigenvalues = A.eigenvalues()
        
        # Count multiplicities
        from collections import Counter
        ev_counts = Counter([float(e) for e in eigenvalues])
        
        print("\nEigenvalues and multiplicities:")
        for ev, mult in sorted(ev_counts.items(), key=lambda x: -x[1]):
            print(f"  e = {ev:6.2f}  multiplicity = {mult}")
        
        # Verify they match expected
        print("\nExpected: e1=12 (×1), e2=2 (×24), e3=-4 (×15)")
        
except Exception as e:
    print(f"Eigenvalue analysis failed: {e}")

# =====================================================
# AUTOMORPHISM GROUP
# =====================================================
print("\n" + "=" * 60)
print("AUTOMORPHISM GROUP")
print("=" * 60)

try:
    if G is not None:
        aut = G.automorphism_group()
        print(f"\nAutomorphism group:")
        print(f"  Order: |Aut(W33)| = {aut.order()}")
        print(f"  Expected: 51840")
        
        # Factor the order
        n = aut.order()
        print(f"\n  Factorization: {factor(n)}")
        
        # Group structure
        print(f"  Is solvable: {aut.is_solvable()}")
        
except Exception as e:
    print(f"Automorphism analysis failed: {e}")

# =====================================================
# VERIFY THE ALPHA FORMULA
# =====================================================
print("\n" + "=" * 60)
print("PHYSICS FROM GRAPH THEORY")
print("=" * 60)

try:
    if G is not None:
        v_param, k_param, lam, mu = G.is_strongly_regular(parameters=True)
        
        print(f"\nW33 parameters verified from graph:")
        print(f"  v = {v_param}")
        print(f"  k = {k_param}")
        print(f"  λ = {lam}")
        print(f"  μ = {mu}")
        
        # The alpha formula
        alpha_inv_base = k_param**2 - 2*mu + 1
        denom = (k_param - 1) * ((k_param - lam)**2 + 1)
        alpha_inv = alpha_inv_base + v_param / denom
        
        print(f"\nFine structure constant formula:")
        print(f"  α⁻¹ = k² - 2μ + 1 + v/[(k-1)×((k-λ)²+1)]")
        print(f"  α⁻¹ = {alpha_inv_base} + {v_param}/{denom}")
        print(f"  α⁻¹ = {float(alpha_inv):.10f}")
        print(f"  Experimental: 137.035999084")
        
except Exception as e:
    print(f"Physics verification failed: {e}")

# =====================================================
# GRAPH PROPERTIES
# =====================================================
print("\n" + "=" * 60)
print("ADDITIONAL GRAPH PROPERTIES")
print("=" * 60)

try:
    if G is not None:
        print(f"\nGraph metrics:")
        print(f"  Diameter: {G.diameter()}")
        print(f"  Girth: {G.girth()}")
        print(f"  Chromatic number: {G.chromatic_number()}")
        print(f"  Clique number: {G.clique_number()}")
        print(f"  Independence number: {G.independent_set(value_only=True)}")
        
except Exception as e:
    print(f"Graph properties failed: {e}")

print("\n" + "=" * 60)
print("W33 GRAPH CONSTRUCTION COMPLETE")
print("=" * 60)
