# BT1228 -- Compressed Sp43 Generator Certificate

## Purpose

BT1221 generated the two-qutrit Clifford target using all 40 unique transvections. BT1228 compresses that to a concrete four-transvection generating set.

## Generator vectors

The four vectors over F3 are

\[
(0,0,0,2),
\quad
(0,2,0,0),
\quad
(0,0,2,2),
\quad
(1,0,0,0).
\]

For each vector \(v\), the transvection is

\[
T_v=I+v(Jv)^T.
\]

## Result

The four generated transvections close to

\[
|Sp(4,3)|=51840.
\]

Thus the generator count is reduced from 40 to 4:

\[
40\to4.
\]

## Boundary

This is a compressed generator certificate, not a proof that four is absolutely minimal. The next mathematical step would be to test all one-, two-, and three-generator candidates or prove a lower bound.

## Files

- Code: `analysis/bt1228_sp43_compressed_generators.py`
- Result: `data/bt1228_sp43_compressed_generators_summary.json`
