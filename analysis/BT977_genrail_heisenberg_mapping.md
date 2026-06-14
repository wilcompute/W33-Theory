# BT977 — GenRail mapping to Heisenberg generation machinery

BT977 maps the existing generation machinery onto the selector-fixed GenRail faces.

## Source anchor

`analysis/BT874_texture_triality_is_heisenberg_center.md` proves that the texture/generation order-3 map is the Heisenberg center, a long-root transvection.

Used facts:

```text
Heisenberg center order = 3
27 matter shell = 9 free orbits of 3
Steinberg matter register split = 27+27+27
fixed gauge perp-plane = 13 points
```

## Selector-fixed generation faces

```text
GenRail_A = (0,1,3), phase 0
GenRail_B = (0,2,3), phase 1
GenRail_C = (1,2,3), phase 2
CompRail_0 = (0,1,2)
```

## Boundary

No charge or field label is asserted here. BT977 attaches the proven order-3 generation source to selector-fixed 27-faces only.

## Witness

```text
analysis/bt977_genrail_heisenberg_mapping.py
data/bt977_genrail_heisenberg_mapping.json
```
