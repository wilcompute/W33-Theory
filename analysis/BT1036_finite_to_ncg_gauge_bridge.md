# BT1036 — Finite centralizer to NCG gauge-algebra bridge

BT1036 turns the BT1035 audit into an exact bridge dictionary.

## Bridge

| finite W33 object | dim | NCG algebra object | dim |
| --- | ---: | --- | ---: |
| fixed singlet in `C[12]` | 1 | `u(1)` unimodular hypercharge direction | 1 |
| A4 four-line quotient traceless part | 3 | `su(2)` weak adjoint | 3 |
| within-line traceless octet | 8 | `su(3)` color adjoint | 8 |

Total:

```text
finite total = 12
NCG total    = 12
profile      = 1 + 3 + 8
```

## Carrier compatibility

```text
gauge orbit                = 12
triangle-boundary sector   = 120
ratio                     = 10
```

The finite 12-dimensional gauge module is the local adjoint profile; the 120
cellular boundary sector is the larger carrier that can host localized gauge
one-forms.

## Required next tests

1. Construct an explicit `A_F` block action on the 81 matter zero modes or the
   162 doubled fermion carrier.
2. Compute the commutator span `[D_F, A_F]` and project to self-adjoint /
   unimodular one-forms.
3. Verify the dimension and representation split `1+3+8`.
4. Identify Higgs off-diagonal scalar blocks and compute `tr_F(Phi^2)`,
   `tr_F(Phi^4)`.

## Boundary

The bridge dictionary is exact. The representation-level inner-fluctuation proof
remains open.

## Witnesses

```text
analysis/bt1036_finite_to_ncg_gauge_bridge.py
data/bt1036_finite_to_ncg_gauge_bridge.json
```
