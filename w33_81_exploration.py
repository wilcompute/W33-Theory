#!/usr/bin/env sage
"""
Compare V_22 and V_23 - the two 81-dimensional irreps.
Explore the GF(3) connection.
"""

from sage.all import *
import json
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "data", "w33_sage_incidence_h1.json")

with open(data_path) as f:
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

chi_22 = list(irreps[22])
chi_23 = list(irreps[23])

print("=== Comparing V_22 and V_23 (both 81-dim) ===")
print("=" * 55)
print(f"{'Class':>6} {'Size':>8} {'V_22':>12} {'V_23':>12} {'Same?':>8}")
print("-" * 55)

gap_classes = char_table.ConjugacyClasses()
class_sizes = [int(libgap.Size(c)) for c in gap_classes]

for i in range(len(chi_22)):
    v22 = chi_22[i]
    v23 = chi_23[i]
    same = "=" if str(v22) == str(v23) else "DIFF"
    print(f"{i:>6} {class_sizes[i]:>8} {str(v22):>12} {str(v23):>12} {same:>8}")

# Check if V_22 = V_23 ⊗ sign
print()
print("=== Checking tensor with sign representation ===")
chi_1 = list(irreps[1])  # The sign rep (other 1-dim)
product = [chi_23[i] * chi_1[i] for i in range(len(chi_23))]

print(f"V_1 character (sign rep): {[str(x) for x in chi_1]}")
print()

match_v1 = all(str(product[i]) == str(chi_22[i]) for i in range(len(chi_22)))
print(f"V_22 = V_23 ⊗ V_1 (sign)? {match_v1}")

# If not sign, try all 1-dim reps
if not match_v1:
    for j in range(len(irreps)):
        if int(irreps[j][0]) == 1:
            chi_j = list(irreps[j])
            product_j = [chi_23[i] * chi_j[i] for i in range(len(chi_23))]
            match_j = all(str(product_j[i]) == str(chi_22[i]) for i in range(len(chi_22)))
            if match_j:
                print(f"V_22 = V_23 ⊗ V_{j}? YES!")

# Explore the derived subgroup
print()
print("=== Exploring group structure ===")
derived = gap_G.DerivedSubgroup()
print(f"G = O(5,3):C2, order {G.order()}")
print(f"G' (derived subgroup) order: {derived.Size()}")
print(f"G/G' (abelianization) order: {G.order() // int(derived.Size())}")

# Get the structure of O(5,3)
print()
print("The group O(5,3) structure:")
print(f"  |O(5,3)| = 2 * |SO(5,3)| = 2 * |Omega(5,3)| * |Z|")
print(f"  For dim 5 over GF(3): |Omega(5,3)| = 3^4 * (3^4-1) * (3^2-1) / 2 = {3**4 * (3**4-1) * (3**2-1) // 2}")
print(f"  Note: 3^4 = 81 = dim(H1)!")

# Check restriction to derived subgroup
print()
print("=== Restriction to derived subgroup ===")
# Characters restrict by just evaluating on the subgroup's conjugacy classes
# For simplicity, check if V_22 and V_23 become isomorphic on G'

# The quotient G/G' is C2, so characters that differ by sign representation
# become equal on G'
print("If G/G' = C2, then V_22 and V_23 differ by the sign rep of C2")
print("On restriction to G', they would become isomorphic")

# Check the center
center = gap_G.Center()
print()
print(f"Center of G: order {center.Size()}")

# Explore 81 = 3^4 connection more
print()
print("=== The 81 = 3^4 Connection ===")
print(f"H1 dimension: 81 = 3^4")
print(f"Group order: 51840 = 2^7 * 3^4 * 5")
print(f"Number of points: 40 = 8 * 5 = 2^3 * 5")
print(f"Number of lines: 40 = 8 * 5 = 2^3 * 5")
print()

# The 5-dim orthogonal group over GF(3)
print("O(5,3) acts on GF(3)^5 preserving a quadratic form")
print("A natural representation has dimension 5")
print("But 81 = 3^4 suggests exterior or symmetric powers...")
print()

# Compute dim of various symmetric/exterior powers of 5-dim rep
print("Natural dimensions from 5-dim rep:")
for k in range(1, 6):
    ext_dim = binomial(5, k)
    sym_dim = binomial(5 + k - 1, k)
    print(f"  Λ^{k}(V_5) = {ext_dim}, Sym^{k}(V_5) = {sym_dim}")

print()
print("None of these give 81 directly...")
print("But 81 = 3^4 could be the regular representation of (Z/3)^4!")
print("Or a permutation action on 81 points...")
