# BT1667 — Calibrated Loss Sweep

## Purpose

BT1664 introduced named optical components but used one placeholder point. BT1667
turns that point into a component-range sweep.

This is still not measured lab data. It is a named-parameter sweep designed to be
replaced by calibrated component distributions.

## Grid

The sweep covers:

\[
\eta_{\rm switch}\in\{0.90,0.95,0.98,0.995\},
\]

\[
\eta_{\rm delay}\in\{0.90,0.95,0.99\},
\]

\[
\eta_{\rm detector}\in\{0.15,0.30,0.60,0.85\},
\]

\[
p_{\rm flip}\in\{0,0.10,0.20,0.35,0.45\},
\]

and

\[
\sigma_\phi\in\{0,0.10,0.25,0.50\}.
\]

The fixed terms are:

\[
\eta_{\rm phase}=0.999,
\qquad
\eta_{\rm analyzer}=0.98,
\qquad
p_{\rm dark/bin}=10^{-6},
\qquad
N=2048.
\]

## Result

The sweep has

\[
960
\]

cases. Of those,

\[
721
\]

pass the five-sigma rule and

\[
239
\]

fail.

Thus the pass rate is

\[
\boxed{0.751042.}
\]

The minimum and maximum observed separator SNR are

\[
1.165254\le S\le40.367122.
\]

## Design rule

The decisive variable is parity/sign-flip probability:

\[
\begin{array}{c|c|c}
p_{\rm flip} & \text{passes}/192 & \text{pass rate} \\
\hline
0.00 & 192/192 & 1.000000 \\
0.10 & 192/192 & 1.000000 \\
0.20 & 192/192 & 1.000000 \\
0.35 & 145/192 & 0.755208 \\
0.45 & 0/192 & 0.000000
\end{array}
\]

So the separator is robust under broad loss and detector ranges as long as the
sign/parity channel stays below roughly the high-20 to low-30 percent regime.

## Boundary

This sweep is not a lab calibration. It is a component-named pass/fail region.
Measured component values should be substituted before experimental claims.

## Files

- `analysis/bt1667_calibrated_loss_sweep.py`
- `data/PART_BT1667_CALIBRATED_LOSS_SWEEP_results.json`
