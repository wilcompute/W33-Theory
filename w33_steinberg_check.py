#!/usr/bin/env sage
"""
Check if H1 = V_23 is the Steinberg representation of O(5,3).

The Steinberg representation is a famous representation of groups of Lie type
that has dimension q^N where N is the number of positive roots and q is the
field size. For O(5,3), q=3.

Key property: Steinberg rep restricted to a Sylow p-subgroup gives
the regular representation.
"""

import json

from sage.all import *

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
perms = [S(Permutation([p + 1 for p in perm])) for perm in perm_gens]
G = PermutationGroup(perms)

gap_G = libgap(G)

print("=== Is H1 the Steinberg Representation? ===")
print()

# Background on Steinberg representation
print("Background: The Steinberg representation")
print("-" * 50)
print("For a group of Lie type over GF(q), the Steinberg representation:")
print("  1. Has dimension q^N where N = # positive roots")
print("  2. Restricts to regular representation on Sylow p-subgroup")
print("  3. Is irreducible and faithful")
print("  4. Has Frobenius-Schur indicator +1 (real)")
print()

# For O(5,3) = orthogonal group in dimension 5 over GF(3)
# This is related to type B_2 or D_3 depending on form
print("For O(5,3) (type B_2 or related):")
print("  Field: q = 3")
print("  Type B_2 has N = 4 positive roots")
print("  So Steinberg dimension would be 3^4 = 81 ✓")
print()

# We already know:
print("What we've established:")
print("  ✓ dim(H1) = 81 = 3^4")
print("  ✓ H1 = V_23 is irreducible")
print("  ✓ V_23 is faithful")
print("  ✓ F-S indicator = +1 (real)")
print("  ✓ V_23|_P = regular rep of Sylow 3-subgroup")
print()
print("ALL these match the Steinberg representation!")
print()

# Additional check: degree of Steinberg
# For O_n(q) with n odd, the Steinberg has degree q^{(n-1)(n-2)/4}
# Wait, that doesn't work for n=5...

# Actually for O(5,3), we need to be more careful about the type
# The group O(5,3) has structure depending on the discriminant of the form

print("=== More detailed analysis ===")
print()

# Get the derived series
derived = gap_G.DerivedSubgroup()
derived2 = derived.DerivedSubgroup()
print(f"G = O(5,3):C2, order {G.order()}")
print(f"G' order: {derived.Size()}")
print(f"G'' order: {derived2.Size()}")

# Check if G' is simple
is_simple = derived.IsSimple()
print(f"G' is simple: {is_simple}")

if is_simple:
    print()
    print("G' is simple! This is likely Omega(5,3) ≅ PSp(4,3)")
    print()
    # PSp(4,3) has Steinberg rep of dimension 3^4 = 81
    print("For PSp(4,3) (type C_2 = B_2):")
    print("  Root system C_2 has 4 positive roots")
    print("  Steinberg dimension = 3^4 = 81 ✓")

# Check character table name if available
print()
print("=== Checking GAP's character table library ===")
try:
    # Try to identify the group
    id_info = gap_G.IdGroup()
    print(f"GAP IdGroup: {id_info}")
except:
    print("Group too large for IdGroup")

# Check the number of conjugacy classes
char_table = gap_G.CharacterTable()
num_classes = len(list(char_table.ConjugacyClasses()))
print(f"Number of conjugacy classes: {num_classes}")

# The character of Steinberg representation has a special property:
# It's supported only on semisimple elements (elements of order coprime to p)
print()
print("=== Checking support of V_23 character ===")
irreps = char_table.Irr()
chi_23 = irreps[23]
gap_classes = char_table.ConjugacyClasses()

print("Elements where V_23 has non-zero character:")
for i, c in enumerate(gap_classes):
    rep = c.Representative()
    order = int(rep.Order())
    chi_val = chi_23[i]
    if chi_val.IsInt():
        val = int(chi_val)
    else:
        val = complex(str(chi_val.sage()))

    if val != 0:
        # Check if order is coprime to 3
        coprime_to_3 = (order % 3 != 0) or order == 1
        p_part = 1
        temp = order
        while temp % 3 == 0:
            p_part *= 3
            temp //= 3
        print(
            f"  Class {i}: order={order}, chi={val}, 3-part={p_part}, coprime to 3: {coprime_to_3}"
        )

print()
print("For Steinberg rep, non-zero values occur only on semisimple elements")
print("(those with order coprime to p=3)")
