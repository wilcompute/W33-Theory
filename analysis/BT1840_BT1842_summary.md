# BT1840-BT1842 summary

Executed the three requested moves after BT1837-BT1839.

## BT1840 — full 12x12 covariance estimator

Materialized a 12x12 upper correlation matrix over the syndrome blocks:

```text
P0 P1 P2 G0 G1 E01 E12 E20 Cwind Cslip01 Cslip12 Cslip20
```

The matrix is symmetric and PSD.  Its spectral budget is:

```text
lambda_max = 1.821589796573715
base sigma from BT1836 = 4.259701234272514
covariance sigma = 5.749160488907887
runs for 3 sigma = 75
runs for 5 sigma = 207
```

This is less pessimistic than the scalar BT1837 upper budget of 254 runs at 5 sigma.

## BT1841 — numeric F12 phase table

Generated the full numeric Givens phase table for the C12 winding analyzer.

```text
rotations = 66
output phases = 12
Frobenius reconstruction error = 2.351156386898407e-15
offdiagonal norm after nullification = 5.625739853018683e-15
```

The full table is committed in `data/bt1841_f12_phase_table.json`.

## BT1842 — covariance-aware SPRT

Fed the BT1840 covariance spectral width into the adaptive decoder.

```text
sigma_covariance = 5.749160488907887
LLR threshold = ln(999) = 6.906754778648554
fixed 5 sigma budget = 207 runs
adaptive median stop = 103 runs
adaptive mean stop = 117.6056 runs
adaptive p95 stop = 239 runs
wrong decisions = 3 / 5000
```

Comparison:

```text
BT1839 scalar covariance-upper median = 129
BT1842 matrix-aware median = 103
BT1839 scalar covariance-upper fixed 5 sigma = 254
BT1842 matrix-aware fixed 5 sigma = 207
```

The full covariance matrix therefore improves both the conservative fixed budget and the typical adaptive stopping time.
