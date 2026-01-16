"""Verify conjugacy class alignment between our computation and Sage's character table."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def main():
    print("=== Verifying Conjugacy Class Alignment ===", flush=True)
    
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    
    from lib.w33_io import W33DataPaths, load_w33_lines
    from sage.all import QQ, Graph, matrix, gap
    
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
    
    A = G.automorphism_group(partition=[list(range(1, 41)), list(range(41, 81))])
    order = int(A.order())
    
    # Get conjugacy classes from A.conjugacy_classes()
    cc = A.conjugacy_classes()
    
    # Get character table
    char_table = A.character_table()
    
    print(f"Group order: {order}")
    print(f"Number of conjugacy classes: {len(cc)}")
    print(f"Character table shape: {char_table.nrows()} x {char_table.ncols()}")
    
    # The character table columns correspond to conjugacy classes
    # Column 0 is identity class
    
    # Check: first column should all be positive (dimensions)
    print("\n--- First column (dimensions) ---")
    dims = [int(char_table[i, 0]) for i in range(char_table.nrows())]
    print(f"Dimensions: {dims}")
    print(f"Sum of d^2: {sum(d*d for d in dims)}")
    
    # Check class sizes match
    print("\n--- Conjugacy class sizes ---")
    class_sizes_from_cc = [len(c) for c in cc]
    print(f"From conjugacy_classes(): {class_sizes_from_cc}")
    print(f"Sum: {sum(class_sizes_from_cc)}")
    
    # Use GAP to get the class sizes from character table context
    gap_grp = A._gap_()
    gap_cc = gap.ConjugacyClasses(gap_grp)
    gap_sizes = [int(gap.Size(c)) for c in gap_cc]
    print(f"From GAP ConjugacyClasses: {gap_sizes}")
    print(f"Sum: {sum(gap_sizes)}")
    
    # Check if the character table uses GAP's ordering
    print("\n--- Comparing class orderings ---")
    
    # The character table in Sage is computed via GAP
    # Let's see if the orderings match
    for i in range(min(5, len(cc))):
        rep = cc[i].representative()
        gap_rep = gap_cc[i].Representative()
        print(f"Class {i}: Sage rep order={rep.order()}, GAP rep order={gap_rep.Order()}")
    
    # The issue: Sage's conjugacy_classes() and GAP's may have different orderings
    # Let's use GAP directly for character computation
    
    print("\n--- Using GAP's character table directly ---")
    gap_char_table = gap.CharacterTable(gap_grp)
    gap_irreps = gap.Irr(gap_char_table)
    n_irreps = len(gap_irreps)
    print(f"Number of GAP irreps: {n_irreps}")
    
    # Get irrep dimensions
    gap_dims = [int(gap_irreps[i][1]) for i in range(n_irreps)]  # [1] is identity class
    print(f"GAP irrep dimensions: {sorted(set(gap_dims))}")


if __name__ == "__main__":
    main()
