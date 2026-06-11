# BT814 — Tomotope Middle Layer from Residual Tetrahedra

BT798 identified the residual `16+16+8+8 = 48` packet as four common
transversal `K4` tetrahedra of a skew-line chart.  BT814 reads that same carrier
as the local tomotope middle layer.

For each of the four transversal tetrahedra:

```text
3 opposite-edge axes
4 triangular faces
2 base/shadow antipode sheets
```

Therefore the local object has:

```text
vertices = 4
edges    = 4 * 3 = 12
faces    = 4 * 4 = 16
cells    = 4 * 2 = 8
middle edge-face blocks = 4 * 3 * 4 = 48
```

This is exactly the tomotope middle profile recorded by the true tomotope
`<r0,r3>` block data:

```text
48 blocks
4 blocks per tomotope edge
3 blocks per tomotope face
48 * 4 = 192 flags after the 2x2 flag fiber is restored
```

## Meaning

The BT798 residual is not only “four tetrahedra” and not only a count match.
It has the same edge/face middle-incidence profile as the tomotope:

```text
transversal K4 axis  -> local tomotope edge
transversal K4 face  -> local tomotope face
base/shadow pair     -> local tomotope cell sheet
```

So the rank-4 residual carrier is the local finite mechanism that realizes the
tomotope edge-face middle layer inside W(3,3).

## Boundary

BT814 identifies the 48 middle blocks objectwise.  The full `2x2` flag fiber is
inherited from the existing tomotope block model and is not re-derived here.

## Validation

Run:

```bash
python3 analysis/bt814_tomotope_middle_layer_from_residual_tetrahedra.py
```
