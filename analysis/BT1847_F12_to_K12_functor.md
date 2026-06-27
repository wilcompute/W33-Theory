# BT1847 — F12-to-K12 Functor Dictionary

BT1847 makes the BT1844/BT1846 bridge explicit as a functor from the optical mesh incidence category to the genus-6 `K12` rotation-system incidence category.

## Object map

```text
F12 mode i                  -> K12 vertex i
two-mode rotation R_ij      -> edge {i,j}
rotation phase theta_ij     -> edge current / phase weight
mesh layer order            -> edge traversal order
output phase at mode i      -> vertex gauge at i
```

## Edge map

The functor sends every unordered mesh pair to the corresponding complete-graph edge:

```text
(i,j) -> {i,j}
```

There are exactly:

```text
66 mesh rotations
66 K12 edges
```

## Phase/current rule

For a pair `(i,j)`, define cyclic distance/current

```text
d = (j-i) mod 12.
```

The phase/current bucket sizes are:

```text
1: 12
2: 12
3: 12
4: 12
5: 12
6: 6
7: 6
8: 12
9: 12
10: 12
11: 12
```

The only special case is the antipodal distance-6 tie, which needs an extra orientation gauge.  This is exactly the same tie that appears in the BT1846 orientation convention.

## Verdict

The functor is exact on:

```text
objects
edges
incidence
vertex gauges
complete-pair schedule
```

Phase labels can encode cyclic current/distance data, but distance-6 edges require an additional orientation gauge.

Boundary: this is a combinatorial functor, not a geometric embedding theorem.
