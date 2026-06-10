# BT749 — The Dihedral Phase Theorem: Lifts are Reflections of D12

The local capstone of the BT745-BT748 chain.  Every pair-involution
stabilizes its own rectangle, so the lift structure of a rectangle R can be
read inside Stab_PGSp(R).  Exact results (one rectangle suffices, by
transitivity):

## T1: the rectangle stabilizer is dihedral

```text
Stab_PGSp(R) has order 24 = Z12 (inner, BT746) + 12 outer elements
ALL 12 outer elements are involutions  =>  Stab_PGSp(R) = D12.
```

## T2: lifts -> reflections, two-to-one

All 24 lifts of R (both chiralities) have their canonical BT747 involution
inside this single copy of D12, hitting all 12 reflections exactly 2-to-1:
each reflection fixes exactly 2 lifts.

## T3: the reflection classes ARE the chiralities

Z12-conjugation splits the 12 reflections of D12 into two classes of 6
(the standard even-dihedral split).  Measured against lift labels:

```text
reflection class 0:  all 12 mask-weight-2 lifts (Type-B)
reflection class 1:  all 12 mask-weight-3 lifts (Type-A)
```

The global chirality invariant of BT745/BT746 is, locally at every
rectangle, the even/odd reflection-class split of D12.  This EXPLAINS
absoluteness: rotations of D12 can never mix the two reflection classes,
and the geometry supplies no outer automorphism that would.

## The selector datum, fully factored

Choosing one of the 12 chiral lifts of a rectangle decomposes canonically:

```text
12  =  6 (dihedral phase: which reflection of the chiral class)
     x 2 (residual duo: which of the 2 lifts fixed by that reflection)
```

Combined with BT746 (Z12 = Z4 x Z3 rotation clock) and BT748 (coordinates
540 x 2 x 48), the BT705 "hinge datum" is now completely factored into
elementary group-theoretic choices: a dihedral phase, a duo bit, against
the rotation clock.  Substrate readings: 24 = f lifts per rectangle,
12 = k reflections, 6 = q! phases, 2 = lambda duo.

## The full session architecture (BT739-BT749)

```text
GLOBAL                                  LOCAL (per rectangle)
Steinberg = chart81 = LeviE4 (742)      D12 stabilizer (749)
Tits building, apartments (744)         24 lifts -> 12 reflections, 2:1
two torsors, chirality (745,746)        chirality = reflection classes
root triples 540 x 2 x 48 (747,748)     hinge = phase(6) x duo(2)
braid words sigma^5 = Z (740)           Z12 = Z4 x Z3 rotation clock
flat F2^4 register (741)
```

## Boundary

Open: what distinguishes the 2 lifts sharing a reflection (the duo bit) -
conjecturally the BT741 flat-bundle gluing orientation; whether choosing
"the same dihedral phase everywhere" (possible after one global base
choice, by BT748 torsor coordinates) yields the root-natural selector that
repairs BT748's non-uniformity; and the Q(4,3) mirror of the whole D12
structure.
