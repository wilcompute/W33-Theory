# Z3 Edge Potential Analysis

We analyze the edge labels (mod 3) from the Z3 edge potential solution and
correlate them with ray-family structure, basis involvement, and symplectic
omega values (via the ray->F3 mapping).

## Edge label distribution
```
{0: 150, 1: 195, 2: 195}
```

## Family-pair counts by label (selected)
Balanced and structured patterns appear. A few highlights:
- **F2–F3** is perfectly balanced: {0:18, 1:18, 2:18}.
- **B–F3** heavily favors label 0 (11 vs 8/8).
- **B–F2** is closer to balanced (7,10,10).
- **F3–F3** leans to label 0 (13 vs 6/8).

Full table is in `docs/witting_z3_edge_potential_analysis.txt`.

## Basis involvement (BB/BN/NN)
```
BN: {0:22, 1:40, 2:46}
NN: {0:128, 1:155, 2:149}
```
The edge potential is **not uniform**; label 0 is suppressed on basis-nonbasis
edges relative to labels 1 and 2.

## Symplectic omega vs label
```
omega=1: {0:67, 1:77, 2:93}
omega=2: {0:83, 1:118, 2:102}
```
Both omega classes realize all labels with mild bias; omega does not fix the
label but shifts the distribution.

## Interpretation
The Z3 edge potential is **structured** by ray families and basis involvement
but is not determined by omega alone. The perfectly balanced F2–F3 sector suggests
an internal symmetry, while basis-containing pairs bias label 0. This is
consistent with the Z3 potential being an **edge-derived gauge** rather than a
simple symplectic invariant.

Script: `tools/witting_z3_edge_potential_analysis.py`
Output: `docs/witting_z3_edge_potential_analysis.txt`
