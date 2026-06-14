# BT944 — Bitset recursion search kernel

BT944 upgrades BT941 from a table scaffold to a concrete recursive search kernel.

## Encoding

```text
H nonzero classes = 255
class encoding = 8-bit masks 1..255
pairing table entries = 65025
ordered B(e,f)=1 pairs = 32640
unordered hyperbolic pair slots = 16320
```

## Current certificate

```text
current best profile = [6, 6, 6, 10, 10, 10, 14, 14]
current best sum = 76
raw lower bound = 48
gap = 28
```

## Recursion kernel

1. choose the least unused vector in the current symplectic subspace;
2. enumerate partners pairing to 1;
3. append the hyperbolic pair;
4. replace the current space by its symplectic orthogonal quotient;
5. prune if support-so-far plus raw lower bound for remaining basis vectors is at least current best;
6. memoize by row-reduced subspace mask and remaining pair count.

## Boundary

BT944 does not yet report a completed exhaustive search. It is the executable kernel needed for a longer no-support-below-76 certificate run.

## Witness

```text
analysis/bt944_bitset_recursion_search.py
data/bt944_bitset_recursion_search.json
```
