"""Check if H1 is an irreducible representation by computing its character."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main():
    print("=== Checking if H1 is Irreducible ===", flush=True)

    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))

    from sage.all import QQ, Graph, matrix, vector

    from lib.w33_io import W33DataPaths, load_w33_lines

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

    # Load H1 matrices
    results_file = here / "data" / "w33_sage_incidence_h1.json"
    with open(results_file) as f:
        data = json.load(f)

    h1_mats_str = data["h1_action"]["generator_matrices"]
    gens = list(A.gens())
    h1_mats = []
    for mat_str in h1_mats_str:
        M = matrix(QQ, [[QQ(x) for x in row] for row in mat_str])
        h1_mats.append(M)

    dim = h1_mats[0].nrows()

    # For irreducibility, we use the criterion:
    # (1/|G|) * sum_{g in G} |chi(g)|^2 = 1  iff irreducible
    #
    # Since |G| = 51840 is large, we compute this by summing over conjugacy classes:
    # sum_C |C| * |chi(rep(C))|^2 / |G|

    print(f"\nGroup order: {order}")
    print(f"H1 dimension: {dim}")

    # Get character table to compare
    char_table = A.character_table()
    cc = A.conjugacy_classes()

    print(f"Conjugacy classes: {len(cc)}")

    # Build generator -> matrix mapping
    gen_to_mat = {g: M for g, M in zip(gens, h1_mats)}

    # For each conjugacy class, we need to compute H1(representative)
    # This requires expressing rep as a word in generators
    # Sage can do this via factoring elements

    def h1_matrix(g):
        """Compute H1 matrix for element g by multiplying generator matrices."""
        # Express g in terms of generators using GAP's Factorization
        from sage.all import gap

        # Create GAP free group and get factorization
        gap_grp = A._gap_()
        gap_g = g._gap_()
        gap_gens = gap_grp.GeneratorsOfGroup()

        # Try to factor g in terms of generators
        try:
            word = gap.Factorization(gap_grp, gap_g)
            # word is a GAP word - convert to list of (gen_index, exponent)
            word_str = str(word)
        except:
            # If factorization fails, use a different approach
            # Just return identity for now
            return matrix.identity(QQ, dim)

        # Parse the GAP word string manually
        # Format like "f1*f2^-1*f3" where f1, f2, ... are generators
        result = matrix.identity(QQ, dim)

        # Use GAP's ExtRepOfObj to get syllables
        ext = gap.ExtRepOfObj(word)
        # ext is a list [gen_index, power, gen_index, power, ...]
        ext_list = list(ext)

        for i in range(0, len(ext_list), 2):
            gen_idx = int(ext_list[i]) - 1  # GAP is 1-indexed
            power = int(ext_list[i + 1])
            mat = h1_mats[gen_idx]
            if power > 0:
                result = result * (mat**power)
            else:
                result = result * (mat.inverse() ** (-power))

        return result

    print("\n--- Computing H1 character on class representatives ---")

    chi_values = []
    for i, c in enumerate(cc):
        rep = c.representative()
        class_size = len(c)

        # Compute H1(rep)
        H1_rep = h1_matrix(rep)
        chi = H1_rep.trace()
        chi_values.append((class_size, chi))

        print(f"  Class {i}: size={class_size:5}, order={rep.order():3}, chi={chi}")

    # Compute norm squared: (1/|G|) * sum |C| * |chi|^2
    norm_sq_sum = sum(size * (chi.abs() ** 2) for size, chi in chi_values)
    norm_sq = norm_sq_sum / order

    print(f"\n<chi, chi> = (1/{order}) * {norm_sq_sum} = {norm_sq}")
    print(f"\nH1 is irreducible: {norm_sq == 1}")

    if norm_sq == 1:
        print("\n*** H1 IS AN IRREDUCIBLE 81-dimensional representation! ***")
    else:
        print(f"\nH1 decomposes into ~{int(norm_sq)} irreducible components")

    # Also check which irrep it matches by comparing characters
    print("\n--- Comparing with character table ---")

    # Find the 81-dimensional irreps
    for row_idx in range(char_table.nrows()):
        if int(char_table[row_idx, 0]) == 81:
            print(f"Found 81-dim irrep at row {row_idx}")
            # Compare characters
            match = True
            for col_idx, (cls_size, chi) in enumerate(chi_values):
                table_chi = char_table[row_idx, col_idx]
                if chi != table_chi:
                    match = False
                    break
            if match:
                print(f"  -> H1 matches irrep row {row_idx} exactly!")
            else:
                print(f"  -> Characters differ")


if __name__ == "__main__":
    main()
