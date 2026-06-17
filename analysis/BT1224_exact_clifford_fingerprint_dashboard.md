# BT1224 -- Exact Clifford Fingerprint Dashboard

## Purpose

BT1219 gave the exact single-qutrit finite group. BT1221 gave the exact two-qutrit finite group. BT1224 fuses them into one tomography-facing dashboard.

## Single-qutrit layer

The single-qutrit target is

\[
SL(2,3),
\qquad |SL(2,3)|=24.
\]

The exact element-order spectrum is

\[
\{1^1,2^1,3^8,4^6,6^8\}.
\]

The trace fingerprint mod 3 is

\[
0:6,
\qquad
1:9,
\qquad
2:9.
\]

## Two-qutrit layer

The two-qutrit Clifford target is

\[
Sp(4,3),
\qquad |Sp(4,3)|=51840.
\]

The exact element-order spectrum and fixed-space-rank fingerprint are pulled from BT1221.

## Result

The dashboard passes. The finite Clifford tomography target is now exact at both layers:

\[
SL(2,3)
\longrightarrow
Sp(4,3).
\]

## Files

- Code: `analysis/bt1224_exact_clifford_fingerprint_dashboard.py`
- Result: `data/bt1224_exact_clifford_fingerprint_dashboard_summary.json`

## Boundary

This is a finite target dashboard, not measured hardware tomography. It specifies what real tomography must recover.
