# BT1084 — Incidence ladder operator choice and commutator-weight ledger

BT1084 promotes the line-edge adjacency operator as the current best W33-native nearest-sector ladder.

## BT1081 projected ranks

For nearest sector pairs `(0,4)`, `(4,10)`, `(10,16)`, the line-edge adjacency operator has ranks

```text
0 -> 4    rank 31
4 -> 10   rank 24
10 -> 16  rank 15
```

The triangle-edge adjacency ranks are

```text
0 -> 4    rank 38
4 -> 10   rank 22
10 -> 16  rank 15
```

The line-edge adjacency is preferred because it is full target rank on the last two steps:

```text
4 -> 10   full rank 24
10 -> 16  full rank 15.
```

## Commutator weights for Q = Delta_1 / 4

The nearest-sector gaps are

```text
0 <-> 4    gap 1
4 <-> 10   gap 3/2
10 <-> 16  gap 3/2.
```

Using oriented adjoint pairs and the line-edge ranks, the gap-square ledger is

```text
2*(31*1^2 + 24*(3/2)^2 + 15*(3/2)^2)
= 2*(31 + 54 + 135/4)
= 475/2.
```

The corresponding unsigned first-gap ledger is

```text
2*(31*1 + 24*(3/2) + 15*(3/2)) = 179.
```

## Comparison with triangle-edge adjacency

For triangle-edge adjacency the gap-square ledger would be

```text
2*(38*1^2 + 22*(3/2)^2 + 15*(3/2)^2) = 485/2.
```

Thus line-edge adjacency is slightly cheaper by the gap-square metric while also preserving the full last-step ranks.

## Boundary

BT1084 chooses a W33-native ladder operator by rank and gap cost. It does not yet prove this ladder is the physical scalar/gauge mixing operator.
