# BT1842 — Covariance-Aware SPRT

BT1839 used scalar Gaussian widths.  BT1842 feeds the BT1840 covariance-matrix spectral width into the sequential decoder.

## Inputs

```text
section A = 9980
section B = 9978
gap = 2
lambda_max(BT1840) = 1.821589796573715
sigma_covariance = 5.749160488907887
LLR threshold = ln(999) = 6.906754778648554
```

## Fixed budget

```text
runs for 3 sigma = 75
runs for 5 sigma = 207
```

## Adaptive packet

Using the covariance-aware width:

```text
trials = 5000
median stop = 103
mean stop = 117.6056
p95 stop = 239
max stop = 589
wrong decisions = 3 / 5000
```

## Comparison

```text
BT1839 scalar covariance-upper median = 129
BT1839 scalar covariance-upper fixed 5 sigma = 254
BT1842 matrix-aware median = 103
BT1842 matrix-aware fixed 5 sigma = 207
```

## Interpretation

The full covariance matrix improves the decoder over the scalar upper bound.  The median adaptive stop falls from 129 to 103 runs, and the fixed 5σ budget falls from 254 to 207 runs.

Boundary: this uses the top eigenvalue as a spectral width.  The next layer should sample from the full multivariate covariance, not just its worst eigenmode.
