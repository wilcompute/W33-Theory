# BT938 — Low-support branch-and-bound scaffold

BT938 strengthens BT934 by turning the support-minimal problem into a bounded recursive search target.

## Known data

The current best profile is:

```text
[6, 6, 6, 10, 10, 10, 14, 14]
```

with support sum 76.

The raw lower bound from the eight smallest nonzero class supports is only:

```text
6+6+6+6+6+6+6+6 = 48
```

so support distribution alone cannot prove optimality.

## Implemented scaffold

The search rules are:

1. sort H classes by support;
2. maintain symplectic-rank feasibility;
3. lower-bound partial support before continuing;
4. require `B(e_i,f_i)=1` and orthogonality to earlier pairs.

## Honest boundary

BT938 does not yet prove that no support sum below 76 exists. It records the exact gap between the trivial lower bound 48 and the best certificate 76, and specifies the recursive certificate that must be completed.

## Witness

```text
analysis/bt938_low_support_branch_bound.py
data/bt938_low_support_branch_bound.json
```
