# BT954 — Metric selector among support-60 minimizers

BT954 tests the six exact BT951 minimizers in the BT929 vertex E8 metric gauge.

## Result

Five of the six support-60 minimizers give positive unimodular integer vertex lifts. Candidate 5 is singular in this gauge.

The unique lowest-height positive unimodular lift is minimizer 2:

```text
[[3,68], [4,42], [38,65], [90,144]]
```

Winner score:

```text
trace = 38
frobenius_squared = 444
max_abs_entry = 8
min_eigenvalue = 0.010596380201028571
```

## Reading

Support minimization reduces the selector to six minimizers. The vertex E8 metric height then selects one candidate in the BT929 gauge.

## Boundary

The tetracode metric gauge should still be evaluated with an explicit stored BT930 tetracode isometry matrix. The current BT930 JSON records existence of that map but not the full matrix.

## Witness

```text
analysis/bt954_metric_selector_among_support60.py
data/bt954_metric_selector_among_support60.json
```
