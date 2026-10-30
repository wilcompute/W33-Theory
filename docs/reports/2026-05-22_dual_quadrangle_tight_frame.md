# 2026-05-22 - Dual Quadrangle Tight-Frame and 20-Fiber Theorem

## Breakthrough

The signed phase matrix is tight on both sides.

Rows (`X_min` flags):

```text
160 unit vectors in R^81
frame bound = 160/81
```

Columns (`Z_min` quadrangles):

```text
1620 unit vectors in R^81
frame bound = 1620/81 = 20
```

The number `20` is not arbitrary:

```text
20 = 1620 / 81 = 240 / 12 = n_B / h.
```

So the quadrangle frame redundancy equals the W33 bulk-to-horizon projection fiber.

## Theorem

Let `A` be the signed `160 x 1620` flag-quadrangle phase matrix.

Then:

```text
rank(A) = 81
A A^T has spectrum 160^81 + 0^79
A^T A has spectrum 160^81 + 0^1539
```

Every row has squared norm `81`.
Every column has squared norm `8`.

Therefore:

```text
A A^T / 81 = Gram matrix of 160 unit flag vectors in R^81
A^T A / 8  = Gram matrix of 1620 unit quadrangle vectors in R^81
```

The column-side frame bound is

```text
1620 / 81 = 20.
```

## Interpretation

The previous theorem said:

```text
phase protects homology
```

This theorem sharpens it:

```text
flag side:       160 local flag probes over 81 protected dimensions
quadrangle side: 1620 loop probes over 81 protected dimensions
redundancy:      20 = W33 bulk/horizon fiber
```

So the same signed phase matrix simultaneously acts as:

1. a rank-81 projector on the flag surface;
2. a quadrangle tight frame with holographic redundancy 20;
3. a bridge between the minimal logical surface and the bulk-to-horizon fiber `240/12`.

## Machine certificate

Added:

- `analysis/w33_dual_quadrangle_tight_frame.py`
- `data/w33_dual_quadrangle_tight_frame.json`

The script reconstructs W(3,3), builds the signed phase matrix, verifies both projector relations, and records the dual frame/fiber identities.
