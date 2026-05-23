# 2026-05-22 - Flat and Curved Frame Projector Split

## Result

The flat and curved point frames separate the W33 point space into two exact parts.

The flat sector sees the constant mode and the 24-dimensional W33 mode.  It does not see the 15-dimensional mode.

The curved sector sees the full point space, including that missing 15-dimensional mode.

## Exact projectors

Let A be the W33 adjacency matrix.

The rank 15 projector is

```text
E15 = (8 I + J - 4 A) / 24
```

The rank 25 projector is

```text
E25 = (16 I + 4 A - J) / 24
```

The script verifies that these are complementary projectors:

```text
E15 plus E25 equals identity
E15 times E25 equals zero
```

## Frame residual

The flat frame has Gram matrix

```text
G_flat = 8 I + J + 2 A
```

The curved frame has Gram matrix

```text
G_curved = 272 I + 16 J + 20 A
```

The exact residual identity is

```text
G_curved - 26 G_flat + 18 J = 192 E15
```

So the rank 15 sector is the exact residual left after subtracting the flat-visible part from the curved frame.

## Meaning

Flat geometry controls the rank 25 part.

Curved geometry restores the rank 15 part.

This gives an exact algebraic split:

```text
flat-visible sector: rank 25
curvature-active sector: rank 15
```

## New code

- `analysis/w33_projector_split.py`

When run, it writes:

- `data/w33_projector_split.json`
