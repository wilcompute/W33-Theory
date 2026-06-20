# BT1405 Continuous Q6 Path Router

BT1374 lowered holonet packet digits to Q6/tomotope edge addresses, but it kept
the honest boundary that these were packet-address rows, not a continuous path
in the Q6 graph.

BT1405 closes that boundary at the ABI level.  Each compiled BT828 packet
program is now routed as an ordered Q6 walk:

1. orient the packet Q6 edges to minimize connector distance,
2. insert shortest Q6 connector walks between consecutive packet edges,
3. map every traversed edge back through the BT1371 tomotope flag table.

The result is a continuous path certificate, not only a list of waypoint edge
addresses.

## Stress Route

The BT828 six-digit stress program keeps the six BT1374 packet edges:

```text
175, 133, 56, 37, 142, 77
```

BT1405 stitches them into a single Q6 walk with ten connector edges:

```text
110111 -> 110101  packet    edge 175  flag 159  block 39
110101 -> 100101  connector edge 134  flag  83  block 20
100101 -> 101101  packet    edge 133  flag  84  block 21
101101 -> 001101  connector edge  58  flag  22  block  5
001101 -> 001111  packet    edge  56  flag  13  block  3
001111 -> 001011  connector edge  49  flag 144  block 36
001011 -> 001010  connector edge  45  flag 135  block 33
001010 -> 001000  packet    edge  37  flag 134  block 33
001000 -> 101000  connector edge  40  flag  58  block 14
101000 -> 101100  packet    edge 142  flag  63  block 15
101100 -> 001100  connector edge  55  flag 112  block 28
001100 -> 011100  connector edge  54  flag 113  block 28
011100 -> 010100  connector edge  82  flag  44  block 11
010100 -> 010110  connector edge  81  flag  37  block  9
010110 -> 010111  connector edge  87  flag  73  block 18
010111 -> 010011  packet    edge  77  flag 180  block 45
```

So the stress route is:

```text
6 packet edges + 10 connector edges = 16 Q6 steps
48 tomotope-body ticks - 16 Q6 steps = 32 slack ticks
```

This upgrades the earlier reading.  The six-digit stress route does not merely
land on six distinct Q6 edges inside the 48-tick body; it has a continuous
16-edge Q6 trace that still fits the same body with large slack.

## Program Profile

```text
local_flip         1 Q6 step   /  8 tick bound
single_digit_far   1 Q6 step   /  8 tick bound
two_digit_cross    3 Q6 steps  / 16 tick bound
three_digit_far    9 Q6 steps  / 24 tick bound
six_digit_stress  16 Q6 steps  / 48 tick bound
```

Every traversed edge is checked against the BT1371 192-row address table, every
step changes exactly one Q6 bit, no stress-route edge repeats, the packet edges
are preserved in order, and the body ticks are contiguous.

## Boundary

This is a Q6/tomotope ABI route certificate.  It is not yet a physical
waveguide layout, detector timing calibration, or optical loss model.  It proves
that the packet-address rows can be executed as a continuous hypercube path
inside the already verified tomotope body budget.

## Verification

```bash
python tools/bt1405_continuous_q6_path_router.py
python tests/test_bt1405_continuous_q6_path_router.py
python -m py_compile tools/bt1405_continuous_q6_path_router.py tests/test_bt1405_continuous_q6_path_router.py
python -m json.tool data/bt1405_continuous_q6_path_router.json
```
