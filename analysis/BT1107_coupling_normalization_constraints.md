# BT1107 — Coupling normalization constraints

BT1107 derives the symbolic constraints on the gauge-coupling slots

```text
g1, g2, g3
```

from the whitened reservoir readout, trace pairing, and projector ledger.

## Normalized packet basis

BT1098--BT1102 fix an orthonormal compact packet basis for

```text
A12 = u(1) direct_sum su(2) direct_sum su(3)
```

under

```text
<X,Y> = -Re Tr(XY).
```

BT1101 fixes the whitened readout

```text
K_white : T66 -> A12
```

with

```text
K_white K_white^* = I_12.
```

## Coupling-scaled packet metric

Introduce

```text
G_A = diag(g1^2 I_1, g2^2 I_3, g3^2 I_8).
```

The coupling-scaled readout is

```text
K_g = G_A^{1/2} K_white.
```

Then

```text
K_g K_g^* = G_A.
```

Equivalently, if the kinetic metric is

```text
G_kin = G_A^{-1} = diag(g1^{-2} I_1, g2^{-2} I_3, g3^{-2} I_8),
```

then

```text
K_g^* G_kin K_g = K_white^* K_white = P_K.
```

Thus the reservoir projector is coupling-independent once the kinetic metric convention is used.

## Forced constraints

The reservoir geometry forces only nondegeneracy and positivity:

```text
g1, g2, g3 > 0.
```

It does not by itself determine numerical ratios.

## Optional normalization conventions

Several conventional closures are possible:

1. Trace-normalized total packet energy:

```text
g1^2 + 3 g2^2 + 8 g3^2 = 12.
```

2. Unified packet scale:

```text
g1 = g2 = g3.
```

With the trace-normalized convention this gives

```text
g1 = g2 = g3 = 1.
```

3. Sector-equal total energy:

```text
g1^2 = 3 g2^2 = 8 g3^2.
```

With trace-normalized total packet energy this gives

```text
g1^2 = 4,
g2^2 = 4/3,
g3^2 = 1/2.
```

## Boundary

BT1107 separates geometry from convention.  The W33 reservoir readout fixes the coisometry/projector structure, but numerical coupling ratios require an additional physical or arithmetic closure principle.
