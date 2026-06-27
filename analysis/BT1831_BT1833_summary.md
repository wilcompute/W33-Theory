# BT1831-BT1833 summary

Executed the three requested moves after BT1828-BT1830.

## BT1831

Added the first finite error ledger for the BT1830 component grammar.

```text
component count = 15
survival probability = 0.9704163817442235
erasure probability = 0.02958361825577649
per-run syndrome bound = 0.00872
combined bound = 0.03830361825577649
postselected success rate = 0.9619540256157939
```

Boundary: this is a first-pass bound, not a calibrated chip model.

## BT1832

Lowered the grammar into optical primitive classes.

```text
component graph nodes = 33
component graph edges = 39
ring bins = 12
qutrit sorter meshes = 3
D4 encoders = 3
D4 parity ancillas = 2
K4 equality interferometers = 3
coincidence guards = 3
```

Boundary: primitive grammar only; exact matrices and calibration pulses remain future work.

## BT1833

Computed the repetition budget for the two finite section totals.

```text
section A = 9980
section B = 9978
gap = 2
local terms = 1728
per-term bound = 0.00872
single-run width = 3.864811204289286
runs for 3 sigma = 34
runs for 5 sigma = 94
```

Conclusion: one run is not enough; repeated postselected runs separate the gap under the BT1831 independent-error bound.
