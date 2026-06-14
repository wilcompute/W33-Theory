# BT996 — R3 edgewise Hodge stack paper patch

BT996 packages BT991--BT995 into the paper stack.

## Evidence now available

- **BT991:** explicit local `k=2,d=4` edgewise 4-simplex template with f-vector
  `[15,55,85,60,16]`, 16 top 4-simplices, Euler characteristic 1, and valid
  boundary/internal tetrahedron counts.
- **BT992:** true level-1 edgewise incidence on the real CP2_9/K3_16 facets.
- **BT993:** carrier-exact edgewise f-vector recurrence replacing barycentric
  `120/19` and `860/19`.
- **BT994:** sparse Hodge-Laplacian certificates with harmonic dimensions
  `[1,0,1,0,1]` for CP2_9 and `[1,0,22,0,1]` for K3_16.
- **BT995:** exact real-seed heat-supertrace samples and large-time harmonic
  endpoints.

## Paper artifacts

```text
paper/BT996_r3_edgewise_hodge_stack_insert.tex
paper/BT996_holonet_edgewise_hodge_pointer.tex
tools/integrate_bt996_r3_edgewise_hodge_stack_w33.py
tools/integrate_bt996_holonet_edgewise_hodge.py
data/bt996_r3_edgewise_hodge_stack_patch.json
```

## Boundary

The connector committed inserts and idempotent integration helpers. It did not
directly rewrite the large TeX files. The next technical layer is a production
nonzero-mode heat-trace estimator for K3_16 middle degree.
