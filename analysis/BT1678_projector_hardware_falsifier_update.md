# BT1678 — Projector-Hardware Falsifier Update

## Updated section

BT1678 updates

`paper/sections/sec_bt1672_projector_hardware_falsifier.tex`

so the paper section now includes the correction layer from BT1673--BT1677.

## Corrections inserted

### 1. Block-encoding normalization

The section now states that block-encoded hardware supplies

\[
H=L/\Lambda,
\]

so

\[
\sum_i c_iL^i=\sum_i c_i\Lambda^iH^i.
\]

With

\[
\Lambda_c=6,
\qquad
\Lambda_m=30,
\]

the raw high-degree \((9,8)\) point has block-encoded LCU mass

\[
289713.4069956163,
\]

while the best tested monomial block-encoded point is

\[
(d_c,d_m)=(4,2),
\qquad
\|c\|_{1,\rm block}=334.6461794019932.
\]

### 2. Chebyshev/QSVT audit

The section now records the sampled bounded-Chebyshev candidate mass

\[
\|c\|_{1,\rm Cheb}=215.6020503790747.
\]

It explicitly marks this as an audit, not a completed parity-valid QSVT phase
sequence.

### 3. Phase-precision limits

For a \(10^{-2}\) projector-error budget, the section now compares:

\[
(4,2):\quad \sigma_{\phi,\max}=1.71079969939437\times10^{-3},
\]

versus

\[
(8,8):\quad 4.3872988575743546\times10^{-7},
\]

and

\[
(9,8):\quad 1.0112501159704773\times10^{-7}.
\]

### 4. Hodge bridge boundary

The section now includes the BT1675 result:

\[
\|P_{H_1}\mathbf1_E\|=2.3633435577592544\times10^{-14},
\]

and

\[
\frac{\mathbf1_E^TP_{H_1}\mathbf1_E}{\mathbf1_E^T\mathbf1_E}
=-6.817896941457846\times10^{-16}.
\]

Thus the full support twirl kills the homological bridge.

## Final falsifier statement

The final falsifier now requires calibrated loss, sign-flip, block-encoding
normalization, and phase-precision budgets before claiming a pass or fail.

## Files

- `paper/sections/sec_bt1672_projector_hardware_falsifier.tex`
- `data/PART_BT1678_PROJECTOR_HARDWARE_FALSIFIER_UPDATE_results.json`
- `analysis/BT1678_projector_hardware_falsifier_update.md`
