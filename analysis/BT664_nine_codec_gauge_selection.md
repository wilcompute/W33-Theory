# BT664 — Nine Codec-Gauge Selection Test

BT660 showed that the secondary Q4 codec relation on the 16 complement flags requires choosing square structures on two four-point sets:

```text
C16 = A x B,
|A|=|B|=4.
```

Each four-point set has three square structures, equivalently three choices of omitted perfect matching in K4.  Therefore the product codec has

```text
3 x 3 = 9
```

gauge choices before a Fano/tomotope boundary chart is imposed.

## Gauge labels

Label the three square structures on A as

```text
A0, A1, A2
```

and the three square structures on B as

```text
B0, B1, B2.
```

The nine codec gauges are

```text
(Ai,Bj), 0 <= i,j <= 2.
```

Every gauge gives a graph isomorphic to Q4, and every antipodal quotient is isomorphic to K4,4.

So ordinary graph invariants do not select a unique gauge.

## Fano/tomotope selection rule

The Fano/tomotope chart must do more than demand Q4.  It must choose a compatible square structure on the four complement cells and on the four local flags.

The natural selection criterion is diagonal compatibility:

```text
Ai and Bj carry the same Fano parity class.
```

This leaves the three diagonal gauges

```text
(A0,B0), (A1,B1), (A2,B2).
```

The remaining cyclic order/orientation of the three diagonal gauges is acted on by

```text
S3.
```

Thus the gauge test gives a two-stage reduction:

```text
9 gauges -> 3 diagonal Fano-compatible gauges -> 1 gauge after choosing a tomotope hinge/orientation.
```

## Count interpretation

The three surviving diagonal gauges match the three metric carrier pairs from BT661:

```text
far, middle, active.
```

This is the first clean bridge between the 16-complement codec gauge freedom and the six-carrier 2+2+2 split.

## Boundary

This is a selection-rule theorem, not a numeric uniqueness theorem from raw Levi data alone.  Raw Levi adjacency gives only 4K4.  The nine Q4 gauges are all graph-isomorphic.  Fano/tomotope labeling is required to select the diagonal 3 and then a hinge/orientation is required to select one.
