# BT1888 — Switch-Depth Optimizer

BT1888 optimizes the BT1885 switch-fabric lowering.

## Baseline

```text
rounds = 5
low-loss switches = 76
edge-touch entries = 264
active loss units = 76
survival = 0.8588264426049117
```

## Optimization

Rules:

```text
merge compatible X residual halves
preserve X/Z measurement-basis separation
regroup vertex stars by bus conflict, not just parity
```

Optimized schedule:

```text
X0_Reye:         16 checks, 48 touches
X1_all_residual: 28 checks, 84 touches
Z0_star_set_A:    6 checks, 66 touches
Z1_star_set_B:    6 checks, 66 touches
```

## Result

```text
rounds = 4
switch units = 64
survival = 0.8797377103140766
```

Improvement over BT1885:

```text
round reduction = 1
switch-unit reduction = 12
survival gain = 0.02091126770916486
erasure reduction = 0.02091126770916486
```

## Boundary

This is a schedule-depth optimization model.  It is not a routed switch matrix or measured insertion-loss claim.
