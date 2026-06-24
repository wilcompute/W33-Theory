# BT1735-BT1737 execution summary

Executed all three requested next moves.

## BT1735: Hesse/Fano 8-cycle descent

Added `analysis/bt1735_hesse_fano_8cycle_descent.py`.

A single cocycle mutation improves the BT1732 witness:

```text
old 8-cycles: 54
new 8-cycles: 49
old 10-cycles: 75
new 10-cycles: 84
```

The witness remains connected, cubic, has the `63/63/189` profile, and has no 4-cycles or 6-cycles.  It still has girth 8, so this is a descent step rather than the final split-Cayley object.

## BT1736: self-frame puncture from 64/64/192 to 63/63/189

Added `analysis/bt1736_self_frame_puncture_64_to_63.py`.

This formalizes the user's idea that the object as a whole can become one point of itself.  In the framed 64-bit lift, one global self-frame consists of:

```text
one object-point
one object-line
three local R,C,S self-channel incidences
```

Removing that self-frame pair gives exactly:

```text
64/64/192 - one self frame with 3 channels = 63/63/189
```

Boundary: this explains the arithmetic carrier relation between the 64-bit tomotope lift and the 63 split-Cayley count profile.  It does not prove that the punctured carrier has split-Cayley incidence.

## BT1737: docs/index master atlas promotion

Added `docs/BT1737_master_16_cell_atlas.html` and updated `docs/index.html`.

The atlas page places the 16-cell carrier into docs with columns for:

```text
knight order
cell coordinate
Gray bits
Clifford grade
q2025 slot
genus axes
Latin symbol
magic-square label
Hesse/exceptional block
```

It also records the active count laws:

```text
Clifford grades: 1,4,6,4,1
Hesse/exceptional: 9+7=16
Genus incidences: 16*3=48
Q4 bit slots: 16*4=64
Tomotope flag lift: 64*3=192
Self-frame puncture: 64/64/192 - 1 self frame with 3 channels = 63/63/189
```
