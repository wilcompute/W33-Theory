# BT1837-BT1839 summary

Executed the three requested moves after BT1834-BT1836.

## BT1837 — covariance calibration loop

A scalar covariance upper bound is fed into the BT1834 stress model.

```text
blocks = 12
block size = 144
local checks = 1728
rho_hat = 0.006
rho_upper_95 = 0.012
variance inflation = 2.716
single-run width = 6.369321430990651
runs for 3 sigma = 92
runs for 5 sigma = 254
```

Comparison:

```text
BT1833 independent 5 sigma = 94
BT1836 scalar-calibrated 5 sigma = 114
BT1837 covariance-upper 5 sigma = 254
```

## BT1838 — mesh decomposition theorem

The BT1835 matrix catalog is lowered into exact mesh schedules.

```text
F3 qutrit sorter: 3 two-mode rotations + 3 phases
F12 winding analyzer: 66 two-mode rotations + 12 phases
H2 tensor H2 D4 encoder: 4 balanced 50/50 couplers
D4 parity ancilla: 6 logical XOR gates + 2 chi offsets
K4 comparator: 2 bitwise XORs + one multi-control flag
C12 phase-slip guard: equality flag on 144 valid clock pairs
```

## BT1839 — adaptive sequential decoder

The fixed run budget is replaced by a sequential likelihood-ratio rule:

```text
stop when |LLR| >= ln(999)
ln(999) = 6.906754778648554
```

For the BT1837 covariance-upper width:

```text
fixed 5 sigma budget = 254 runs
adaptive median stop = 129 runs
adaptive mean stop = 144.454 runs
adaptive p95 stop = 286 runs
wrong decisions = 3 / 5000
```

Interpretation: adaptive stopping nearly halves the median run count while retaining a tail comparable to the conservative fixed budget.
