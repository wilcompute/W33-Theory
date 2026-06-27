# BT1865 — CSS Commutation Matrix

BT1865 tests whether the natural BT1859 split is already a valid qutrit CSS split.

## Proposed split

```text
HX = 44 K12 face-current rows
HZ = 6 cyclic-distance rows
field = GF(3)
edge symbols = 66
```

## Result

The CSS commutation matrix

```text
HX HZ^T mod 3
```

has:

```text
shape = 44 x 6
rank = 5
nonzero entries = 116
zero face rows = 1
nonzero face rows = 43
```

Row support profile:

```text
0 nonzero columns: 1 face
2 nonzero columns: 13 faces
3 nonzero columns: 30 faces
```

Column nonzero counts:

```text
[18, 22, 21, 21, 22, 12]
```

Column sums mod 3:

```text
[0, 0, 0, 0, 0, 0]
```

## Kernel clue

The right kernel is one-dimensional:

```text
(1,1,1,1,1,1)
```

So the all-distance/global clock-sum row commutes with every face row.

## Verdict

The naive CSS split fails:

```text
HX HZ^T != 0
```

but the failure is structured.  The commutation defect has rank 5, leaving one genuine commuting global clock-sum stabilizer and five distance-contrast directions that must be treated as gauge defects, quotiented, or paired with a dual set of face rows.

Boundary: exact GF(3) CSS commutation test only; no quantum CSS/subsystem distance theorem is claimed.
