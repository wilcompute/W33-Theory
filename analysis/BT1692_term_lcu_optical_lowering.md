# BT1692 — Term-LCU Optical Lowering

## Purpose

BT1692 lowers the parity-routed QSVT/LCU design into explicit term-level optical
operations.  The implementation remains logical: it names switch, delay, analyzer,
and detector stages, but it does not yet choose a foundry-specific component
library.

## Primitive lowering rule

Each Chebyshev term is implemented as a zero-phase signal-walk sequence:

\[
T_k \longmapsto k\text{ signal-walk delay passes}.
\]

Each weighted term product is lowered as:

1. route an LCU arm by switch network;
2. apply the clock rail term \(T_i\) using \(i\) clock signal-walk passes;
3. apply the matter rail term \(T_j\) using \(j\) matter signal-walk passes;
4. apply analyzer phase \(0\) for positive coefficient or \(\pi\) for negative
   coefficient;
5. combine into the resonance or companion detector port;
6. postselect the LCU success flag and record the timing separator phase.

## Resonance port

The resonance selector is

\[
P_{c,6}\otimes P_{m,24}.
\]

Clock terms:

\[
T_0\frac5{28},\quad T_2\frac9{28},\quad T_1\frac{19}{56},\quad T_3\frac9{56}.
\]

Matter terms:

\[
T_0\frac{1325}{2048},\quad T_2\left(-\frac{175}{512}\right),\quad
T_4\left(-\frac{625}{2048}\right).
\]

Thus the resonance port has

\[
4\times3=12
\]

term-product arms.  Its maximum tensor depth is

\[
3+4=7.
\]

The unrolled walk-pass count is

\[
42.
\]

## Companion port

The companion selector is

\[
P_{c,0}\otimes P_{m,30}.
\]

Clock terms:

\[
T_0\frac5{28},\quad T_2\frac9{28},\quad T_1\left(-\frac{19}{56}\right),\quad
T_3\left(-\frac9{56}\right).
\]

Matter terms:

\[
T_0\left(-\frac18\right),\quad T_2\frac58,\quad T_1\frac12.
\]

Thus the companion port has

\[
4\times3=12
\]

term-product arms.  Its maximum tensor depth is

\[
3+2=5.
\]

The unrolled walk-pass count is

\[
36.
\]

## Envelope

The maximum depth is

\[
7,
\]

inside the

\[
2048
\]

time-bin envelope, leaving depth margin

\[
2041.
\]

## Boundary

This is a logical optical lowering table.  It does not yet assign component-level
layout, calibrated loss, or foundry-specific switch/delay/analyzer choices.

## Files

- `analysis/bt1692_term_lcu_optical_lowering.py`
- `data/PART_BT1692_TERM_LCU_OPTICAL_LOWERING_results.json`
