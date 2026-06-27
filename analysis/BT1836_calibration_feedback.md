# BT1836 — Calibration Feedback Loop

BT1836 closes the loop from BT1831 and BT1833: use control states to estimate the live syndrome and erasure rates, then feed the upper confidence bound back into the section-gap repetition budget.

## Control run

```text
shots = 10000
erasures = 296
kept = 9704
syndrome events = 85
```

## Estimates

```text
p_hat = 85 / 9704 = 0.008759274525968672
p_upper_95 = 0.010613251409451746
erasure_hat = 0.0296
erasure_upper_95 = 0.03292182937165653
```

## Updated repetition budget

Using the conservative upper bound `p_upper_95` over 1728 local terms and gap 2 gives:

```text
single-run upper width = 4.259701234272514
runs for 3 sigma = 41
runs for 5 sigma = 114
```

Compared to BT1833:

```text
old 3 sigma = 34
old 5 sigma = 94
new 3 sigma = 41
new 5 sigma = 114
```

## Interpretation

The calibration loop does not destroy the section separation; it raises the 5σ budget from 94 to 114 runs under the conservative live-control upper bound.

Boundary: this is the first independent-error feedback pass.  Correlated drift must be fed through the BT1834 covariance stress model next.
