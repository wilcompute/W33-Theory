# BT1885 — Switch-Fabric Lowering

BT1885 lowers the BT1882 payload-reuse architecture into explicit switch, delay, memory, and control primitives.

## Inputs

BT1882 reuse architecture:

```text
payload paths = 66
check ancillas = 56
rounds = 5
edge/check touches = 264
switching layers = 5
memory delays = 4
```

## Round map

```text
X0_Reye:          16 checks, 48 touches
X1_residual_A:    14 checks, 42 touches
X2_residual_B:    14 checks, 42 touches
Z0_even_stars:     6 checks, 66 touches
Z1_odd_stars:      6 checks, 66 touches
```

## Lowered primitives

```text
low-loss switches = 76
phase memory segments = 66
round delay latches = 4
ancilla reset channels = 56
shared F12 edge-address bus = 1
edge-touch schedule entries = 264
```

The 76 switch/loss units match BT1882:

```text
56 check ancilla channels + 20 aggregate switch/memory overhead units
```

## Critical paths

```text
payload phase memory across five rounds
switch table fanout into 264 edge/check touches
vertex-star eleven-edge parity fan-in
ancilla reset between rounds
```

Boundary: primitive-lowering bill of materials only; not a routed chip layout, calibrated insertion-loss model, or fabrication design.
