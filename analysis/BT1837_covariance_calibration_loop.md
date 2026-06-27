# BT1837 — Covariance Calibration Loop

BT1836 gave a scalar live-control bound.  BT1837 adds the first covariance-aware correction.

## Model

Use the BT1834 block stress form:

```text
12 syndrome blocks
144 local checks per block
1728 local checks total
variance inflation = 1 + 143*rho
```

A control packet estimates the mean off-block correlation:

```text
shots = 10000
rho_hat = 0.006
rho_upper_95 = 0.012
```

## Budget using rho_upper_95

```text
variance inflation = 2.716
single-run width = 6.369321430990651
runs for 3 sigma = 92
runs for 5 sigma = 254
```

## Comparison

```text
BT1833 independent 5 sigma = 94
BT1836 scalar-calibrated 5 sigma = 114
BT1837 covariance-upper 5 sigma = 254
```

## Interpretation

Scalar calibration is not enough.  Even a small off-block covariance upper bound more than doubles the safe 5σ run count relative to BT1836.

Boundary: this is still a scalar mean-covariance upper bound, not the full 12x12 empirical covariance matrix.
