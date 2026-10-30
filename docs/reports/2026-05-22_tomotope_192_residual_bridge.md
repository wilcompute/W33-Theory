# 2026-05-22 - Tomotope 192 Curvature-Residual Bridge

## Why this matters

The flat/curved projector split produced the exact identity

```text
G_curved - 26 G_flat + 18 J = 192 E15
```

where E15 is the rank-15 projector onto the W33 minus-four eigenspace.

The coefficient 192 is not an isolated number.  It matches the tomotope packet scale already present in the repo.

## Existing tomotope 192 mechanisms

The repo had already separated two related 192 mechanisms:

```text
intermediate D4/tetrahedral packet: 192 = 8 * 24
tomotope flag carrier:             192 = 2 * 96
```

The tomotope packet also satisfies:

```text
96 = 12 * 8
192 = 12 * 16 = 4 * 48
1152 = 6 * 192
```

Readings:

```text
12 = tomotope edges / Reye points / local codec scale
16 = tomotope triangles / Reye lines
48 = edge-triangle incidences in the Reye spine
96 = tomotope automorphism order
192 = tomotope flag carrier
1152 = F4 / 24-cell scale
```

## New bridge

The W33 curvature residual has trace

```text
trace(192 E15) = 192 * 15 = 2880.
```

But 2880 is exactly the number of one-centered curved events in the Z3 curvature layer.

So:

```text
curved events = 15 tomotope-flag packets
```

or

```text
2880 = 15 * 192.
```

## Verified identities

The new verifier checks:

```text
G_curved - 26 G_flat + 18 J = 192 E15
E15 has rank 15
trace residual = 2880
2880 = 15 * 192
192 = 2 * 96
192 = 12 * 16
192 = 4 * 48
96 = 12 * 8
192 = 8 * 24
1152 = 6 * 192
```

## Meaning

The coefficient 192 in the curvature residual is best read as a tomotope packet scale on the rank-15 curvature-active W33 sector.

The flat sector kills the rank-15 mode.
The curved sector restores it.
The residual is exactly 15 copies of the 192 tomotope flag-carrier packet.

## Boundary

This is a packet/projector/trace theorem.  It does not yet prove an object-by-object bijection between the 192 tomotope flags and curved events inside each rank-15 mode.

The next target is to find whether the 2880 curved events split canonically into 15 packets of 192, and whether each packet carries a tomotope-like 12-by-16 Reye spine.

## New code

- `analysis/w33_tomotope_192_residual_bridge.py`

When run, it writes:

- `data/w33_tomotope_192_residual_bridge.json`
