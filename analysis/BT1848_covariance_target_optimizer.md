# BT1848 — Covariance Target Optimizer

BT1845 manually proposed covariance hardware targets.  BT1848 solves the targeting problem as a weighted spectral optimization:

```text
minimize weighted covariance reductions
subject to lambda_max <= 1.4
```

## Starting point

```text
starting lambda_max = 1.821589796573715
starting 5 sigma run budget = 200
```

## Optimized target

The greedy spectral optimizer selects four knobs:

```text
C12_C internal: 0.20 -> 0.055
qutrit_P internal: 0.18 -> 0.07
E_C cross: 0.08 -> 0.035
D4_G internal: 0.16 -> 0.08
```

Result:

```text
optimized lambda_max = 1.392744103256981
optimized 5 sigma run budget = 157
```

## Interpretation

The optimizer largely agrees with BT1845 but is sharper.  It does not need to lower every family target.  The smallest high-value set is:

```text
1. C12_C internal covariance
2. qutrit_P internal covariance
3. K4_E to C12_C cross covariance
4. D4_G internal covariance
```

That reaches the spectral target and lowers the fixed 5σ budget from 200 to 157 runs.

Boundary: this is a greedy spectral covariance optimizer.  It is not yet a physical control-theory optimizer with actuator costs and calibration time.
