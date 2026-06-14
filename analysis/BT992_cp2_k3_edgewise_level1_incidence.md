# BT992 — True level-1 CP2/K3 edgewise incidence

BT992 applies the BT991 local `k=2,d=4` edgewise template to the explicit CP2_9
and K3_16 facets already present in the repo. The script builds actual level-1
top facets with globally shared edge-midpoint vertices, enumerates all faces,
and computes boundary ranks over `F2` with sparse bitset Gaussian elimination.

## Level-1 result

| seed | f-vector | boundary ranks mod 2 | Betti mod 2 | chi |
| --- | ---: | ---: | ---: | ---: |
| CP2_9 | [45, 414, 1236, 1440, 576] | [44, 370, 865, 575] | [1, 0, 1, 0, 1] | 3 |
| K3_16 | [136, 2640, 9440, 11520, 4608] | [135, 2505, 6913, 4607] | [1, 0, 22, 0, 1] | 24 |

The topology is preserved at level 1. This is the first incidence-matrix pass on
the corrected R3 tower.

## Witnesses

```text
analysis/bt992_cp2_k3_edgewise_level1_incidence.py
data/bt992_cp2_k3_edgewise_level1_incidence.json
```
