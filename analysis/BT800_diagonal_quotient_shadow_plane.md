# BT800 - Diagonal Quotient and Shadow F4 Split

BT800 turns the abstract module repair into geometry.

## Base Quotient

The base skew-pair chart is a `Q3`.  It has four antipode pairs.  A Gray-code
labeling exists in which every antipode pair differs by:

```text
111
```

Therefore quotienting the cube by `<111>` gives four cosets.  Those four
cosets are exactly the four common transversals from BT798.

```text
C2^3/<111> = {four transversal lines}
```

## Shadow Split

The shadow endpoints on those transversals do not form another untwisted cube.
Instead:

```text
shadow collinearity     = K4,4
shadow noncollinearity  = K4 + K4
shadow pairs            = perfect matching across K4,4
```

So the added phase plane is a two-sheet shadow split, not a duplicate of the
base cube.

## Meaning

This is the concrete geometric version of:

```text
C2^3 = 1 + 2
C2^4 = 2 + 2
```

The fixed diagonal bit is killed by quotienting the base cube by antipodes; the
replacement phase plane appears as a matched two-sheet shadow `F4` split on the
transversal tetrad.

## Validation

Run:

```bash
python3 analysis/bt800_diagonal_quotient_shadow_plane.py
```
