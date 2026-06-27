# BT1840 — Full 12x12 Covariance Estimator

BT1837 used a scalar covariance upper bound.  BT1840 materializes a full 12x12 upper correlation matrix over the syndrome blocks:

```text
P0 P1 P2 G0 G1 E01 E12 E20 Cwind Cslip01 Cslip12 Cslip20
```

## Matrix structure

The matrix is symmetric and positive semidefinite.  It uses family-level upper correlations:

```text
P-family internal upper correlation = 0.18
G-family internal upper correlation = 0.16
E-family internal upper correlation = 0.14
C-family internal upper correlation = 0.20
P-G = 0.06
P-E = 0.02
P-C = 0.03
G-E = 0.04
G-C = 0.02
E-C = 0.08
```

## Spectral budget

The largest eigenvalue is:

```text
lambda_max = 1.821589796573715
```

Feeding this into the BT1836 calibrated base width gives:

```text
base sigma = 4.259701234272514
covariance sigma = 5.749160488907887
runs for 3 sigma = 75
runs for 5 sigma = 207
```

## Interpretation

The full matrix is less pessimistic than the scalar BT1837 upper bound:

```text
BT1837 scalar covariance-upper 5 sigma = 254
BT1840 matrix-eigenvalue 5 sigma = 207
```

Boundary: this is a materialized upper correlation matrix, not a measured chip covariance matrix.
