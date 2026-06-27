# BT1852 — Face-Word Current Closure Test

BT1850 extracted the 44 oriented triangular face words.  BT1852 tests their `Z/12Z` current closure.

## Rule

For an oriented face

```text
(a,b,c)
```

define currents

```text
(b-a, c-b, a-c) mod 12.
```

## Result

```text
faces = 44
closed mod 12 = 44
ordinary flat = 32
antipodal flat = 12
twisted nonzero = 0
```

Split:

```text
Reye:     16 faces = 12 ordinary flat + 4 antipodal flat
Residual: 28 faces = 20 ordinary flat + 8 antipodal flat
```

The 12 antipodal-flat faces are precisely those containing one distance-6 edge.

## Interpretation

This is stronger than expected: the genus-6 face system is completely flat as a `Z/12Z` current system.  The only special faces are not curvature defects; they are antipodal sheet defects.

Therefore the six genus-hole parity symbols in the `[72,66,6]` code should absorb antipodal sheet data, not generic face curvature.

Boundary: this is a finite incidence/current result, not an optical phase-noise measurement.
