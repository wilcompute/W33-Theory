# Part CXVII — Qutrit MUB Meaning of the Spread-Intersection Geometry

Status: theorem-grade structural extension  
Date: April 28, 2026

The existing qutrit foundation proves:

```text
W(3,3) = two-qutrit Pauli commutation geometry.
```

This part attaches the recent spread/Sylvester/Petersen graph work to that qutrit foundation.

## Dictionary

```text
vertex = projective nonidentity two-qutrit Pauli observable.
edge = commuting Pauli pair.
line = maximal commuting Pauli context.
spread = complete two-qutrit stabilizer MUB frame.
```

A line contains four projective Pauli rays. Including powers and identity, it is a maximal abelian two-qutrit Pauli subgroup and therefore defines one stabilizer basis in Hilbert dimension

```text
d = 9.
```

A spread contains ten disjoint lines, partitioning the forty Pauli rays. Therefore a spread is a complete stabilizer MUB:

```text
d + 1 = 10 bases.
```

## Counts

```text
40 vertices = Pauli rays.
40 lines = stabilizer bases / maximal commuting contexts.
36 spreads = complete two-qutrit stabilizer MUB frames.
9 spreads through each line = 9 complete MUB frames containing each stabilizer basis.
```

## Numeric qutrit verification

For one spread, the script constructs the ten commuting Pauli contexts, builds the joint stabilizer eigenbases using rank-one projectors,

```text
P_rs = (1/9) sum_{a,b in F3} omega^{-ra-sb} A^a B^b,
```

and verifies that all cross-basis overlaps satisfy

```text
|<psi|phi>|^2 = 1/9.
```

So the spread really is a complete two-qutrit MUB.

## Hidden 20 as MUB-frame overlap

For a fixed complete MUB frame S:

```text
20 other complete MUB frames share exactly one basis with S.
15 other complete MUB frames share exactly four bases with S.
```

Therefore the hidden 20 is now a qutrit object:

```text
20 = one-basis-overlap valency among complete two-qutrit stabilizer MUB frames.
```

## The 2-(10,4,2) design as MUB-overlap design

The fifteen four-overlap frames define fifteen four-subsets of the ten bases of S.

These form

```text
2-(10,4,2).
```

So every pair of bases inside a fixed complete MUB frame is jointly retained by exactly two of the fifteen four-overlap frames.

The twenty one-overlap frames double-cover the ten bases:

```text
2 one-overlap frames through each basis.
```

## Qutrit meaning of the Sylvester/Petersen residue

The recent six-letter/Sylvester/Petersen structure is therefore not an abstract graph add-on.

It is the local overlap geometry of complete two-qutrit stabilizer MUB frames:

```text
10 bisections = 10 bases of a fixed complete MUB.
20 oriented triples = 20 one-basis-overlap MUB frames.
15 duads/synthemes = 15 four-basis-overlap MUB frames.
Petersen/S6 = switching symmetry of the local MUB-frame overlap residue.
```

## Structural slogan

```text
The hidden 20 is the one-basis-overlap valency among complete two-qutrit stabilizer MUB frames.
```
