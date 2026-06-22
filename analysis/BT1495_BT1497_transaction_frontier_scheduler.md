# BT1495--BT1497: transaction words, quotient frontier, and Steinberg scheduler lift

## Recent-commit reading

The post-BT1485 commits added the canonical Fano fiber and physical pulse compiler.  BT1492 fixes the shared 24-state fiber as the Fano point stabilizer with a native D4 flag stabilizer of order 8.  BT1493 lowers row actions to detector slots, mirror-slot residues, and Hesse lanes, producing 1728 row-pulse records with 576 native D4 square-pulse rows.  BT1494 restores the photonic-QEC release artifacts and validates the release lock.

## BT1495 -- 72-tick transaction words

BT1493 row pulses are now grouped into full transaction words.  There are 24 S4 action words.  Each word contains 72 ticks:

- 3 C3 channels;
- 4 Fano/V4 branches;
- 6 row-value slots.

Thus

24 words x 72 ticks = 1728 row ticks.

The native D4 subgroup contributes 8 words and 576 ticks.  The remaining 16 S4 actions contribute 1152 analyzer/ABI relabel ticks.  Each tick carries the path:

Fano branch -> detector slot -> mirror-slot residue -> Hesse feed-forward lane.

## BT1496 -- quotient/SAT frontier packet

The BT1373 witness has 210 identity edges and 330 corrections among 540 skew-line residuals.  BT1376 proves this witness is a radius-3 local optimum, but not a global optimum over the raw root-fixed space 6^39.

BT1496 starts the better attack: use the canonical Fano quotient

168 = 7*24 = 21*8, 24 = 3*8

to build point/flag/fiber quotient blocks and a WCNF scaffold.  This is not yet a global optimality proof; it is the certificate path that avoids raw gauge enumeration.

## BT1497 -- Steinberg scheduler D4 flag lift

The D4 flag stabilizer is lifted into the Steinberg scheduler by invariant profile data rather than chosen row coordinates:

- D4 order 8;
- D4 order profile 1:1, 2:5, 4:2;
- central scheduler C3 order 3;
- Steinberg scheduler carrier has 81 states;
- central C3 has 27 cycles of length 3;
- abstract lift C3 x D4 has order 24.

This is the basis-independent finite scheduler certificate.  Optical calibration of the individual D4 generators remains a hardware task.

## Current synthesis

Fano 168 -> shared fiber 24 -> native D4 8 now runs end-to-end through transaction words, quotient/SAT frontier scaffolding, and the Steinberg scheduler invariants.
