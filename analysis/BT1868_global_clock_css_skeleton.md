# BT1868 — Global-Clock CSS Skeleton

BT1868 follows the BT1865 commutation obstruction instead of fighting it.

## BT1865 input

```text
HX face rank = 42
HZ distance rows = 6
HX HZ^T rank = 5
right kernel = span{(1,1,1,1,1,1)}
```

So only the all-distance row commutes with every face row.

## Repair

Do not use all six distance rows as stabilizers.  Instead:

```text
Z stabilizer = global clock-sum row = H1 + H2 + H3 + H4 + H5 + H6
five distance-class contrasts = gauge/defect rows
```

## Payload skeleton

On the 66 edge/rotation payload symbols:

```text
physical qutrits = 66
X rank = 42
Z rank = 1
commuting = true
candidate k = 66 - 42 - 1 = 23
```

## Full 72-symbol skeleton

Including the six parity/hole symbols before gauge fixing:

```text
physical symbols = 72
X rank = 42
Z rank = 1
candidate k before gauge fixing = 29
parity/gauge degrees = 6
```

## Interpretation

This is the first clean CSS-compatible object in the chain:

```text
44 face checks + 1 global clock stabilizer
```

The five remaining distance contrasts are not stabilizers yet.  They are gauge degrees, defect rows, or a signal that a dual face system must be added.

Boundary: CSS skeleton only.  Distance, decoder, and physical protection remain open.
