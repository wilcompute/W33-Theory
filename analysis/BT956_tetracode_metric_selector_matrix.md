# BT956 — Tetracode metric selector matrix

BT956 recovers the missing BT930 chain-to-tetracode matrix and evaluates all six exact support-60 minimizers in the tetracode E8 metric gauge.

## Result

The recovered matrix is an 8 by 8 binary matrix with determinant absolute value 1 and satisfies

```text
M^T G_tetracode M = B_chain mod 2
```

The base lifted Gram has determinant 1 and is positive definite.

## Candidate test

Five of the six support-60 minimizers give positive unimodular tetracode lifts. Candidate 5 is singular.

The tetracode metric winner is minimizer 2:

```text
[[3,68], [4,42], [38,65], [90,144]]
```

Winner tetracode score:

```text
trace = 56
frobenius_squared = 1320
max_abs_entry = 16
min_eigenvalue = 0.004850303102819915
```

## Reading

The tetracode metric selector agrees with BT954's vertex metric selector. Both independently select minimizer 2 from the six exact support-minimal decompositions.

## Witness

```text
analysis/bt956_tetracode_metric_selector_matrix.py
data/bt956_tetracode_metric_selector_summary.json
```
