# BT795 — Middle Layer from Four Transversal Tetrahedra

BT794 proves that every skew chart has four common isotropic transversals.  BT795
reads those four transversals as the four local carrier tetrahedra.

Each carrier has:

```text
3 opposite-edge axes
4 triangular faces
```

Therefore the local middle layer has:

```text
edge-axis labels       = 4 * 3 = 12
triangular face labels = 4 * 4 = 16
incidence blocks       = 4 * 4 * 3 = 48
```

This exactly matches the local 48-unit from BT781/BT785.

The useful structural reading is:

```text
four common transversals  ->  four carrier tetrahedra
12 edge axes              ->  middle edge layer
16 face labels            ->  face layer
48 incidence blocks       ->  local packet
```

So the tomotope middle layer is not a loose count.  It is carried by the four
common-transversal tetrahedra of each W33 skew chart.
