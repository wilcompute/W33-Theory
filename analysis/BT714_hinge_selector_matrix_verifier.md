# BT714 — Hinge Selector Matrix Verifier

BT714 executes the first BT713 next step using the rank-complete selector sheet

```text
mask = 1110
residual channel = 0
```

The verifier calculation, performed locally against the BT713 primitives, gives:

```text
centered K33 rectangles = 2160
local K33 charts = 240
Levi flag columns = 160
selected sheet rank = 81
selected chart-row rank = 81
Levi incidence rank = 79
boundary-defective rows = 0
rank(D_Levi) + rank(S_hinge) = 79 + 81 = 160
```

Therefore the selected hinge sheet is a boundaryless signed Levi-cycle matrix whose row space is the full Levi cycle space. In the BT545--BT551 notation, this is exactly the protected \(E_4/H_1\) Hodge sector.

Boundary: this is a rank-complete executable hinge representative, not a uniqueness theorem for the final tomotope hinge.
