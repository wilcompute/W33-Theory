# 2026-05-22 - Flat Curvature Triples Produce the 45 Tetrad-Pair Graph

## Breakthrough

The flat part of the Z3 curvature is not just a set of 360 triples.
It organizes into the same 45-object geometry that appeared earlier in the E6 / Schlaefli transport layer.

## From flat triples to tetrads

A pairwise noncollinear triple has either one common center or four common centers.

The Z3 curvature result showed:

```text
F=0     <=> 4-centered triple
F!=0    <=> 1-centered triple
```

There are 360 flat triples.

Each flat triple has four centers.  These center sets are four-point cocliques, called tetrads here.

The 360 flat triples produce:

```text
90 tetrads
```

Each tetrad appears from exactly four flat triples.

## Center involution

For any tetrad T, take any 3-subset of T and compute its four centers.  The result is independent of the 3-subset.

This defines an involution on the 90 tetrads:

```text
T -> T*
```

The involution is fixed-point-free, so the 90 tetrads pair into:

```text
45 dual tetrad pairs
```

Each pair has complete bipartite incidence between its two tetrads:

```text
4 x 4 = 16 W33 collinearity edges
```

and no internal edges inside either tetrad.

## The 45-object graph

Represent each dual tetrad pair by the union of its two tetrads, an 8-point object.

Two such objects intersect in either:

```text
2 points: 720 pairs
0 points: 270 pairs
```

Joining objects that intersect in 2 points gives:

```text
SRG(45,32,22,24)
```

with spectrum:

```text
32^1 + 2^24 + (-4)^20
```

The complementary disjointness graph is:

```text
SRG(45,12,3,3)
```

with spectrum:

```text
12^1 + 3^20 + (-3)^24
```

## Meaning

This connects the new phase-curvature branch to the older 45-object E6 / Schlaefli branch.

```text
flat Z3 curvature triples
-> 90 tetrads
-> 45 dual tetrad pairs
-> SRG(45,32,22,24)
```

So the E6-like 45-object transport geometry emerges as the flat sector of the Z3 phase curvature.

## New code

- `analysis/w33_flat_curvature_45_tetrad_pairs.py`

When run, it writes:

- `data/w33_flat_curvature_45_tetrad_pairs.json`
