# BT1000 — K3_16 level-2 feasibility gate

BT998 proved CP2_9 level 2 directly. BT1000 asks whether K3_16 level 2 should be
attempted directly, blockwise, or only through sparse trace estimates.

## Predicted size

From the BT993 edgewise recurrence:

```text
K3_16 level 2 f-vector = [2776, 45120, 152960, 184320, 73728]
```

For comparison:

```text
CP2_9 level 2 f-vector = [459, 5976, 19344, 23040, 9216]
```

The K3/CP2 level-2 face ratios are approximately:

```text
[6.0479, 7.5502, 7.9074, 8.0, 8.0]
```

## Sparse-size estimates

Exact boundary nonzero counts by simplex incidence:

```text
[90240, 458880, 737280, 368640]
```

Planning estimates for K3_16 level-2 Hodge Laplacian nnz:

```text
[110488, 2835035, 2956737, 1773920, 442368]
```

Using a conservative 16-byte per nonzero storage rule, the largest estimated
Laplacian block is about 45.12 MiB before solver/workspace overhead.

## Verdict

K3_16 level 2 is feasible as a staged sparse/blockwise computation. It should not
be treated as a monolithic dense rank/eigensolve job.

## Witnesses

```text
analysis/bt1000_k3_level2_feasibility_gate.py
data/bt1000_k3_level2_feasibility_gate.json
```
