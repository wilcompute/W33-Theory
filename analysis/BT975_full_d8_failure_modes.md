# BT975 — Full D8 lane partition failure modes

BT975 classifies how the full square lane action interacts with the current light/cache split.

## Result

```text
current partition = light [0,1] versus cache [2,3]
D8 order = 8
preserving elements = 4
breaking elements = 4
```

No nontrivial 2+2 lane partition is invariant under the full transitive D8 action.

## Reading

The present ABI partition is preserved by a four-element subgroup only. Full D8 requires either all four lanes as one family or a refined non-partition ABI.

## Witness

```text
analysis/bt975_full_d8_failure_modes.py
data/bt975_full_d8_failure_modes_summary.json
```
