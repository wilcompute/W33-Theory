# BT1237 -- Word-Metric Recovery Bands

## Purpose

BT1233 gave the exact word-metric fingerprint for the minimal four-transvection `Sp(4,3)` target. BT1237 turns that fingerprint into recovery bands for future synthetic or hardware tomography comparisons.

## Exact target

The target is

\[
|G|=51840,
\qquad
\operatorname{diam}=14.
\]

The sphere histogram is

\[
1,8,36,126,363,916,2052,4096,7396,12170,16916,7247,476,36,1.
\]

The checkpoint balls are

\[
|B_4|=534,
\quad
|B_8|=14994,
\quad
|B_{12}|=51803,
\quad
|B_{14}|=51840.
\]

## Bands

A `pass` recovery requires:

\[
\text{local order-three law},
\quad
|G|=51840,
\quad
\operatorname{diam}=14,
\]

plus

\[
\max_i\frac{|B_i^{obs}-B_i|}{B_i}\le 10^{-3},
\qquad
TV(S^{obs},S)\le 2.5\times10^{-3}.
\]

A `review` recovery allows relaxed distribution drift:

\[
\max_i\frac{|B_i^{obs}-B_i|}{B_i}\le 10^{-2},
\qquad
TV(S^{obs},S)\le 2\times10^{-2}.
\]

Everything else is `fail`.

## Boundary

These are finite-target recovery bands. They do not certify experimental hardware; they specify what future experimental or synthetic reconstructions must match before stronger claims are allowed.

## Files

- Code: `analysis/bt1237_word_metric_recovery_bands.py`
- Result: `data/bt1237_word_metric_recovery_bands_summary.json`
