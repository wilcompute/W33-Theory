#!/usr/bin/env sage
"""
Debug H1 action by verifying the group homomorphism property.
"""

import json
import numpy as np
from sage.all import *

# Load the JSON data
json_path = 'claude_workspace/data/w33_sage_incidence_h1.json'
with open(json_path, 'r') as f:
    data = json.load(f)

print("=== Verifying H1 is a Group Homomorphism ===\n")

# Get H1 action matrices
h1_matrices = []
for mat_data in data['h1_action']['generator_matrices']:
    mat = np.array([[float(x) for x in row] for row in mat_data], dtype=float)
    h1_matrices.append(mat)

h1_dim = data['homology']['beta1']
n_gens = len(h1_matrices)
print(f"H1 dim: {h1_dim}, # generators: {n_gens}")

# Build the permutation group
generators_data = data['incidence']['generators']
perm_gens = []
for gen in generators_data:
    pts = gen['points']
    lns = gen['lines']
    combined = pts + [l + 40 for l in lns]
    perm_gens.append(combined)

n = 80
S = SymmetricGroup(n)
perms = [S(Permutation([p+1 for p in perm])) for perm in perm_gens]
G = PermutationGroup(perms)

sage_gens = G.gens()
gap_G = libgap(G)

print(f"Group generators: {len(sage_gens)}")
print(f"H1 matrices: {len(h1_matrices)}")

# Verify generator correspondence
print("\n--- Generator correspondence ---")
for i, g in enumerate(sage_gens):
    order_g = g.order()
    mat = h1_matrices[i]
    tr = np.trace(mat)
    
    # Check matrix order matches
    mat_power = np.eye(h1_dim)
    for _ in range(order_g):
        mat_power = mat_power @ mat
    mat_order_ok = np.allclose(mat_power, np.eye(h1_dim))
    
    print(f"  Gen {i}: group order={order_g}, trace={tr:.1f}, M^order=I? {mat_order_ok}")

# Check group relations are satisfied
print("\n--- Checking group relations ---")

# Get relations using GAP
fp = gap_G.Image(gap_G.IsomorphismFpGroup())
fp_gens = list(fp.FreeGeneratorsOfFpGroup())
rels = list(fp.RelatorsOfFpGroup())

print(f"Number of relations: {len(rels)}")

def eval_relator_matrix(rel):
    """Evaluate a relator word as a matrix product."""
    ext_rep = list(rel.ExtRepOfObj())
    result = np.eye(h1_dim, dtype=float)
    
    for i in range(0, len(ext_rep), 2):
        gen_idx = int(ext_rep[i]) - 1
        power = int(ext_rep[i+1])
        
        mat = h1_matrices[gen_idx]
        
        if power > 0:
            for _ in range(power):
                result = result @ mat
        else:
            mat_inv = np.linalg.inv(mat)
            for _ in range(-power):
                result = result @ mat_inv
    
    return result

# Check first few relations
for i, rel in enumerate(rels[:10]):
    mat = eval_relator_matrix(rel)
    is_identity = np.allclose(mat, np.eye(h1_dim))
    if not is_identity:
        print(f"  Relation {i}: FAILS! Max deviation: {np.max(np.abs(mat - np.eye(h1_dim)))}")
    else:
        print(f"  Relation {i}: OK (=I)")

# Now test homomorphism: ρ(gh) = ρ(g)ρ(h)
print("\n--- Testing homomorphism property ---")

gen_to_matrix = {i: h1_matrices[i] for i in range(n_gens)}

def h1_matrix_via_factorization(g):
    gap_g = libgap(g)
    factored = gap_G.Factorization(gap_g)
    ext_rep = list(factored.ExtRepOfObj())
    
    result = np.eye(h1_dim, dtype=float)
    
    for i in range(0, len(ext_rep), 2):
        gen_idx = int(ext_rep[i]) - 1
        power = int(ext_rep[i+1])
        
        mat = gen_to_matrix[gen_idx]
        
        if power > 0:
            for _ in range(power):
                result = result @ mat
        else:
            mat_inv = np.linalg.inv(mat)
            for _ in range(-power):
                result = result @ mat_inv
    
    return result

# Test: ρ(g0 * g1) = ρ(g0) * ρ(g1)
g0, g1 = sage_gens[0], sage_gens[1]
g01 = g0 * g1

mat_g0 = h1_matrix_via_factorization(g0)
mat_g1 = h1_matrix_via_factorization(g1)
mat_g01 = h1_matrix_via_factorization(g01)
mat_product = mat_g0 @ mat_g1

print(f"ρ(g0)ρ(g1) = ρ(g0*g1)? {np.allclose(mat_product, mat_g01)}")

# Test with inverse
g0_inv = g0.inverse()
mat_g0_inv = h1_matrix_via_factorization(g0_inv)
mat_g0_direct_inv = np.linalg.inv(mat_g0)

print(f"ρ(g0^-1) = ρ(g0)^-1? {np.allclose(mat_g0_inv, mat_g0_direct_inv)}")

# The issue might be that factorization and direct generator application give different results
# Let's check if direct H1 matrix matches factorization
print("\n--- Direct vs Factorization for generators ---")
for i, g in enumerate(sage_gens):
    mat_direct = h1_matrices[i]
    mat_fact = h1_matrix_via_factorization(g)
    match = np.allclose(mat_direct, mat_fact)
    if not match:
        print(f"  Gen {i}: MISMATCH! Max diff: {np.max(np.abs(mat_direct - mat_fact))}")
    else:
        print(f"  Gen {i}: match")

# The problem might be in how Sage/GAP numbers generators vs our indexing
# Let's check the factorization of each generator
print("\n--- Factorization of generators ---")
for i, g in enumerate(sage_gens):
    gap_g = libgap(g)
    factored = gap_G.Factorization(gap_g)
    ext_rep = list(factored.ExtRepOfObj())
    print(f"  Gen {i}: factorizes as {ext_rep}")
