#!/usr/bin/env sage
"""
Explore the Sylow 3-subgroup and its relationship to H1.
The Sylow 3-subgroup has order 3^4 = 81 = dim(H1)!
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

print("=== Sylow 3-subgroup Analysis ===")
print(f"G = O(5,3):C2, order {G.order()} = 2^7 * 3^4 * 5")
print()

# Get Sylow 3-subgroup
sylow3 = gap_G.SylowSubgroup(3)
print(f"Sylow 3-subgroup P:")
print(f"  Order: {sylow3.Size()} = 3^4 = 81")
print(f"  Is abelian: {sylow3.IsAbelian()}")
print(f"  Is elementary abelian: {sylow3.IsElementaryAbelian()}")

# Structure of Sylow 3-subgroup
print()
print("Structure of P:")
print(f"  {sylow3.StructureDescription()}")

# If elementary abelian, it's (Z/3)^4
if sylow3.IsElementaryAbelian():
    print("  P ≅ (Z/3)^4 - elementary abelian of rank 4")
    print()
    print("  This means P is a 4-dimensional vector space over GF(3)!")
    print("  And dim(H1) = |P| = 3^4 = 81")

# Conjugacy classes in P
p_classes = sylow3.ConjugacyClasses()
print(f"\n  Conjugacy classes in P: {len(list(p_classes))}")

# Center of P
center_p = sylow3.Center()
print(f"  Center of P: order {center_p.Size()}")

# Normalizer of P in G
normalizer = gap_G.Normalizer(sylow3)
print(f"\nNormalizer N_G(P):")
print(f"  Order: {normalizer.Size()}")
print(
    f"  Index [G : N_G(P)] = {G.order() // int(normalizer.Size())} (= number of Sylow 3-subgroups)"
)

# The quotient N_G(P)/P is important - it's how G acts on P
quotient_order = int(normalizer.Size()) // 81
print(f"  |N_G(P)/P| = {quotient_order}")

# Restriction of V_23 to P
print()
print("=== Restriction of H1 = V_23 to Sylow 3-subgroup ===")

# Get character table of P
p_char_table = sylow3.CharacterTable()
p_irreps = p_char_table.Irr()
print(f"Number of irreps of P: {len(list(p_irreps))}")

# For elementary abelian (Z/3)^4, all irreps are 1-dimensional
# There are 81 of them
if sylow3.IsElementaryAbelian():
    print("Since P is elementary abelian, all irreps of P are 1-dimensional")
    print(f"P has {81} irreducible 1-dim representations")
    print()
    print("The restriction of an 81-dim rep to P would decompose as")
    print("a sum of 1-dim reps. If it's the regular representation,")
    print("each 1-dim rep appears exactly once!")

# Check if V_23 restricted to P is the regular representation
print()
print("=== Checking if V_23|_P is the regular representation ===")

# The regular representation of P has character:
# chi_reg(e) = |P| = 81
# chi_reg(g) = 0 for g ≠ e

# Get V_23 character
char_table = gap_G.CharacterTable()
irreps = char_table.Irr()
chi_23 = irreps[23]

# Restrict to P by evaluating on elements of P
# For elementary abelian P, we just need to check:
# - chi(e) = 81 ✓
# - chi(g) = 0 for all g ≠ e in P

# Get elements of P
p_elements = list(sylow3.Elements())
print(f"Checking character on {len(p_elements)} elements of P...")

# Compute character values on P
chi_on_p = {}
for g in p_elements:
    order_g = int(g.Order())
    if order_g not in chi_on_p:
        chi_on_p[order_g] = []
    # Find which conjugacy class of G this element belongs to
    # Use GAP to find class
    class_idx = gap_G.ConjugacyClass(g)
    rep = class_idx.Representative()

    # Find the index in the character table
    gap_classes = char_table.ConjugacyClasses()
    for i, c in enumerate(gap_classes):
        if rep in c:
            chi_val = chi_23[i]
            chi_on_p[order_g].append(
                int(chi_val) if chi_val.IsInt() else complex(str(chi_val.sage()))
            )
            break

print("\nCharacter values on P by element order:")
for order, vals in sorted(chi_on_p.items()):
    unique_vals = set(int(v) if isinstance(v, (int, float)) else v for v in vals)
    print(f"  Order {order}: {len(vals)} elements, values: {unique_vals}")

# Count non-zero values
identity_count = sum(1 for o, vs in chi_on_p.items() if o == 1)
nonidentity_zero = sum(1 for o, vs in chi_on_p.items() if o > 1 for v in vs if v == 0)
total_nonidentity = sum(len(vs) for o, vs in chi_on_p.items() if o > 1)

print(f"\nIdentity has chi = 81 ✓")
print(f"Non-identity elements with chi = 0: {nonidentity_zero}/{total_nonidentity}")

if nonidentity_zero == total_nonidentity:
    print("\n★ V_23 restricted to P IS the regular representation! ★")
    print("  This explains why dim(H1) = |P| = 3^4 = 81")
else:
    print("\n  V_23|_P is NOT the regular representation")
    print("  Need to investigate further...")
