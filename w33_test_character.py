#!/usr/bin/env sage
"""
Test H1 character with proper inner product calculation.
"""

import json
import numpy as np
from sage.all import *

# Load the JSON data
json_path = 'claude_workspace/data/w33_sage_incidence_h1.json'
with open(json_path, 'r') as f:
    data = json.load(f)

print("=== H1 Character Analysis ===\n")

# Get H1 action matrices
h1_matrices = []
for mat_data in data['h1_action']['generator_matrices']:
    mat = np.array([[float(x) for x in row] for row in mat_data], dtype=float)
    h1_matrices.append(mat)

h1_dim = data['homology']['beta1']
n_gens = len(h1_matrices)

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
group_order = G.order()

sage_gens = G.gens()
gap_G = libgap(G)

print(f"H1 dim: {h1_dim}, Group order: {group_order}")

# Create map from generator index to H1 matrix
gen_to_matrix = {i: h1_matrices[i] for i in range(n_gens)}

def h1_matrix_for_element(g):
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

# Test homomorphism on several random elements
print("--- Testing homomorphism property ---")
import random
random.seed(42)

for trial in range(5):
    # Generate two random elements
    word1 = [(random.randint(0, n_gens-1), random.choice([1, -1])) for _ in range(3)]
    word2 = [(random.randint(0, n_gens-1), random.choice([1, -1])) for _ in range(3)]
    
    g1 = G.identity()
    for gen_idx, power in word1:
        g1 = g1 * (sage_gens[gen_idx] ** power)
    
    g2 = G.identity()
    for gen_idx, power in word2:
        g2 = g2 * (sage_gens[gen_idx] ** power)
    
    g12 = g1 * g2
    
    mat1 = h1_matrix_for_element(g1)
    mat2 = h1_matrix_for_element(g2)
    mat12 = h1_matrix_for_element(g12)
    
    product = mat1 @ mat2
    
    match = np.allclose(product, mat12)
    print(f"  Trial {trial}: ρ(g1*g2) = ρ(g1)*ρ(g2)? {match}")
    if not match:
        print(f"    Max diff: {np.max(np.abs(product - mat12))}")

# Alternative: Use Sage's conjugacy_classes() instead of GAP's
print("\n--- Using Sage conjugacy classes ---")
sage_classes = G.conjugacy_classes()
print(f"Sage conjugacy classes: {len(sage_classes)}")

sage_class_sizes = [len(c) for c in sage_classes]
print(f"Class sizes: {sage_class_sizes}")
print(f"Sum: {sum(sage_class_sizes)}")

# Compute H1 character on Sage conjugacy classes
h1_chi_sage = []
for i, cc in enumerate(sage_classes):
    rep = cc[0]  # Get representative (first element in the conjugacy class)
    mat = h1_matrix_for_element(rep)
    trace = np.trace(mat)
    h1_chi_sage.append(round(trace))

print(f"\nH1 character (Sage ordering): {h1_chi_sage}")

# Compute <chi, chi> using Sage class sizes
chi_squared_sage = sum(sage_class_sizes[j] * h1_chi_sage[j]**2 for j in range(len(sage_classes))) / group_order
print(f"<chi_H1, chi_H1> = {chi_squared_sage}")

if chi_squared_sage >= 0.999:
    print("✓ Valid character!")
else:
    print("✗ Something wrong with character computation")

# Let's also verify by computing in a different way
# The character norm satisfies: <chi,chi> = sum_i m_i^2 where m_i are multiplicities
# For any character, <chi,chi> >= 1 with equality iff irreducible

# Actually, let me just enumerate all elements and compute average of |chi|^2
print("\n--- Brute force character norm (sampling) ---")
sample_size = min(1000, group_order)
total = 0
for i, g in enumerate(G):
    if i >= sample_size:
        break
    mat = h1_matrix_for_element(g)
    trace = np.trace(mat)
    total += trace**2

estimated_norm = total / sample_size
print(f"Estimated <chi,chi> from {sample_size} samples: {estimated_norm}")
