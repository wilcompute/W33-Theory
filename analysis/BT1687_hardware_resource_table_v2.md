# BT1687 — Hardware Resource Table v2

## Purpose

BT1687 compiles the parity-routed QSVT/LCU design into an explicit resource table.

The architecture is:

\[
\text{LCU of Chebyshev-term QSP schedules.}
\]

## Component defaults

The placeholder component defaults are inherited from BT1664:

\[
\eta_{\rm walk}=0.99201699,
\qquad
\eta_{\rm analyzer}=0.98,
\qquad
\eta_{\rm detector}=0.85,
\]

with

\[
N=2048,
\qquad
\sigma_\phi=0.05,
\qquad
p_{\rm flip}=0.05,
\qquad
p_{\rm dark/bin}=10^{-6}.
\]

## Selector resources

\[
\begin{array}{c|c|c|c|c}
\text{selector} & \text{route} & \text{subseq.} & \text{terms} & \text{max depth} \\
\hline
P_{c,6} & e_c+o_c & 2 & 4 & 3 \\
P_{c,0} & e_c-o_c & 2 & 4 & 3 \\
P_{m,24} & p_{24} & 1 & 3 & 4 \\
P_{m,30} & e_{30}+o_{30} & 2 & 3 & 2
\end{array}
\]

Their logical LCU masses are:

\[
1,
\qquad
1,
\qquad
1.2939453125,
\qquad
1.25.
\]

## Two-port resources

For the resonance port,

\[
P_{c,6}\otimes P_{m,24},
\]

the resources are:

\[
\|c\|_1=1.2939453125,
\qquad
\text{subsequence products}=2,
\qquad
\text{term products}=12,
\qquad
\text{max depth}=7.
\]

The placeholder shot-noise SNR is

\[
37.034240801677326.
\]

For the companion port,

\[
P_{c,0}\otimes P_{m,30},
\]

the resources are:

\[
\|c\|_1=1.25,
\qquad
\text{subsequence products}=4,
\qquad
\text{term products}=12,
\qquad
\text{max depth}=5.
\]

The placeholder shot-noise SNR is

\[
37.33164132928002.
\]

Combined:

\[
\boxed{\|c\|_{1,\rm combined}=2.5439453125.}
\]

The max depth is

\[
7,
\]

leaving time-bin margin

\[
2041
\]

inside the 2048-bin envelope.

## Comparison

BT1661 had raw monomial depth 5 and raw mass

\[
19/48.
\]

BT1673 showed that block-encoded monomial normalization changes the best tested
mass to

\[
334.6461794019932.
\]

BT1687's parity-routed logical mass is

\[
2.5439453125.
\]

Thus the new route has slightly greater max depth than the raw monomial compiler,
but avoids the huge block-encoding normalization blowup.

## Boundary

The SNR estimates use placeholder component defaults and treat LCU
success/amplitude amplification separately from shot-noise port contrast.  Real
hardware needs calibrated component data and explicit ancilla success accounting.

## Files

- `analysis/bt1687_hardware_resource_table_v2.py`
- `data/PART_BT1687_HARDWARE_RESOURCE_TABLE_V2_results.json`
