# BT937 — Transported tetracode action on chain H

BT935 found that the tetracode glue has signed monomial symmetry group of order 48. BT937 transports the coordinate-permutation subgroup through the BT930 chain-to-tetracode isometry.

## Transported subgroup

The coordinate permutations are:

```text
[0,1,2,3]
[0,2,3,1]
[0,3,1,2]
```

On the four A2 blocks this is a C3 action with order profile:

```text
[1, 3, 3]
```

## Reading

Via BT930, this gives the first nontrivial chain-side symmetry action for quotienting selector candidates.

## Boundary

This does **not** construct the full order-48 signed monomial action on chain H. The signed/A2-plane part still needs an explicit chain-complex lift. BT937 only transports the coordinate C3 subgroup honestly.

## Witness

```text
analysis/bt937_tetracode_action_on_chain.py
data/bt937_tetracode_action_on_chain.json
```
