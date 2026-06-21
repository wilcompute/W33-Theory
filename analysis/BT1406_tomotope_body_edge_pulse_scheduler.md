# BT1406 Tomotope-Body Edge Pulse Scheduler

BT1405 proved that the BT1374 packet addresses can be stitched into a
continuous Q6 walk.  BT1406 turns that walk into a 48-tick tomotope-body pulse
schedule.

The pulse microcycle is ternary:

```text
phase 0: LOAD_FLAG     load tomotope flag/block/transversal
phase 1: FLIP_Q6_AXIS  traverse the one-bit Q6 edge
phase 2: LATCH_VERTEX  latch the target Q6 vertex and ABI record
```

Thus the same \(q=3\) substrate that supplies the route trit also supplies the
three-phase edge pulse.

## Stress Route

BT1405 found that the six-digit stress route is a continuous 16-edge Q6 walk.
BT1406 expands each Q6 edge into the three-phase pulse microcycle:

```text
16 Q6 edge traversals * 3 pulse phases = 48 tomotope-body ticks
```

So the old BT1405 slack is not wasted.  It becomes the physical timing shell:
the continuous Q6 route now fills the entire 48-tick body with no idle tick.

The packet edge load ticks are:

```text
0, 6, 12, 21, 27, 45
```

The last packet edge is therefore the final body cell:

```text
tick 45: LOAD_FLAG     edge 77, flag 180, block 45
tick 46: FLIP_Q6_AXIS  010111 -> 010011
tick 47: LATCH_VERTEX  target 010011
```

The stress pulse histogram is exactly balanced:

```text
LOAD_FLAG:    16
FLIP_Q6_AXIS: 16
LATCH_VERTEX: 16
IDLE:          0
```

## Reading

BT1374 said "the packet has Q6 edge addresses."  BT1405 said "those addresses
are a continuous Q6 walk."  BT1406 says "that walk has a complete tick-level
body schedule."  The physical handoff is now:

```text
tomotope flag -> Q6 bit flip -> latched target vertex
```

repeated sixteen times.

## Boundary

This is a timing ABI, not a calibrated optical claim.  It assigns the continuous
hypercube route to tomotope-body ticks, but it does not model optical pulse
widths, detector jitter, crosstalk, dispersion, or waveguide loss.

## Verification

```bash
python tools/bt1406_tomotope_body_edge_pulse_scheduler.py
python tests/test_bt1406_tomotope_body_edge_pulse_scheduler.py
python -m py_compile tools/bt1406_tomotope_body_edge_pulse_scheduler.py tests/test_bt1406_tomotope_body_edge_pulse_scheduler.py
python -m json.tool data/bt1406_tomotope_body_edge_pulse_scheduler.json
```
