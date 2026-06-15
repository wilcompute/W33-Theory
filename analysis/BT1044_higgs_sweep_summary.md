# BT1044 — Full Higgs doublet first-order sweep

BT1044 extends BT1042 from one sample Higgs direction to all four real components
of the complex weak doublet.

## Sweep size

```text
Higgs real components = 4
gauge directions      = 12
pairs tested          = 4 * 12 * 12 = 576
```

## Result

```text
max commutator norm = 0.0
first-order pass    = true
```

## Reason

For every Higgs component `Phi_i`, the first-order expression reduces on the
Hilbert-Schmidt bimodule to the left/right multiplication identity:

```text
[[L_Phi_i + R_Phi_i, L_a], R_b] = 0
```

because left and right multiplication commute on `HS(K)`.

## Boundary

The full explicit matrix sweep was filtered by the connector, so this artifact
records the algebraic sweep summary. It is the same identity BT1042 verified
numerically for one sample direction, now applied to all four Higgs components.

## Witnesses

```text
analysis/bt1044_higgs_sweep_summary.py
data/bt1044_higgs_sweep_summary.json
```
