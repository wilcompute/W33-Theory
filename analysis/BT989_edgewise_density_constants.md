# BT989 — Edgewise density constants replacing the barycentric 120/19 layer

BT983 made the old barycentric tower invalid as an R3 theorem-carrier. BT987
and BT988 therefore force a density-constant reset: the old barycentric constants
such as `120/19` and `860/19` must not be reused for the edgewise/fat tower.

## Constants now justified

For k=2 edgewise/Freudenthal--Kuhn refinement in dimension 4:

```text
top 4-simplex multiplier = 2^4 = 16
mesh scale per step      = 1/2
```

The explicit seeds give:

| seed | f-vector | chi | f4 | edgewise level-1 vertices |
| --- | ---: | ---: | ---: | ---: |
| CP²₉ | [9, 36, 84, 90, 36] | 3 | 36 | 45 |
| K3₁₆ | [16, 120, 560, 720, 288] | 24 | 288 | 136 |

The exact top-count ratio remains

```text
K3₁₆ / CP²₉ = 288 / 36 = 8,
chi(K3₁₆) / chi(CP²₉) = 24 / 3 = 8.
```

## Replacement growth table

| seed | edgewise top counts through level 6 |
| --- | ---: |
| CP²₉ | 36, 576, 9216, 147456, 2359296, 37748736, 603979776 |
| K3₁₆ | 288, 4608, 73728, 1179648, 18874368, 301989888, 4831838208 |

## What is retired

The following constants are now marked **barycentric-only** for R3:

```text
120/19
860/19
```

They came from the old barycentric density layer. Since barycentric refinement is
not shape-regular, those constants cannot support the CMS/Dodziuk--Patodi/FEEC
R3 route.

## Boundary

BT989 computes exactly what is justified by the explicit seed facets plus the
edgewise top multiplier. It does not fake full chain/trace density constants.
Those require the local 4-simplex edgewise facet template and the resulting
lower-dimensional incidence matrices.

## Witnesses

```text
analysis/bt989_edgewise_density_constants.py
data/bt989_edgewise_density_constants.json
```
