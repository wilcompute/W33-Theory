# BT928 — Symplectic basis extractor for the BT925 form

BT928 computes an explicit hyperbolic basis for the canonical BT925 form on

```text
H = ker(A2) / im(A2).
```

## Result

The divided form

```text
B(x,y) = (x^T A y)/2 mod 2
```

has rank 8 and is transformed to the standard symplectic normal form with four hyperbolic pairs.

## Hyperbolic pairs

The extractor returns four pairs `(e_i,f_i)` with `B(e_i,f_i)=1` and all other cross-pair products zero.

Support sizes:

| pair | |e_i| | |f_i| |
|---:|---:|---:|
| 0 | 6 | 6 |
| 1 | 6 | 14 |
| 2 | 14 | 10 |
| 3 | 10 | 10 |

## Why this matters

BT925 proved that the chain shadow has the right symplectic mod-2 form. BT928 makes it operational: later maps into vertex or tetracode E8 coordinates can now start from an explicit symplectic basis rather than an abstract rank-8 quotient.

## Witness

```text
analysis/bt928_symplectic_basis_extractor.py
data/bt928_symplectic_basis_extractor.json
```
