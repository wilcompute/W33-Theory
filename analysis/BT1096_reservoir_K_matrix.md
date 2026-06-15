# BT1096 — Matrix form of K:T66 -> A12

BT1096 turns the BT1090/BT1092 reservoir map into a sparse rational matrix.

## Domain ordering

The domain is

```text
T66 = P22(0) direct_sum P22(1) direct_sum P22(2).
```

Each generation block has dimension 22 and is ordered as

```text
F13 columns 0..12, followed by D9 columns 13..21.
```

Thus generation `g` starts at column `22*g`.

## Target ordering

The target is the BT1095 basis

```text
Y, W0, Wp, Wm, C12, C21, C13, C31, C23, C32, C0, C8.
```

## Matrix rule

For row `i=0..11` and generation `g=0..2`, set

```text
K[i, 22*g + i]  =  1/3
K[i, 22*g + 12] = -1/3.
```

All other entries are zero.  In particular, every `D9` column is in the kernel.

## Checks

```text
shape(K) = 12 x 66
nonzero entries = 72
rank(K) = 12
kernel dimension = 54.
```

The rank is 12 because each row has a pivot in the first generation's `F13` block, while the trace direction in each `F13` block and all `D9` directions vanish under the quotient.

## Witnesses

```text
analysis/bt1096_reservoir_K_matrix.py
data/bt1096_reservoir_K_matrix.json
```
