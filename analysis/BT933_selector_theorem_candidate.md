# BT933 — Selector theorem candidate

BT933 packages BT931 and BT932 into a concrete selector theorem candidate.

## What failed as a selector

- Positivity alone fails: BT931 found that all 512 random basis choices still gave valid unimodular positive lifts.
- Vertex equivariance fails: BT932 found that the BT926 vertex E8 witness has trivial preserving symmetry, so equivariance there is vacuous.

## Candidate selector rule

The current least-arbitrary rule is:

1. minimize total support of the four hyperbolic pairs in the chain representatives;
2. tie-break by support spread;
3. require determinant-1 positive-definite lift into the BT926 vertex E8 witness;
4. require determinant-1 positive-definite lift into the tetracode E8 witness;
5. do not count vertex-equivariance as a selector.

## Current candidate score

```text
support_sum = 76
support_spread = 8
vertex_metric_penalty = 0
tetracode_metric_penalty = 0
equivariance_penalty = 0
total_score = 84
```

Best seen sorted support profile:

```text
[6, 6, 6, 10, 10, 10, 14, 14]
```

## Boundary

This is a theorem candidate, not a proved uniqueness theorem. The next proof obligation is exhaustive: classify support-minimal symplectic bases and check whether dual vertex+tetracode compatibility leaves one orbit.

## Witness

```text
analysis/bt933_selector_theorem_candidate.py
data/bt933_selector_theorem_candidate.json
```
