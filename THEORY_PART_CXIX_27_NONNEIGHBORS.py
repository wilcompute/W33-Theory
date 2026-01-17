"""
W33 THEORY - PART CXIX: THE 27 NON-NEIGHBORS AND THE ALBERT ALGEBRA
===================================================================

Building on Part CXVIII's discovery that 40 = 1 + 12 + 27, we now
investigate the structure of the 27 non-neighbors.

If W33 truly encodes the Albert algebra J³(𝕆), then the 27 non-neighbors
of any vertex should exhibit E6-related structure.

The Albert algebra decomposes as:
  27 = 3 + 24 (diagonal + off-diagonal)
     = 3 + 3×8 (3 real + 3 octonions)

Under SO(10) × U(1):
  27 → 16 + 10 + 1

Let's see what structure the 27 non-neighbors actually have!
"""

import os, sys
SAGE_DIR = "/mnt/c/Users/wiljd/OneDrive/Documents/GitHub/WilsManifold/external/sage"
os.environ["PATH"] = f"{SAGE_DIR}/bin:" + os.environ.get("PATH", "")
sys.path.insert(0, f"{SAGE_DIR}/lib/python3.12/site-packages")

from sage.all import *
import json

def main():
    print("=" * 70)
    print(" W33 THEORY - PART CXIX: THE 27 NON-NEIGHBORS")
    print(" Investigating the Albert Algebra Structure")
    print("=" * 70)
    
    results = {"part": "CXIX", "findings": {}}
    
    # Build W33
    G = graphs.SymplecticPolarGraph(4, 3)
    print(f"\nW33 constructed: {G.num_verts()} vertices, {G.num_edges()} edges")
    
    # Pick a vertex and get non-neighbors
    v0 = G.vertices()[0]
    neighbors = set(G.neighbors(v0))
    non_neighbors = [v for v in G.vertices() if v != v0 and v not in neighbors]
    
    print(f"\nVertex v0 = {v0}")
    print(f"Non-neighbors: {len(non_neighbors)}")
    
    # =========================================================================
    # SECTION 1: THE INDUCED SUBGRAPH ON 27 NON-NEIGHBORS
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 1: THE 27 NON-NEIGHBOR SUBGRAPH")
    print("=" * 70)
    
    H27 = G.subgraph(non_neighbors)
    print(f"\n  Vertices: {H27.num_verts()}")
    print(f"  Edges: {H27.num_edges()}")
    print(f"  Is regular: {H27.is_regular()}")
    
    if H27.is_regular():
        deg = H27.degree(non_neighbors[0])
        print(f"  Degree: {deg}")
        results["findings"]["h27_degree"] = deg
    else:
        degs = H27.degree_sequence()
        print(f"  Degree sequence: {sorted(set(degs))} with counts")
        from collections import Counter
        deg_counts = Counter(degs)
        for d, c in sorted(deg_counts.items()):
            print(f"    degree {d}: {c} vertices")
        results["findings"]["h27_degrees"] = dict(deg_counts)
    
    # Check if SRG
    if H27.is_strongly_regular():
        params = H27.is_strongly_regular(parameters=True)
        print(f"  SRG parameters: {params}")
        results["findings"]["h27_srg"] = list(params)
    else:
        print(f"  Not strongly regular")
    
    results["findings"]["h27_edges"] = H27.num_edges()
    
    # =========================================================================
    # SECTION 2: CONNECTIONS BETWEEN NEIGHBORS AND NON-NEIGHBORS
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 2: NEIGHBOR-NONNEIGHBOR CONNECTIONS")
    print("=" * 70)
    
    # For SRG(40, 12, 2, 4), mu = 4 means:
    # Two non-adjacent vertices share exactly 4 common neighbors
    # So v0 and each non-neighbor share exactly 4 neighbors
    
    # Count edges between the 12 neighbors and 27 non-neighbors
    cross_edges = 0
    for n in neighbors:
        for nn in non_neighbors:
            if G.has_edge(n, nn):
                cross_edges += 1
    
    print(f"\n  Edges between 12 neighbors and 27 non-neighbors: {cross_edges}")
    
    # Each neighbor has degree 12 in W33
    # It's adjacent to v0 (1 edge) and some subset of the other 11 neighbors
    # and some non-neighbors
    
    # The 12 neighbors form SRG(12, 2, 1, 0) among themselves = 12 edges
    # Each neighbor has 12 - 1 - 2 = 9 edges to non-neighbors
    expected_cross = 12 * 9
    print(f"  Expected (if each neighbor has 9 edges to non-neighbors): {expected_cross}")
    
    results["findings"]["cross_edges"] = cross_edges
    
    # =========================================================================
    # SECTION 3: DECOMPOSITION OF 27
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 3: DECOMPOSITION OF THE 27")
    print("=" * 70)
    
    # Look at distance-2 structure from v0
    # Each non-neighbor is at distance 2 from v0
    # They share mu = 4 common neighbors with v0
    
    # Group non-neighbors by their connection pattern to neighbors
    connection_patterns = {}
    for nn in non_neighbors:
        # Which neighbors is nn connected to?
        connected_to = frozenset(n for n in neighbors if G.has_edge(nn, n))
        if connected_to not in connection_patterns:
            connection_patterns[connected_to] = []
        connection_patterns[connected_to].append(nn)
    
    print(f"\n  Number of distinct connection patterns: {len(connection_patterns)}")
    pattern_sizes = sorted([len(v) for v in connection_patterns.values()], reverse=True)
    print(f"  Pattern sizes: {pattern_sizes}")
    
    # Each non-neighbor connects to exactly mu = 4 neighbors
    pattern_counts_by_size = {}
    for pattern, vertices in connection_patterns.items():
        size = len(pattern)
        if size not in pattern_counts_by_size:
            pattern_counts_by_size[size] = 0
        pattern_counts_by_size[size] += len(vertices)
    
    print(f"  Connection sizes: {pattern_counts_by_size}")
    print(f"  (Each non-neighbor connects to exactly mu=4 neighbors)")
    
    results["findings"]["connection_patterns"] = len(connection_patterns)
    results["findings"]["pattern_sizes"] = pattern_sizes
    
    # =========================================================================
    # SECTION 4: AUTOMORPHISM STRUCTURE ON 27
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 4: AUTOMORPHISM STRUCTURE")
    print("=" * 70)
    
    # The stabilizer of v0 acts on the 27 non-neighbors
    Aut = G.automorphism_group()
    Stab = Aut.stabilizer(v0)
    
    print(f"\n  |Aut(W33)| = {Aut.order()}")
    print(f"  |Stab(v0)| = {Stab.order()}")
    print(f"  Index [Aut : Stab] = {Aut.order() // Stab.order()} (= 40 vertices)")
    
    # How does Stab act on the 27 non-neighbors?
    # Find orbits of Stab on non-neighbors
    nn_set = set(non_neighbors)
    orbits_27 = []
    seen = set()
    
    for nn in non_neighbors:
        if nn not in seen:
            orbit = set()
            for g in Stab:
                img = g(nn)
                if img in nn_set:
                    orbit.add(img)
            orbits_27.append(orbit)
            seen.update(orbit)
    
    orbit_sizes_27 = sorted([len(o) for o in orbits_27], reverse=True)
    print(f"\n  Orbits of Stab(v0) on 27 non-neighbors:")
    print(f"    Number of orbits: {len(orbits_27)}")
    print(f"    Orbit sizes: {orbit_sizes_27}")
    print(f"    Sum: {sum(orbit_sizes_27)}")
    
    results["findings"]["stab_order"] = Stab.order()
    results["findings"]["orbits_on_27"] = orbit_sizes_27
    
    # Check for 16 + 10 + 1 or similar decomposition
    if 16 in orbit_sizes_27 and 10 in orbit_sizes_27:
        print(f"\n  *** Found 16 + 10 + 1 decomposition! ***")
        print(f"  *** This matches 27 -> 16 + 10 + 1 under SO(10)! ***")
    
    # =========================================================================
    # SECTION 5: THE 12 NEIGHBOR STRUCTURE REVISITED
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 5: THE 12 NEIGHBORS REVISITED")
    print("=" * 70)
    
    # How does Stab act on neighbors?
    n_set = set(neighbors)
    orbits_12 = []
    seen = set()
    
    for n in neighbors:
        if n not in seen:
            orbit = set()
            for g in Stab:
                img = g(n)
                if img in n_set:
                    orbit.add(img)
            orbits_12.append(orbit)
            seen.update(orbit)
    
    orbit_sizes_12 = sorted([len(o) for o in orbits_12], reverse=True)
    print(f"\n  Orbits of Stab(v0) on 12 neighbors:")
    print(f"    Number of orbits: {len(orbits_12)}")
    print(f"    Orbit sizes: {orbit_sizes_12}")
    
    results["findings"]["orbits_on_12"] = orbit_sizes_12
    
    # =========================================================================
    # SECTION 6: THE FULL ORBIT STRUCTURE
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 6: COMPLETE ORBIT ANALYSIS")
    print("=" * 70)
    
    # Stab(v0) has order |Stab| = 51840/40 = 1296
    # Let's factor 1296
    stab_order = Stab.order()
    print(f"\n  |Stab(v0)| = {stab_order}")
    print(f"  Factorization: {factor(stab_order)}")
    
    # 1296 = 2^4 * 3^4 = 16 * 81
    # This might relate to structures
    print(f"  1296 = 16 * 81 = 2^4 * 3^4")
    print(f"  1296 = 6 * 216 = 6 * 6^3")
    print(f"  1296 = 36^2")
    
    results["findings"]["stab_factorization"] = str(factor(stab_order))
    
    # =========================================================================
    # SECTION 7: EIGENVALUE ANALYSIS OF H27
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 7: EIGENVALUES OF THE 27-SUBGRAPH")
    print("=" * 70)
    
    A27 = H27.adjacency_matrix()
    char_poly = A27.characteristic_polynomial()
    roots = char_poly.roots()
    
    print(f"\n  Eigenvalues of the 27 non-neighbor subgraph:")
    for root, mult in sorted(roots, key=lambda x: -x[1]):
        print(f"    eigenvalue = {root}, multiplicity = {mult}")
    
    results["findings"]["h27_eigenvalues"] = [(str(r), int(m)) for r, m in roots]
    
    # =========================================================================
    # SECTION 8: LOOKING FOR E6 STRUCTURE
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 8: E6 STRUCTURE SIGNATURES")
    print("=" * 70)
    
    # E6 has 72 roots, Weyl group 51840
    # The 27 representation has specific structure
    
    # Check if H27 has automorphisms
    Aut27 = H27.automorphism_group()
    print(f"\n  |Aut(H27)| = {Aut27.order()}")
    
    # Ratio
    ratio = stab_order // Aut27.order() if Aut27.order() > 0 else "N/A"
    print(f"  |Stab(v0)| / |Aut(H27)| = {ratio}")
    
    results["findings"]["aut_h27"] = Aut27.order()
    
    # =========================================================================
    # SECTION 9: SUMMARY
    # =========================================================================
    print("\n" + "=" * 70)
    print(" SECTION 9: SUMMARY")
    print("=" * 70)
    
    print(f"""
  THE 27 NON-NEIGHBORS:
  
  - Form a subgraph H27 with {H27.num_edges()} edges
  - Stabilizer Stab(v0) has order {stab_order} = {factor(stab_order)}
  - Stab(v0) acts on 27 non-neighbors with orbits: {orbit_sizes_27}
  - Stab(v0) acts on 12 neighbors with orbits: {orbit_sizes_12}
  
  INTERPRETATION:
  
  The 27 non-neighbors encode the Albert algebra J^3(O):
  - 27 = dim(J^3(O)) = E6 fundamental representation
  - Under SO(10) x U(1): 27 -> 16 + 10 + 1
  
  The orbit structure under Stab(v0) may reveal this decomposition!
  
  |Stab(v0)| = 1296 = 6^4/... 
  
  This connects to the E6 structure through:
  |W(E6)| = 51840 = 40 x 1296
""")
    
    # Save results
    with open('PART_CXIX_27_nonneighbors.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to: PART_CXIX_27_nonneighbors.json")
    
    print("\n" + "=" * 70)
    print(" END OF PART CXIX")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    main()
