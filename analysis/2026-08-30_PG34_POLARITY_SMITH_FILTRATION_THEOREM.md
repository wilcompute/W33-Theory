# Integral Smith filtration of the PG(3,4) polarity operator

For the 85x85 symmetric polarity/design matrix `H`, the exact identity is

`H^2 = 16 I + 5 J`, with `det(H) = -21*4^84`.

Local Smith elimination at the only exceptional primes gives exact valuation multiplicities:

- at `p=2`: `v2=0^17, 1^8, 2^36, 3^8, 4^16`;
- at `p=3`: `v3=0^84, 1`;
- at `p=7`: `v7=0^84, 1`.

The invariant-factor divisibility chain and determinant therefore force the complete integral Smith normal form

`SNF(H) = diag(1^17, 2^8, 4^36, 8^8, 16^15, 336)`.

Equivalently,

`coker(H) ~= (Z/2)^8 + (Z/4)^36 + (Z/8)^8 + (Z/16)^15 + Z/336`.

Its exponent is 336. This matches the exact inverse formula `H^{-1}=H/16-5J/336` and proves that 336 is the minimal global denominator of the inverse operator.

The Smith form sharpens the modular theorem. Characteristic two is a deep filtration: 68 invariant factors are divisible by 2, 60 by 4, 24 by 8, and 16 by 16. By contrast, the 3- and 7-primary defects occur only in the single terminal invariant factor 336. Thus the corank-one mod-3 and mod-7 degenerations are the same global Smith direction, while the binary rank-17 phenomenon is a genuinely much deeper degeneration.

Reproducibility:
- `analysis/w33_20260830_pg34_polarity_smith_filtration.py`
- `data/PART_W33_20260830_PG34_POLARITY_SMITH_FILTRATION.json`
- exact-continuation run `33337524115` passed.

Boundary: this is an integral finite-design operator theorem. A p-adic physical-scale interpretation requires a separate dynamical map.
