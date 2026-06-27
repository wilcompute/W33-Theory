# BT1877 — Glider Phase-Class Extractor

BT1877 classifies the BT1874 packet velocities by the `Z/6Z` hole phase.

## Phase rule

BT1861 updates the hole track by

```text
h -> h + 1 mod 6
```

at each time step.  Along a diagonal packet of velocity `v`, position changes by `v`, so the hole phase evolves as:

```text
h_t = h_0 + (v+1)t mod 6
```

## Velocity classes

```text
v = 0:
  phase step = 1
  cycle = 0,1,2,3,4,5
  full six-phase stationary/domain packet
```

```text
v = -4:
  phase step = 3
  cycles = (0,3), (1,4), (2,5)
  antipodal two-phase packet
```

```text
v = 3:
  phase step = 4
  cycles = (0,4,2), (1,5,3)
  three-phase chiral packet
```

```text
v = 10:
  phase step = 5
  cycle = 0,5,4,3,2,1
  full six-phase reverse packet
```

```text
v = -11:
  phase step = 2
  cycles = (0,2,4), (1,3,5)
  three-phase reverse/alias packet
```

## Survival by active ring

```text
N=78:  v=0, v=-4, v=3
N=204: v=0, v=-4, v=3, v=10
```

## Interpretation

The active rings preserve three packet types:

```text
six-phase clock packets
antipodal two-phase packets
three-phase chiral packets
```

The `Z/6Z` hole track is therefore a phase/gauge clock on top of the binary Rule-110 dynamics.  It does not create the gliders, but it classifies their phase.

## Code connection

This is the same six-distance/gauge layer that appears in BT1873.  So the computation side and the code side now share the same interpretation:

```text
Z6 hole phase = gauge/clock layer, not stabilizer protection itself
```

Boundary: finite phase-class extractor only; no infinite glider theorem or physical computation proof is claimed.
