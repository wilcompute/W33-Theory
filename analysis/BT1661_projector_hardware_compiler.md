# BT1661 — Projector Hardware Compiler

## Goal

BT1658 produced exact spectral projectors. BT1661 lowers those projectors into a
walk-power / LCU schedule suitable for the 2048-bin time-bin hardware envelope.

## Clock projectors

For the Heawood flag-clock Laplacian \(L_c\),

\[
P_{c,6}=\frac{L_c((L_c-3I)^2-2I)}{42}
=\frac{1}{42}L_c^3-\frac{1}{7}L_c^2+\frac{1}{6}L_c.
\]

For the clock ground sector,

\[
P_{c,0}
=-\frac{(L_c-6I)((L_c-3I)^2-2I)}{42}
=I-\frac{43}{42}L_c+\frac{2}{7}L_c^2-\frac{1}{42}L_c^3.
\]

So the clock hardware block only needs walk powers

\[
\boxed{I,L_c,L_c^2,L_c^3.}
\]

## Matter projectors

For the matter graph Laplacian \(L_m\),

\[
P_{m,24}=\frac{L_m(L_m-30I)}{24(24-30)}
=\frac{5}{24}L_m-\frac{1}{144}L_m^2,
\]

and

\[
P_{m,30}=\frac{L_m(L_m-24I)}{30(30-24)}
=-\frac{2}{15}L_m+\frac{1}{180}L_m^2.
\]

So the matter hardware block only needs walk powers

\[
\boxed{L_m,L_m^2.}
\]

## Tensor selectors

The two BT1658 blocks compile to

\[
P_{\rm res}=P_{c,6}\otimes P_{m,24},
\qquad
\operatorname{rank}=120,
\]

and

\[
P_{\rm comp}=P_{c,0}\otimes P_{m,30},
\qquad
\operatorname{rank}=24.
\]

## Hardware lowering

The compiled schedule is:

1. allocate the 21-mode clock-flag rail inside the 2048-bin envelope;
2. allocate the 40-mode matter rail inside the 2048-bin envelope;
3. realize \(L_c,L_c^2,L_c^3\) by repeated graph-walk switch/delay passes;
4. realize \(L_m,L_m^2\) by repeated graph-walk switch/delay passes;
5. combine walk powers by LCU weights matching the rational coefficients;
6. send the resulting amplitudes to resonance and companion analyzer ports.

## Boundary

This is a graph-to-hardware compiler for the exact projectors. It does not yet
assign physical loss, phase drift, or detector-count budgets to each switch and
delay element.

## Files

- `analysis/bt1661_projector_hardware_compiler.py`
- `data/PART_BT1661_PROJECTOR_HARDWARE_COMPILER_results.json`
