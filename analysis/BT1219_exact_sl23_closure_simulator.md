# BT1219 -- Exact SL(2,3) Closure Simulator

## Purpose

BT1216 used synthetic finite-signature data for the single-qutrit tomography target. BT1219 replaces that single-qutrit metadata with an exact matrix computation.

We enumerate

\[
SL(2,3)=\{A\in M_2(\mathbb F_3):\det A=1\}.
\]

## Result

The exact enumeration gives

\[
|SL(2,3)|=24.
\]

Closure under multiplication holds, and the element-order spectrum is

\[
\{1^1,2^1,3^8,4^6,6^8\}.
\]

This exactly matches the BT1214 and BT1216 single-qutrit target.

## Additional invariant

The trace distribution modulo 3 is

\[
\operatorname{tr}\equiv 0:6,\qquad
\operatorname{tr}\equiv 1:9,\qquad
\operatorname{tr}\equiv 2:9.
\]

This gives a second finite fingerprint for noisy tomography.

## Files

- Code: `analysis/bt1219_exact_sl23_closure_simulator.py`
- Result: `data/bt1219_exact_sl23_closure_summary.json`

## Boundary

BT1219 verifies the exact single-qutrit group. It does not yet enumerate the full two-qutrit \(Sp(4,3)\) closure. That is now the next natural finite-group upgrade.
