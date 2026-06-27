# BT1876 — Optical Measurement Schedule for `[[66,13,3]]_3`

BT1876 compiles the BT1872 CSS matrix code into a finite optical syndrome schedule.

## Code

```text
[[66,13,3]]_3
```

with:

```text
44 X face checks
12 Z dual vertex-star checks
66 F12/K12 edge payload rotations
```

## Touch counts

Each triangular face check touches 3 edge rotations:

```text
44 * 3 = 132 X edge touches
```

Each vertex-star check touches 11 incident edges:

```text
12 * 11 = 132 Z edge touches
```

Total per full syndrome cycle:

```text
264 edge/check touches
```

## Five-round schedule

```text
X0_Reye_faces:         16 checks, 48 touches
X1_residual_faces_A:   14 checks, 42 touches
X2_residual_faces_B:   14 checks, 42 touches
Z0_even_vertex_stars:   6 checks, 66 touches
Z1_odd_vertex_stars:    6 checks, 66 touches
```

## Rank dependencies

```text
X rows measured = 44, X rank = 42, dependencies = 2
Z rows measured = 12, Z rank = 11, dependencies = 1
```

## Interpretation

This schedule uses the existing 66 F12 edge rotations as the payload.  The syndrome layer adds:

```text
44 face-check ancillas
12 vertex-star-check ancillas
5 measurement rounds
```

The checks commute by BT1872 boundary-of-boundary cancellation, so the schedule can be repeated as a syndrome cycle.

Boundary: compiler-level optical measurement schedule only; not a calibrated circuit layout or hardware threshold.
