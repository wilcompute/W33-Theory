# BT1674 — Phase-Precision Failure Surface

## Model

BT1674 turns the BT1670 calibration-sensitivity proxy into an explicit
phase-precision surface.  For a candidate projector with sensitivity \(\kappa\),
use the first-order bound

\[
\epsilon_{\rm proj}\le \kappa\sigma_\phi,
\]

where \(\sigma_\phi\) is RMS phase error.

## Candidates

The three compared candidates are:

\[
(4,2),\qquad(8,8),\qquad(9,8).
\]

The \((4,2)\) point is the BT1673 block-encoded optimum.  The \((8,8)\) point is
the BT1670 proxy physical optimum before block-encoding normalization.  The
\((9,8)\) point is the BT1669 raw algebraic optimum.

## Result

For an error budget

\[
\epsilon_{\rm proj}\le10^{-2},
\]

the maximum phase RMS values are:

\[
\begin{array}{c|c|c}
(d_c,d_m) & \kappa & \sigma_{\phi,\max} \\
\hline
(4,2) & 5.845219638242888 & 1.71079969939437\times10^{-3} \\
(8,8) & 22793.067727163656 & 4.3872988575743546\times10^{-7} \\
(9,8) & 98887.50411072331 & 1.0112501159704773\times10^{-7}
\end{array}
\]

Thus the block-encoded \((4,2)\) point is many orders of magnitude more
phase-tolerant than the high-degree points.

## Interpretation

The BT1673 normalization correction and BT1674 phase surface point to the same
hardware conclusion: the shallow normalized projector is the realistic target for
near-term optical compilation.

## Boundary

This is a first-order sensitivity bound.  A full optical simulation should sample
phase errors through the actual switch/delay/analyzer interferometer.

## Files

- `analysis/bt1674_phase_precision_failure_surface.py`
- `data/PART_BT1674_PHASE_PRECISION_FAILURE_SURFACE_results.json`
