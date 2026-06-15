# BT1054 — Amplitude protocol

BT1054 records a protocol for replacing the free sector amplitudes from BT1046 with quantities derived from W33 data.

## Sector labels

```text
lambda = 0, 4, 10, 16
sector dimensions = 81, 120, 24, 15
```

## Protocol

Let `P_lam` be the projector onto a sector and let `Q` be the finite scalar slot operator. Define the sector average

```text
A_lam^2 = trace(P_lam Q^2 P_lam) / trace(P_lam)
```

and similarly

```text
A_lam^4 = trace(P_lam Q^4 P_lam) / trace(P_lam).
```

## Substitution targets

```text
a0  -> A_0
a4  -> A_4
a10 -> A_10
a16 -> A_16
```

## Boundary

This is a derivation protocol, not a completed numerical derivation. The missing object is the concrete W33 scalar slot operator `Q` on the 240-chain carrier.
