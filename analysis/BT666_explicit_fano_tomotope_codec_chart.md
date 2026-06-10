# BT666 — Explicit Fano/Tomotope Codec Chart

This executes the chart demanded by BT664.  The goal is to realize the reduction

```text
9 codec gauges -> 3 Fano-compatible gauges -> 1 hinge-oriented tomotope chart
```

without changing the verified raw statement:

```text
raw Levi complement = 4K4.
```

## 1. Four-point square structures

For any four-point set identified with

```text
F2^2 = {00,01,10,11},
```

a square structure is obtained by deleting one perfect matching from K4.
Equivalently it is indexed by a nonzero direction

```text
r in F2^2 \ {0} = {01,10,11}.
```

The square graph C4(r) has edge set

```text
x -- x+u   for u in (F2^2 \ {0,r}).
```

Thus each four-point factor has exactly three square structures.

## 2. The 16-codec product chart

Write the 16 complement flags as a secondary codec product

```text
C16 = A x B,
A = F2^2,
B = F2^2.
```

A codec gauge is a pair of omitted directions

```text
(rA,rB) in (F2^2\{0}) x (F2^2\{0}).
```

So there are

```text
3*3 = 9
```

gauges.

For every gauge, define

```text
G(rA,rB) = C4_A(rA) square-product C4_B(rB).
```

Since

```text
C4 square-product C4 ~= Q4,
```

every gauge gives a graph isomorphic to Q4.

Therefore Q4 alone does not select the gauge.

## 3. Fano labels for the three directions

Choose the standard Fano/tomotope hinge chart on

```text
F2^3.
```

Let the tetrahedral hinge axis be

```text
000.
```

Let the four hinge-adjacent odd axes be

```text
O = {001,010,100,111},
```

and the three nonadjacent even toroidal axes be

```text
E = {011,101,110}.
```

The three nonzero directions in F2^2 are now labeled by the three even toroidal axes:

```text
01 -> 011,
10 -> 101,
11 -> 110.
```

This is the missing explicit Fano chart.

## 4. Diagonal compatibility: 9 -> 3

A product gauge `(rA,rB)` is Fano-compatible exactly when the two omitted directions carry the same even Fano label:

```text
rA = rB.
```

Thus the nine gauges reduce to the three diagonal gauges

```text
(01,01), (10,10), (11,11).
```

In Fano labels these are

```text
011, 101, 110.
```

They are the three even toroidal axes, hence the three nonadjacent toroidal axes relative to the hinge.

This realizes

```text
9 -> 3.
```

## 5. Hinge/orientation: 3 -> 1

The remaining three diagonal gauges are permuted by the S3 symmetry of the even Fano line

```text
{011,101,110}.
```

Choosing a tomotope orientation orders the even axes cyclically, for example

```text
011 -> 101 -> 110 -> 011.
```

Choosing the first even axis as the hinge-facing phase selects the representative

```text
(01,01).
```

The other two representatives are equivalent under the remaining cyclic gauge.

Therefore the complete chart reduction is

```text
9 gauges -> 3 diagonal Fano gauges -> 1 oriented tomotope chart.
```

## 6. Relation to the six carriers

The three diagonal Fano gauges are identified with the three metric carrier-pair channels:

```text
011 <-> far,
101 <-> middle,
110 <-> active.
```

This attaches the six-carrier split

```text
6 = 2_far + 2_middle + 2_active
```

to the explicit Fano/tomotope codec chart.

## Boundary

This construction is a secondary codec chart on the verified 4K4 complement.  It does not claim that raw Levi adjacency is Q4.  It also does not claim a flag-level W(G2) action.
