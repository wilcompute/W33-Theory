# BT1016 — K3 middle rank row format smoke test

BT1016 validates the row format before full K3_16 level-2 middle-rank runs.

## Smoke windows

| map | sample rows | sample columns | expected row weight | smoke rank |
| --- | ---: | ---: | ---: | ---: |
| degree 2 | 16 | 64 | 3 | 16 |
| degree 3 | 16 | 80 | 4 | 16 |

The deterministic windows use the same row weights as the real middle maps and
are reduced through the exact F2 bitset rank core from BT1015.

## Boundary

The smoke test does not claim the full K3 level-2 middle ranks. It verifies that
row bitsets, row weights, and reducer plumbing work before launching the full
checkout or CI rank jobs.

## Witnesses

```text
analysis/bt1016_k3_middle_rank_smoke_test.py
data/bt1016_k3_middle_rank_smoke_test.json
```
