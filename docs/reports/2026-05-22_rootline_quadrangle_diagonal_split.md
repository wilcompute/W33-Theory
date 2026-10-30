# 2026-05-22 - Root-Line Quadrangle Diagonal Split

## Breakthrough

The previous species result showed that W33 quadrangles become a distinct 12-root-line species whose complement splits as

```text
6 + 6
```

This pass identifies what those two six-blocks are.

## Result

For every W33 quadrangle, the two 6-blocks are exactly the two diagonal pairs of the quadrangle.

A quadrangle has four point-triads:

```text
T_a, T_b, T_c, T_d
```

and two noncollinear diagonal pairs. The root-line complement split is

```text
(T_a union T_b)  +  (T_c union T_d)
```

for the two diagonal pairs, each block containing six root lines.

The script verifies this for all 1620 quadrangles.

## Line comparison

For a W33 line, the 12-root-line subsystem complement splits as

```text
3 + 3 + 3 + 3
```

and those four 3-blocks are exactly the four point-triads on the line.

So the root-line layer distinguishes:

```text
line:       four point-triads, 3+3+3+3
quadrangle: two diagonal-pair blocks, 6+6
```

## Line-quadrangle intersections

Root-line intersection sizes between the 40 line systems and 1620 quadrangle systems are:

```text
0: 45360
3: 12960
6: 6480
```

Interpretation:

- 6 means the W33 line contains one diagonal pair of the quadrangle as a six-block.
- 3 means the W33 line meets the quadrangle in one point-triad.
- 0 means no root-line overlap.

## New code

- `analysis/w33_rootline_quadrangle_diagonal_split.py`

When run, it writes:

- `data/w33_rootline_quadrangle_diagonal_split.json`
