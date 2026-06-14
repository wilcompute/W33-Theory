# BT998 — CP2_9 level-2 edgewise rank pipeline

BT998 pushes the corrected R3 tower one refinement level deeper for CP2_9. It
uses the BT991 local template twice, enumerates all level-2 faces, and computes
boundary ranks over `F2` by sparse bitset Gaussian elimination.

## Result

```text
f-vector            = [459, 5976, 19344, 23040, 9216]
boundary ranks mod2 = [458, 5518, 13825, 9215]
Betti mod2          = [1, 0, 1, 0, 1]
Euler characteristic = 3
```

This matches the BT993 edgewise recurrence and preserves CP2_9 topology at level
2.

## Reading

BT998 is the memory-safe checkpoint before attempting K3_16 level 2. It proves
that the local template and recurrence do not merely work at level 1; they can be
iterated and still produce a rank-certified Hodge profile.

## Witnesses

```text
analysis/bt998_cp2_level2_edgewise_rank_pipeline.py
data/bt998_cp2_level2_edgewise_rank_pipeline.json
```
