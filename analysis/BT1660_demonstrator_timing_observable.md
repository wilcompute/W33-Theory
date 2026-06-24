# BT1660 — Demonstrator Timing Observable Contract

## Purpose

BT1658 split the degenerate coupled eigenvalue

\[
30
\]

into two natural projector blocks:

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

BT1660 turns that projector split into a time-bin observable.

## Stage 1: coupled 30-strobe

Use the coupled graph Hamiltonian

\[
L_{\rm coupled}=L_c\otimes I+I\otimes L_m.
\]

At

\[
\tau_{30}=\frac{2\pi}{30}=\frac{\pi}{15},
\]

any state supported in the coupled eigenvalue-30 sector returns with phase

\[
\exp(-i30\tau_{30})=1.
\]

This checks support in the full rank-144 coupled 30-sector.

## Stage 2: clock-sector separator

Use the partial clock operator

\[
K_c=L_c\otimes I.
\]

At

\[
\tau_c=\frac{\pi}{6},
\]

the resonance block has clock eigenvalue 6, hence

\[
\exp(-i6\tau_c)=\exp(-i\pi)=-1,
\]

while the companion block has clock eigenvalue 0, hence

\[
\exp(-i0\tau_c)=+1.
\]

So the timing separator is

\[
\boxed{
P_{c,6}\otimes P_{m,24}\mapsto -1,
\qquad
P_{c,0}\otimes P_{m,30}\mapsto +1.
}
\]

This is the hardware-readable version of the BT1658 projector split.

## Stage 3: matter-gap probe

Use the matter-side operator

\[
I\otimes L_m.
\]

At

\[
\tau_m=\frac{\pi}{24},
\]

the resonance block has matter eigenvalue 24 and phase

\[
\exp(-i24\tau_m)=-1.
\]

The companion block has matter eigenvalue 30 and phase

\[
\exp(-i30\tau_m)=\exp(-i5\pi/4).
\]

This distinguishes matter-gap support from matter-top support.

## Minimal protocol

1. Prepare support using the BT1658 polynomial projectors.
2. Run the coupled 30-strobe at \(\tau=\pi/15\) and measure return visibility.
3. Run the partial-clock separator at \(\tau=\pi/6\) and read the \(-1/+1\) split.
4. Run the matter-gap probe at \(\tau=\pi/24\) to cross-check the \(24\)-gap support.

## Boundary

This is a graph-spectral timing contract.  Optical loss, detector dark counts,
and calibration drift belong to the separate guard-shell hardware budget from the
BT1651--BT1653 hardware stack.

## Files

- `data/PART_BT1660_DEMONSTRATOR_TIMING_OBSERVABLE_results.json`
- `analysis/BT1660_demonstrator_timing_observable.md`
