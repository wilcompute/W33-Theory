# 2026-05-22 - Root-Line Line/Quadrangle Species Split

## Question

After the 120-axis to root-line map, W33 lines become 12-root-line sets. What do W33 quadrangles become?

A W33 quadrangle has four points. Each point maps to a 3-root-line triad, so a quadrangle also gives a 12-root-line set.

The question was whether these 12-sets are the same kind of root-line object as W33 lines, or a distinct species.

## Result

They are distinct uniform species.

## W33 line species

The 40 W33 lines become 40 identical 12-root-line systems.

Internal orthogonality graph:

```text
9-regular on 12 vertices
spectrum = 9^1 + 0^8 + (-3)^3
absolute dot distribution = 0^54 + 1^12
```

The complement splits as

```text
3 + 3 + 3 + 3
```

matching the four point-triads on a W33 line.

## W33 quadrangle species

The 1620 W33 quadrangles become 1620 identical 12-root-line systems.

Internal orthogonality graph:

```text
7-regular on 12 vertices
spectrum = 7^1 + 1^4 + (-1)^6 + (-5)^1
absolute dot distribution = 0^42 + 1^24
```

The complement splits as

```text
6 + 6
```

So quadrangle loops are not D4-type line subsystems. They are a second 12-line species distinguished by a split 6-plus-6 complement.

## Meaning

The root-line layer now distinguishes two W33 geometries:

| W33 object | root-line image | internal signature |
|---|---|---|
| line | 12-line D4-type subsystem | 9-regular, complement 3+3+3+3 |
| quadrangle | 12-line loop subsystem | 7-regular, complement 6+6 |

This gives a root-line classification of both local incidence lines and nonlocal quadrangle loops.

## New code

- `analysis/w33_rootline_line_vs_quadrangle_species.py`

When run, it writes:

- `data/w33_rootline_line_vs_quadrangle_species.json`
