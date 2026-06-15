# BT1114 — Coupling-closure falsifier table

BT1114 turns the BT1111 coupling closures into explicit algebraic predictions.

## Shared definitions

The packet metric is

```text
G_A = diag(g1^2 I_1, g2^2 I_3, g3^2 I_8).
```

The weighted packet trace is

```text
Tr(G_A) = g1^2 + 3 g2^2 + 8 g3^2.
```

The sector energies are

```text
E1 = g1^2,
E2 = 3 g2^2,
E3 = 8 g3^2.
```

## Closure A: channel-equal baseline

```text
g1:g2:g3 = 1:1:1,
Tr(G_A)=12.
```

Predictions:

```text
(g1^2,g2^2,g3^2) = (1,1,1)
(E1,E2,E3) = (1,3,8)
sector fractions = (1/12, 1/4, 2/3)
```

This closure preserves all twelve packet channels equally.  It predicts unequal sector energies exactly proportional to the dimensions `1:3:8`.

## Closure B: sector-equal energy

```text
g1^2 = 3 g2^2 = 8 g3^2,
Tr(G_A)=12.
```

Predictions:

```text
(g1^2,g2^2,g3^2) = (4,4/3,1/2)
(E1,E2,E3) = (4,4,4)
sector fractions = (1/3,1/3,1/3)
```

This closure equalizes the `u(1)`, `su(2)`, and `su(3)` sector energies, not the twelve channels.

## Falsifier logic

Any later W33 or physical closure must specify which invariant is held fixed:

```text
channel equality -> Closure A,
sector equality  -> Closure B,
Phi_3 denominator -> Tr(G_A)=13 family,
reservoir split   -> keep 66 bookkeeping decoupled from 12 packet.
```

The falsifier table is therefore:

| closure | channel energies | sector energies | decisive observable |
|---|---|---|---|
| A | equal | 1:3:8 | channel-uniform packet action |
| B | 4,4/3,1/2 per channel | equal | sector-uniform packet action |
| C | family | family | projective denominator 13 appears in packet norm |
| D | delegates to A/B | delegates to A/B | 66-block remains kinetically decoupled |

## Boundary

BT1114 creates falsifiable algebraic predictions, not measured Standard Model coupling values.  Any physical comparison must specify scale, normalization convention, and whether `g_i` are bare, spectral-action, or renormalized couplings.
