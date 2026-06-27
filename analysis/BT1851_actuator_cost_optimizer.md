# BT1851 — Actuator-Cost Covariance Optimizer

BT1848 optimized abstract covariance knobs.  BT1851 maps those knobs onto BT1832 primitive families and adds modeled actuator costs.

## Repo anchors searched

The actuator layer connects directly to:

```text
analysis/bt1832_optical_primitive_lowering.py
analysis/BT1845_covariance_hardware_targets.md
data/bt1848_covariance_target_optimizer.json
```

BT1832 supplies the primitive families:

```text
3 qutrit sorters
2 D4 parity ancillas
3 K4 equality interferometers
1 C12 ring winding readout
3 phase-slip guards
```

## Objective

```text
minimize actuator cost
subject to lambda_max <= 1.4
```

## Selected actuator set

```text
ring_guard_thermal_decoupler
qutrit_path_balancer
D4_parity_clock_isolator
```

Modeled cost:

```text
total cost = 10.5
```

Result:

```text
lambda_max start = 1.821589796573715
lambda_max after selected actuators = 1.386912
fixed 5 sigma runs start = 200
fixed 5 sigma runs after selected actuators = 156
```

## Why K4 is not first

K4 phase dithering helps, especially through the E-C cross term, but the first cost-efficient actions are:

```text
1. decouple C12 ring thermal drift from phase-slip guard thresholds
2. balance qutrit path-splitter common drift
3. isolate D4 parity ancilla clocks
```

These cover the highest-value BT1848 target reductions with lower modeled actuator cost.

Boundary: actuator costs are modeled engineering weights, not measured hardware time, power, or bill-of-material costs.
