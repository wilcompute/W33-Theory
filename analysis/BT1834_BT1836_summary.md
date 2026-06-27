# BT1834-BT1836 summary

Executed the three requested moves after BT1831-BT1833.

## BT1834 — correlated error stress

The independent BT1833 repetition budget is upgraded to a block-correlation stress model.

```text
12 syndrome-term blocks
144 local checks per block
1728 total local checks
variance inflation = 1 + 143*rho
```

Results:

```text
rho = 0      : 3σ / 5σ runs = 34 / 94
rho = 0.01   : 3σ / 5σ runs = 82 / 227
rho = 0.05   : 3σ / 5σ runs = 274 / 761
rho = 0.10   : 3σ / 5σ runs = 515 / 1429
```

## BT1835 — exact optical matrices

Assigned exact matrices/permutation unitaries to the BT1832 primitive grammar:

```text
qutrit sorter          = F3
glue quartet encoder  = H2 tensor H2 / 2
winding analyzer       = F12
D4 parity ancilla      = reversible XOR permutation, dimension 256
K4 comparator          = reversible inequality comparator, dimension 32
phase-slip guard       = reversible equality comparator, dimension 288
```

## BT1836 — calibration feedback

A calibration control packet:

```text
shots = 10000
erasures = 296
kept = 9704
syndrome events = 85
```

gives:

```text
p_hat = 0.008759274525968672
p_upper_95 = 0.010613251409451746
erasure_hat = 0.0296
erasure_upper_95 = 0.03292182937165653
```

Feeding the conservative bound back into the section-gap decoder gives:

```text
single-run upper width = 4.259701234272514
runs for 3 sigma = 41
runs for 5 sigma = 114
```

So calibration raises the 5σ budget from 94 to 114 runs, while correlated drift can raise it much further and must be controlled.
