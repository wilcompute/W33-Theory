#!/usr/bin/env sage
"""
Direct H1 irreducible decomposition using matrix traces.
Compute character by evaluating trace of action matrices on class representatives.
"""

import json
import numpy as np
from sage.all import *

# Load the JSON data
with open('claude_workspace/data/w33_sage_incidence_h1.json', 'r') as f:
    data = json.load(f)

print("=== H1 Irreducible Decomposition (Direct Approach) ===")

# Get H1 matrices from the JSON - they're in h1_action.generator_matrices
h1_action = data.get('h1_action', {})
h1_matrices_data = h1_action.get('generator_matrices', [])
h1_dim = data.get('homology', {}).get('beta1', None)

if not h1_matrices_data:
    print("No H1 action matrices found in JSON!")
    sys.exit(1)

print(f"H1 dimension: {h1_dim}")
print(f"Number of generator matrices: {len(h1_matrices_data)}")

# Convert matrices to numpy for easier computation
# h1_matrices_data is a list of matrices (one per generator)
h1_matrices = {}
for i, mat_data in enumerate(h1_matrices_data):
    # Convert string matrix to float
    mat = np.array([[float(x) for x in row] for row in mat_data], dtype=complex)
    gen_name = f"f{i}"
    h1_matrices[gen_name] = mat
    print(f"  Generator {i} ({gen_name}): {mat.shape}")

# Get the automorphism group from Sage
# We need to reconstruct the group to get conjugacy class structure

# Load incidences from the JSON
incidence_data = data.get('incidence', {})
generators = incidence_data.get('generators', [])

# Need to rebuild the bipartite graph from generator permutations
# First get n_points and n_blocks
n_points = len(generators[0]['points']) if generators else 40
n_blocks = len(generators[0]['lines']) if generators else 40

print(f"\nNumber of points: {n_points}")
print(f"Number of blocks: {n_blocks}")

# Build bipartite incidence graph
from sage.graphs.graph import Graph
G = Graph()

point_labels = {p: f"P{p}" for p in points}
block_labels = {b: f"B{b}" for b in blocks}

for p in points:
    G.add_vertex(point_labels[p])
for b in blocks:
    G.add_vertex(block_labels[b])

for p, b in incidences:
    G.add_edge(point_labels[p], block_labels[b])

# Get automorphism group
Aut = G.automorphism_group()
order = Aut.order()
print(f"\nAutomorphism group order: {order}")

# Get GAP representation for character table
gap_G = libgap(Aut)
char_table = gap_G.CharacterTable()
irreps = char_table.Irr()
n_irreps = len(irreps)

# Get class representatives  
class_reps = char_table.ConjugacyClasses()
n_classes = len(class_reps)
class_sizes = [int(libgap.Size(c)) for c in class_reps]

print(f"Number of conjugacy classes: {n_classes}")
print(f"Number of irreps: {n_irreps}")

# Now compute H1 character directly from matrices
# For each conjugacy class, pick a representative and compute trace

print("\n--- Computing H1 character from matrices ---")

# We need to map automorphism group elements to H1 matrices
# The H1 matrices are labeled by generators f0, f1, ... (Sage's names)

# Get generator names and matrices
gen_names = sorted(h1_matrices.keys())
print(f"Generators: {gen_names}")

# Get Sage generators in the same order
gens = Aut.gens()
n_gens = len(gens)
print(f"Number of group generators: {n_gens}")

# Create a map from generator to H1 matrix
# Assuming f0, f1, ... correspond to gens()[0], gens()[1], ...
gen_to_matrix = {}
for i, g in enumerate(gens):
    gen_name = f"f{i}"
    if gen_name in h1_matrices:
        gen_to_matrix[i] = h1_matrices[gen_name]
        print(f"  Generator {i} ({gen_name}): mapped")
    else:
        print(f"  Warning: {gen_name} not in H1 matrices")

# Function to compute H1 matrix for arbitrary group element
def compute_h1_matrix(g, gen_to_matrix, gens):
    """Compute H1 matrix for group element g by factoring into generators."""
    # Use GAP's Factorization
    gap_g = libgap(g)
    gap_gens = [libgap(gen) for gen in gens]
    
    try:
        factored = gap_G.Factorization(gap_g)
        ext_rep = list(factored.ExtRepOfObj())
    except:
        print(f"    Cannot factor element")
        return None
    
    # Parse the external representation
    dim = list(gen_to_matrix.values())[0].shape[0]
    result = np.eye(dim, dtype=complex)
    
    for i in range(0, len(ext_rep), 2):
        gen_idx = int(ext_rep[i]) - 1  # 1-indexed in GAP
        power = int(ext_rep[i+1])
        
        if gen_idx not in gen_to_matrix:
            print(f"    Generator {gen_idx} not found in map")
            return None
        
        mat = gen_to_matrix[gen_idx]
        
        if power > 0:
            for _ in range(power):
                result = result @ mat
        else:
            mat_inv = np.linalg.inv(mat)
            for _ in range(-power):
                result = result @ mat_inv
    
    return result

# Compute H1 character on each conjugacy class
h1_chi = []

for c_idx in range(n_classes):
    gap_class = class_reps[c_idx]
    # Get a representative element from the class
    rep = gap_class.Representative()
    
    # Convert to Sage
    try:
        sage_rep = Aut(rep.sage())
    except:
        # Try another way
        try:
            sage_rep = Aut._element_from_gap(rep)
        except:
            print(f"  Class {c_idx}: cannot convert representative")
            h1_chi.append(0)
            continue
    
    # Compute H1 matrix and trace
    mat = compute_h1_matrix(sage_rep, gen_to_matrix, gens)
    if mat is None:
        h1_chi.append(0)
        continue
    
    trace = np.trace(mat)
    h1_chi.append(round(trace.real))
    
    order_elem = int(libgap.Order(rep))
    print(f"  Class {c_idx}: size={class_sizes[c_idx]:5}, order={order_elem:2}, chi={h1_chi[-1]}")

print(f"\nH1 character: {h1_chi}")

# Verify: chi(1) should equal dimension
print(f"chi(1) = {h1_chi[0]}, H1 dim = {data.get('h1_dim')}")

# Now compute inner product of H1 character with itself
chi_squared = sum(class_sizes[j] * h1_chi[j]**2 for j in range(n_classes)) / order
print(f"<chi, chi> = {chi_squared}")
print(f"Is H1 irreducible? {abs(chi_squared - 1) < 0.01}")

# Compute multiplicities
print("\n--- Multiplicities of irreps in H1 ---")

decomposition = []
total_dim = 0

for i in range(n_irreps):
    irrep_chi = list(irreps[i])
    irrep_deg = int(irrep_chi[0].IsInt() and int(irrep_chi[0]) or round(complex(str(irrep_chi[0].sage())).real))
    
    # Compute inner product
    inner_sum = 0
    for j in range(n_classes):
        # Get irrep character value
        gap_val = irrep_chi[j]
        try:
            if gap_val.IsInt():
                chi_i_val = int(gap_val)
            elif gap_val.IsRat():
                chi_i_val = float(gap_val)
            else:
                chi_i_val = complex(str(gap_val.sage()))
        except:
            chi_i_val = complex(str(gap_val.sage()))
        
        chi_i_conj = chi_i_val.conjugate() if isinstance(chi_i_val, complex) else chi_i_val
        
        inner_sum += class_sizes[j] * h1_chi[j] * chi_i_conj
    
    inner = inner_sum / order
    mult_approx = inner.real if hasattr(inner, 'real') else float(inner)
    
    if abs(mult_approx) > 0.01 or irrep_deg == 81:  # Always show 81-dim irreps
        mult = round(mult_approx)
        print(f"  Irrep {i}: dim={irrep_deg:3}, <chi_H1,chi_i>≈{mult_approx:.6f}, mult={mult}")
        if mult > 0:
            decomposition.append((i, irrep_deg, mult))
            total_dim += mult * irrep_deg

print("\n--- Decomposition ---")
for idx, deg, mult in decomposition:
    print(f"  V_{idx} (dim {deg}) with multiplicity {mult}")

print(f"\nTotal dimension from decomposition: {total_dim}")
print(f"H1 dimension: {data.get('h1_dim')}")
print(f"Match: {total_dim == data.get('h1_dim')}")
