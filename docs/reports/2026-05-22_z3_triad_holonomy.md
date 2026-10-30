# 2026-05-22 - Z3 Triad Holonomy

## Breakthrough

Each point is represented as a 3-root-line triad.

For two noncollinear points, their two triads have exactly three orthogonal cross-pairs. These three cross-pairs form a perfect matching, so a noncollinear point pair defines a transport permutation between two 3-element triads.

Now take three pairwise noncollinear points. Composing the three matching transports around the triangle gives a holonomy permutation of one triad.

## Result

The holonomy is always cyclic:

```text
identity or a 3-cycle
```

So the holonomy group is contained in

```text
A3 ~= Z3.
```

The script verifies all pairwise noncollinear triples:

```text
3240 triples total
```

These split by number of common centers in W33:

```text
4 centers: 360 triples
1 center: 2880 triples
```

The holonomy detects the split exactly:

```text
identity holonomy     <=> 4-centered triad
nonidentity Z3 turn   <=> 1-centered triad
```

## Meaning

This is the cleanest finite version so far of the orientation or phase-transport layer.

```text
point = self-cancelling 3-phase triad
noncollinear pair = perfect-matching transport
noncollinear triangle = Z3 holonomy
```

The distinction between one center and four centers in the generalized quadrangle becomes a phase-holonomy distinction.

## New code

- `analysis/w33_z3_triad_holonomy.py`

When run, it writes:

- `data/w33_z3_triad_holonomy.json`
