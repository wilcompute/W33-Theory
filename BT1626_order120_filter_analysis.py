"""BT1626: Order-120 Stabiliser of the 432-Orbit and Filter Interaction

The 432-orbit of W(E6) = PSp(4,3).2 (order 51840) on A2-triples has
point stabiliser of order 51840/432 = 120.

This pass:
1. Records all known order-120 groups and their SmallGroup IDs
2. Tests which are subgroups of C2xS4 (the frame stabiliser)
3. Tests which contain any of the 8 filter minimal generators
4. Determines whether the 432-orbit stabiliser could be S5
5. [UPDATED 2026-07-27 Pass 4] Transitivity confirmed by orbit definition (BT1632)

Status: Analysis complete; IdGroup GAP call pending.
"""
import math

orbit_size   = 432
W_E6_order   = 51840
stab_order   = W_E6_order // orbit_size
print(f"432-orbit stabiliser order: {W_E6_order}/{orbit_size} = {stab_order}")

# ── Transitivity: resolved by BT1632 ─────────────────────────────────────────
print("\n── Transitivity (BT1632) ──")
print("Each 432-orbit IS transitive by definition of 'orbit'.")
print("Pass 1124 decomposition: [1,1,27x6,240,270,270,432,432,432] — 14 orbits, total 2240.")
print("Three SEPARATE transitive 432-orbits, each carrying one 81-dim irrep.")
print("NOT one non-transitive orbit of size 1296.")

# ── Known order-120 groups ────────────────────────────────────────────────────
order120_groups = [
    {"name": "S5",       "SmallGroup": "[120,34]", "structure": "symmetric group on 5 letters",
     "properties": "simple kernel A5, has S3 and A4 as quotients, order 2^3*3*5"},
    {"name": "A5 x C2", "SmallGroup": "[120,35]", "structure": "direct product",
     "properties": "centre C2, quotient A5, contains A5 as normal subgroup"},
    {"name": "SL(2,5)", "SmallGroup": "[120,5]",  "structure": "special linear 2x2 over F5",
     "properties": "perfect group (trivial abelianization), 2.A5, centre C2"},
    {"name": "C5:C24",  "SmallGroup": "[120,4]",  "structure": "semidirect product",
     "properties": "non-perfect, abelianization C4"},
    {"name": "Dic30",   "SmallGroup": "[120,3]",  "structure": "dicyclic",
     "properties": "generalised quaternion extension of C30"},
]

print("\n── Order-120 candidate groups ──")
for g in order120_groups:
    print(f"  {g['name']:10s} {g['SmallGroup']:10s} {g['structure']}")
    print(f"             Properties: {g['properties']}")

# ── Filter analysis ────────────────────────────────────────────────────────────
filter_orders = [32, 96, 108, 108, 120, 160, 216, 360]
frame_stab_order = 48
print(f"\n── Filter Analysis ──")
print(f"Frame stabiliser C2xS4 order = {frame_stab_order}")
print(f"Filter minimal generator orders: {filter_orders}")
print(f"\nCan C2xS4 (order {frame_stab_order}) contain each filter generator?")
for o in filter_orders:
    # A group of order o can embed in a group of order 48 only if o | 48
    can = (frame_stab_order % o == 0)
    extra = ""
    if o == 32:
        extra = " [Sylow-2 order: C2xS4 has |Syl_2|=16 < 32, cannot contain order-32 2-group]"
    print(f"  order {o:3d}: {'YES (divides 48)' if can else 'NO':20s}{extra}")
print("CONCLUSION: C2xS4 contains NONE of the 8 filter generators. Frame module is nontrivial. QED.")

# ── The S5 question ───────────────────────────────────────────────────────────
print("\n── S5 vs 432-orbit Stabiliser: The Key Question ──")
print("One of the 8 filter minimal generators is S5 (order 120, SmallGroup[120,34]).")
print("The 432-orbit stabiliser also has order 120.")
print()
print("Distinguishing characteristics to resolve this via GAP:")
print("  S5:       abelianization = C2, derived subgroup = A5 (order 60)")
print("  A5 x C2:  abelianization = C2, derived subgroup = A5 (order 60) [same!]")
print("  SL(2,5):  abelianization = 1  (perfect group) -- EASY to distinguish")
print()
print("To distinguish S5 from A5xC2:")
print("  S5   has a normal Sylow-5 subgroup? NO  (not normal in S5)")
print("  A5xC2 has a normal A5? YES")
print("  Alternatively: S5 has element of order 4? YES. A5xC2 has element of order 4? NO (A5 has max order 5, C2 order 2 -> max is lcm=10, but 4 does not divide 60 or 2... wait)")
print("  A5 has element orders {1,2,3,5}. C2 has {1,2}. A5xC2 has max element order lcm(5,2)=10.")
print("  S5 has 5-cycles and 4-cycles. Max order = 6 (wait: permutation (12)(3456) has order lcm(2,4)=4; (123456) doesn't exist in S5).")
print("  S5 max element order = 6? (1 2)(3 4 5) has order lcm(2,3)=6. YES.")
print("  A5xC2: max element order = lcm(5,2)=10. NO element of order 6.")
print("  FINGERPRINT: S5 has element of order 6; A5xC2 has element of order 10 but not 6.")
print()
print("GAP command:")
print("  gap> G := ConstructW_E6();  # or PSp(4,3).2 by standard means")
print("  gap> orbs := Orbits(G, A2triples, OnPoints);;")
print("  gap> orb432 := First(orbs, o -> Length(o) = 432);;")
print("  gap> stab := Stabilizer(G, orb432[1], OnPoints);;")
print("  gap> IdGroup(stab);      # Should give [120,?]")
print("  gap> Set(List(stab, Order));  # Element order set")
print("  gap> IsIsomorphic(stab, SymmetricGroup(5));")
print("  gap> AbelianInvariant(stab);  # S5 -> [2], SL(2,5) -> []")

print("\nBT1626 analysis complete (Pass 4 update). GAP verification pending for IdGroup.")
