"""Decompose H1 into irreducible components using GAP's character table directly."""
from __future__ import annotations
import json
import sys
from pathlib import Path


def main():
    print("=== H1 Irreducible Decomposition (GAP-aligned) ===", flush=True)
    
    here = Path(__file__).resolve().parent
    sys.path.insert(0, str(here))
    
    from lib.w33_io import W33DataPaths, load_w33_lines
    from sage.all import QQ, Graph, matrix, gap, libgap
    
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
    gens = list(A.gens())
    
    # Load H1 matrices
    results_file = here / "data" / "w33_sage_incidence_h1.json"
    with open(results_file) as f:
        data = json.load(f)
    
    h1_mats_str = data["h1_action"]["generator_matrices"]
    h1_mats = [matrix(QQ, [[QQ(x) for x in row] for row in mat_str]) for mat_str in h1_mats_str]
    dim = h1_mats[0].nrows()
    
    # Use libgap for cleaner interface
    gap_grp = libgap(A)
    
    # Get character table via libgap
    char_table_gap = gap_grp.CharacterTable()
    irreps = char_table_gap.Irr()
    n_irreps = len(irreps)
    
    # Get conjugacy classes via libgap  
    cc_gap = gap_grp.ConjugacyClasses()
    n_classes = len(cc_gap)
    
    print(f"Group order: {order}")
    print(f"H1 dimension: {dim}")
    print(f"Number of irreps: {n_irreps}")
    print(f"Number of conjugacy classes: {n_classes}")
    
    # Get class sizes
    class_sizes = [int(cc_gap[i].Size()) for i in range(n_classes)]
    print(f"Class sizes: {class_sizes}")
    print(f"Sum: {sum(class_sizes)}")
    
    # Function to compute H1 matrix for a group element
    def h1_matrix(g):
        """Compute H1 matrix for element g."""
        gap_g = libgap(g)
        word = gap_grp.Factorization(gap_g)
        ext = word.ExtRepOfObj()
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
    
    # Compute H1 character on each conjugacy class representative
    # Using GAP's ordering
    print("\n--- Computing H1 character (GAP ordering) ---")
    h1_chi = []
    for i in range(n_classes):
        rep_gap = cc_gap[i].Representative()
        # Convert GAP element back to Sage
        rep = A(rep_gap.sage())
        
        H1_rep = h1_matrix(rep)
        chi_val = H1_rep.trace()
        h1_chi.append(chi_val)
        
        print(f"  Class {i}: size={class_sizes[i]:5}, order={int(rep_gap.Order()):3}, chi={chi_val}")
    
    # Compute multiplicities
    print("\n--- Multiplicities of irreps in H1 ---")
    
    from sage.all import CC
    
    total_dim = 0
    decomposition = []
    
    for i in range(n_irreps):
        # Get irrep character values from GAP
        irrep_chi = list(irreps[i])
        
        # Convert first entry to integer (dimension)
        irrep_deg = int(irrep_chi[0].IsInt() and int(irrep_chi[0]) or int(irrep_chi[0].IsRat() and float(irrep_chi[0]) or 0))
        if irrep_deg == 0:
            irrep_deg = int(complex(str(irrep_chi[0].sage())).real)
        
        # Compute inner product <chi_H1, chi_i>
        # = (1/|G|) * sum_C |C| * chi_H1(C) * conj(chi_i(C))
        inner_sum = 0
        for j in range(n_classes):
            chi_h1_val = int(h1_chi[j])  # H1 character is integer
            
            # Convert GAP element to complex number
            gap_val = irrep_chi[j]
            try:
                if gap_val.IsInt():
                    chi_i_val = int(gap_val)
                elif gap_val.IsRat():
                    chi_i_val = float(gap_val)
                else:
                    # Cyclotomic number - convert via sage
                    chi_i_val = complex(gap_val.IsRat() and float(gap_val) or complex(str(gap_val.sage())))
            except:
                chi_i_val = complex(str(gap_val.sage()))
            
            chi_i_conj = chi_i_val.conjugate() if isinstance(chi_i_val, complex) else chi_i_val
            
            inner_sum += class_sizes[j] * chi_h1_val * chi_i_conj
        
        inner = inner_sum / order
        
        # Get numerical approximation
        mult_approx = inner.real if hasattr(inner, 'real') else float(inner)
        
        if abs(mult_approx) > 0.01:
            mult = round(mult_approx)
            print(f"  Irrep {i}: dim={irrep_deg:3}, <chi_H1,chi_i>≈{mult_approx:.4f}")
            if mult > 0:
                decomposition.append((i, irrep_deg, mult))
                total_dim += mult * irrep_deg
    
    print(f"\n--- Decomposition ---")
    for idx, deg, mult in decomposition:
        print(f"  {mult} x V_{idx} (dim {deg})")
    
    print(f"\nTotal dimension from decomposition: {total_dim}")
    print(f"H1 dimension: {dim}")
    print(f"Match: {total_dim == dim}")
    
    # Summary
    if total_dim == dim:
        print("\n" + "=" * 50)
        print("SUCCESS: H1 decomposes as:")
        for idx, deg, mult in decomposition:
            print(f"  {mult} copies of {deg}-dimensional irrep (index {idx})")
        print("=" * 50)


if __name__ == "__main__":
    main()
