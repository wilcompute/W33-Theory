# BT1075 — Nearest-ladder sparse skeleton

BT1075 turns the BT1071 abstract ladder into a concrete dimensioned sparse skeleton.

## Sector dimensions

```text
E0  : 81
E4  : 120
E10 : 24
E16 : 15
```

## Partial-identity block skeleton

Use maximal rectangular partial-identity blocks between nearest sectors:

```text
X04 rank 81
X40 rank 81
X4,10 rank 24
X10,4 rank 24
X10,16 rank 15
X16,10 rank 15
```

Total oriented block rank count:

```text
2*81 + 2*24 + 2*15 = 240
```

## Commutator gaps for Q = Delta_1 / 4

```text
X04     gap  1
X40     gap -1
X4,10   gap  3/2
X10,4   gap -3/2
X10,16  gap  3/2
X16,10  gap -3/2
```

## Weighted square check

With partial-identity blocks, the Hilbert-Schmidt weighted gap-square total is

```text
2*81*(1^2) + 2*24*(3/2)^2 + 2*15*(3/2)^2
= 162 + 108 + 67.5
= 337.5
```

Equivalently,

```text
675/2.
```

## Boundary

This is a sparse skeleton with canonical rectangular identity blocks. It is not yet the W33 incidence-derived ladder. The incidence-derived version should replace the partial identities with maps built from W33 boundary, adjacency, or centralizer data.
