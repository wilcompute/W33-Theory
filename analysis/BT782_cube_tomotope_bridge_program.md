# BT782 — Cube/Tomotope Bridge Program

BT781 showed that the two order-48 groups are not the same:

```text
cube chart half:       C2^3 : S3
tomotope chiral half:  C2^4 : C3
```

This is the first clean algebraic formulation of the bridge problem.

## The bridge equation

Since

```text
C2^3 : S3  = C2^3 : (C3 ⋊ C2)
C2^4 : C3  = (C2^3 × C2_chiral) : C3
```

there is a natural exchange:

```text
cube reflection bit  <-->  tomotope chiral binary bit
```

So the desired bridge is not an isomorphism.  It is a **phase lift**:

```text
BT782 bridge = forget S3/C3 reflection sign, then attach a new chirality bit.
```

Symbolically:

```text
C2^3 : S3
   -> C2^3 : C3                orientation-preserving cube half, order 24
   -> C2^4 : C3                chiral binary lift, order 48
```

## Why this matters

This is exactly parallel to the CE2 / L∞ phase-lift mechanism described in the
GraphTheory snippet: a grade-level object has a finite obstruction; the repair is
not a lookup table but a coherent phase/binary lift.  There, the missing cocycle
is repaired by a Weyl-Heisenberg / metaplectic phase.  Here, the missing bit is
repaired by replacing the cube reflection sign with a tomotope chiral bit.

The likely dictionary is:

```text
cube C2^3                  = Q3 translation/address bits
cube S3/C3 reflection      = orientation-reversing dimension permutation
tomotope C2^4              = 4-rank flag parity / hemicubic bit system
tomotope C3                = oriented triality around the rank-4 maniplex
```

## Concrete targets for the next verifier

1. Compute the orientation-preserving cube subgroup:

```text
(C2^3 : S3)^+ = C2^3 : C3, order 24
```

2. Compute the tomotope derived subgroup:

```text
Gamma(T)' = C2^4 : C3, order 48
```

3. Exhibit a surjection or embedding pattern:

```text
Gamma(T)' / C2_chiral  ≅  C2^3 : C3
```

If true, then the bridge is exact:

```text
tomotope derived half is a central C2 extension of the orientation-preserving
cube-chart half.
```

That would be the cleanest possible statement:

```text
1 -> C2_chiral -> Gamma(T)' -> Aut^+(Q3) -> 1
```

## Why the order-48 clue was so strong

The prior repo already knew:

```text
Tomotope flags = 192 = 4 * 48
Tomotope symmetry = 96 = 2 * 48
W33 directed edges / EH action = 480 = 10 * 48
```

BT780 added:

```text
cube chart stabilizer = 48
```

BT781 sharpened this into:

```text
48 is not a single group; it is an exchange currency.
```

The cube spends its 48 as `three bits + full S3`; the tomotope spends its 48 as
`four bits + oriented C3`.  The missing bridge is the exchange rate.

## Status

This file records the program.  The next code check should test whether
`Gamma(T)'` has a normal central/noncentral C2 quotient isomorphic to
`Aut^+(Q3) = C2^3:C3`.  If yes, BT782 becomes a theorem; if no, the obstruction
itself should be the next CE2 cocycle.
