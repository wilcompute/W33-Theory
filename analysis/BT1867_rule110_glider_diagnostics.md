# BT1867 — Rule-110 Glider Diagnostics

BT1867 diagnoses the BT1864 orbit for glider-like structure, domain walls, entropy, and recurrence.

## Input

```text
BT1864 orbit
length = 30
steps = 120
states = 121
```

## Density and entropy

```text
ones_min = 9
ones_max = 24
entropy_min = 0.7219280948873623
entropy_max = 1.0
entropy_t0 = 0.9709505944546686
entropy_t120 = 0.9480782435939055
```

The gap track neither empties nor fills, and its entropy remains high.

## Domain walls

```text
cyclic transitions min = 6
cyclic transitions max = 24
```

So the orbit preserves moving interfaces rather than collapsing to a uniform domain.

## Neighborhood usage

All eight Rule-110 neighborhoods occur:

```text
111: 761
011: 570
110: 570
001: 409
100: 409
101: 358
000: 356
010: 197
```

## Diagonal persistence

Maximum consecutive 1-runs along spacetime diagonals:

```text
v=-4: 9
v=-3: 12
v=-2: 12
v=-1: 12
v= 0: 18
v= 1: 6
v= 2: 7
v= 3: 12
v= 4: 9
```

## Verdict

The finite ring orbit shows real domain-wall and diagonal persistence, but no isolated long-lived Rule-110 glider family is proven in the 30-cell periodic box.  The best signatures are stationary persistence length 18 and diagonal persistence length 12 at velocities `-3,-2,-1,+3`.

The six-hole track remains active as a phase/gauge clock on top of the binary dynamics; it is not the source of the binary complexity itself.

Boundary: finite glider diagnostic only; no universal Rule-110 glider catalogue or physical implementation proof is claimed.
