# 2026-05-22 - Point-Pair Root-Line Species

## Core result

A W33 point is now best represented as an A2-type triad of root lines.

The next object is a pair of points.  The script classifies the six-root-line union of two point-triads.

There are exactly two species.

## Collinear point pair

If two W33 points are collinear, the two triads have maximum cross-orthogonality:

```text
3 x 3 = 9 orthogonal cross-pairs
```

The six-line internal orthogonality graph is 3-regular on 6 vertices, with complement split

```text
3 + 3
```

So a collinear point-pair is a complete bipartite orthogonality block between two triads.

Count:

```text
240 collinear point pairs
```

## Noncollinear point pair

If two W33 points are noncollinear, the two triads have minimal structured cross-orthogonality:

```text
3 orthogonal cross-pairs
```

Those three orthogonal cross-pairs form a perfect matching between the two triads.

The remaining nonorthogonal relation is octahedral: the complement is connected on 6 vertices and has the octahedron-style structure.

Count:

```text
540 noncollinear point pairs
```

## Meaning

The point-first picture becomes:

```text
point = A2 triad
collinear relation = K3,3 cross-orthogonality
noncollinear relation = perfect matching plus octahedral complement
```

This is a strong finite analogue of the idea that relation is primary.  The geometry is recovered by how two local phase-triads face each other.

## New code

- `analysis/w33_point_pair_rootline_species.py`

When run, it writes:

- `data/w33_point_pair_rootline_species.json`
