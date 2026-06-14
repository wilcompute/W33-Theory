# BT990 — R3 fat-tower paper patch packet

BT990 packages the corrected R3 route for the papers and frontier ledger.

## What changed conceptually

R3 should no longer be described as a barycentric-refinement continuum program.
BT983 showed that barycentric refinement violates the fatness/shape-regularity
hypotheses required by the Cheeger--Müller--Schrader / Dodziuk--Patodi / FEEC
route. The correct theorem-carrier is the edgewise/Freudenthal--Kuhn tower.

## Evidence stack now available

- **BT984:** individual Whitney-0/P1 eigenvalue convergence on the edgewise unit
  square tower.
- **BT985:** heat-trace convergence on the same fat tower; level-6 80-mode error
  is `2.1205e-03` at `t=0.05`.
- **BT986:** Regge curvature convergence proxy on the projected edgewise sphere;
  area error falls to `1.9894e-04`, Regge scalar error is roundoff, and local
  deficits decay.
- **BT988:** explicit CP²₉/K3₁₆ facets are loaded from the repo's existing
  orbit-generating module.
- **BT989:** barycentric `120/19` and `860/19` are retired for R3; justified
  edgewise top-channel constants are multiplier `16`, mesh scale `2^-r`, and
  CP²/K3 ratio `8`.

## Paper artifacts

```text
paper/BT990_r3_fat_tower_insert.tex
paper/BT990_holonet_r3_fat_tower_pointer.tex
tools/integrate_bt990_r3_fat_tower_w33.py
tools/integrate_bt990_r3_fat_tower_holonet.py
tools/integrate_bt990_open_frontiers.py
data/bt990_r3_fat_tower_paper_patch.json
```

## Boundary

The connector committed inserts and idempotent integration helpers. It did not
directly rewrite the large TeX papers in this step. The remaining technical task
is the local 4-simplex edgewise facet template, needed to recompute exact
lower-dimensional incidence and heat-density constants on CP²₉/K3₁₆.
