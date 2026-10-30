# 2026-05-22 - A2 Point Triads and D4 Line Subsystems

## Breakthrough

After constructing an explicit graph isomorphism from the 120 W33 local axes to the 120 root lines, the next question was what W33 points and lines become under that map.

They become recognizable root-line objects.

## Point result: 40 A2-type triads

Each W33 point has three local octahedron axes.

Under the explicit 120-axis to 120-root-line graph isomorphism, those three axes map to a root-line triad with:

```text
0 internal orthogonality edges
absolute dot products = (1,1,1)
2 sign choices whose vector sum is zero
```

So each W33 point maps to an A2-type triad of root lines.

There are 40 such triads.

## Line result: 40 D4-type subsystems

Each W33 line contains four points. Taking the three axes at each point gives 12 local axes.

Under the root-line map, those 12 axes form a D4-type root-line subsystem:

```text
12 root lines
internal orthogonality graph degree = 9
spectrum = 9^1 + 0^8 + (-3)^3
absolute dot distribution = 0^54 + 1^12
```

The complement of the internal orthogonality graph splits as four disjoint triangles:

```text
3 + 3 + 3 + 3
```

These four triangles are exactly the four point triads on the W33 line.

There are 40 such D4-type subsystems.

## W33 collinearity recovery

For two W33 points p and q, take their two mapped A2-type triads. Count the number of orthogonal root-line pairs between the two triads.

The rule is exact:

```text
9 orthogonal pairs  <=>  p and q are collinear in W33
3 orthogonal pairs  <=>  p and q are not collinear in W33
```

The certificate verifies:

```text
collinear pairs:     240 all have count 9
noncollinear pairs:  540 all have count 3
```

## Meaning

The 120-axis to root-line map is not arbitrary. It carries the W33 incidence geometry into root-line incidence:

| W33 object | root-line image |
|---|---|
| point | A2-type triad |
| line | D4-type 12-line subsystem |
| collinearity | 9-vs-3 orthogonality count between triads |
| local octahedron axes | root lines |

This is a major step toward a closed W33-to-E8 correspondence.

## Machine certificate

Added:

- `analysis/w33_axis_rootline_a2_d4_decomposition.py`

When run, the script writes:

- `data/w33_axis_rootline_a2_d4_decomposition.json`
