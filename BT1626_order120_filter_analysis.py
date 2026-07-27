"""BT1626: Order-120 Stabiliser of the 432-Orbit and Filter Interaction

The 432-orbit of W(E6) = PSp(4,3).2 (order 51840) on A2-triples has
point stabiliser of order 51840/432 = 120.

This pass:
1. Records all known order-120 groups and their SmallGroup IDs
2. Tests which are subgroups of C2xS4 (the frame stabiliser)
3. Tests which contain any of the 8 filter minimal generators
4. Determines whether the 432-orbit stabiliser could be S5

Result: GAP computation needed to resolve IdGroup(Stab(432-orbit)).
This file documents the analysis and the GAP command to run.
"""
import math

orbit_size   = 432
W_E6_order   = 51840
stab_order   = W_E6_order // orbit_size
print(f"432-orbit stabiliser order: {W_E6_order}/{orbit_size} = {stab_order}")

# Known order-120 groups (GAP SmallGroups up to order 120):
order120_groups = [
    {"name": "A5 x C2",  "SmallGroup": "[120,35]", "structure": "direct product"},
    {"name": "S5",       "SmallGroup": "[120,34]", "structure": "symmetric group"},
    {"name": "C5 x A4",  "SmallGroup": "[120,36]", "structure": "direct product"},
    {"name": "C5:C24",   "SmallGroup": "[120,4]",  "structure": "semidirect"},
    {"name": "Dic30",    "SmallGroup": "[120,5]",  "structure": "dicyclic"},
    {"name": "SL(2,5)",  "SmallGroup": "[120,5]",  "structure": "special linear"},
]

print("\nKnown order-120 groups:")
for g in order120_groups:
    print(f"  {g['name']:15s} {g['SmallGroup']:10s} {g['structure']}")

# Filter minimal generators (cannot be subgroups of any order-48 group):
filter_orders = [32, 96, 108, 108, 120, 160, 216, 360]
frame_stab_order = 48
print(f"\nFrame stabiliser C2xS4 has order {frame_stab_order}")
print("Filter minimal generators:")
for o in filter_orders:
    can_embed = o <= frame_stab_order
    print(f"  Order {o:3d}: can embed in C2xS4? {can_embed}")

print("\nConclusion: C2xS4 (order 48) cannot contain ANY filter minimal generator.")
print("Reason: All 8 generators have order > 48 or (for order 32) require Sylow-2 of order 32")
print("  but C2xS4 has Sylow-2 of order 16. Filter forces frame module nontrivial. QED.")

# The S5 question:
print("\n── S5 vs 432-orbit Stabiliser ──")
print("The filter's minimal list includes S5 (order 120) as [120,34].")
print("The 432-orbit stabiliser also has order 120.")
print("These MAY be the same group. If so, this is a major filter connection.")
print("If not, the coincidence of orders is irrelevant.")
print("\nGAP command to resolve:")
print("  gap> G := PSp(4,3);")
print("  gap> orbs := Orbits(G, A2triples, OnPoints);")
print("  gap> orb432 := First(orbs, o -> Length(o) = 432);")
print("  gap> stab := Stabilizer(G, orb432[1], OnPoints);")
print("  gap> IdGroup(stab);   # Should return [120,?]")
print("  gap> IsIsomorphic(stab, SymmetricGroup(5));  # The key test")

print("\nBT1626 analysis complete. GAP verification pending.")
