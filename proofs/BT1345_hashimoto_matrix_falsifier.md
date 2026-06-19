# BT1345 -- Matrix-Derived Hashimoto Falsifier

## Purpose

BT1345 promotes BT1342 from synthetic phase samples to a matrix-derived Hashimoto calculation.

## Exact graph layer

The script constructs W(3,3) from projective points over F3^4 and verifies:

```text
v = 40
edges = 240
directed edges = 480
adjacency eigenvalues = {-4, 2, 12}
```

## Standard Hashimoto result

The non-backtracking Hashimoto matrix on directed edges has nontrivial phase clusters:

```text
72.452 degrees, multiplicity 48
127.087 degrees, multiplicity 30
```

These are the standard phases derived from adjacency eigenvalues r=2 and s=-4 by the regular graph Hashimoto relation.

## Protocol correction

The earlier synthetic protocol targets were:

```text
63.435 degrees
112.208 degrees
```

Those do not match the standard Hashimoto matrix phases. Therefore the protocol angles need one of two repairs:

1. redefine the experimental operator as a nonstandard normalized/renormalized phase observable, or
2. update the protocol targets to the standard Hashimoto phases above.

## Boundary

This is a strengthening: the falsifier simulator now distinguishes exact matrix predictions from inherited heuristic angles.

## Files

```text
tools/bt1345_hashimoto_matrix_falsifier.py
data/bt1345_hashimoto_matrix_summary.json
```
