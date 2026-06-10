# BT663 — Six-Carrier K3,3 / G2 Secondary Relation Theorem

BT661 left the honest next test: build a secondary relation on the six regular S4 carrier labels and test whether the result is a K3,3 / hexagon / G2-root object.

## Input from BT658/BT661

The six regular 24-flag S4 carriers split around the 4K4 complement as

```text
6 = 2_far + 2_middle + 2_active.
```

Write the six carrier labels as

```text
F+, F-, M+, M-, A+, A-
```

where F/M/A denote the far, middle, active metric channels, and +/- distinguish the two carriers inside each pair.

The verified metric data is still only the pair split:

```text
far pair:    d3=96, d4=288
middle pair: d2=48, d3=192, d4=144
active pair: d1=24, d2=96, d3=120, d4=144
```

## Secondary carrier graph

Define the secondary carrier graph by connecting every + carrier to every - carrier:

```text
{F+,M+,A+}  --  {F-,M-,A-}.
```

The graph is

```text
K3,3.
```

It has

```text
6 vertices,
9 edges,
3-regular,
bipartition 3+3.
```

This is not raw Levi adjacency.  It is a carrier-label relation induced after the BT660 secondary codec layer.

## Metric matching and Weyl quotient

The verified metric pairs form a perfect matching inside K3,3:

```text
M_metric = {F+F-, M+M-, A+A-}.
```

The full automorphism group of K3,3 has order

```text
|Aut(K3,3)| = 72.
```

The stabilizer of the metric matching has order

```text
12.
```

Indeed, it permutes the three metric pairs and may flip the two sides globally:

```text
S3 semidirect C2 ~= D6 ~= W(G2).
```

Thus the verified three-pair carrier split selects a canonical Weyl-sized subgroup inside the full K3,3 frame symmetry:

```text
Aut(K3,3, M_metric) ~= W(G2).
```

## Hexagon form

Choosing a cyclic order of the three metric channels, for example

```text
F -> M -> A -> F,
```

the same six labels can be written as the hexagon

```text
F+ -- M- -- A+ -- F- -- M+ -- A- -- F+.
```

The hexagon automorphism group is again

```text
D6 ~= W(G2).
```

The cyclic order is a gauge choice.  The invariant content is the matching-preserving K3,3 stabilizer of order 12.

## Boundary

This theorem does not claim W(G2) acts on the original 160 Levi flags.  It proves a secondary carrier-label structure:

```text
six S4 carriers + metric pairing -> K3,3 with W(G2)-sized matching stabilizer.
```

A full Weyl-equivariant action on the flags remains a separate construction.
