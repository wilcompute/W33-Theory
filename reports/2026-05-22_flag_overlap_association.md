# 2026-05-22 - W33 Flag Overlap Association Theorem

## Breakthrough

The previous theorem identified the projective minimal `X` supports with isotropic line-stars. That means:

```text
X_min = flags of W(3,3)
```

where a flag is a point-line incidence `(p,L)` with `p in L`.

The earlier numerical overlap scheme

```text
1, 3, 9, 27
```

is exactly the relative-position scheme of two flags in the generalized quadrangle.

## Theorem

For two ordered distinct flags `f=(p,L)` and `g=(q,M)`:

| Relative flag position | Overlap |
|---|---:|
| same point or same line | 27 |
| one cross-incidence: `p in M` or `q in L` | 9 |
| lines meet elsewhere, or lines are skew but `p,q` are collinear | 3 |
| lines are skew and `p,q` are noncollinear | 1 |

Per fixed flag this gives

```text
27^6, 9^18, 3^54, 1^81
```

or equivalently

```text
1^81, 3^54, 9^18, 27^6.
```

The global unordered distribution is therefore

```text
1: 6480
3: 4320
9: 1440
27: 480
```

matching the unsigned Gram matrix `U U^T` from the minimal logical surface.

## Interpretation

This upgrades the `3`-adic overlap theorem from a spectral fact to an incidence-geometric theorem.

```text
The 3-adic overlap value is a flag-distance invariant.
```

So the minimal logical surface now has a clean hierarchy:

```text
X_min support        = W33 flags
Z_min support        = ordinary quadrangles
X/Z noncommutation   = E6 Weyl count
signed phase         = rank-81 homology projector
```

## Machine certificate

Added:

- `analysis/w33_flag_overlap_scheme.py`
- `data/w33_flag_overlap_scheme.json`

The script reconstructs W(3,3), enumerates all 160 flags, classifies every ordered flag pair, and verifies the overlap distribution and per-flag counts.
