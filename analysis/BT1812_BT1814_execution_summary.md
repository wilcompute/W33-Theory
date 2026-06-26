# BT1812-BT1814 execution summary

Executed all three frontier moves after BT1810-BT1811.

## BT1812

Completed the W(E6)/Schlaefli orbit computation using the standard 27-line cubic-surface model rather than slow full VF2 enumeration.

Results:

```text
Aut(Schlaefli) order = 51840
BT1795 image stabilizer size = 36
observed three-table support orbit size = 36
intersection of that orbit with Hesse hinges = 6
```

Interpretation: W(E6) does not fix the observed hinge uniquely. It selects a six-hinge slice, and six is exactly the edge count of a four-state quartet.

## BT1813

Resolved the hidden quartet structurally as a K4 on four local states:

```text
{00,01,10,11}
```

The six W(E6)-compatible Hesse hinges are interpreted as the six unordered edges of this K4. The observed repair is one oriented edge transfer, with table-level sign pattern:

```text
-2, -2, +2
```

Boundary: the four states are identified structurally, not yet as specific physical D4/GKP operators.

## BT1814

Reduced the next search space:

```text
all three-table supports: 816
Hesse hinges: 54
Schlaefli stabilizer slices: 10
```

The observed repair lies in a size-6 slice, again matching the six edges of the hidden K4 quartet.

## Breakthrough

The fibre law is now sharper:

```text
12 = 3 x 4
3 = Hesse/BC strand coordinate
4 = hidden K4/D4/GKP quartet
visible repair = oriented K4 edge transfer
```

The next law is no longer a blind table-count search. It is an oriented-edge selection problem inside a Schlaefli-distinguished K4 slice.
