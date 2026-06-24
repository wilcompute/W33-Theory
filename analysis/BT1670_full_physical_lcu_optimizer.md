# BT1670 — Full Physical LCU Optimizer

## Purpose

BT1669 found the algebraic high-degree LCU frontier. BT1670 adds a transparent
hardware proxy score so that smaller coefficient mass is not treated as the only
criterion.

## Score

The score is

\[
S_{\rm phys}
=
\frac{\|c\|_1}{\eta_{\rm walk}^{d}}
(1+\epsilon_{\rm cal}\kappa)
(1+w\log_{10}R),
\]

where:

- \(\eta_{\rm walk}=0.99201699\);
- \(d\) is max walk depth;
- \(\kappa\) is calibration sensitivity;
- \(R\) is coefficient dynamic range;
- \(\epsilon_{\rm cal}=10^{-6}\);
- \(w=10^{-3}\).

These are proxy penalties, not measured hardware constants.

## Result

The raw algebraic best remains

\[
(d_c,d_m)=(9,8),
\qquad
\|c\|_1=2.0822330410596202\times10^{-10}.
\]

But its calibration sensitivity is

\[
\kappa=98887.50411072331.
\]

The best proxy-physical point is instead

\[
\boxed{(d_c,d_m)=(8,8)}
\]

with

\[
\|c\|_1=2.1857339296641894\times10^{-10},
\]

\[
\kappa=22793.067727163656,
\]

and

\[
S_{\rm phys}=2.5483448393748145\times10^{-10}.
\]

## Interpretation

BT1669 was right algebraically: deeper projectors reduce coefficient mass. BT1670
adds the first physical correction: calibration sensitivity eventually dominates.
Within this tested range, the optimum backs off from \((9,8)\) to \((8,8)\).

## Boundary

This is not a measured hardware optimizer. The penalty constants should be
replaced by actual phase precision, component dynamic range, and block-encoding
calibration limits.

## Files

- `analysis/bt1670_lcu_physical_score.py`
- `data/PART_BT1670_FULL_PHYSICAL_LCU_OPTIMIZER_results.json`
