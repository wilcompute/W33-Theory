# BT1684 — Projector-Hardware Falsifier Update

## Updated section

BT1684 updates

`paper/sections/sec_bt1672_projector_hardware_falsifier.tex`

with the BT1679--BT1682 QSVT compiler corrections and the BT1681 oriented bridge
twirl reconciliation.

## Inserted QSVT parity correction

The section now states that in the centered signal model

\[
x=2(L/\Lambda)-1,
\]

single-sequence QSVT polynomials obey

\[
p(-x)=(-1)^d p(x).
\]

Therefore endpoint selectors such as \(P_{c,6}\), \(P_{c,0}\), and
\(P_{m,30}\) cannot be single parity-constrained QSVT sequences.

## Inserted two-sequence compiler

For the clock endpoint selectors, the section now gives

\[
e_c(x)=\frac{9}{14}x^2-\frac17,
\qquad
 o_c(x)=\frac{9}{14}x^3-\frac17x,
\]

so

\[
P_{c,6}=e_c+o_c,
\qquad
P_{c,0}=e_c-o_c.
\]

For matter-30, it gives

\[
e_{30}(x)=\frac54x^2-\frac34,
\qquad
 o_{30}(x)=x/2,
\]

so

\[
P_{m,30}=e_{30}+o_{30}.
\]

## Inserted matter-24 certificate

The section now includes the exact BT1680 even quartic

\[
P_{m,24}(x)=-\frac{625}{256}x^4+\frac{225}{128}x^2+\frac{175}{256},
\]

with

\[
\|P_{m,24}\|_{\infty,[-1,1]}=1.
\]

The resulting two-port logical QSVT/LCU mass is

\[
\boxed{2.5439453125.}
\]

## Inserted oriented bridge twirl

The paper section now distinguishes support twirl from oriented subspace twirl.
The oriented result is

\[
\frac1{|G|}\sum_{g\in G}\rho(g)P_B\rho(g)^{-1}
=\frac{8}{81}P_{H_1},
\]

with Frobenius error

\[
1.0598553943057821\times10^{-14}.
\]

## Final falsifier update

The final falsifier statement now requires calibrated loss, sign flips,
block-encoding normalization, QSVT parity routing, and phase-precision budgets.

## Files

- `paper/sections/sec_bt1672_projector_hardware_falsifier.tex`
- `data/PART_BT1684_PROJECTOR_HARDWARE_FALSIFIER_UPDATE_results.json`
- `analysis/BT1684_projector_hardware_falsifier_update.md`
