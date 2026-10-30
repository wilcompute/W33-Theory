# 2026-05-22 - Flat 45 Point-Frame and W33 Eigenspace Filter

## Breakthrough

The 45 flat dual tetrad-pair objects form a clean incidence frame over the original 40 W33 points.

Each flat object is the union of two dual tetrads, so it has 8 points.

There are 45 such blocks.

## Incidence design

Let M be the 40 x 45 point-block incidence matrix.

The script verifies:

```text
block size = 8 for all 45 blocks
point degree = 9 for all 40 points
total incidences = 40*9 = 45*8 = 360
```

Point-pair coincidences recover W33 adjacency:

```text
adjacent W33 point pair:    appears together in 3 flat blocks
nonadjacent W33 point pair: appears together in 1 flat block
```

So the point Gram matrix is exactly

```text
M M^T = 8 I_40 + J_40 + 2 A_W33.
```

## Spectral meaning

Since W33 has spectrum

```text
12^1 + 2^24 + (-4)^15
```

the flat-sector point Gram has spectrum

```text
72^1 + 12^24 + 0^15.
```

So the flat 45-sector preserves the W33 constant plus 24-dimensional eigenspaces and kills the 15-dimensional -4 eigenspace.

## Block Gram

On the 45 block side, if A_45 is the SRG(45,32,22,24) adjacency matrix, then

```text
M^T M = 8 I_45 + 2 A_45.
```

Its spectrum is

```text
72^1 + 12^24 + 0^20.
```

## Meaning

The flat curvature sector is not only the 45-object E6-like graph.  It is a rank-25 point-frame that projects W33 onto the 1+24 spectral sector.

```text
flat curvature -> 45 blocks -> point-frame -> W33 eigenspace filter
```

This may be the cleanest current algebraic role of the flat sector: it removes the 15-dimensional -4 mode while retaining the 24-dimensional mode.

## New code

- `analysis/w33_flat_45_point_frame.py`

When run, it writes:

- `data/w33_flat_45_point_frame.json`
