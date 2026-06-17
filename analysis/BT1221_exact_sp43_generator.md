# BT1221 -- Exact Sp(4,3) Generator

## Purpose

BT1219 made the single-qutrit target exact by enumerating \(SL(2,3)\). BT1221 does the same for the two-qutrit Clifford target by generating \(Sp(4,3)\) over \(\mathbb F_3\).

## Construction

Use the standard symplectic form

\[
J=\begin{pmatrix}0&I\\-I&0\end{pmatrix}
\]

on the basis \(e_1,e_2,f_1,f_2\). For each nonzero vector \(v\in\mathbb F_3^4\), form the symplectic transvection

\[
T_v = I + v(Jv)^T.
\]

The unique transvection matrices generated this way form a 40-generator set. Breadth-first closure gives the full group.

## Result

The exact generated group has

\[
|Sp(4,3)|=51840.
\]

Every generated matrix preserves the symplectic form. The element-order spectrum is

\[
\{1^1,2^{91},3^{800},4^{1620},5^{5184},6^{8000},8^{6480},9^{5760},10^{5184},12^{12960},18^{5760}\}.
\]

The trace distribution mod 3 is

\[
\operatorname{tr}\equiv0:18630,
\qquad
\operatorname{tr}\equiv1:16605,
\qquad
\operatorname{tr}\equiv2:16605.
\]

The fixed-space-rank fingerprint is

\[
0:1,\quad 1:80,\quad 2:2070,\quad 3:16560,\quad 4:33129.
\]

## Files

- Code: `analysis/bt1221_exact_sp43_generator.py`
- Result: `data/bt1221_exact_sp43_generator_summary.json`

## Why this matters

The full two-qutrit tomography target is now exact. BT1214 and BT1216 no longer rely on order metadata alone: the repo now has a generator, a closure certificate, and finite fingerprints for noisy recovery.
