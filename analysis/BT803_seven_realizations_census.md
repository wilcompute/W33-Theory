# BT803 — The Seven Realizations: Census, Repair, and the Frobenius Echo

Machine verification of data/Toroidal-Polyhedra-Realizations.txt:
5 Csaszar + 2 Szilassi = 7 geometric realizations of the two genus-1
seven-objects (7 vertices / 7 faces, mutually dual).

## Verified exactly

```text
T1  all 7: V - E + F = 0 (genus 1), 21 = q*Phi6 edges each
T2  |Aut(Moebius 7-torus)| = 42 = lambda*q*Phi6 = Frobenius Z7:Z6
    element orders {1:1, 2:7, 3:14, 6:14, 7:6}
    -> the order SET {1,2,3,6,7} = substrate primitives {1,lambda,q,q!,Phi6}
T3  SYMMETRY BREAKING: every realization keeps EXACTLY C2 of the 42
    combinatorial symmetries; breaking index 42/2 = 21 = edge count.
    Csaszar C2 fixes exactly 1 vertex (3 free pairs + 1);
    Szilassi C2 is FREE (7 free pairs, 0 fixed) - the dual pair breaks
    symmetry in dual ways (pointed vs free).
T4  all stated closed-form volumes verified (rel err <= 2e-16):
    C1 = 125 = F_5^3 EXACT     C2 = 16(21 sqrt15 - 2)
    C3 = 72(11 - 2 sqrt2)      C4 = 2644 sqrt2 / 3    C5 = 816 sqrt2
    S1 = 5226/5                S2 = 7976/9
    volume number fields: {Q, Q(sqrt15), Q(sqrt2) x3, Q, Q}
T5  Szilassi hexagons are EXACTLY planar (Fraction determinant proof)
T6  distinct edge lengths: C 10,9,9,8,9 | S 12,11
```

## Dataset repair

Csaszar version 3 uses a constant C0 in its vertex coordinates but never
defines it (the only omission in the file).  The edge table forces it:
2*C0 = 12 sqrt2 (edge 7) and |V0V6| = sqrt(144 + 4 C0^2) = 12 sqrt3
(edge 8) both give

```text
C0 = 6 sqrt2,
```

validated by the exact volume reproduction 72(11 - 2 sqrt2) at 2e-16.

## The Frobenius echo (the user's 7-of-7 observation, sharpened)

The combinatorial symmetry group F42 = Z7:Z6 has EXACTLY 7 involutions
(order profile 2:7, one per vertex of Z7).  Exactly 7 geometric
realizations are known, and each realizes exactly ONE involution.

```text
7 involutions in F42   <->   7 known realizations (5 Csaszar + 2 Szilassi)
```

All 7 involutions are conjugate, so the correspondence is not canonical -
but the count match is the precise form of the observation that the
seven-objects' realization census is itself "about 7".  Splitting 7 = 5+2:
5 = F_5 Csaszar shapes (volume fields Q, Q(sqrt15), Q(sqrt2)^3), 2 =
lambda Szilassi shapes (both rational volumes).  The dual pair splits the
involution geometry: pointed (vertex-fixing) on the Csaszar side, free on
the Szilassi side.

## Substrate ledger

```text
42 = lambda * q * Phi6      combinatorial symmetry budget
21 = q * Phi6               edges = symmetry breaking index
14 = lambda * Phi6          Csaszar faces = Szilassi vertices
 7 = Phi6                   vertices/faces, involutions, realizations
 6 = q!                     Frobenius complement Z6 = clock quotient (BT774)
125 = F_5^3                 volume of the canonical Csaszar realization
```

## Boundary

Open: whether more realizations exist (the census is the known list, not
a completeness theorem - Bokowski-style oriented matroid enumeration
would decide); the C2 axes as substrate duo bits (the Csaszar fixed
vertex vs the BT776 corner-center); and transporting the 7-realization
volume fields {Q, Q(sqrt15), Q(sqrt2)} onto the W33 eigenvalue fields
{Q, Q(sqrt10), Q(sqrt73)} of the cube web (BT777).
