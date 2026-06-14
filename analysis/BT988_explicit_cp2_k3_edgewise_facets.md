# BT988 — Explicit CP²₉/K3₁₆ facets loaded into the edgewise R3 path

BT987 marked the missing incidence-data boundary. BT988 tightens that boundary:
the repo already contains executable CP²₉/K3₁₆ facet generators in
`exploration/w33_explicit_curved_4d_complexes.py`, so the R3 edgewise path can
start from actual facets rather than f-vector placeholders.

## Source module

`exploration/w33_explicit_curved_4d_complexes.py` reconstructs:

- `CP2_9` from Kühnel's 9-vertex orbit description;
- `K3_16` from the Casella--Kühnel/Sage permutation-orbit construction.

## Loaded seed data

| seed | facets | f-vector | Betti | chi | edgewise level-1 vertices |
| --- | ---: | ---: | ---: | ---: | ---: |
| CP²₉ | 36 | [9, 36, 84, 90, 36] | [1, 0, 1, 0, 1] | 3 | 45 |
| K3₁₆ | 288 | [16, 120, 560, 720, 288] | [1, 0, 22, 0, 1] | 24 | 136 |

The level-1 vertex count is exact for k=2 edgewise refinement:

```text
new vertices = old vertices + old edges.
```

## Top-dimensional edgewise counts

| seed | level 0 | level 1 | level 2 | level 3 | level 6 |
| --- | ---: | ---: | ---: | ---: | ---: |
| CP²₉ | 36 | 576 | 9216 | 147456 | 603979776 |
| K3₁₆ | 288 | 4608 | 73728 | 1179648 | 4831838208 |

## Boundary

BT988 does **not** fabricate the local 4-simplex edgewise triangulation template.
The explicit seed facets are loaded and the exact level-1 vertex/top-simplex
count layer is now wired. Exact lower-dimensional edgewise incidence matrices
still require the local 4-simplex template.

## Witnesses

```text
analysis/bt988_explicit_cp2_k3_edgewise_facets.py
data/bt988_explicit_cp2_k3_edgewise_facets.json
```
