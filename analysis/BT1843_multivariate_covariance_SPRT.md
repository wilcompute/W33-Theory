# BT1843 — Multivariate Covariance SPRT

BT1842 used the largest eigenvalue of the BT1840 covariance matrix as a conservative scalar width.  BT1843 uses the full 12-dimensional covariance matrix directly.

## Model

Each run emits a 12-block Gaussian section increment over the BT1840 syndrome block order:

```text
P0 P1 P2 G0 G1 E01 E12 E20 Cwind Cslip01 Cslip12 Cslip20
```

The section gap is distributed uniformly across the 12 block coordinates:

```text
delta_i = 2/12 = 0.16666666666666666
```

The SPRT increment uses the full inverse covariance:

```text
LLR_increment = delta^T Sigma^{-1} x
```

## Information geometry

```text
uniform-direction variance inflation = 1.763333333333333
aggregate sigma = 5.656481204831619
delta^T Sigma^{-1} delta = 0.12635807264797333
LLR drift under section A = 0.06317903632398666
LLR sd per run = 0.3554688068564854
```

## Budgets

```text
fixed 3 sigma budget = 72 runs
fixed 5 sigma budget = 200 runs
```

Adaptive packet:

```text
trials = 5000
seed = 1843
median stop = 99
mean stop = 111.886
p95 stop = 224
max stop = 637
wrong decisions = 3 / 5000
```

## Interpretation

The full matrix beats the BT1842 lambda-max compression:

```text
BT1842 lambda-max median = 103
BT1843 full-matrix median = 99
BT1842 fixed 5 sigma = 207
BT1843 fixed 5 sigma = 200
```

Boundary: this is a full multivariate Gaussian model, not yet a measured non-Gaussian hardware process.
