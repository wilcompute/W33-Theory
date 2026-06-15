# BT1098 — Real-form normalization for A12

BT1098 fixes the Hermitian/anti-Hermitian real form and trace pairing for the BT1095 gauge-packet basis.

## Complexified starting point

BT1095 used

```text
A12_C = C direct_sum sl2(C) direct_sum sl3(C)
```

with ordered basis

```text
Y, W0, Wp, Wm, C12, C21, C13, C31, C23, C32, C0, C8.
```

## Real form

Use the compact anti-Hermitian real form

```text
A12_R = u(1) direct_sum su(2) direct_sum su(3).
```

Use the positive trace pairing

```text
<X,Y> = -Re Tr(XY).
```

## Normalized U1 line

As an abstract one-dimensional line, choose

```text
Y = i
```

with norm one.  When embedded as an `n x n` scalar matrix, use

```text
Y_n = i I_n / sqrt(n),
```

so that

```text
-Tr(Y_n^2) = 1.
```

## Normalized su(2) basis

Let `sigma_1,sigma_2,sigma_3` be the Pauli matrices.  Define

```text
W_a = i sigma_a / sqrt(2),  a=1,2,3.
```

Then

```text
-Re Tr(W_a W_b) = delta_ab.
```

This is the compact real form of the earlier complex basis `(W0,Wp,Wm)`.

## Normalized su(3) basis

Let `lambda_1,...,lambda_8` be the Gell-Mann matrices with

```text
Tr(lambda_a lambda_b) = 2 delta_ab.
```

Define

```text
C_a = i lambda_a / sqrt(2),  a=1,...,8.
```

Then

```text
-Re Tr(C_a C_b) = delta_ab.
```

## Result

The normalized real gauge packet is

```text
A12_R = span_R(Y) direct_sum span_R(W_1,W_2,W_3) direct_sum span_R(C_1,...,C_8),
```

with an orthonormal basis for the trace pairing.

## Boundary

BT1098 fixes the compact trace-normalized real form.  Coupling constants and physical hypercharge embeddings remain separate normalization choices.
