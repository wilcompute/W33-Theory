# BT1105 — Gauge-coupled bracket ledger

BT1105 introduces symbolic gauge-coupling slots on the normalized BT1102 packet

```text
A12_R = u(1) direct_sum su(2) direct_sum su(3).
```

## Normalized basis

BT1102 uses orthonormal compact generators

```text
Y,
W_a = i sigma_a / sqrt(2),
C_a = i lambda_a / sqrt(2),
```

for the trace pairing

```text
<X,Y> = -Re Tr(XY).
```

The uncoupled brackets are

```text
[Y, anything] = 0,
[W_a,W_b] = -sqrt(2) epsilon_abc W_c,
[C_a,C_b] = -sqrt(2) f_abc C_c.
```

## Coupling-scaled packet coordinates

Introduce symbolic coupling slots

```text
g1, g2, g3
```

and define scaled packet coordinates

```text
Yhat   = g1 Y,
What_a = g2 W_a,
Chat_a = g3 C_a.
```

The trace norms become

```text
<Yhat,Yhat>     = g1^2,
<What_a,What_b> = g2^2 delta_ab,
<Chat_a,Chat_b> = g3^2 delta_ab.
```

## Coupled bracket constants

The U1 line remains central:

```text
[Yhat, anything] = 0.
```

For weak and color:

```text
[What_a, What_b] = -sqrt(2) g2 epsilon_abc What_c,
[Chat_a, Chat_b] = -sqrt(2) g3 f_abc Chat_c.
```

All cross-sector brackets remain zero.

## Kinetic-metric convention

Equivalently, one may keep the normalized basis fixed and put couplings into the gauge kinetic metric:

```text
G_kin = g1^{-2} on u(1),
G_kin = g2^{-2} on su(2),
G_kin = g3^{-2} on su(3).
```

The scaled-basis and kinetic-metric conventions are related by a diagonal change of packet coordinates.

## Boundary

BT1105 introduces symbolic coupling slots only.  It does not derive numerical values for `g1,g2,g3` from W33 data.
