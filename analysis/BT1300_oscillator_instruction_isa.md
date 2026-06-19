# BT1300 - Oscillator Instruction ISA

## Summary

BT1299 identified the oscillator horizon

```text
[72,66]_3 = 66 payload lanes + 6 parity lanes
```

as the clocked holonet microframe.  BT1300 promotes that frame into an
instruction-set layout.

The 72 lanes are no longer just a count.  They are the explicit F3 horizon
coordinates:

```text
66 payload lanes = edges of K12 on the 3x4 CSS grid
 6 parity lanes  = the six column-pair checks
```

The clock is:

```text
9 route digits per frame
8 ticks per route digit
72 = 9 * 8
```

and the q=3 factorial identity gives the instruction boundary:

```text
q! + q = q^2
6  + 3 = 9
```

So the frame splits as:

```text
72 = 48 + 18 + 6
48 = q! * 2^q          tomotope packet body
24 = q  * 2^q          local-lift epilogue
24 = 18 payload + 6 parity
```

## The 8-Tick Word

Each ternary route digit lowers into one fixed 8-tick micro-op word:

```text
tick 0: q3_xor_axis_0
tick 1: q3_xor_axis_1
tick 2: q3_xor_axis_2
tick 3: apartment_hop_0
tick 4: apartment_hop_1
tick 5: apartment_hop_2
tick 6: apartment_hop_3
tick 7: apartment_hop_4
```

This is exactly the BT828 route compiler budget:

```text
3 Q3 XOR axes + 5 apartment hops = 8 ticks.
```

The existing route programs compile without changing their reversible-move
counts:

```text
local_flip        4 active ticks inside an 8-tick word
single_digit_far  7 active ticks inside an 8-tick word
two_digit_cross  12 active ticks inside a 16-tick packet
three_digit_far  19 active ticks inside a 24-tick packet
six_digit_stress 47 active ticks inside a 48-tick packet
```

The six-digit stress program has route bound 48 and active work 47, so it fills
the tomotope body with exactly one idle tick of slack.

## Horizon Coordinate Split

The F3 parity matrix supplies the lane coordinates:

```text
18 row edges
12 column edges
36 mixed edges
 6 parity symbols
```

Equivalently:

```text
pure sector   = 18 + 12 = 30
routed sector = 36 + 6  = 42
total         = 72
```

The tomotope body occupies the first 48 lanes.  The local-lift epilogue occupies
the last 24 lanes, and that epilogue is exactly:

```text
18 residual payload lanes + 6 F3 parity lanes.
```

This gives a concrete ABI for the holonet machine:

```text
body     = execute the tomotope packet
epilogue = lift the local chart and close the parity syndrome
```

## Architectural Reading

BT1300 makes the fractal computer/network less metaphorical.  A W33 node now
has:

```text
8 ticks      one route digit
72 ticks     one oscillator microframe
2160 ticks   one E8-Coxeter mirror bus
51840 ticks  one full Clifford supercycle
```

The same unit is simultaneously a packet, a parity frame, a local network route,
and a gate-synthesis clock.  The tomotope is the executable body.  The horizon
code is the parity closure.  The E8-Coxeter bus is the repeating carrier.

## Verification

```text
python3 analysis/w33_horizon_f3_parity_matrix.py
python3 analysis/bt1300_oscillator_instruction_isa.py
python3 tests/test_bt1300_oscillator_instruction_isa.py
python3 -m py_compile analysis/bt1300_oscillator_instruction_isa.py tests/test_bt1300_oscillator_instruction_isa.py
python3 -m json.tool data/bt1300_oscillator_instruction_isa.json
```

## Boundary

BT1300 proves a deterministic instruction layout and verifies coverage for the
existing BT828 route compiler packets.  It is not yet a shortest-path optimizer
for the full 540-chart transversal atlas.
