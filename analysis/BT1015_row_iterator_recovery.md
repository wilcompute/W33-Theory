# BT1015 — Full row iterator recovery by module split

BT1015 recovers the blocked BT1012 monolithic iterator by splitting it into
smaller accepted modules.

## Recovered modules

```text
analysis/bt1015_f2_bitset_rank_core.py
analysis/bt1015_k3_middle_stream_contracts.py
```

## K3 level-2 middle contracts

```text
f-vector = [2776, 45120, 152960, 184320, 73728]
```

| map | rows | cols | nnz | row weight | target rank |
| --- | ---: | ---: | ---: | ---: | ---: |
| degree 2 | 45120 | 152960 | 458880 | 3 | 42345 |
| degree 3 | 152960 | 184320 | 737280 | 4 | 110593 |

Rows are Python integer bitsets over high-dimensional simplex columns and are
reduced by the exact F2 reducer in `bt1015_f2_bitset_rank_core.py`.

## Boundary

The reducer and stream contracts are now reusable. Full face generation remains
the next checkout/CI layer.

## Witnesses

```text
data/bt1015_row_iterator_recovery.json
```
