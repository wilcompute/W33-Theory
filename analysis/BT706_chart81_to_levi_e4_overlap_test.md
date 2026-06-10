# BT706 — Chart-81 to Levi-E4 Overlap Test

BT706 takes the corrected BT700 statement seriously.

The chart/nonedge incidence matrix satisfies

```text
HH^T = 9I + A_Gamma.
```

Therefore the 81-dimensional chart sector is

```text
A_Gamma eigenvalue -1
```

and hence

```text
HH^T eigenvalue 8.
```

So the chart side is not null.  It is a positive-energy incidence eigenspace.

The Levi side has the protected Hodge idempotent

```text
E4 = (1/160) C C^T
   = (1/160)(81 A0 - 27 A1 + 9 A2 - 3 A3 + A4),
```

with rank

```text
81.
```

## Test result

There are now three distinct maps to compare:

1. coordinate selector from BT702,
2. all-lift average from BT703,
3. hinge-selected geometric functor from BT705.

The coordinate selector is rejected:

```text
chart81 -> LeviE4 is not canonically balanced.
```

The all-lift average is accepted only as a correspondence:

```text
2160 * 24 = 51840 = 1620 * 32.
```

It is balanced but non-selective.

The geometric selector is the only candidate functor:

```text
24 -> 3 -> 1.
```

## Main conclusion

The chart 81-sector and Levi E4 sector have matching dimension, but equality is not automatic.  The bridge must be mediated by the BT705 tomotope-hinge selector.

Thus the corrected status is:

```text
chart 81-sector: verified as HH^T eigenvalue 8
Levi E4-sector: verified as Hodge/Kirchhoff cycle projector
coordinate intertwiner: fails / not geometric
average correspondence: balanced but non-functorial
hinge selector: unique viable functorial candidate
```

## Boundary

BT706 does not claim a completed numerical eigenspace isometry.  It proves the right comparison diagram and rules out the false shortcut.  The all-the-way target is now an explicit hinge-selected matrix whose rank-81 image equals Levi `E4`.
