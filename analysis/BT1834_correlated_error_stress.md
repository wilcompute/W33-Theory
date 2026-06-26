# BT1834 — Correlated Error Stress Test

BT1833 used the independent-error width for separating the two finite section totals:

```text
9980 vs 9978, gap = 2.
```

BT1834 replaces the independent model with a conservative block-correlation stress model.

## Model

Use the BT1830/BT1832 syndrome grammar as 12 syndrome-term blocks, each of size 144, so

```text
12 * 144 = 1728
```

local checks.  For intra-block correlation `rho`, the variance inflation factor is

```text
1 + 143*rho.
```

## Results

```text
rho = 0      : sigma = 3.864811204289286,  runs = 34 / 94   for 3σ / 5σ
rho = 0.01   : sigma = 6.024644430741453,  runs = 82 / 227  for 3σ / 5σ
rho = 0.05   : sigma = 11.033342195596038, runs = 274 / 761 for 3σ / 5σ
rho = 0.10   : sigma = 15.117291899194115, runs = 515 / 1429 for 3σ / 5σ
```

## Interpretation

The key finding is that the 9980/9978 section-gap decoder survives modest correlated bursts, but the repetition budget changes sharply:

```text
independent 5σ budget : 94 runs
rho = 0.01 5σ budget  : 227 runs
rho = 0.05 5σ budget  : 761 runs
```

So the next hardware target is no longer just lowering primitive matrices; it is bounding register-family covariance.

Boundary: this is a variance-inflation stress test, not a calibrated covariance matrix.
