# BT1009 — K3_16 level-2 middle rank block eliminator

BT1009 implements the staged sparse mod-2 eliminator interface for the two
remaining K3_16 level-2 middle boundary maps.

## Targets

```text
f-vector = [2776, 45120, 152960, 184320, 73728]
```

Middle maps:

| map | shape rows x cols | nnz | target rank |
| --- | ---: | ---: | ---: |
| second boundary | 45120 x 152960 | 458880 | 42345 |
| third boundary | 152960 x 184320 | 737280 | 110593 |

## Algorithm

Rows are represented as Python integer bitsets and reduced over F2 by sparse
Gaussian elimination. This is exact arithmetic, promoted to the K3_16 level-2
middle maps.

## Boundary

The exact eliminator interface and targets are committed. The full middle-rank
runs are intentionally left for checkout or CI wall-clock budget; they were not
claimed as completed in this connector session.

## Witnesses

```text
analysis/bt1009_k3_level2_middle_rank_block_eliminator.py
data/bt1009_k3_level2_middle_rank_block_eliminator.json
```
