# BT1663 — Timing-Noise Robustness Simulator

## Model

BT1663 gives a first analytic robustness model for the BT1660 timing separator.
The separator signal is the \(-1/+1\) phase split between the rank-120 resonance
block and the rank-24 companion block.

Use the contrast model

\[
C=\exp(-\sigma_\phi^2/2)(1-2p_{\rm flip})(1-b),
\]

where:

- \(\sigma_\phi\) is RMS phase jitter;
- \(p_{\rm flip}\) is separator sign/parity flip probability;
- \(b\) is background fraction.

Loss reduces the effective number of shots:

\[
N_{\rm eff}=N(1-\ell).
\]

The pass statistic is

\[
S=|C|\sqrt{N_{\rm eff}}.
\]

The default pass rule is

\[
\boxed{S\ge 5.}
\]

## Nominal case

For

\[
N=2048,
\qquad
\ell=0.1,
\qquad
\sigma_\phi=0.05,
\qquad
b=0.02,
\qquad
p_{\rm flip}=0.05,
\]

the simulator returns

\[
C=0.880898,
\qquad
S=37.800938.
\]

So the sign separator is safely above the five-sigma threshold in the nominal
analytic model.

## Threshold behavior

At fixed \(N=2048\), \(\sigma_\phi=0.05\), and \(b=0.02\), the maximum tolerated
parity-flip probability for a five-sigma separator is approximately:

\[
\begin{array}{c|c}
\ell & p_{\rm flip,max} \\
\hline
0.00 & 0.443559 \\
0.10 & 0.440506 \\
0.25 & 0.434828 \\
0.50 & 0.420181 \\
0.75 & 0.387119
\end{array}
\]

Uniform loss matters, but it is not the leading enemy. Sign/parity flips are the
direct contrast killer.

## Boundary

This is a first analytic model. The next layer should insert component-level
switch, delay, analyzer, and detector parameters from the BT1653 hardware
compiler and BT1651 guard-shell simulator.

## Files

- `analysis/bt1663_timing_noise_robustness.py`
- `data/PART_BT1663_TIMING_NOISE_ROBUSTNESS_results.json`
