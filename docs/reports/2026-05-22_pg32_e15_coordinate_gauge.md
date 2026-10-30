# 2026-05-22 - PG(3,2) E15 Coordinate Gauge and 192 Affine Packets

## Breakthrough

The PG(3,2) relation is stronger than a cardinality match.

The W33 rank-15 curvature-active sector admits a PG(3,2)-indexed coordinate gauge.

## Coordinate identity

Let E15 be the rank-15 W33 curvature projector.  The verifier constructs a 40 x 15 coordinate matrix X whose columns are indexed by the 15 points/directions of PG(3,2), and checks

```text
X X^T = 24 E15 = 8I + J - 4A_W33
```

and

```text
X^T X = 24 I_15.
```

So the 15 PG(3,2) directions provide an orthogonal coordinate gauge for the E15 sector.

## PG(3,2) incidence facts

PG(3,2) has:

```text
15 points/directions
15 projective planes, each of size 7
15 affine half-spaces, each the complement of a plane, each of size 8
```

The verifier checks:

```text
projective planes intersect pairwise in 3 points
affine half-spaces intersect pairwise in 4 points
```

## Tomotope 192 packet

In the E15 coordinate gauge, take the sum of the 8 coordinate directions belonging to any affine half-space.

Each such 8-direction packet has squared norm

```text
8 * 24 = 192.
```

The verifier checks:

```text
15 affine packets
norm squared = 192 for every packet
pairwise packet overlap = 96
```

So the tomotope 192 appears as the PG(3,2) affine-half-space packet norm in the W33 curvature-active sector.

## Plane packet comparison

For the 7-direction projective-plane packets, the verifier finds:

```text
norm squared = 168
pairwise overlap = 72
```

So the 8-direction affine half-space, not the 7-direction plane, is the direct tomotope-192 packet.

## Meaning

The chain is now:

```text
W33 curvature-active sector E15
-> PG(3,2)-indexed 15-coordinate gauge
-> affine half-space packets of size 8
-> norm squared 192
-> tomotope flag-carrier scale
```

This upgrades the PG(3,2) relation from a count to an explicit coordinate-packet theorem.

## Boundary

The E15 basis is unique only up to orthogonal gauge.  The PG(3,2) incidence matrix fixes a natural PG-labeled gauge, but this is not yet a canonical automorphism-equivariant identification of W33 E15 coordinates with PG(3,2) directions.

## New code

- `analysis/w33_pg32_e15_coordinate_gauge.py`

When run, it writes:

- `data/w33_pg32_e15_coordinate_gauge.json`
