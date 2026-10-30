# 2026-05-22 - W33 Local Axes Spectral Bridge

## Target

The previous synthesis produced a canonical internal set of 120 objects:

```text
40 W33 points times 3 local pencil-octahedron axes per point = 120.
```

The natural next test was whether this 120-set carries the same graph-level structure as the older 120-object exceptional-geometry layer already explored elsewhere in the repo.

## Construction on the W33 side

Rows are the 120 local axes.
Columns are the 1620 ordinary quadrangles.

A local axis is incident to a quadrangle when the quadrangle uses one of the two opposite local octahedron vertices contained in that axis.

The incidence matrix has shape

```text
120 x 1620
```

with

```text
row degree = 54
column weight = 4
120 * 54 = 1620 * 4 = 6480
```

Define the unweighted axis graph by joining two axes when they share at least one quadrangle.

## Result

The W33 local-axis graph is strongly regular:

```text
SRG(120, 63, 30, 36)
```

with spectrum

```text
63^1 + 3^84 + (-9)^35.
```

The comparison graph built from the 120 antipodal pairs of the 240 eight-dimensional roots has the same parameters:

```text
SRG(120, 63, 30, 36)
```

and the same spectrum:

```text
63^1 + 3^84 + (-9)^35.
```

## Weighted incidence layer

The weighted axis-quadrangle Gram matrix has off-diagonal values

```text
0, 2, 3
```

with distribution

```text
0: 3360
2: 1620
3: 2160
```

and spectrum

```text
216^1 + 66^24 + 60^60 + 36^20 + 24^15.
```

## Interpretation boundary

This proves a strong spectral bridge. It does not yet provide a labeled object-by-object bijection.

The next target is to construct a labeled bijection or prove uniqueness of this graph type, which would upgrade the spectral bridge into an explicit correspondence.

## New code

- `analysis/w33_axes_e8_rootline_spectral_bridge.py`

The script builds both 120-object graphs from scratch and checks the parameters and spectra.
