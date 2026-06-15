# BT1099 — Spectrum of K*K and KK*

BT1099 computes the exact singular-value structure of the BT1096 reservoir map

```text
K : T66 -> A12.
```

## Matrix rule recalled

For rows `i=0,...,11` and generations `g=0,1,2`,

```text
K[i,22*g+i]  =  1/3,
K[i,22*g+12] = -1/3,
```

and all other entries vanish.

## Row Gram matrix

The row Gram matrix is

```text
KK* = (1/3) I_12 + (1/3) J_12,
```

where `J_12` is the all-ones matrix.  Indeed, diagonal entries are

```text
3*((1/3)^2 + (1/3)^2) = 2/3,
```

and off-diagonal entries share the three anchor columns, giving

```text
3*((-1/3)*(-1/3)) = 1/3.
```

## Eigenvalues

Since `J_12` has eigenvalues `12,0,...,0`,

```text
spec(KK*) = {13/3, (1/3)^11}.
```

Therefore

```text
spec(K*K) = {13/3, (1/3)^11, 0^54}.
```

The singular values are

```text
sqrt(13/3), 1/sqrt(3) with multiplicity 11, and 0 with multiplicity 54.
```

## Interpretation

The generation-averaged trace-free readout has one enhanced uniform target direction and eleven transverse directions.  The 54-dimensional kernel consists of all D9 bookkeeping directions plus the trace/equalizer redundancies inside the three F13 blocks.

## Optional whitening

A normalized readout can be obtained by

```text
K_white = (KK*)^{-1/2} K,
```

which satisfies

```text
K_white K_white* = I_12.
```

## Boundary

BT1099 computes the exact spectrum of the prototype readout.  It does not yet decide whether the enhanced `13/3` direction should be physically retained, rescaled, or projected away.
