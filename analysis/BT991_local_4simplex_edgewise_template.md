# BT991 — Local k=2,d=4 edgewise 4-simplex template

BT991 supplies the missing local Freudenthal--Kuhn template for the corrected R3
fat tower.

## Vertex set

The local vertices are integer barycentric coordinates

```text
(a0,a1,a2,a3,a4),  ai >= 0,  sum ai = 2.
```

Thus the template has:

- 5 original vertices `2e_i`;
- 10 edge midpoints `e_i + e_j`.

Total vertex count: `15`.

## Top cells

The top 4-simplices split as:

```text
5 corner 4-simplices
11 central 4-simplices triangulating Delta(2,5)
```

The central piece is the rectified 4-simplex / hypersimplex `Delta(2,5)` and is
triangulated by a pulling triangulation. The total top-cell count is therefore:

```text
5 + 11 = 16 = 2^4.
```

## Certificate

The generated template has:

```text
f-vector                 = [15, 55, 85, 60, 16]
Euler characteristic     = 1
boundary tetrahedra      = 40
internal tetrahedra      = 20
bad tetrahedra           = 0
expected boundary tets   = 5 * 8 = 40
```

Every tetrahedral 3-face appears either once, on the boundary, or twice,
internally. The boundary count agrees with the k=2 edgewise subdivision of the
five tetrahedral boundary faces: each boundary tetrahedron subdivides into 8
tetrahedra.

## Reading

This closes the BT987/BT989 placeholder. The local edgewise 4-simplex template is
now explicit and can be applied to the CP²₉/K3₁₆ facets. The full generated
facet list is produced by the script rather than hand-maintained in markdown.

## Witnesses

```text
analysis/bt991_local_4simplex_edgewise_template.py
data/bt991_local_4simplex_edgewise_template.json
```
