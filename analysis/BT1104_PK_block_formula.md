# BT1104 — Block formula for the reservoir domain projector P_K

BT1104 derives the explicit block form of

```text
P_K = K^* (K K^*)^{-1} K = K_white^* K_white
```

on the three generation blocks of

```text
T66 = (F13 + D9)_0 direct_sum (F13 + D9)_1 direct_sum (F13 + D9)_2.
```

## Ingredients

For each generation, `K` uses the quotient

```text
pi12(x0,...,x12) = (x0-x12, ..., x11-x12)
```

and ignores the `D9` block.  With the generation average convention,

```text
K = (1/3) [ pi12  pi12  pi12 ]
```

on the three `F13` blocks, and zero on the three `D9` blocks.

BT1099 gave

```text
K K^* = (1/3)(I_12 + J_12),
```

so

```text
(K K^*)^{-1} = 3 I_12 - (3/13) J_12.
```

## The 13 by 13 block B

Define

```text
B = (1/9) pi12^T (3 I_12 - (3/13) J_12) pi12.
```

Then the `F13`-to-`F13` block entries are:

```text
B_ab = 1/3 delta_ab - 1/39,       0 <= a,b <= 11
B_a,12 = B_12,a = -1/39,          0 <= a <= 11
B_12,12 = 4/13.
```

Every row of `B` sums to zero, reflecting the removed trace line.

## Full 66 by 66 projector

In generation block form,

```text
P_K =
[ B  B  B
  B  B  B
  B  B  B ]
```

on the `F13_0 + F13_1 + F13_2` part, and zero on every row/column touching a `D9` block.

Equivalently,

```text
P_K|_{D9} = 0.
```

## Checks

```text
rank(P_K) = 12
P_K^2 = P_K
ker(P_K) = ker(K)
dim ker(K) = 54.
```

The all-to-all generation block structure is the algebraic signature of the generation-averaged readout: the projector does not select one generation, it projects onto the common trace-free gauge-packet component shared by all three.

## Boundary

BT1104 gives the exact rational block formula.  It does not choose physical coupling constants or break generation symmetry.
