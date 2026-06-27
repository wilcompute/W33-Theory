# BT1874 — Larger-Ring Rule-110 Glider Catalog

BT1874 extends BT1871 from a short recurrence diagnostic to a longer `16N` catalog.

## Rings

BC/Sturmian ring lengths:

```text
48, 78, 126, 204
```

Each ring is evolved for:

```text
16N steps
```

## Results

### N = 48

```text
steps = 768
repeat = 120 -> 216, period 96
ones = 15..39
entropy = 0.6962122601251458..1.0
transitions = 10..34
best diagonals: v=-2 length 26, v=0 length 21, v=10 length 21
```

### N = 78

```text
steps = 1248
repeat = none
ones = 24..63
entropy = 0.7062740891876007..1.0
transitions = 16..56
best diagonals: v=0 length 130, v=-4 length 46, v=-8 length 38, v=3 length 30
```

### N = 126

```text
steps = 2016
repeat = 759 -> 766, period 7
ones = 36..102
entropy = 0.7024665512903903..1.0
transitions = 24..92
best diagonals: v=10 length 1336, v=-11 length 1335, v=3 length 1329, v=-4 length 1323
```

### N = 204

```text
steps = 3264
repeat = none
ones = 60..165
entropy = 0.7039260680195971..1.0
transitions = 40..148
best diagonals: v=0 length 388, v=-4 length 88, v=3 length 68, v=10 length 42
```

## Velocity classes

The recurring candidate packet velocities are:

```text
v = 0
v = -4
v = 3
v = 10 / -11 aliases
```

## Interpretation

The larger-ring catalog splits the dynamics into two regimes:

```text
finite-box locks: N=48, N=126
nonrepeating active rings: N=78, N=204
```

The N=126 period-7 lock is not a collapse; it is a traveling-wave/glider-lock regime with very long diagonal packets.  The N=78 and N=204 rings remain better test beds for nonrepeating glider/domain-wall dynamics.

Boundary: finite larger-ring catalog only; no infinite Rule-110 glider theorem or physical universality proof is claimed.
