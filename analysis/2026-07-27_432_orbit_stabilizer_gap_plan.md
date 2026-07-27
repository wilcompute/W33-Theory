# Step 3 — 432-Orbit Stabilizer Computational Plan (GAP)

**Date:** 2026-07-27  
**Context:** Three 432-orbits under `Sp(4,3)` carry Steinberg-bearing structures.
Each has a point-stabilizer of order `|Sp(4,3)|/432 = 25920/432 = 60`,
which is consistent with either `A₅ ≅ PSL(2,5)` or other order-60 groups.
The question is whether all three stabilizers are conjugate in `Sp(4,3)`,
or represent distinct isomorphism types — and specifically whether any
are isomorphic to `S₅` (order 120) rather than order-60 groups.

**Correction from other assistant:** The other assistant's Top 5 labels these
as "order-120 stabilizers". If `|Sp(4,3)| = 25920` and orbit size is 432,
then the stabilizer order is exactly 60, not 120. The GAP script below
computes the actual order to resolve this.

## GAP Script

```gap
# GAP computation for 432-orbit stabilizers in Sp(4,3)
# Run: gap -q analysis/w33_432_orbit_stabilizer.g

LoadPackage("grape");

# Construct Sp(4,3)
G := Sp(4, 3);
Print("Group order: ", Order(G), "\n");  # Expected: 25920

# Construct the W(3,3) collinearity graph on projective points of PG(3,3)
# Points of PG(3,3): 1-dim subspaces of GF(3)^4, total = (3^4-1)/(3-1) = 40
# Symplectic form: standard J = [[0,0,0,1],[0,0,1,0],[0,-1,0,0],[-1,0,0,0]]
# Two points are adjacent iff their symplectic product = 0

# Action of G on the 40 points
pts := Orbit(G, [1,0,0,0]*Z(3)^0, OnLines);
Print("Number of points: ", Length(pts), "\n");  # Expected: 40

# Identify orbits of G on triples or pairs (to find 432-orbits)
# The 432 comes from the number of ordered/unordered triples of a specific type
# Here we look for G-orbits on ordered pairs of collinear non-equal points
orb_pairs := Orbits(G, Combinations(pts, 2), OnSets);
Print("Number of G-orbits on 2-element subsets: ", Length(orb_pairs), "\n");
for orb in orb_pairs do
  Print("  Orbit size: ", Length(orb), "\n");
od;

# For each orbit of size 432 (if found), compute stabilizer
for orb in orb_pairs do
  if Length(orb) = 432 then
    stab := Stabilizer(G, orb[1], OnSets);
    Print("Stabilizer order: ", Order(stab), "\n");
    id := IdGroup(stab);
    Print("GAP IdGroup: ", id, "\n");
    Print("IsAbelian: ", IsAbelian(stab), "\n");
    Print("IsSolvable: ", IsSolvable(stab), "\n");
    Print("Abelianization order: ", Order(CommutatorFactorGroup(stab)), "\n");
    ords := Collected(List(Elements(stab), Order));
    Print("Element order spectrum: ", ords, "\n");
    # Conjugacy test with other 432-orbit stabilizers
  fi;
od;

# Test whether the three 432-orbit stabilizers are conjugate in G
stabs_432 := [];
for orb in orb_pairs do
  if Length(orb) = 432 then
    Add(stabs_432, Stabilizer(G, orb[1], OnSets));
  fi;
od;

if Length(stabs_432) >= 2 then
  for i in [1..Length(stabs_432)-1] do
    for j in [i+1..Length(stabs_432)] do
      conj := RepresentativeAction(G, stabs_432[i], stabs_432[j], OnPoints);
      if conj <> fail then
        Print("Stabilizers ", i, " and ", j, " ARE conjugate in G\n");
      else
        Print("Stabilizers ", i, " and ", j, " are NOT conjugate in G\n");
      fi;
    od;
  od;
fi;

Print("Done.\n");
```

## Expected outcomes and interpretation

| Result | Implication |
|---|---|
| All three stabs conjugate, IdGroup = [60,5] = A₅ | Single orbit type, Steinberg-bearing A₅ class |
| All three stabs conjugate, IdGroup = [60,1] | Cyclic or other order-60 group |
| Stabs non-conjugate | Three distinct classes; Steinberg localization is class-specific |
| Stab order = 120, IdGroup = [120,34] = S₅ | Orbit size is 216, not 432 — recheck orbit census |

## Connection to the corrected spectrum

The 432-orbit structure lives on the point carrier of W(3,3), which now has
the canonical `1 + 24 + 15` eigenspace decomposition. If the Steinberg-bearing
orbits correspond to a specific eigenspace projection, the stabilizer type
should align:

- The 24-dimensional eigenspace of D (eigenvalue 1) is the "middle" isotypic
  component and is the most likely carrier of non-trivial stabilizer structure.
- The 15-dimensional eigenspace (eigenvalue −5) corresponds to the complement
  and may carry the Steinberg module directly.

## Status

- [x] GAP script written
- [ ] GAP script executed (requires local GAP installation)
- [ ] IdGroup computed for each 432-orbit stabilizer
- [ ] Conjugacy test completed
- [ ] Result cross-referenced with Steinberg module decomposition (Step 4)
