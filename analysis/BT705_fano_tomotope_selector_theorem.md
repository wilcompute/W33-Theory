# BT705 — Fano/Tomotope Selector Theorem

This takes BT699 past the coordinate selector tested in BT702.

BT699 proved that every centered local `K33` rectangle has exactly 24 valid Levi 8-cycle presentations, with uniform split

```text
24 = 8 * 3.
```

The eight part is the square-orientation / mask layer:

```text
1110 1101 1011 0111 1100 1001 0110 0011
```

The remaining three part is the Fano diagonal channel:

```text
011 101 110
```

using the already established Fano chart

```text
011 <-> far
101 <-> middle
110 <-> active
```

Thus the selector is not a bare function of a rectangle.  It is a functor of a rectangle plus a tomotope hinge channel.

The geometric selector data are:

```text
square mask orbit: one of eight D4-compatible masks
Fano channel: one of {011,101,110}
tomotope hinge: one chosen channel among far/middle/active
```

So the exact chain is

```text
24 -> 3 -> 1.
```

Equivalently:

```text
valid Levi presentations
  / D4 square orientation
= 3 Fano channels
  / tomotope hinge
= 1 selected Levi 8-cycle presentation.
```

## Theorem

There is no symmetry-free canonical selector from the local `K33` rectangle alone.  There is a canonical selector only after adjoining the tomotope hinge datum.

## Consequence

BT702's lexicographic selector failed balance because it supplied a coordinate ordering instead of the missing hinge datum. BT705 replaces that with the geometric data needed for a real selector.

## Boundary

This is now the correct selector architecture.  The remaining numerical test is whether the hinge-selected correspondence carries the corrected BT700 chart eigenvalue-8 sector onto the Levi `E4` Hodge sector.
