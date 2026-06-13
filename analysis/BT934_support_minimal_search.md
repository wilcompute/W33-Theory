# BT934 — Support-minimal selector search

BT934 begins the deterministic support-minimal search demanded by BT933.

## Current best certificate

From BT931:

```text
support_sum = 76
support_spread = 8
sorted profile = [6, 6, 6, 10, 10, 10, 14, 14]
```

The 255 nonzero classes of H have support distribution:

| support | count |
|---:|---:|
| 6 | 10 |
| 8 | 20 |
| 10 | 52 |
| 12 | 85 |
| 14 | 54 |
| 16 | 29 |
| 18 | 4 |
| 20 | 1 |

## Branch-and-bound rule

1. enumerate hyperbolic pairs `e,f` with `B(e,f)=1`;
2. prune partial decompositions whose support lower bound exceeds the current best;
3. rank-reduce the symplectic orthogonal complement after each pair;
4. tie-break by support spread and sorted support profile.

## Honest boundary

This pass does **not** claim that support sum 76 is globally minimal or unique. It converts the BT931 stress evidence into a deterministic proof scaffold and records the current best support certificate. The exhaustive proof is the next step.

## Witness

```text
analysis/bt934_support_minimal_search.py
data/bt934_support_minimal_search.json
```
