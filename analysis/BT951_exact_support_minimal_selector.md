# BT951 — Exact support-minimal selector theorem

BT951 supersedes the earlier support-76 selector candidate.

## Result

The exact support-minimal hyperbolic basis problem for the BT925 form has minimum

```text
support_sum = 60
```

not 76.

There are six unordered minimizing decompositions in the chosen BT925 coordinate gauge, all with the same sorted support profile:

```text
[6, 6, 6, 6, 6, 8, 10, 12]
```

## Certificate method

The verifier uses Bellman recursion over symplectic subspaces. At each step it chooses an unordered hyperbolic pair `B(e,f)=1`, recurses on the symplectic orthogonal quotient, and memoizes subspaces by 8-bit masks.

Reference run:

```text
states_explored = 5914
minimizer_count = 6
old support-76 candidate = disproved
```

## Boundary

This proves the support-minimal value in the BT925 coordinate gauge. The next quotient problem is to classify the six minimizers under the transported tetracode stabilizer action.

## Witness

```text
analysis/bt951_exact_support_minimal_selector.py
data/bt951_exact_support_minimal_selector.json
```
