# 2026-05-22 - W33 Quadrangle Dual Visibility Theorem

## Breakthrough

The Z-side distribution

```text
0^1187, 1^288, 2^96, 3^32, 4^16
```

has a direct finite-geometric meaning.

After the previous theorem:

```text
X_min = point-line flags of W(3,3)
Z_min = ordinary quadrangles of W(3,3)
```

each quadrangle `Q` has four cycle edges. Each edge lies on a unique isotropic line, and each endpoint gives one point-line flag. Therefore every quadrangle determines an 8-element incident-flag boundary:

```text
F(Q) = {endpoint-line flags along the four cycle edges}
|F(Q)| = 8
```

## Theorem

For two distinct ordinary quadrangles `Q,Q'`, the Z-side overlap equals

```text
|F(Q) ∩ F(Q')|.
```

For every fixed `Q`, the distribution over the other `1619` quadrangles is

```text
0^1187, 1^288, 2^96, 3^32, 4^16.
```

The global unordered distribution is therefore

```text
0: 961470
1: 233280
2: 77760
3: 25920
4: 12960
```

## Interpretation

The Z-side distribution is not a black-box numerical artifact. It is the intersection distribution of eight-flag quadrangle boundaries.

So the paired minimal logical geometry now has a closed dictionary:

| object | geometric meaning |
|---|---|
| `X_min` | point-line flags / local line-stars |
| `Z_min` | ordinary quadrangles / 4-step exchange loops |
| X-X overlap | flag relative-position invariant |
| Z-Z overlap | intersection size of 8-flag quadrangle boundaries |
| X-Z noncommutation | E6 Weyl count |
| signed X-Z phase | rank-81 projector |

## Machine certificate

Added:

- `analysis/w33_quadrangle_dual_visibility_scheme.py`
- `data/w33_quadrangle_dual_visibility_scheme.json`

The script reconstructs W(3,3), enumerates all 1620 quadrangles, forms each 8-flag boundary, and checks the full distribution.
