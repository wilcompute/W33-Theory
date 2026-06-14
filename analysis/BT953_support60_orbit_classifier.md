# BT953 — Support-60 orbit/invariant classifier

BT951 reduced the support selector problem to six exact minimizers. BT953 classifies the intrinsic certificate graph on those six minimizers.

## Common core

All six minimizers share the hyperbolic pair

```text
(90, 144)
```

## Certificate graph

The weighted intersection matrix has automorphism group of order 2. It only swaps minimizers 0 and 1.

Orbit partition under this intrinsic certificate symmetry:

```text
[[0,1], [2], [3], [4], [5]]
```

## Boundary

This is not the full tetracode quotient. It is the strongest quotient available from the support-60 certificate alone. A larger transported tetracode action would be needed to collapse more orbits.

## Witness

```text
analysis/bt953_support60_orbit_classifier.py
data/bt953_support60_orbit_classifier.json
```
