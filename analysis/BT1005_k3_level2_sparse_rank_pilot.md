# BT1005 — K3_16 level-2 sparse rank pilot

BT1005 gives the K3_16 level-2 rank computation exact sparse targets before any
large blockwise elimination is attempted.

## Input

From the BT993 recurrence:

```text
f-vector = [2776, 45120, 152960, 184320, 73728]
```

K3 topology target:

```text
Betti = [1, 0, 22, 0, 1]
```

## Rank targets

The target boundary ranks are:

```text
[2775, 42345, 110593, 73727]
```

The Euler characteristic is 24.

## Sparse stage plan

1. Compute the first boundary rank by vertex-edge connectivity; target `2775`.
2. Compute the top boundary rank by sparse elimination or dual connectivity;
   target `73727`.
3. Compute the two middle boundary ranks blockwise; targets `42345` and `110593`.
4. Verify recovered Betti profile `[1,0,22,0,1]`.

Exact boundary nonzero counts by simplex incidence:

```text
[90240, 458880, 737280, 368640]
```

## Witnesses

```text
analysis/bt1005_k3_level2_sparse_rank_pilot.py
data/bt1005_k3_level2_sparse_rank_pilot.json
```
