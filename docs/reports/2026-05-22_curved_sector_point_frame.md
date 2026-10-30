# 2026-05-22 - Curved Sector Point-Frame Restores the W33 Minus-Four Sector

## Breakthrough

The flat 45-sector is a rank-25 point-frame.  It preserves the constant and 24-dimensional W33 eigenspaces and kills the 15-dimensional minus-four eigenspace.

The natural companion question was whether the curved sector controls the missing 15-dimensional mode.

It does.

## Curved centered blocks

A curved event is a one-centered noncollinear triple together with its unique center:

```text
{x,a,b,c}
```

There are

```text
2880
```

such four-point blocks.

Let M_curved be the 40 x 2880 point-block incidence matrix.

The script verifies:

```text
each block has size 4
each point lies in 288 curved blocks
```

Point-pair coincidences are:

```text
adjacent W33 pair:    appears together in 36 curved blocks
nonadjacent W33 pair: appears together in 16 curved blocks
```

Therefore the point Gram is exactly

```text
M_curved M_curved^T = 272 I_40 + 16 J_40 + 20 A_W33.
```

## Spectrum

Using the W33 spectrum

```text
12^1 + 2^24 + (-4)^15
```

the curved-sector point Gram has spectrum

```text
1152^1 + 312^24 + 192^15.
```

So the curved sector is full rank on the W33 point space and preserves all three W33 eigenspaces.

## Flat/curved complementarity

Flat sector:

```text
M_flat M_flat^T = 8 I_40 + J_40 + 2 A_W33
spectrum = 72^1 + 12^24 + 0^15
```

Curved sector:

```text
M_curved M_curved^T = 272 I_40 + 16 J_40 + 20 A_W33
spectrum = 1152^1 + 312^24 + 192^15
```

Thus:

```text
flat sector  = E6-like rank-25 filter, kills minus-four mode
curved sector = full-rank dynamical frame, restores minus-four mode
```

## Meaning

The 15-dimensional W33 minus-four sector appears to be the mode that is invisible to flat curvature but visible to curved events.

This gives a sharp algebraic split:

```text
flat curvature geometry controls 1+24
curved curvature geometry controls 1+24+15
```

## New code

- `analysis/w33_curved_sector_point_frame.py`

When run, it writes:

- `data/w33_curved_sector_point_frame.json`
