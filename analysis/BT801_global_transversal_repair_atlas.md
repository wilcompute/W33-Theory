# BT801 - Global Transversal Repair Atlas

BT800 proved the diagonal quotient and shadow split for one cube chart.  BT801
globalizes it to all 540 skew-line charts of W(3,3).

For every chart:

```text
four common transversals
four base antipode pairs = transversal base pairs
shadow collinearity = K4,4
shadow noncollinearity = K4 + K4
shadow pairs = perfect matching across the two K4 sheets
```

The global slot count is:

```text
540 charts * 4 transversals = 2160 chart-transversal slots.
```

Each W33 line appears as a transversal in exactly:

```text
54 charts.
```

So the diagonal repair is not a base-chart artifact.  It is an atlas law.

## Validation

Run:

```bash
python3 analysis/bt801_global_transversal_repair_atlas.py
```
