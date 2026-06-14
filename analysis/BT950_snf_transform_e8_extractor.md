# BT950 — Smith-transform E8 extractor protocol

BT950 attacks the BT924 residual directly.

## Convention correction

For an SNF decomposition

```text
D = U A V
```

the torsion generators of `coker(A)` live on the left/codomain basis. Therefore the eight `d_i=2` directions are represented in original coordinates by columns of `U^{-1}`, not blindly by columns of `V`.

## Result

The SNF diagonal is

```text
1^16, 2^8, 8^15, 24^1
```

and the `d_i=2` indices are

```text
[16,17,18,19,20,21,22,23]
```

The eight pulled-back `U^{-1}` columns satisfy `A_col_even = true`, so the divided pairing is defined.

## Mod-2 form

The divided pairing modulo 2 on this sector is exactly four hyperbolic blocks:

```text
[[0,1],[1,0]] x 4
```

with rank 8.

## Boundary

The raw divided integral form on the `U^{-1}` d=2 sector is huge and indefinite, not the positive E8 Cartan form. BT950 therefore validates the canonical valuation-one mod-2 E8 shadow, but it also proves that the positive E8 metric still needs an additional selector.

## Witness

```text
analysis/bt950_snf_transform_e8_extractor.py
data/bt950_snf_transform_e8_extractor.json
```
