# BT1101 — Whitened reservoir readout

BT1101 constructs the exact whitened version of the BT1096 reservoir readout

```text
K : T66 -> A12.
```

## Starting spectrum

BT1099 found

```text
KK* = (1/3) I_12 + (1/3) J_12,
```

with eigenvalues

```text
13/3 on the uniform target line,
1/3  on the 11-dimensional transverse target space.
```

Let

```text
P_u = J_12 / 12,
P_t = I_12 - J_12 / 12.
```

Then

```text
KK* = (13/3) P_u + (1/3) P_t.
```

## Whitening operator

The inverse square root is

```text
W = (KK*)^{-1/2} = sqrt(3/13) P_u + sqrt(3) P_t.
```

Define

```text
K_white = W K.
```

Then

```text
K_white K_white* = I_12.
```

## Domain projector

The corresponding rank-12 domain projector is

```text
P_K = K* (KK*)^{-1} K = K_white* K_white.
```

Thus

```text
P_K^2 = P_K,
rank(P_K) = 12,
ker(P_K) = ker(K),
dim ker(K) = 54.
```

## Uniform/transverse split

The whitened readout explicitly separates:

```text
uniform packet mode:    scale sqrt(3/13),
transverse packet modes: scale sqrt(3).
```

The enhanced BT1099 direction is therefore not removed; it is normalized into an orthonormal packet coordinate.

## Boundary

BT1101 fixes the canonical mathematical whitening of the prototype readout.  It does not decide whether the physical theory should use `K`, `K_white`, or a coupling-rescaled variant.
