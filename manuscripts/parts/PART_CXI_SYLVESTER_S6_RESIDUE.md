# Part CXI — Sylvester S6 Residue and Oriented-Triple Hidden 20

Status: theorem-grade structural extension  
Date: April 28, 2026

Part CX localized the B29/C9 rank lock inside every fixed spread. This part identifies the local residue explicitly as a six-letter Sylvester object.

For every fixed spread:

```text
15 four-neighbor spreads = 15 duads of a 6-set.
10 lines of the fixed spread = 10 unordered 3+3 bisections of a 6-set.
20 one-neighbor spreads = 20 oriented triples of a 6-set.
```

## The six-letter model

Take a set of six letters.

There are

```text
C(6,2)=15
```

duads.

There are

```text
C(6,3)/2=10
```

unordered bisections into two triples.

There are

```text
C(6,3)=20
```

oriented triples.

A duad is incident with a bisection exactly when the two letters of the duad lie on the same side of the bisection.

This gives the local design:

```text
10 points, 15 blocks, block size 4, point replication 6, pair lambda 2.
```

## Hidden 20

Each bisection has two oriented halves.

So the 20 oriented triples double-cover the 10 bisections:

```text
20 = 2 * 10.
```

This matches the local spread fact:

```text
20 one-line neighbors double-cover the 10 lines of the fixed spread.
```

Therefore the hidden heavy 20-sector is locally modeled by oriented triples of a six-set.

## S6 symmetry

The six-letter model carries the natural S6 action.

The script verifies that all

```text
720
```

letter permutations preserve the incidence design.

## Local rank dictionary

The local dictionary is:

```text
four-neighbor spreads = duads = C(6,2)=15.
fixed-spread lines = bisections = C(6,3)/2=10.
one-neighbor spreads = oriented triples = C(6,3)=20.
```

Therefore

```text
C9 = bisections minus constants = 10 - 1 = 9.
```

and

```text
B29 = oriented triples + nonconstant bisection modes = 20 + 9.
```

So

```text
B29 = C(6,3) + (C(6,3)/2 - 1).
```

## Structural slogan

```text
The hidden heavy 20-sector is the oriented-triple double cover of the ten bisections inside each spread residue.
```
