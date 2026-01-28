#!/usr/bin/env sage
"""
H1 Irreducible Decomposition for W33
Directly computes character on conjugacy class representatives.
"""

import json

import numpy as np
from sage.all import *

# Load the JSON data
json_path = "claude_workspace/data/w33_sage_incidence_h1.json"
with open(json_path, "r") as f:
    data = json.load(f)

print("=== H1 Irreducible Decomposition for W33 ===\n")

# Extract info
incidence_data = data["incidence"]
homology_data = data["homology"]
h1_action = data["h1_action"]

h1_dim = homology_data["beta1"]
group_order = incidence_data["group_order"]
structure = incidence_data["structure_description"]

print(f"H1 dimension: {h1_dim}")
print(f"Automorphism group order: {group_order}")
print(f"Structure: {structure}")

# Get H1 action matrices
h1_matrices = []
for mat_data in h1_action["generator_matrices"]:
    mat = np.array([[float(x) for x in row] for row in mat_data], dtype=float)
    h1_matrices.append(mat)

n_gens = len(h1_matrices)
print(f"Number of generators: {n_gens}")
print(f"Matrix shape: {h1_matrices[0].shape}")

# Build the permutation group from generators
# Each generator acts on points and lines
generators_data = incidence_data["generators"]

# Create permutations on the combined point+line set (80 elements: 0-39 points, 40-79 lines)
perm_gens = []
for gen in generators_data:
    pts = gen["points"]  # permutation of points 0-39
    lns = gen["lines"]  # permutation of lines 0-39
    # Combine into single permutation on 0-79
    combined = pts + [l + 40 for l in lns]  # Shift lines to 40-79
    perm_gens.append(combined)

# Create permutation group
n = 80
S = SymmetricGroup(n)
perms = [S(Permutation([p + 1 for p in perm])) for perm in perm_gens]
G = PermutationGroup(perms)

print(f"\nReconstructed group order: {G.order()}")
assert G.order() == group_order, "Group order mismatch!"

# Get GAP representation for character table
gap_G = libgap(G)
char_table = gap_G.CharacterTable()
irreps = char_table.Irr()
n_irreps = len(irreps)

# Get conjugacy class info
class_reps = char_table.ConjugacyClasses()
n_classes = len(class_reps)
class_sizes = [int(libgap.Size(c)) for c in class_reps]

print(f"Number of conjugacy classes: {n_classes}")
print(f"Number of irreps: {n_irreps}")

# Print irrep dimensions
irrep_dims = []
for i in range(n_irreps):
    chi_i = list(irreps[i])
    d = int(
        chi_i[0].IsInt() and int(chi_i[0]) or round(complex(str(chi_i[0].sage())).real)
    )
    irrep_dims.append(d)

print(f"Irrep dimensions: {sorted(set(irrep_dims))}")

# Get Sage generators
sage_gens = G.gens()
print(f"Number of Sage generators: {len(sage_gens)}")

# Create map from generator index to H1 matrix
gen_to_matrix = {i: h1_matrices[i] for i in range(min(n_gens, len(sage_gens)))}


# Function to compute H1 matrix for group element
def h1_matrix_for_element(g):
    """Compute H1 matrix for group element g using GAP factorization."""
    gap_g = libgap(g)

    # Factor into generators
    factored = gap_G.Factorization(gap_g)
    ext_rep = list(factored.ExtRepOfObj())

    dim = h1_dim
    result = np.eye(dim, dtype=float)

    for i in range(0, len(ext_rep), 2):
        gen_idx = int(ext_rep[i]) - 1  # 1-indexed in GAP
        power = int(ext_rep[i + 1])

        if gen_idx not in gen_to_matrix:
            raise ValueError(f"Generator {gen_idx} not in map")

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
print("\n--- Computing H1 character ---")
h1_chi = []

for c_idx in range(n_classes):
    gap_class = class_reps[c_idx]
    rep = gap_class.Representative()

    # Convert to Sage element
    # GAP permutation -> Sage permutation
    gap_perm = list(rep.ListPerm())
    if not gap_perm:  # Identity
        gap_perm = list(range(1, n + 1))
    else:
        # Extend to full length if needed
        while len(gap_perm) < n:
            gap_perm.append(len(gap_perm) + 1)

    sage_perm = SymmetricGroup(n)(gap_perm)

    # Find corresponding element in G
    try:
        g = G(sage_perm)
    except:
        print(f"  Class {c_idx}: cannot convert representative")
        h1_chi.append(0)
        continue

    # Compute H1 matrix and trace
    try:
        mat = h1_matrix_for_element(g)
        trace = np.trace(mat)
        h1_chi.append(round(trace))
    except Exception as e:
        print(f"  Class {c_idx}: error computing trace - {e}")
        h1_chi.append(0)
        continue

    order_elem = int(libgap.Order(rep))
    print(
        f"  Class {c_idx}: size={class_sizes[c_idx]:5}, order={order_elem:2}, chi={h1_chi[-1]}"
    )

# Verify chi(1) = dim
print(f"\nchi(identity) = {h1_chi[0]}, H1 dim = {h1_dim}")

# Compute <chi, chi>
chi_squared = (
    sum(class_sizes[j] * h1_chi[j] ** 2 for j in range(n_classes)) / group_order
)
print(f"<chi_H1, chi_H1> = {chi_squared}")
print(f"Is H1 irreducible? {abs(chi_squared - 1) < 0.01}")

# Compute multiplicities
print("\n--- Multiplicities of irreps in H1 ---")

decomposition = []
total_dim = 0

for i in range(n_irreps):
    irrep_chi_values = list(irreps[i])
    dim_i = irrep_dims[i]

    # Compute inner product <chi_H1, chi_i>
    inner_sum = 0
    for j in range(n_classes):
        gap_val = irrep_chi_values[j]

        # Convert GAP value to Python number
        try:
            if gap_val.IsInt():
                chi_i_val = int(gap_val)
            elif gap_val.IsRat():
                from fractions import Fraction

                chi_i_val = float(Fraction(str(gap_val)))
            else:
                chi_i_val = complex(str(gap_val.sage()))
        except:
            chi_i_val = complex(str(gap_val.sage()))

        # Take conjugate
        chi_i_conj = (
            chi_i_val.conjugate() if isinstance(chi_i_val, complex) else chi_i_val
        )

        inner_sum += class_sizes[j] * h1_chi[j] * chi_i_conj

    inner = inner_sum / group_order
    mult_approx = inner.real if hasattr(inner, "real") else float(inner)
    mult = round(mult_approx)

    # Only print non-zero multiplicities or 81-dim irreps
    if abs(mult_approx) > 0.1 or dim_i == 81:
        print(
            f"  Irrep {i:2}: dim={dim_i:3}, <chi_H1,chi_{i}>={mult_approx:8.4f}, mult={mult}"
        )

    if mult > 0:
        decomposition.append((i, dim_i, mult))
        total_dim += mult * dim_i

print("\n=== Decomposition of H1 ===")
for idx, deg, mult in decomposition:
    print(f"  V_{idx} (dimension {deg}) appears with multiplicity {mult}")

print(f"\nTotal dimension: {total_dim}")
print(f"Expected (H1 dim): {h1_dim}")
print(f"Match: {total_dim == h1_dim}")

if total_dim == h1_dim:
    print("\n✓ H1 decomposes as:")
    terms = [
        f"{mult}×V_{idx}({deg}-dim)" if mult > 1 else f"V_{idx}({deg}-dim)"
        for idx, deg, mult in decomposition
    ]
    print("  H1 = " + " ⊕ ".join(terms))
