# BT987 — CP²₉/K3₁₆ edgewise conversion scaffold

BT983 changed the correct R3 route: the CP²₉/K3₁₆ curved refinement program
must move from barycentric refinement to a shape-regular edgewise/Freudenthal--
Kuhn tower. BT987 records the concrete conversion boundary for the actual
minimal 4D seeds already used by the corpus.

## Existing seed facts

The current `w33_minimal_triangulation_bridge.py` uses the vertex-minimal
3-neighborly seeds:

| seed | vertices | f-vector | chi |
| --- | ---: | ---: | ---: |
| CP²₉ | 9 | [9, 36, 84, 90, 36] | 3 |
| K3₁₆ | 16 | [16, 120, 560, 720, 288] | 24 |

## Edgewise replacement

For a 4-simplex:

```text
edgewise k=2 top multiplier = 2^4 = 16
barycentric top multiplier = 5! = 120
```

Therefore the old barycentric density constants cannot be reused. In particular,
anything built from the barycentric 120-per-simplex growth, including the
`120/19` and `860/19` density constants, must be rederived for the edgewise
fat tower.

## Top-simplex growth

| seed | level | edgewise top 4-simplices | barycentric top 4-simplices | bary/edge ratio |
| --- | ---: | ---: | ---: | ---: |
| CP²₉ | 0 | 36 | 36 | 1 |
| CP²₉ | 1 | 576 | 4320 | 7.5 |
| CP²₉ | 2 | 9216 | 518400 | 56.25 |
| CP²₉ | 3 | 147456 | 62208000 | 421.875 |
| K3₁₆ | 0 | 288 | 288 | 1 |
| K3₁₆ | 1 | 4608 | 34560 | 7.5 |
| K3₁₆ | 2 | 73728 | 4147200 | 56.25 |
| K3₁₆ | 3 | 1179648 | 497664000 | 421.875 |

By level 6 the barycentric tower is already larger by a factor of
177978.515625 in top-dimensional simplex count. The edgewise tower is not only
the correct theorem-carrier; it is computationally much more plausible.

## Patch points

1. `exploration/w33_minimal_triangulation_bridge.py`: replace the barycentric
   f-vector refinement routine with edgewise facet refinement once explicit
   CP²₉/K3₁₆ facet lists are loaded.
2. `exploration/w33_curved_barycentric_density_bridge.py`: retire the
   barycentric `120/19` and `860/19` constants for R3 verification; rederive the
   edgewise density constants.
3. `exploration/w33_transport_curved_dirac_refinement_bridge.py`: rename and
   reroute the heat-density bridge from the barycentric tower to the edgewise
   tower.
4. `w33_paper.tex` / `OPEN_FRONTIERS.md`: state that CP²₉/K3₁₆ R3 verification
   now means edgewise/fat refinement, not barycentric refinement.

## Boundary

BT987 does not fake missing incidence data. Exact lower-dimensional edgewise
f-vectors and chain matrices require explicit CP²₉/K3₁₆ facet lists. What BT987
locks down is the correct tower type, exact top-simplex multiplier, and the
files that must change next.

## Witnesses

```text
analysis/bt987_cp2_k3_edgewise_conversion.py
data/bt987_cp2_k3_edgewise_conversion.json
```
