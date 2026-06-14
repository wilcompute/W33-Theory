# BT997 — K3_16 middle-degree heat trace estimator

BT997 implements the production path identified in BT994/BT995: estimate the
middle-degree heat trace on the real level-1 edgewise K3_16 complex using sparse
matrix exponentials rather than dense eigensolves.

## Operator

```text
degree = 2
shape  = [9440, 9440]
nnz    = 182368
harmonic nullity = 22
```

## Method

The script builds the actual level-1 edgewise K3_16 middle Hodge Laplacian and
uses random sign trace estimation with `scipy.sparse.linalg.expm_multiply`.

## Estimates

With random seed 997 and 8 samples:

| t | estimate | standard error |
| ---: | ---: | ---: |
| 0.01 | 8730.448450900843 | 2.8812050282392105 |
| 0.05 | 6517.153579984 | 6.451863462045166 |
| 0.1 | 4689.188846613879 | 8.478521475667293 |
| 1.0 | 315.2835608902251 | 4.826383697654219 |

The estimates include the 22 zero modes plus the nonzero contribution.

## Witnesses

```text
analysis/bt997_k3_middle_heat_estimator.py
data/bt997_k3_middle_heat_estimator.json
```
