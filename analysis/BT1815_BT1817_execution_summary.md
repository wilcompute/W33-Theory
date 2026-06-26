# BT1815-BT1817 execution summary

Executed all three requested next moves after BT1812-BT1814.

## BT1815: D4/GKP quartet assignment

The hidden quartet is assigned to the D4 discriminant/glue group:

```text
D4*/D4 = (Z2)^2
00 = root coset 0
01 = vector coset v
10 = spinor coset s
11 = conjugate-spinor coset c
```

The six W(E6)-compatible Hesse hinges are the six K4 edges among these four cosets. In the BT1813 edge order, the observed repair support `{10,22,44}` is the edge `00--11`, i.e. the conjugate-spinor displacement relative to the root coset. The sign pattern orients that edge transfer.

Boundary: D4 triality can permute `v,s,c`, so the invariant claim is the K4 edge structure and observed difference class, not an absolute naming of the nonzero cosets without a D4 gauge.

## BT1816: hinge orientation solver

The BT1801 F3 left-kernel basis gives the basis-consistent count syndrome:

```text
[0,2,1,1,2]
```

Therefore a repair must evaluate to:

```text
[0,1,2,2,1]
```

Search space:

```text
54 directed Hesse hinges
3 possible return tables per hinge
162 oriented candidates
```

Result:

```text
unique repairing candidate = T010,T210,T222
return table = T222
source/removal tables = T010,T210
support indices = 10,22,44
```

This is the strongest result in the packet: the observed repair is the unique directed hinge orientation that repairs the BT1801 F3 syndrome while preserving the parity layer.

## BT1817: BC/600-cell tetrahedral quartet lift

The K4 quartet has a direct local 600-cell/BC reading:

```text
four quartet states = four faces/local neighbor directions of a tetrahedral cell
six K4 edges = six unordered face-pairs = six edges of the tetrahedron
```

Thus the same hidden object has three consistent faces:

```text
D4/GKP: four glue cosets
Schlaefli/W(E6): six compatible hinge supports
BC/600-cell: four tetrahedral faces and six tetrahedral edges
```

## Breakthrough

The missing fibre law is no longer just an ansatz. It is now constrained from three sides:

```text
D4/GKP gives the 4-state K4 quartet.
W(E6) gives the six-edge hinge slice.
The F3 syndrome uniquely orients one edge: T010,T210 -> T222.
BC/600-cell gives the tetrahedral face-pair geometry of the same K4.
```

So the active law is:

```text
12 = 3 x 4
3 = BC/Hesse strand coordinate
4 = D4/GKP tetrahedral quartet
visible correction = unique syndrome-valid oriented K4 edge transfer
```
