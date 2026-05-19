# Hamming/Fano Horizon Functor Search

## Why this experiment

The earlier Fano-Hamming horizon bridge had the clean parameter identity

```text
72 = q^2 * 2^q = 9 * 8
```

but it left a real gap: no coordinate-level functor from the binary
Hamming/Fano syndrome space to the explicit 72-coordinate ternary horizon
model.

This experiment tries that missing construction directly.

## External pressure check

Hamming's original 1950 construction uses a checking number from the parity
checks to identify a single error position; in the seven-position case the
table gives `n=7, m=4, k=3`.  That is the binary Hamming `[7,4,3]` shadow we
need to respect.

Finite-projective-plane references give the standard Fano boundary: the order
2 plane has seven points and seven lines, three points on each line and three
lines through each point, and it is unique up to isomorphism.

Sources checked:

- R. W. Hamming, "Error Detecting and Error Correcting Codes," Bell System
  Technical Journal 29 (1950), 147-160:
  https://zoo.cs.yale.edu/classes/cs323/doc/Hamming.pdf
- Finite Projective Geometry notes, section on the Fano plane:
  https://www.homepages.ucl.ac.uk/~ucahbdo/FiniteProjectivePlanes.pdf

## New construction

Use the tetrahedral model of the Fano plane.

The seven nonzero binary labels are:

```text
four K4 vertex labels:      V00, V10, V01, V11
three K4 direction labels:  D10, D01, D11
```

with the zero coset label:

```text
Z = 000
```

The six horizon parity checks are the six edges of `K4`.  The K4 edge joining
columns `c` and `c'` becomes the Fano line

```text
{ V_c, V_c', D_(c+c') }.
```

That gives an actual rule for every one of the 72 horizon coordinates:

```text
18 row edges      -> direction labels
12 column edges   -> vertex labels
36 mixed edges    -> endpoint labels plus residual zero/direction labels
6 parity symbols  -> direction labels
```

The residual rule is gauge-fixed.  Choose a row origin and a column origin.
For each direction, one parallel K4 edge through the column origin donates one
row-origin residual mixed edge to the direction label; all remaining
row-origin residual mixed edges go to the zero sheet.

The script found 24 balanced gauge-fixed lifts.

## Computed result

The exact sheet split is:

```text
Z   = 9 mixed edges

V00 = 3 column edges + 6 mixed edges
V10 = 3 column edges + 6 mixed edges
V01 = 3 column edges + 6 mixed edges
V11 = 3 column edges + 6 mixed edges

D10 = 6 row edges + 2 parity symbols + 1 mixed edge
D01 = 6 row edges + 2 parity symbols + 1 mixed edge
D11 = 6 row edges + 2 parity symbols + 1 mixed edge
```

So every one of the eight Hamming/Fano labels receives exactly nine horizon
coordinates.

More importantly, every nonzero label is incident with the actual parity-check
line supporting that coordinate.  The zero sheet is not an error or leftover:
it is exactly the nine mixed row-origin residual coordinates.

## Support-row profile

Every full horizon parity row still sees 16 coordinates.

The three K4 checks through the column-origin gauge split as:

```text
5 + 5 + 5 + 1
```

meaning five on each of the three Fano-line labels, plus one zero-sheet
residual.

The three opposite checks split as:

```text
5 + 5 + 4 + 2
```

meaning five on the two endpoint vertex labels, four on the direction label,
plus two zero-sheet residuals.

Across each pair of parallel K4 checks, the direction label total is restored
to nine.

## Zero-sheet follow-through

The zero sheet is not an unstructured leftover.  In the local `K12` horizon
graph it is:

```text
vertices:   8
edges:      9
components: 1
cycle rank: 2
triangles:  0
```

The simple cycles have lengths:

```text
4, 4, 6
```

The two 4-cycles share one mixed edge; their symmetric difference is the
6-cycle.  This is exactly the shape expected from a rank-two residual gauge
sector rather than an arbitrary pile of nine unmatched edges.

The row/column incidence imbalance is also structured:

```text
row incidence:    0 -> 9, 1 -> 3, 2 -> 6
column incidence: 0 -> 3, 1 -> 5, 2 -> 5, 3 -> 5
```

So the chosen row origin is fully saturated, while the chosen column origin is
the unique deficient column.  That asymmetry is not hidden by the construction;
it is the gauge cost of making the `72 = 8 * 9` functor literal.

## Interpretation

This appears to be the missing literal functor, but in a precise limited
sense:

```text
binary Hamming/Fano cosets
        |
        v
eight 9-coordinate sheets in the ternary horizon model
```

The functor is not fully symmetric.  It requires a row-origin and column-origin
gauge.  That is the unexpected part worth following: the zero coset becomes a
physical residual sheet, not an empty label.  Its internal graph has rank two.

## Boundary

This is not a claim that the ternary horizon code is equivalent to the binary
Hamming code, the ternary Golay code, or a full quantum code.  It is a
coordinate-level incidence lift:

- exact balanced `72 = 8 * 9` labeling;
- exact Fano-line compatibility with the six actual horizon parity checks;
- exact zero-sheet classification as nine mixed residuals.

The next useful experiment is to compose this sheet map with the actual W(3,3)
edge/triangle chain maps and test whether the zero sheet is a boundary, a
cycle, or a genuine gauge choice in the local chain complex.
