#!/usr/bin/env sage
"""
Get detailed info about the 81-dimensional irrep V_23.
"""

from sage.all import *
import json

# Load W33 incidence graph
with open("claude_workspace/data/w33_sage_incidence_h1.json") as f:
    data = json.load(f)

generators_data = data["incidence"]["generators"]
perm_gens = []
for gen in generators_data:
    pts = gen["points"]
    lns = gen["lines"]
    combined = pts + [l + 40 for l in lns]
    perm_gens.append(combined)

n = 80
S = SymmetricGroup(n)
perms = [S(Permutation([p+1 for p in perm])) for perm in perm_gens]
G = PermutationGroup(perms)

gap_G = libgap(G)
char_table = gap_G.CharacterTable()
irreps = char_table.Irr()

print("=== Detailed Analysis of H1 = V_23 ===\n")

# Get info about V23 (the 81-dim irrep)
chi_23 = list(irreps[23])
print("V_23 (81-dim irrep) character values:")
for i, val in enumerate(chi_23):
    print(f"  Class {i}: {val}")

print()

# Check if it is faithful - use character value at non-identity classes
# Faithful iff only identity has chi(g) = dim
print("Checking faithfulness of V_23:")
dim_23 = 81
faithful = True
for i in range(1, len(chi_23)):
    if int(chi_23[i]) == dim_23:
        faithful = False
        print(f"  Non-identity class {i} has chi = {chi_23[i]} = dim (not faithful)")
        break
print(f"V_23 is faithful: {faithful}")

# Get Frobenius-Schur indicator
fs = char_table.Indicator(2)
print(f"Frobenius-Schur indicator of V_23: {fs[23]}")
# +1 = real (orthogonal), -1 = quaternionic (symplectic), 0 = complex
indicator_map = {1: "real (orthogonal)", -1: "quaternionic (symplectic)", 0: "complex"}
print(f"V_23 type: {indicator_map.get(int(fs[23]), 'unknown')}")

print()
print("All irrep dimensions and Frobenius-Schur indicators:")
print("-" * 50)
for i in range(len(irreps)):
    dim = int(irreps[i][0])
    fs_i = int(fs[i])
    indicator = {1: "real", -1: "quat", 0: "cplx"}.get(fs_i, str(fs_i))
    print(f"  V_{i:2}: dim={dim:3}, F-S={indicator}")

# Check tensor products
print()
print("=== Tensor Products ===")
print("V_23 ⊗ V_23 decomposition:")
chi_23_gap = irreps[23]
chi_squared = chi_23_gap * chi_23_gap
decomp = char_table.ScalarProduct(chi_squared, chi_23_gap)
print(f"  <V_23 ⊗ V_23, V_23> = {decomp}")

# Full decomposition of V_23 ⊗ V_23
print("\nV_23 ⊗ V_23 = ", end="")
first = True
for i in range(len(irreps)):
    mult = int(char_table.ScalarProduct(chi_squared, irreps[i]))
    if mult > 0:
        if not first:
            print(" ⊕ ", end="")
        dim_i = int(irreps[i][0])
        if mult > 1:
            print(f"{mult}×V_{i}({dim_i})", end="")
        else:
            print(f"V_{i}({dim_i})", end="")
        first = False
print()
print(f"Total: {sum(int(char_table.ScalarProduct(chi_squared, irreps[i])) * int(irreps[i][0]) for i in range(len(irreps)))}")
print(f"Expected: 81² = {81*81}")
