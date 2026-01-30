"""Decompose H1 into irreducible components."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def main():
    print("=== H1 Irreducible Decomposition ===", flush=True)
    
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    
    from lib.w33_io import W33DataPaths, load_w33_lines
    from sage.all import QQ, Graph, matrix, vector
    
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
    h1_mats = [matrix(QQ, [[QQ(x) for x in row] for row in mat_str]) for mat_str in h1_mats_str]
    dim = h1_mats[0].nrows()
    
    # Get character table
    char_table = A.character_table()
    cc = A.conjugacy_classes()
    n_irreps = char_table.nrows()
    
    print(f"Group order: {order}")
    print(f"H1 dimension: {dim}")
    print(f"Number of irreps: {n_irreps}")
    
    # Build H1 character vector (one value per conjugacy class)
    from sage.all import gap
    
    def h1_matrix(g):
        """Compute H1 matrix for element g."""
        gap_grp = A._gap_()
        gap_g = g._gap_()
        word = gap.Factorization(gap_grp, gap_g)
        ext = gap.ExtRepOfObj(word)
        ext_list = list(ext)
        
        result = matrix.identity(QQ, dim)
        for i in range(0, len(ext_list), 2):
            gen_idx = int(ext_list[i]) - 1
            power = int(ext_list[i + 1])
            mat = h1_mats[gen_idx]
            if power > 0:
                result = result * (mat ** power)
            else:
                result = result * (mat.inverse() ** (-power))
        return result
    
    # Compute H1 character
    h1_chi = []
    class_sizes = []
    for c in cc:
        rep = c.representative()
        H1_rep = h1_matrix(rep)
        h1_chi.append(H1_rep.trace())
        class_sizes.append(len(c))
    
    print("\nH1 character:", h1_chi)
    
    # Compute multiplicity of each irrep in H1
    # m_i = (1/|G|) * sum_C |C| * chi_H1(C) * conj(chi_i(C))
    print("\n--- Multiplicities of irreps in H1 ---")
    
    from sage.all import conjugate, QQbar
    
    # Get the character ring for proper inner products
    # The character table entries may be in QQbar
    
    total_dim = 0
    decomposition = []
    for i in range(n_irreps):
        irrep_deg = int(char_table[i, 0])  # dimension of irrep i
        
        # Compute inner product <chi_H1, chi_i>
        inner = sum(
            class_sizes[j] * QQ(h1_chi[j]) * conjugate(char_table[i, j])
            for j in range(len(cc))
        ) / order
        
        # The multiplicity should be a non-negative integer
        # Use numerical approximation to check
        inner_approx = complex(inner)
        mult_approx = inner_approx.real
        
        if abs(mult_approx) > 0.01:  # Non-zero multiplicity
            mult = round(mult_approx)
            print(f"  Irrep {i}: dim={irrep_deg:3}, mult≈{mult_approx:.4f} -> {mult}")
            if mult > 0:
                decomposition.append((i, irrep_deg, mult))
                total_dim += mult * irrep_deg
    
    print(f"\nTotal dimension from decomposition: {total_dim}")
    print(f"H1 dimension: {dim}")
    print(f"Match: {total_dim == dim}")
    
    # Also show all irrep dimensions
    print("\n--- All irrep dimensions ---")
    irrep_dims = [int(char_table[i, 0]) for i in range(n_irreps)]
    for d in sorted(set(irrep_dims)):
        count = irrep_dims.count(d)
        print(f"  dim {d}: {count} irrep(s)")


if __name__ == "__main__":
    main()
