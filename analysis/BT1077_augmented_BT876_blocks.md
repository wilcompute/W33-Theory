# BT1077 — Augmented BT876 block export

BT1077 patches the BT1076 gap by reconstructing the BT876 transvection data and exporting the actual permutation/fixed/cycle data needed for the true projector search.

## Exported data

```text
data/bt1077_augmented_bt876_blocks.json
```

contains:

```text
R_perm
fixed_indices
neighbour_indices
shell_indices
R_cycles_all
R_cycles_on_shell
```

## Main extracted blocks

The selected transvection has 13 fixed indices:

```text
0,1,2,3,13,14,15,16,17,18,19,20,21
```

The shell has 27 indices arranged into nine 3-cycles:

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

## Critical correction

The BT876 split

```text
22 + 9 + 9
```

is not a split into three disjoint point-index subsets. It is a Fourier/eigenspace split for the transvection action on `C[40]`.

The grade-zero 22-dimensional space is:

```text
13 fixed basis vectors + 9 shell-cycle sums.
```

The two 9-dimensional off-grade spaces are one Fourier mode on each shell 3-cycle.

## Consequence for P22

The true BT876 `P22` is not a diagonal selector of 22 points. It is a linear projector onto fixed basis vectors plus cycle-sum vectors. BT1068 remains a valid rank/idempotent slot template, but it is not the true BT876 projector.
