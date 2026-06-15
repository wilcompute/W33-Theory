# BT1069 — Solving the `S2=S4=64` coefficient constraint

BT1069 solves the simplest idempotent sector-coefficient version of the BT1066 constraints.

## Constraint system

For

```text
Q = c0 P0 + c4 P4 + c10 P10 + c16 P16,
```

BT1066 defined

```text
S2 = 54 c0^2 + 80 c4^2 + 16 c10^2 + 10 c16^2
S4 = 54 c0^4 + 80 c4^4 + 16 c10^4 + 10 c16^4.
```

The 96-support normalization requires

```text
S2 = 64,
S4 = 64.
```

## Idempotent sector solution

If the sector coefficients are projector-like,

```text
c_lambda in {0,1},
```

then the only subset of weights

```text
54, 80, 16, 10
```

summing to 64 is

```text
54 + 10 = 64.
```

Therefore the unique idempotent sector solution is

```text
c0  = 1
c4  = 0
c10 = 0
c16 = 1
```

or

```text
Q_64 = P0 + P16.
```

## Consequences

The support dimension of this sector projector is

```text
dim(E0) + dim(E16) = 81 + 15 = 96.
```

The mixed trace coefficient is

```text
M2 = 320 c4^2 + 160 c10^2 + 160 c16^2 = 160.
```

So

```text
tr_240(Phi^2)          = 64 h2
tr_240(Phi^4)          = 64 h2^2
tr_240(Delta_1 Phi^2) = 160 h2.
```

## Reading

This is a real structural hit: the simplest 96-normalized scalar projector is not `Delta_1/4`, but the endpoint spectral projector

```text
P0 + P16.
```

It selects the harmonic 81-sector plus the 15-sector, matching the recurring W33 `81+15=96` pattern.

## Boundary

This solves the idempotent sector-coefficient constraint on the 240-chain carrier. It does not by itself prove that `P0+P16` is the physical particle projector on the 162-slot carrier, though the dimension match is now highly suggestive.
