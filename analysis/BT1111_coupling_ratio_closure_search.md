# BT1111 — Coupling-ratio closure search

BT1111 compares symbolic coupling closures for

```text
g1,g2,g3
```

against the W33 packet invariants

```text
1+3+8,
13,
66+12,
Tr(P_K)=12.
```

## Fixed facts

BT1107 showed that the reservoir geometry forces

```text
g1,g2,g3 > 0
```

and that, in kinetic-metric convention,

```text
K_g^* G_kin K_g = P_K.
```

Thus coupling ratios require an added closure principle.

## Closure A: unified packet scale

Set

```text
g1 = g2 = g3.
```

If the total packet energy is normalized by

```text
g1^2 + 3 g2^2 + 8 g3^2 = 12,
```

then

```text
g1^2=g2^2=g3^2=1.
```

This is the most symmetric closure and matches the unbroken `1+3+8` packet basis.

## Closure B: sector-equal total energy

Require the three sectors to contribute equal total energy:

```text
g1^2 = 3 g2^2 = 8 g3^2.
```

With total packet energy 12, this yields

```text
g1^2 = 4,
g2^2 = 4/3,
g3^2 = 1/2.
```

This closure treats the `1`, `3`, and `8` summands as three equal reservoirs rather than twelve equal channels.

## Closure C: W33 denominator tie to Phi_3=13

The packet rank 12 sits one below the projective denominator

```text
Phi_3 = 13 = 12 + 1.
```

A denominator-normalized convention is therefore

```text
g1^2 + 3g2^2 + 8g3^2 = 13.
```

This is not trace-normalized to the packet rank, but it ties the coupling metric to the W33 projective direction count.

## Closure D: reservoir split 66+12

The reservoir ledger

```text
78 = 66 + 12
```

suggests separating matter-bookkeeping from gauge packet.  The simplest closure keeps the gauge packet normalized to its own rank:

```text
Tr(G_A)=12.
```

This reduces back to Closure A or B depending on whether one equalizes channels or sectors.

## Scorecard

| closure | W33-native? | conservative? | numerical ratios? | note |
|---|---:|---:|---:|---|
| A unified packet scale | high | high | yes | preserves all 12 channels equally |
| B sector-equal energy | medium | medium | yes | equalizes 1,3,8 sectors |
| C Phi_3 denominator | medium | low | family unless extra constraint | uses 13 rather than packet rank 12 |
| D reservoir split | high | high | delegates to A/B | keeps 66 and 12 roles separate |

## Conclusion

The best current closure for baseline calculations is Closure A:

```text
g1:g2:g3 = 1:1:1.
```

The best exploratory closure is Closure B:

```text
g1^2:g2^2:g3^2 = 4:4/3:1/2.
```

No closure is yet derived as a theorem from W33; they remain normalization conventions to test against later physical observables.
