# BT932 — Symmetry/equivariance test

BT932 tests whether a meaningful symmetry of the BT926 vertex E8 witness can constrain the BT929 chain-to-E8 map.

## Result

The BT926 vertex subset

```text
[0, 1, 4, 22, 27, 35, 23, 34]
```

has:

- W33 graph self-maps preserving the subset setwise: 1;
- nontrivial preserving maps: 0;
- E8 diagram self-maps of the induced Dynkin graph: 1.

## Reading

The vertex E8 witness is symmetry-isolated in this test. Therefore equivariance under the vertex witness is vacuous: it cannot select a unique chain-to-E8 map.

## Next target

A nontrivial equivariant selector should use the tetracode A2^4 block structure or a larger chain-complex symmetry, not the isolated vertex witness alone.

## Witness

```text
analysis/bt932_symmetry_equivariance_test.py
data/bt932_symmetry_equivariance_test.json
```
