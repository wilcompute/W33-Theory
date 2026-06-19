# BT1342 -- Hashimoto Falsifier Simulator

## Purpose

BT1342 turns the 40-mode / 240-mode chip protocol into an executable synthetic pass/fail simulator.

## Exact graph layer

The script constructs W(3,3) from projective points of F3^4 using the standard symplectic form. It verifies:

```text
v = 40
k = 12
edges = 240
lambda = 2
mu = 4
```

## Protocol observables

The simulator produces synthetic measurements for:

```text
Hashimoto gauge angle: 63.43 degrees
Hashimoto chiral angle: 112.21 degrees
flat-band localization length
CSS logical-error proxy
period-6 closure-clock recurrence
```

## Result

With seed 1342, all pass/fail gates pass.

## Boundary

The simulator is not experimental data. It is a deterministic synthetic falsifier harness built from exact W(3,3) combinatorics and the tolerances in the chip protocol.

## Files

```text
tools/bt1342_hashimoto_falsifier_simulator.py
data/bt1342_hashimoto_falsifier_simulation.json
```
