# BT1108 — Generation-symmetry breaking ansatz

BT1108 perturbs the all-generation reservoir projector while preserving the trace-free quotient structure.

## Symmetric projector recap

BT1104 writes the active-domain projector as

```text
P_K = [B B B; B B B; B B B]
```

on the three `F13` blocks, with all `D9` blocks killed.  This is generation-symmetric and has rank 12.

## Weighted readout

Introduce positive generation weights

```text
w0, w1, w2 > 0
```

and define

```text
s = w0^2 + w1^2 + w2^2.
```

Replace the generation-average readout by

```text
K_w = (1/sqrt(s)) [ w0 pi12  w1 pi12  w2 pi12 ].
```

This keeps the same target quotient but changes how strongly each generation header contributes.

## Projector block formula

The target row Gram is unchanged up to the same BT1099 factor:

```text
K_w K_w^* = pi12 pi12^* / s * s = pi12 pi12^*.
```

After whitening, the domain projector has generation blocks

```text
P_w(g,h) = (w_g w_h / s) * P_tracefree_13,
```

where

```text
P_tracefree_13 = pi12^T (pi12 pi12^T)^(-1) pi12.
```

Equivalently, it is the trace-free projector on each `F13` block, weighted by the rank-one generation matrix

```text
M_w = (1/s) w w^T.
```

## Rank and invariants

For all positive weights,

```text
rank(P_w) = 12,
P_w^2 = P_w,
D9 subset ker(P_w),
trace-free quotient preserved.
```

The generation-symmetric case is recovered by

```text
w0 = w1 = w2.
```

## First-order perturbation

Set

```text
w_g = 1 + epsilon a_g,
```

with small `epsilon`.  The generation matrix changes as

```text
M_w = (1/3) 11^T + (epsilon/3)(a 1^T + 1 a^T - (2/3)(sum a) 11^T) + O(epsilon^2).
```

If

```text
sum a_g = 0,
```

the first-order perturbation is purely traceless in generation space.

## Boundary

BT1108 provides a controlled generation-breaking ansatz.  It does not derive the weights from masses, Yukawa data, or W33 centralizer orbits.
