# BT1785 projected adjacency lift

BT1785 lifts the BT1782 selected-adjacency model back toward the 600-cell while respecting the BT1779 obstruction.

The completion graph remains:

```text
C10 square K3
30 vertices
60 selected links
```

Interpretation:

```text
C10 direction: raw selected motion along the BT1773 600-cell ring backbone
K3 direction: projected cross-section relation among the three residual strand states over the same phase
```

Thus the 60 selected links split as:

```text
30 backbone links
30 projected cross-section links
```

This avoids the impossible induced-subgraph demand. The cross-section links are not required to be literal facet-dual adjacencies of the 600-cell. They are quotient/projected relations attached to the ten ring phases.

Boundary: this is a quotient/projection lift, not a proof that every K3 cross-section link is a raw 600-cell facet adjacency. The next geometric test is to choose explicit 600-cell facet representatives for each phase fiber.
