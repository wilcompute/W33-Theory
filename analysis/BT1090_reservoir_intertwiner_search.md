# BT1090 — Reservoir intertwiner search

BT1090 searches for the first nonzero map between the reservoir blocks

```text
R78 = T66 direct_sum A12.
```

## Input blocks

From BT1088,

```text
T66 = P22(0) direct_sum P22(1) direct_sum P22(2),
A12 = A1 direct_sum A3 direct_sum A8.
```

Each `P22(g)` decomposes as

```text
P22(g) = F13(g) direct_sum D9(g),
```

where `F13(g)` is the fixed/gauge-perp part and `D9(g)` is the shell-cycle-sum diagonal matter part.

## Natural 12-dimensional quotient

The fixed block has

```text
13 = 1 + 12.
```

Its trace line is the `1`, and the trace-free part is the `12`.  The gauge packet layer is exactly

```text
12 = 1 + 3 + 8
```

as an adjoint-profile module.  Therefore the natural first intertwiner ignores the three `D9(g)` blocks and maps the fixed 13-blocks to the gauge packet layer through their trace-free quotient.

## Candidate map

Define

```text
K : T66 -> A12
```

by

```text
K = average_g pi_12(g) circ pr_F13(g),
```

where `pr_F13(g)` projects `P22(g)` onto its 13 fixed/gauge-perp part, and `pi_12(g)` removes the scalar trace direction and identifies the trace-free 12 with `A12`.

Then

```text
rank K = 12.
```

The adjoint

```text
K^* : A12 -> T66
```

embeds a gauge packet diagonally into the three generation fixed/gauge-perp blocks.

## Interpretation

This is the first nonzero reservoir coupling compatible with the bookkeeping: the 66-layer carries three copies of the fixed/diagonal transvection data; the 12-layer receives the generation-averaged trace-free fixed part.

## Boundary

BT1090 gives the representation-level candidate.  It still needs explicit matrices for the 13-to-12 quotient and the identification of the 12 with `1+3+8` inside the centralizer module.
