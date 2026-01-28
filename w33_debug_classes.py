#!/usr/bin/env sage
"""
Debug the conjugacy class ordering issue by computing everything in GAP.
"""

import json

import numpy as np
from sage.all import *

# Load the JSON data
json_path = "claude_workspace/data/w33_sage_incidence_h1.json"
with open(json_path, "r") as f:
    data = json.load(f)

print("=== Debug Conjugacy Class Ordering ===\n")

# Extract info
incidence_data = data["incidence"]
h1_dim = data["homology"]["beta1"]
group_order = incidence_data["group_order"]

# Get H1 action matrices
h1_matrices = []
for mat_data in data["h1_action"]["generator_matrices"]:
    mat = np.array([[float(x) for x in row] for row in mat_data], dtype=float)
    h1_matrices.append(mat)

n_gens = len(h1_matrices)
print(f"H1 dim: {h1_dim}, Group order: {group_order}, # generators: {n_gens}")

# Build the permutation group from generators
generators_data = incidence_data["generators"]
perm_gens = []
for gen in generators_data:
    pts = gen["points"]
    lns = gen["lines"]
    combined = pts + [l + 40 for l in lns]
    perm_gens.append(combined)

n = 80
S = SymmetricGroup(n)
perms = [S(Permutation([p + 1 for p in perm])) for perm in perm_gens]
G = PermutationGroup(perms)

print(f"Reconstructed group order: {G.order()}")

# Get Sage generators
sage_gens = G.gens()

# Create map from generator index to H1 matrix
gen_to_matrix = {i: h1_matrices[i] for i in range(n_gens)}

# Function to compute H1 matrix for group element
gap_G = libgap(G)


def h1_matrix_for_element(g):
    gap_g = libgap(g)
    factored = gap_G.Factorization(gap_g)
    ext_rep = list(factored.ExtRepOfObj())

    result = np.eye(h1_dim, dtype=float)

    for i in range(0, len(ext_rep), 2):
        gen_idx = int(ext_rep[i]) - 1
        power = int(ext_rep[i + 1])

        mat = gen_to_matrix[gen_idx]

        if power > 0:
            for _ in range(power):
                result = result @ mat
        else:
            mat_inv = np.linalg.inv(mat)
            for _ in range(-power):
                result = result @ mat_inv

    return result


# Get character table from GAP
char_table = gap_G.CharacterTable()
gap_classes = char_table.ConjugacyClasses()
n_classes = len(gap_classes)

# Get class sizes from GAP
gap_class_sizes = [int(libgap.Size(c)) for c in gap_classes]
print(f"\nGAP class sizes: {gap_class_sizes}")
print(f"Sum: {sum(gap_class_sizes)}")

# For each GAP class, get representative and compute chi_H1
print("\n--- Computing H1 character via GAP class representatives ---")
h1_chi = []

for c_idx in range(n_classes):
    gap_class = gap_classes[c_idx]
    rep_gap = gap_class.Representative()

    # Convert GAP permutation to Sage
    perm_list = list(rep_gap.ListPerm())
    if not perm_list:
        perm_list = list(range(1, n + 1))
    while len(perm_list) < n:
        perm_list.append(len(perm_list) + 1)

    sage_perm = S(perm_list)
    g = G(sage_perm)

    # Compute H1 matrix and trace
    mat = h1_matrix_for_element(g)
    trace = np.trace(mat)
    h1_chi.append(round(trace))

    order_elem = int(libgap.Order(rep_gap))
    print(
        f"  Class {c_idx}: size={gap_class_sizes[c_idx]:5}, order={order_elem:2}, chi={h1_chi[-1]}"
    )

print(f"\nH1 character vector: {h1_chi}")

# Now compute <chi, chi> using GAP class sizes
chi_squared = (
    sum(gap_class_sizes[j] * h1_chi[j] ** 2 for j in range(n_classes)) / group_order
)
print(f"\n<chi_H1, chi_H1> = {chi_squared}")

# This MUST be >= 1 for a valid character
if chi_squared >= 0.999:
    print("✓ Character passes consistency check!")
else:
    print("✗ ERROR: <chi, chi> < 1, something is wrong!")
    print("  Possible issues:")
    print("  - Class sizes don't match GAP ordering")
    print("  - H1 matrix computation is incorrect")
    print("  - Generator correspondence is wrong")

# Let's verify by computing chi(1)^2 / |G| which should be <= 1
print(f"\nchi(1)^2 / |G| = {h1_chi[0]**2 / group_order}")

# Double check: compute character on identity directly
print(f"\nDirect check - trace of identity matrix: {np.trace(np.eye(h1_dim))}")

# Check that identity is indeed the first class representative
id_rep = gap_classes[0].Representative()
print(f"First class rep order: {int(libgap.Order(id_rep))}")
print(f"First class rep is identity? {id_rep == libgap(G.identity())}")

# Let's also verify generator matrices are correct
print("\n--- Verifying generator matrices ---")
for i in range(min(3, n_gens)):
    mat = h1_matrices[i]
    det = np.linalg.det(mat)
    tr = np.trace(mat)
    print(f"  Generator {i}: trace={tr:.1f}, det={det:.4f}")

    # Check it's invertible
    try:
        mat_inv = np.linalg.inv(mat)
        prod = mat @ mat_inv
        is_inv = np.allclose(prod, np.eye(h1_dim))
        print(f"    Invertible: {is_inv}")
    except:
        print(f"    NOT invertible!")

# Test: compute g * g^{-1} for a generator
print("\n--- Testing generator inverse ---")
g0 = sage_gens[0]
mat0 = h1_matrices[0]
mat0_2 = h1_matrix_for_element(g0)
print(f"Direct matrix vs computed: match = {np.allclose(mat0, mat0_2)}")

# Test order of generator
g0_order = g0.order()
print(f"Generator 0 order: {g0_order}")
mat0_power = mat0.copy()
for i in range(1, g0_order):
    mat0_power = mat0_power @ mat0
print(f"M^{g0_order} = I? {np.allclose(mat0_power, np.eye(h1_dim))}")
