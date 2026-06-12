# BT840-BT842: GC Carrier Completion

## BT840: the 180 sentinel sheet is a rook/K6 object

BT839 left a precise gap:

```text
57-cell flags = 3420
W33 Petersen homes = 3240
gap = 180 = k*g = 12*15
```

BT840 identifies the gap objectwise.  The verified Clifford L/R boundary has
36 cells in a `6 x 6` rook grid.  The zero-overlap relation consists of all
pairs in a common row or a common column:

```text
12 row/column fibers * C(6,2) duads = 12*15 = 180.
```

This is not a free correction term.  It is the missing sentinel sheet:

```text
3240 + 180 = 3420 = |PSL(2,19)|.
```

The six-object fibers also explain why the 11-cell keeps appearing: each
fiber's `C(6,2)=15` duads are the K6/hemi-icosahedral edge count of the
11-cell cell.

## BT841: the 660 carrier is `11 x A5`

BT841 builds a local 660-slot carrier from the same Clifford/schedule boundary.
Choose one apex cell `(r,c)` in the `6 x 6` grid.  Its two incident row/column
fibers are the local frame.  The remaining ten fibers plus the apex give

```text
11 = 1 + 5 + 5.
```

Crossing those eleven labels with the verified 60-element Clifford A5 selector
gives

```text
11 * 60 = 660 = k*N_eff.
```

Boundary: this is an explicit carrier, not a claim that `PSL(2,11)` acts inside
W33.

## BT842: tomotope half-flags are 24-cell edge lifts

The 24-cell/Reye/tomotope spine has 48 incidences:

```text
12 axes * 4 = 16 hexagon planes * 3 = 48.
```

BT842 proves the missing edge-level lift.  Every 24-cell edge lies in a unique
central hexagon plane; its two endpoint axes determine the third, missing axis
in that plane.  Hence each edge maps to a Reye incidence `(missing axis,
hexagon plane)`, and every incidence has exactly two edge lifts:

```text
96 24-cell edges = 2 * 48 Reye incidences.
```

That is exactly the tomotope half-flag count: half of BT814's 192 full flags
and the BT839 omnitruncated tomotope count.

The hexagon clue also closes.  Each central 24-cell hexagon is a six-root
cycle.  Completing its cycle `C6` to a full `K6` gives 15 duads, the
hemi-icosahedral skeleton count of the 11-cell cell.  Across all 16 central
hexagons:

```text
16 * C(6,2) = 16*15 = 240.
```

The dot profile of those 240 duad slots is

```text
dot +1: 96    24-cell edges / tomotope half-flags
dot -1: 96    mirror half
dot -2: 48    opposite-axis Reye incidence repetitions
```

So the 24-cell, tomotope, 11-cell cell, and W33/E8 count meet on one tested
object: completed central hexagons.

