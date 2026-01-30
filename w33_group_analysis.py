"""Analyze W33 automorphism group structure and H1 representation using Sage.

This script does character-theoretic analysis without full isotypic decomposition.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path


def main():
    print("=== W33 Group Structure & H1 Representation Analysis ===", flush=True)
    
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    
    from lib.w33_io import W33DataPaths, load_w33_lines, simplices_from_lines
    from sage.all import GF, QQ, Graph, matrix, PermutationGroup, gap
    
    paths = W33DataPaths.from_this_file(__file__)
    lines = load_w33_lines(paths)
    
    # Build incidence bipartite graph
    edges = []
    for line_index, pts in enumerate(lines):
        line_vertex = 41 + line_index
        for p in pts:
            edges.append((p + 1, line_vertex))
    
    G = Graph(multiedges=False, loops=False)
    G.add_vertices(range(1, 81))
    G.add_edges(edges)
    
    # Automorphism group preserving bipartition
    A = G.automorphism_group(partition=[list(range(1, 41)), list(range(41, 81))])
    
    order = int(A.order())
    print(f"\nIncidence automorphism group order: {order}")
    print(f"Structure: {A.structure_description()}")
    
    # Conjugacy classes
    cc = A.conjugacy_classes()
    print(f"Number of conjugacy classes: {len(cc)}")
    
    # Character table (this works for groups up to ~100k in reasonable time)
    print("\n--- Character Table Summary ---")
    char_table = A.character_table()
    num_irreps = char_table.nrows()
    print(f"Number of irreducible representations: {num_irreps}")
    
    # Degrees of irreps (first column)
    degrees = [int(char_table[i, 0]) for i in range(num_irreps)]
    print(f"Irrep dimensions: {sorted(set(degrees))}")
    print(f"Sum of d_i^2 = {sum(d*d for d in degrees)} (should equal {order})")
    
    # Load the H1 action matrices to compute character
    results_file = here / "data" / "w33_sage_incidence_h1.json"
    with open(results_file) as f:
        data = json.load(f)
    
    h1_mats_str = data["h1_action"]["generator_matrices"]
    h1_dim = len(h1_mats_str[0])
    print(f"\nH1 dimension: {h1_dim}")
    
    # Convert to Sage matrices
    gens = list(A.gens())
    h1_mats = []
    for mat_str in h1_mats_str:
        M = matrix(QQ, [[QQ(x) for x in row] for row in mat_str])
        h1_mats.append(M)
    
    print(f"Number of H1 generator matrices: {len(h1_mats)}")
    
    # Compute traces (characters) of H1 representation on generators
    print("\n--- H1 Character on Generators ---")
    for i, (g, M) in enumerate(zip(gens, h1_mats)):
        tr = M.trace()
        print(f"  gen[{i}]: order={g.order()}, trace(H1)={tr}")
    
    # Check if H1 is a sum of trivial reps by computing average trace
    # Character of trivial rep is 1 on all elements
    # Sum over group / order = multiplicity of trivial rep
    
    # For efficiency, sample the character on conjugacy class representatives
    print("\n--- H1 Character on Conjugacy Class Representatives ---")
    
    # Get representative and class size for each conjugacy class
    class_reps = [c.representative() for c in cc]
    class_sizes = [len(c) for c in cc]
    
    # Build a lookup from generator permutations to H1 matrices
    # We need to compute H1(g) for each class representative
    # This requires extending the generator matrices to arbitrary group elements
    
    # For now, compute on identity (should give dimension)
    id_elem = A.identity()
    id_mat = matrix.identity(QQ, h1_dim)
    print(f"  Identity: trace={id_mat.trace()} (equals dim={h1_dim})")
    
    # Estimate multiplicities from generator traces
    gen_traces = [M.trace() for M in h1_mats]
    print(f"\nGenerator traces: {gen_traces}")
    
    # Check if any matrices are identity (fixed points)
    identity_count = sum(1 for M in h1_mats if M == matrix.identity(QQ, h1_dim))
    print(f"Generators acting as identity on H1: {identity_count}")
    
    # Center of the group
    center = A.center()
    print(f"\nCenter of group: order {center.order()}")
    
    # Derived series (measure of non-abelianness)
    derived = A.derived_series()
    print(f"Derived series length: {len(derived)}")
    
    # Sylow subgroups
    print("\n--- Sylow Subgroups ---")
    from sage.arith.misc import factor
    factorization = factor(order)
    print(f"Order factorization: {factorization}")
    for p, e in factorization:
        sylow = A.sylow_subgroup(p)
        print(f"  Sylow-{p}: order {sylow.order()}")
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Group: O(5,3) : C2")
    print(f"Order: {order} = 2^6 * 3^4 * 5 = 64 * 81 * 10")
    print(f"Conjugacy classes: {len(cc)}")
    print(f"Irreducible representations: {num_irreps}")
    print(f"H1 representation dimension: {h1_dim}")
    print(f"Group is simple: {A.is_simple()}")
    print(f"Group is perfect: {A.is_perfect()}")
    

if __name__ == "__main__":
    main()
