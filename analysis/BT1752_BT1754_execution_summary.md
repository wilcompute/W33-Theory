# BT1752-BT1754 execution summary

Executed the three requested next moves.

## BT1752: structured voltage/backtracking cocycle engine

Added `analysis/bt1752_voltage_backtracking_cocycle_engine.py`.

The Hesse/Fano cocycle problem is now encoded as a structured CSP scaffold:

```text
variables = 9 selected Hesse lines
domain size per variable = 1008 oriented Fano systems
Hesse triple split = 18 triangle constraints, 9 concurrent triples, 57 parallel/disjoint triples
incumbent = [459,595,435,694,87,544,347,839,561]
```

The key structural point is that no-6-cycle pruning lives on the 18 Hesse triangle constraints. Boundary: this is the backtracking/voltage scaffold, not yet a new witness below 44 eight-cycles.

## BT1753: Coxeter bus signature

Added `analysis/bt1753_coxeter_bus_signature.py`.

The BT1747 E8 hexagon allocation now has a reusable Coxeter-cycle signature. Rows are 8-hexagon buses and columns are Coxeter 5-cycles on the 40 Witting hexagons. Row and column signatures are invariant under bus relabeling and Coxeter-cycle relabeling.

Boundary: this is Coxeter-cycle aware, not the full E8 Weyl normalizer classification.

## BT1754: Hesse/Q4 Fano orientation decomposition

Added `analysis/bt1754_hesse_q4_fano_orientation_decomposition.py`.

The nine Fano-system choices decompose as:

```text
choice = 6 * PSL(2,7)-automorphism-index + rotation-index
```

The rotation indices are derived from the Hesse/Q4 family-parameter table:

```text
rows      -> [3,1,3]
columns   -> [4,3,4]
diagonals -> [5,5,3]
```

So BT1751/BT1754 derive channel colors and rotation orientation from the Hesse/Q4 layer. The remaining unexplained data are exactly nine PSL(2,7) automorphism indices.
