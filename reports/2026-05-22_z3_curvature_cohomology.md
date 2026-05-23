# 2026-05-22 - Z3 Curvature Cohomology and Bianchi Identity

## Breakthrough

The Z3 voltage cover can now be read as an honest discrete connection on the W33-complement clique complex.

The voltage is a 1-cochain on the 540 noncollinear edges.

Its curvature is the coboundary on pairwise noncollinear triples:

```text
F = dA
```

where A is the Z3 voltage 1-cochain.

## Clique-complex counts

For the W33 complement clique complex:

```text
vertices     = 40
edges        = 540
triangles    = 3240
tetrahedra   = 9450
```

Over F3, the script computes:

```text
rank d0 = 39
rank d1 = 501
rank d2 = 2739
H1(F3)  = 0
H2(F3)  = 0
```

So at this level there is no hidden F3 cohomology ambiguity in dimensions 1 or 2.

## Curvature support

The curvature distribution is:

```text
F = 0: 360
F = 1: 1440
F = 2: 1440
```

This exactly matches the center split:

```text
4-centered triples: 360, all flat
1-centered triples: 2880, all curved, split evenly between F=1 and F=2
```

So:

```text
F=0     <=> four-centered noncollinear triple
F!=0    <=> one-centered noncollinear triple
```

## Bianchi identity

The script checks all 9450 noncollinear tetrahedra and verifies:

```text
dF = 0
```

on every tetrahedron.

So the finite phase curvature obeys a discrete Bianchi identity.

## Meaning

This upgrades the voltage-cover result into a cochain-level gauge statement:

```text
A = Z3 phase connection on noncollinear edges
F = dA = curvature on noncollinear triples
dF = 0 = Bianchi identity
```

The curvature support is not arbitrary. It is exactly the one-center versus four-center split of generalized-quadrangle triads.

## New code

- `analysis/w33_z3_curvature_cohomology.py`

When run, it writes:

- `data/w33_z3_curvature_cohomology.json`
