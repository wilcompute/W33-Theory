# BT1846 — Current-Graph Lift of the 66 Bridge

BT1844 proved the shared complete-pair schedule:

```text
F12 rotations = C(12,2) = 66 = K12 edges.
```

BT1846 orients that schedule as a current-graph/rotation-system object.

## Construction

Use labels in `Z/12Z`.  The 66 unordered pairs are the edges of `K12`.

Orient each pair `{i,j}` as `i -> j` when

```text
(j-i) mod 12 in {1,2,3,4,5,6}
```

with distance-6 ties resolved by using the smaller source.

The current on an oriented edge is:

```text
current(i -> j) = j-i mod 12.
```

## Rotation system

At vertex `i`, use the cyclic neighbor order:

```text
i+1, i+2, ..., i+11 mod 12.
```

## Face trace

The face trace gives:

```text
V = 12
E = 66
F = 44
all faces have length 3
Euler characteristic = 12 - 66 + 44 = -10
genus = 1 - chi/2 = 6
```

So the current-graph lift recovers the abstract genus-6 `K12` triangular map required by the Csaszar/Szilassi horizon.

## Boundary

This is an abstract orientable rotation-system/current-graph lift.  It does not assert a non-self-crossing Euclidean polyhedron realization.
