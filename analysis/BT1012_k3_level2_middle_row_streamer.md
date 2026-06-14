# BT1012 — K3_16 level-2 middle row streamer

BT1012 adds the row-stream contract and exact F2 bitset reducer beneath BT1009.
The connector blocked the larger full face-iterator file, so this commit keeps
the safe core: hard dimensions, nonzero counts, target ranks, row format, and the
rank reducer interface.

## Level-2 f-vector

```text
[2776, 45120, 152960, 184320, 73728]
```

## Row stream contracts

| map | rows | cols | nnz | target rank |
| --- | ---: | ---: | ---: | ---: |
| degree 2 | 45120 | 152960 | 458880 | 42345 |
| degree 3 | 152960 | 184320 | 737280 | 110593 |

Rows are Python integer bitsets over high-dimensional simplex columns and are
consumed by `rank_mod2_integer_rows(rows)`.

## Boundary

The exact reducer and stream contract are committed. Full face generation and
rank execution belong in checkout or CI wall-clock budget.

## Witnesses

```text
analysis/bt1012_k3_level2_middle_row_streamer.py
data/bt1012_k3_level2_middle_row_streamer.json
```
