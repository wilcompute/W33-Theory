# 2026-05-22 - Explicit 120-Axis Root-Line Isomorphism

## Breakthrough

The previous result was spectral:

```text
W33 local-axis graph and the 120 root-line orthogonality graph both have SRG(120,63,30,36).
```

This pass upgrades that to an explicit labeled graph isomorphism.

## Construction

W33 side:

```text
40 points * 3 local pencil-octahedron axes = 120 axes
```

Two W33 axes are adjacent if they share at least one ordinary quadrangle through their local octahedron axis-corner incidence.

Root-line side:

```text
240 roots modulo antipodal pairing = 120 lines
```

Two root lines are adjacent when they are orthogonal.

## Result

The pushed script builds both graphs and runs a graph-isomorphism solver. It finds a bijection

```text
W33 local axes -> 120 root lines
```

and verifies

```text
edge mismatch count = 0.
```

So every adjacency and non-adjacency relation is preserved.

## Meaning

This upgrades the bridge from:

```text
same count
```

to:

```text
same spectrum and strongly regular parameters
```

to:

```text
explicit labeled graph isomorphism.
```

## Boundary

The mapping is explicit as a finite graph isomorphism and is written by the script as a JSON dictionary. It is not yet a closed-form coordinate formula assigning an eight-dimensional root vector directly from a W33 axis label.

## New file

- `analysis/w33_axes_120_iso.py`

When run, the script writes:

- `data/w33_axes_120_iso.json`

containing the full mapping, graph hashes, parameters, and zero-mismatch verification.
