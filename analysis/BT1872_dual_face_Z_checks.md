# BT1872 — Dual-Face Z-Check Construction

BT1872 tests the missing local `Z` layer predicted by BT1869.

## Construction

Keep the 44 oriented K12 face rows as `X` checks.  Replace the failed six cyclic-distance `Z` rows from BT1865 with signed vertex-star rows:

```text
for edge i<j:
  vertex i coefficient = +1
  vertex j coefficient = -1 = 2 mod 3
```

These are the Szilassi-dual face checks: the dual faces around primal vertices.

## Commutation

```text
HX rows = 44
HZ rows = 12
rank(HX) = 42
rank(HZ) = 11
rank(HX HZ^T) = 0
nonzero entries in HX HZ^T = 0
```

So this is the first exact local CSS layer:

```text
boundary of boundary = 0
```

## Parameters

```text
n = 66
k = 66 - 42 - 11 = 13
d_X = 3
d_Z = 3
```

Thus the finite matrix model gives:

```text
[[66,13,3]]_3
```

## Low-weight witnesses

An X-logical of weight 3:

```text
edge(0,1) + 2*edge(0,3) + edge(1,3)
```

A Z-logical of weight 3:

```text
edge(0,3) + 2*edge(3,4) + 2*edge(3,8)
```

No weight-1 or weight-2 logicals occur in the exhaustive low-weight search.

## Interpretation

The correct local `Z` layer was not the six distance rows.  It is the dual vertex-star/face-adjacency layer.  This turns the K12/F12 compiler from a check surface into a bona fide finite CSS matrix code.

Boundary: this is an exact finite GF(3) CSS matrix code.  Physical decoding, optical measurement schedule, and hardware thresholds remain open.
