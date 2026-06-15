# BT1050 — Generation scalar ledger

BT1050 inserts the BT1047 generation/fiber invariants into the BT1048 scalar coefficient ledger.

## Invariants

```text
ys = alpha + 2 beta
yd = alpha - beta
T2 = ys^2 + 2 yd^2
T4 = ys^4 + 2 yd^4
```

## Sector amplitudes

```text
a0  = A0(ys, yd)
a4  = A4(ys, yd)
a10 = A10(ys, yd)
a16 = A16(ys, yd)
```

## Scalar traces

```text
Phi2 = 54 A0^2 h2 + 80 A4^2 h2 + 16 A10^2 h2 + 10 A16^2 h2
Phi4 = 54 A0^4 h2^2 + 80 A4^4 h2^2 + 16 A10^4 h2^2 + 10 A16^4 h2^2
DeltaPhi2 = 320 A4^2 h2 + 160 A10^2 h2 + 160 A16^2 h2
```

## Boundary

This is symbolic only. The `A` functions are constrained by W33 generation/fiber invariants, but they are not yet derived from chain maps.
