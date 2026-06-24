# BT1690 — Projector-Hardware Falsifier Update

## Updated section

BT1690 updates

`paper/sections/sec_bt1672_projector_hardware_falsifier.tex`

with BT1685, BT1688, and BT1689.

## BT1685 term-level QSP schedules

The section now states that the Chebyshev term schedules are exact at the term
level:

\[
T_0:[],\quad T_1:[0],\quad T_2:[0,0],\quad T_3:[0,0,0],\quad T_4:[0,0,0,0].
\]

It explicitly does not claim collapsed single-sequence phase lists for the full
polynomials.

## BT1687 resource table v2

The section now includes:

\[
\|c_{\rm res}\|_1=1.2939453125,
\qquad
\|c_{\rm comp}\|_1=1.25,
\]

with max tensor depth

\[
7.
\]

The placeholder SNRs are

\[
37.034240801677326,
\qquad
37.33164132928002.
\]

## BT1689 ancilla success accounting

The section now includes separate-port success probabilities

\[
p_{\rm res}=0.597413338718975,
\qquad
p_{\rm comp}=0.64.
\]

The monolithic two-port success probability is

\[
0.1544685004281349.
\]

Thus separate-port postselection is the cleaner near-term run-card route.

## BT1688 exact character certificate

The section now removes the BT1683 irreducibility caveat.  The chain character is

\[
\chi_{H_1}(g)=f_E(g)-f_V(g)+1.
\]

Its value distribution over the \(25920\)-element projective symplectic action is

\[
-3^{(810)},\ -1^{(3240)},\ 0^{(16640)},\ 1^{(5184)},\ 9^{(45)},\ 81^{(1)}.
\]

The square sum is

\[
25920,
\]

so

\[
\langle\chi_{H_1},\chi_{H_1}\rangle=1.
\]

Therefore the Levi \(H_1\) character is irreducible over \(\mathbb C\), and the
oriented bridge twirl formula is no longer conditional in this generated-action
model.

## Final falsifier update

The final falsifier now includes calibrated loss, sign flips, block-encoding
normalization, QSVT parity routing, ancilla success accounting, and phase
precision.

## Files

- `paper/sections/sec_bt1672_projector_hardware_falsifier.tex`
- `data/PART_BT1690_PROJECTOR_HARDWARE_FALSIFIER_UPDATE_results.json`
- `analysis/BT1690_projector_hardware_falsifier_update.md`
