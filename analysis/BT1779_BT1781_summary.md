# BT1779-BT1781 summary

Executed all three requested next moves after BT1776-BT1778.

## BT1779

Added `analysis/BT1779_induced_subgraph_obstruction.md`.

The desired 30-facet induced subgraph with 60 links and degree 4 cannot exist inside the connected 4-regular 600-cell facet-dual. If a proper induced subgraph has full degree 4 at every selected facet, it is a union of connected components. The 600-cell facet-dual is connected with 600 facets, so a 30-facet induced full-degree subgraph is impossible.

Conclusion: use a non-induced selected-adjacency model, a larger facet set, or a projection/quotient.

## BT1780

Added `analysis/bt1780_inversion_hexagon_exact_map.py`.

This refines BT1777. The BT1774 inversion witness preserves each of the eight Coxeter 5-cycles setwise and acts as a reflection inside each cycle. With the current phase labels, it is not one single global phase map on all eight cycles; it is a cyclewise dihedral reflection. A uniform phase law can be recovered only after independently rephasing the eight cycles.

## BT1781

Added `analysis/BT1781_consistency_census.md`.

The local table census for the stabilizer problem is:

```text
raw entries: 31104
accepted entries: 9980
```

All nine slot domains remain size 12, and the incumbent remains present in every local table. The next computation must use relations between tables; checking slots one at a time is not enough.
