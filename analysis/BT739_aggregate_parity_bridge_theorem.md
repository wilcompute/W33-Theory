# BT739 — Parity-Aggregate Bridge Theorem

BT714/BT715 closed the BT708 completion target with a *selected* sheet
(mask 1110, channel 011/far).  BT739 answers the complementary question:
what does the fully symmetric, selection-free aggregate see?

## Canonical aggregate

Define the parity-signed rectangle-to-cycle matrix

```text
T[rect, cyc] = sum over valid lifts of sgn(mask),
sgn = +1 for weight-3 D4 masks, -1 for weight-2 masks.
```

`T` is Sp(4,3)-equivariant: no coordinate, ordering, or orientation choice
enters.  Compose with the chart aggregation `Z_chart` and the exact chart81
eigenprojector

```text
P81 ~ (G-36I)(G-18I)(G-12I)(G-6I)G,   G = HH^T.
```

## Results (exact, mod p = 1000003)

```text
rank(P81)                 = 81   projector sanity
R1 rank(Z^T T)            = 239  full chart space (kernel = all-ones)
R2 rank(P81 Z^T T)        = 81   canonical aggregate, chart81: FULL RANK
R3 rank(Z^T T O)          = 81   lex orientation gauge, flag coords
R4 rank(P81 Z^T T O)      = 77   lex gauge restricted to chart81: DEFECTIVE
R5 random gauge sweep     = 81,81,81,81,81
R6 per-channel (lex)      = 78,78,78
R7 per-parity (lex)       = w3:77, w2:77
R8 unsigned aggregate     = cycle:81, flag(lex):77
```

## Theorem (rep-theory forcing)

The canonical aggregate restricted to chart81 has full rank 81.  This was
*forced* before computation: the aggregate is Sp(4,3)-equivariant, so its
kernel inside chart81 would be an invariant subspace; the chart action is
transitive (no trivial subrep in chart81), and PSp(4,3) = U4(2) has minimal
nontrivial irrep dimension 5.  A nonzero kernel of dimension <= 4 is
representation-theoretically impossible, and rank below 77 is excluded by the
gauge computation.  Hence the kernel is 0 and the rank is exactly 81.

## Consequence 1: selection is a functoriality cost, not a rank cost

The chart81 -> Levi cycle-space bridge does not require the tomotope hinge at
the *correspondence* level: the parity aggregate already carries chart81
isomorphically (R2).  The hinge datum of BT705/BT718 is needed only to
upgrade the correspondence to a one-cycle-per-rectangle *selector function*.
This sharpens BT706's "balanced but non-selective" verdict on the all-lift
average: with the D4 parity sign, the average is balanced AND carries the
full sector.

## Consequence 2: the lex orientation gauge is degenerate

An earlier float pilot reported rank 78; the exact value in the lex gauge is
77, and five random orientation gauges all give 81.  The BT713-style
lexicographic cycle orientation is a measure-zero degenerate gauge for
*aggregate* computations (sheet-rank computations are immune, since flipping
a row's sign preserves its span).  Any future aggregate-level computation
must either work in cycle coordinates (gauge-free) or use a generic gauge.

## Boundary

BT739 does not replace the BT718 canonical selector rule — selector
functoriality (one cycle per rectangle) still requires the hinge.  Open:
whether some geometric orientation gauge (e.g. symplectic-form-induced) is
provably non-degenerate, and what the 4-dimensional lex-gauge defect
77 = 81 - 4 means combinatorially (4 = mu, the quadrangle parameter).
