# BT1846-BT1848 summary

Executed the three requested moves after BT1843-BT1845.

## BT1846 — current-graph lift of the 66 bridge

The BT1844 bridge is lifted from a count to an oriented abstract map.

```text
labels = 12
edges = C(12,2) = 66
arcs = 132
current group = Z/12Z
```

Rotation system:

```text
at vertex i: i+1, i+2, ..., i+11 mod 12
```

Face trace:

```text
V = 12
E = 66
F = 44
all faces triangular
Euler characteristic = -10
orientable genus = 6
```

Boundary: abstract current-graph/rotation-system lift only; no non-self-crossing Euclidean realization is claimed.

## BT1847 — F12-to-K12 functor

The F12 mesh and genus-6 K12 map are connected by an explicit incidence functor.

```text
F12 mode i              -> K12 vertex i
two-mode rotation R_ij  -> edge {i,j}
rotation phase theta_ij -> edge current/phase weight
mesh layer order        -> edge traversal order
output phase i          -> vertex gauge i
```

The functor is exact on objects, edges, incidence, and gauges.  The only special case is the distance-6 antipodal tie, which needs an orientation gauge.

## BT1848 — covariance target optimizer

BT1845 manually assigned covariance targets.  BT1848 optimizes them spectrally.

Objective:

```text
minimize weighted covariance reductions subject to lambda_max <= 1.4
```

Selected reductions:

```text
C12_C internal: 0.20 -> 0.055
qutrit_P internal: 0.18 -> 0.07
E_C cross: 0.08 -> 0.035
D4_G internal: 0.16 -> 0.08
```

Result:

```text
starting lambda_max = 1.821589796573715
optimized lambda_max = 1.392744103256981
starting 5 sigma runs = 200
optimized 5 sigma runs = 157
```

Conclusion: the smallest high-value set is C12 internal covariance, qutrit internal covariance, E-C cross covariance, and D4 internal covariance.
