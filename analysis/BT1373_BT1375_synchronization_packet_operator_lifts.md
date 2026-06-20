# BT1373--BT1375 -- Synchronization, Packet Route, and Operator Scheduler Lifts

## Summary

This packet executes the three open moves after BT1370--BT1372.

1. BT1373 tests whether the BT1370 `380`-correction spanning-tree
   counterconnection is minimal.
2. BT1374 compiles real BT828 packet routes into the BT1371 Q6/tomotope
   address table.
3. BT1375 upgrades the BT1372 scheduler from basis labels to a concrete
   linear operator on the BT865 Steinberg cycle-vector witnesses.

## BT1373 -- S3 Gauge Synchronization

BT1370 flattened the connection in a spanning-tree gauge.  That gauge is valid
but not synchronization-minimal:

```text
spanning-tree gauge: 160 identity edges, 380 corrections
improved S3 gauge:   210 identity edges, 330 corrections
```

So the old `380` count is not a lower bound.  The verifier records a concrete
root-fixed 40-line `S3` gauge and recomputes all 540 skew-line residuals.  Its
residual order profile is:

```text
identity:       210
transposition:  240
3-cycle:         90
```

The witness is also strictly stable under every one-line relabeling: the best
single-line move has delta `-5`.  The honest boundary remains: this proves that
`380` is not minimal and that the `330` witness is a strict local optimum, not
that `330` is the global optimum over all `6^39` root-fixed gauges.

## BT1374 -- Q6/Tomotope Packet Route Compiler

BT1371 gave the equivariant table:

```text
192 tomotope flags <-> 192 Q6 edges
```

BT1374 makes it executable.  Each BT828 route digit already carries a
tomotope block and a mirror-bus slot.  The compiler uses the low mirror fiber
as the local transversal:

```text
tomotope_flag = 4 * tomotope_block + (mirror_slot mod 4)
```

That flag is then looked up in the BT1371 table and lowered to one Q6 edge.
Every compiled row round-trips through the inverse table, every Q6 address is
a true one-bit Q6 edge, and the six-digit BT828 stress route lowers to six
distinct Q6 edges inside the 48-tick tomotope body.

The full 540-chart atlas ingress table uses a deliberately sparse six-flag
control lane:

```text
flags 31,95,159 appear 108 times each
flags 63,127,191 appear 72 times each
```

That is a control-lane fact, not a loss of the complete 192-row ABI; arbitrary
packet programs still lower digit-by-digit through the full Q6/tomotope table.

## BT1375 -- Concrete Steinberg Operator Scheduler

BT1372 proved the three-epoch scheduler count:

```text
3 * 2160 = 6480 = 81 * 80
```

BT1375 proves the missing operator statement.  It rebuilds the W33 triangle
complex over `F3`, reloads the BT865 Heisenberg free-module witnesses, and
generates the concrete `3 * 27 = 81` cycle-vector basis modulo boundaries.
Then it acts on those vectors by the unique central `C3` of the Heisenberg
`O3`.

The central operator is a permutation of the concrete cycle witnesses:

```text
27 cycles of length 3
rank(Z-I), rank((Z-I)^2), rank((Z-I)^3) = 54, 27, 0
kernel dimensions = 27, 54, 81
```

This identifies the scheduler coordinates:

```text
matter state = 3 BT865 free copies * 9 central cosets
generation   = position in the central C3 cycle
```

So the BT1372 generation-time rule is not just a label convention.  It is the
actual central order-3 operator on the Steinberg cycle-vector module.

## Verification

```bash
python3 analysis/bt1373_s3_gauge_synchronization_improved_counterconnection.py
python3 analysis/bt1374_q6_tomotope_packet_route_compiler.py
python3 analysis/bt1375_steinberg_cycle_operator_scheduler_lift.py
python3 tests/test_bt1373_bt1375_synchronization_packet_operator_lifts.py
python3 -m py_compile analysis/bt1373_s3_gauge_synchronization_improved_counterconnection.py analysis/bt1374_q6_tomotope_packet_route_compiler.py analysis/bt1375_steinberg_cycle_operator_scheduler_lift.py tests/test_bt1373_bt1375_synchronization_packet_operator_lifts.py
python3 -m json.tool data/bt1373_s3_gauge_synchronization_improved_counterconnection.json
python3 -m json.tool data/bt1374_q6_tomotope_packet_route_compiler.json
python3 -m json.tool data/bt1375_steinberg_cycle_operator_scheduler_lift.json
```
