# BT993 — Edgewise density recurrences

BT993 replaces the retired barycentric density constants with a true edgewise
f-vector recurrence.

## Local f-vectors

For k=2 edgewise subdivision of an i-simplex, i=0..4:

```text
Delta0 -> [1, 0, 0, 0, 0]
Delta1 -> [3, 2, 0, 0, 0]
Delta2 -> [6, 9, 4, 0, 0]
Delta3 -> [10, 25, 24, 8, 0]
Delta4 -> [15, 55, 85, 60, 16]
```

Solving carrier-by-carrier gives the exact subdivision matrix `L`:

```text
rows = old carrier dimension, columns = new face dimension

[1, 0, 0, 0, 0]
[1, 2, 0, 0, 0]
[0, 3, 4, 0, 0]
[0, 1, 8, 8, 0]
[0, 0, 5, 20, 16]
```

Thus

```text
f_next[j] = sum_i f_current[i] * L[i][j].
```

## CP2_9 iterates

```text
r=0: [9, 36, 84, 90, 36]
r=1: [45, 414, 1236, 1440, 576]
r=2: [459, 5976, 19344, 23040, 9216]
r=3: [6435, 89094, 300996, 368640, 147456]
```

## K3_16 iterates

```text
r=0: [16, 120, 560, 720, 288]
r=1: [136, 2640, 9440, 11520, 4608]
r=2: [2776, 45120, 152960, 184320, 73728]
r=3: [47896, 696960, 2385920, 2949120, 1179648]
```

The level-1 rows match the explicit incidence computation in BT992.

## Reading

This is the actual edgewise density layer. It retires the old barycentric
`120/19` and `860/19` constants for R3 and replaces them with a carrier-exact
matrix recurrence. The top multiplier is still `16`, but now all face dimensions
are tracked.

## Witnesses

```text
analysis/bt993_edgewise_density_recurrences.py
data/bt993_edgewise_density_recurrences.json
```
