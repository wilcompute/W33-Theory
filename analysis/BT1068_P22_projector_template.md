# BT1068 — P22 projector template

BT1068 builds the first explicit rank-checked template for the BT1065 split.

## Target

BT1065 identified the dimension target

```text
162 = 96 + 66 = 3*(32 + 22).
```

So we need one rank-22 complement projector per generation.

## Template rule

For each generation, define `P22(g)` as the diagonal slot projector onto:

```text
all singlet weakslot S entries: 2 chirality * 3 fiber * 3 color = 18
plus four doublet anchor entries: 2 chirality * 2 doublet slots at fiber=0,color=0 = 4
```

Therefore

```text
rank P22(g) = 18 + 4 = 22.
```

The physical projector template is

```text
P96 = I_162 - direct_sum_g P22(g).
```

## Rank checks

```text
rank(P22 total) = 3 * 22 = 66
rank(P96)       = 162 - 66 = 96
P22^2           = P22
P96^2           = P96
P22 P96         = 0
```

## Explicit selected indices

```text
g0: 0,1,2,9,10,11,18,19,20,81,82,83,90,91,92,99,100,101,3,6,84,87
g1: 27,28,29,36,37,38,45,46,47,108,109,110,117,118,119,126,127,128,30,33,111,114
g2: 54,55,56,63,64,65,72,73,74,135,136,137,144,145,146,153,154,155,57,60,138,141
```

## Boundary

This is a concrete idempotent rank template on the BT1057 slot table. It is not yet the true BT876 transvection projector. The next task is to replace this slot rule with the actual W33 transvection fixed/diagonal projector and check whether it selects the same kind of 66-complement.
