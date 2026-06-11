# BT786 - Face-Layer Phase Lift

BT786 closes the BT783/BT784 gap.  The tomotope face layer is not a passive
count of 16 triangles.  It is the missing binary phase core.

## The exact bridge

BT783 found the obstruction:

```text
cube binary module:      C2^3 = 1 + 2
tomotope binary module:  C2^4 = 2 + 2
```

BT784 found the count-level shadow:

```text
faces = 16 = 8 + 8
```

BT786 proves these are the same statement.

The rank-32 cube-web atlas has three size-8 packets:

```text
R09, R10, R11
```

Only two of them have the face signature:

```text
R09 and R10:
  size = 8
  relation to base = {equal: 1, one_side: 1}
  point overlap = 5

R11:
  size = 8
  relation to base = {one_side: 2}
  point overlap = 2
```

Therefore the tomotope face layer is exactly

```text
faces = R09 + R10 = 8 + 8 = 16
```

and the third 8-packet is not part of the face layer.

## The module lift

The cube C3 action on its binary core has one fixed diagonal bit:

```text
C2^3 nonzero orbit profile = {1:1, 3:2}
```

Quotient by the diagonal bit:

```text
C2^3 / <111> = F4
nonzero orbit profile = {3:1}
```

Add a second irreducible F4 phase plane:

```text
F4 + F4 = C2^4
nonzero orbit profile = {3:5}
fixed nonidentity bits = 0
```

This is exactly the tomotope derived-half binary profile from BT783.

## The packet identity

The cube and tomotope halves are the same 48-packet seen through different
factorizations:

```text
cube side:      8 cube binary bits * |S3| = 8 * 6 = 48
tomotope side: 16 face-layer bits * |C3| = 16 * 3 = 48
```

So the order-48 coincidence is now explained:

```text
one cube reflection bit is traded for one irreducible face-phase plane
```

With BT785:

```text
480 = 10 * 48
    = (k-r) * (16 faces * C3)
```

The GraphTheory 480 is therefore not just ten local cube stabilizers.  It is
also ten tomotope face-phase packets.

## Interpretation

The bridge is not vertex-level, edge-level, or cell-level.  Those strata appear
as primitive rank-32 packet sizes.  The face layer is special because 16 is not
a primitive rank-32 orbit; it appears only as an 8+8 two-sheet lift.

That is the finite combinatorial shadow of the CE2/L-infinity phase repair:
remove the cube's fixed diagonal bit and replace it with a second irreducible
phase plane.

## Validation

Run:

```bash
python3 analysis/bt786_face_layer_phase_lift.py
```
