# 2026-05-22 - Local Octahedron Axes Canonical 120-Set

## Question tested

The repo repeatedly encounters the number 120 in exceptional geometry. This pass tested whether W(3,3) has an intrinsic 120-object set coming from the new local pencil-octahedra.

## Result

It does.

Each W33 point has four incident isotropic lines. These four lines form a pencil. The local octahedron at the point is the line graph of that four-line pencil.

Each such local octahedron has three axes. Therefore the 40 W33 points give

```text
40 * 3 = 120
```

canonical local axes.

## Quadrangle uniformity

Each local axis contains two opposite local octahedron vertices. Each local octahedron vertex lies on 27 quadrangle corners. Therefore each axis sees

```text
2 * 27 = 54
```

quadrangle corners.

The certificate verifies

```text
120 * 54 = 1620 * 4 = 6480.
```

## Interpretation boundary

This does not yet give an explicit bijection to any external 120-set. It proves the W33 side: W33 contains a canonical 120-set built from the three axes of each of its 40 local pencil-octahedra.

That makes this 120-set a strong candidate interface for future tests involving E8 root-pair or 600-cell structures.

## Machine certificate

Added:

- `analysis/w33_octahedron_axes_120_e8_longshot.py`
- `data/w33_octahedron_axes_120_e8_longshot.json`
