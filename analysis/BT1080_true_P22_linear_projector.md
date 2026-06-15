# BT1080 — True P22 linear projector

BT1080 constructs the actual BT876 grade-zero projector on `C[40]` from the augmented BT1077 transvection data.

## Input from BT1077

The transvection has 13 fixed basis indices:

```text
0,1,2,3,13,14,15,16,17,18,19,20,21
```

and nine shell 3-cycles:

```text
[4,6,5]
[7,9,8]
[10,12,11]
[22,24,23]
[25,27,26]
[28,30,29]
[31,32,33]
[34,35,36]
[37,38,39]
```

## Projector formula

The true BT876 grade-zero projector is

```text
P22 = fixed identity block + cycle-average blocks.
```

For every fixed index `i`,

```text
P22[i,i] = 1.
```

For every shell cycle `C={a,b,c}`, the projector restricts to the average matrix

```text
(1/3) * ones(3,3)
```

on that cycle.

## Rank and idempotence

Each fixed index contributes rank 1. Each 3-cycle average contributes rank 1.

```text
rank(P22) = 13 + 9 = 22
P22^2 = P22
```

The complementary off-grade projector has rank

```text
40 - 22 = 18 = 9 + 9.
```

## Important correction

This is not a diagonal selector of 22 points. It is a linear Fourier/eigenspace projector: fixed basis vectors plus cycle-sum vectors.

## Consequence

The correct BT876 object to lift into the 162-slot carrier is this linear projector, not the BT1068 slot-rule diagonal template.
