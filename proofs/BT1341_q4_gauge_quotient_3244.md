# BT1341 -- Q4 Gauge Quotient Certificate for [[32,4,4]]

## Purpose

BT1338 proved that the literal contractible Q4 cubical chain complex gives:

```text
rank(partial_1) = 15
rank(partial_2) = 17
k = 32 - 15 - 17 = 0
```

BT1341 constructs the missing quotient/gauge layer.

## Construction

Keep the 15 independent vertex/star X checks. Let the 17-dimensional Q4 cycle space be represented by the span of the 24 square-face boundaries.

Choose four independent global quotient/flux functionals on that cycle space:

```text
0x79b8
0x7a2e
0x9ea1
0xada0
```

Define the Z-check space as the kernel of these four functionals inside the cycle space. This kernel has rank:

```text
17 - 4 = 13
```

Therefore:

```text
n = 32
rank(H_X) = 15
rank(H_Z) = 13
k = 32 - 15 - 13 = 4
```

## Distance certificate

The four quotient functionals were selected so their span avoids all induced low-weight dual functionals coming from non-cut vectors of weight < 4. This certifies no X-logical of weight < 4.

The script also searches and finds weight-4 witnesses:

```text
d_X = 4, witness edges [6, 8, 13, 15]
d_Z = 4, witness edges [0, 1, 12, 20]
```

So the quotient code is:

```text
[[32,4,4]]
```

## Boundary

This is a gauge quotient certificate. It proves that a four-functional quotient of the Q4 cycle space yields the claimed code parameters. A geometric toroidal drawing or canonical symmetry-minimal quotient remains a further interpretation layer.

## Files

```text
tools/bt1341_q4_gauge_quotient_3244.py
data/bt1341_q4_gauge_quotient_3244.json
```
