# BT1095 — Centralizer basis for A12 = 1 + 3 + 8

BT1095 fixes an explicit algebraic basis for the gauge-packet layer used by BT1090--BT1092.

## Gauge-packet carrier

Use the complexified adjoint-profile module

```text
A12 = A1 direct_sum A3 direct_sum A8
```

with

```text
A1 ~= C
A3 ~= sl2(C)
A8 ~= sl3(C).
```

This is the algebraic version of the finite `1+3+8` gauge module.  Reality conditions can be imposed later; the present purpose is a clean exact basis for the reservoir map.

## Basis

Use the ordered basis

```text
A1:  Y
A3:  W0, Wp, Wm
A8:  C12, C21, C13, C31, C23, C32, C0, C8
```

where

```text
W0 = diag(1,-1),   Wp = E12,   Wm = E21
```

for `sl2`, and

```text
C12 = E12, C21 = E21, C13 = E13, C31 = E31, C23 = E23, C32 = E32,
C0  = diag(1,-1,0),
C8  = diag(1,1,-2)
```

for `sl3`.

## Dimension check

```text
1 + 3 + 8 = 12.
```

## Relation to BT1092

BT1092 gives the quotient

```text
pi12 : F13 -> C^12.
```

BT1095 identifies the target ordered basis of that `C^12` with

```text
(Y, W0, Wp, Wm, C12, C21, C13, C31, C23, C32, C0, C8).
```

Thus the reservoir map now has both:

```text
1. an explicit 13-to-12 quotient matrix,
2. an explicit centralizer/gauge-packet basis for its target.
```

## Boundary

This is a complexified algebraic basis.  The Hermitian/anti-Hermitian real form and physical normalization conventions remain later choices.
