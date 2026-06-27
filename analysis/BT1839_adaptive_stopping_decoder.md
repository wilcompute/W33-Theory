# BT1839 — Adaptive Sequential Decoder

BT1839 replaces fixed-run section separation with a sequential likelihood-ratio rule.

## Rule

Compare the two finite sections:

```text
section A = 9980
section B = 9978
gap = 2
```

Use the sequential probability ratio test:

```text
stop when |LLR| >= ln(999)
ln(999) = 6.906754778648554
```

This corresponds to an alpha/beta target of about `0.001` under the independent Gaussian section-estimator approximation.

## Monte Carlo packet

For 5000 deterministic trials under section A:

```text
BT1833 independent sigma = 3.864811204289286
median stop = 47
mean stop = 53.7798
p95 stop = 107
wrong decisions = 4 / 5000
```

```text
BT1836 scalar-calibrated sigma = 4.259701234272514
median stop = 57
mean stop = 65.295
p95 stop = 131
wrong decisions = 1 / 5000
```

```text
BT1837 covariance-upper sigma = 6.369321430990651
median stop = 129
mean stop = 144.454
p95 stop = 286
wrong decisions = 3 / 5000
```

## Interpretation

The adaptive rule beats fixed-shot budgeting in the typical case.  Under the BT1837 covariance-upper width:

```text
fixed 5 sigma budget = 254 runs
adaptive median stop = 129 runs
adaptive p95 stop = 286 runs
```

So the median run count is nearly cut in half, while the tail remains comparable to the conservative fixed budget.

Boundary: this is still a Gaussian independent-increment decoder.  A full covariance SPRT must use the BT1837 12x12 covariance matrix once it is materialized.
