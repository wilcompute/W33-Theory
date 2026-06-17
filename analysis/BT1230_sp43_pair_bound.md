# BT1230 -- Sp43 Pair-Bound Certificate

## Purpose

BT1228 compressed the two-qutrit finite Clifford target from all 40 projective transvections to a concrete four-transvection certificate. BT1230 closes the immediate lower-bound loophole: one or two projective transvections cannot generate the full target.

## Construction

Enumerate the 40 projective nonzero vectors of \(\mathbb F_3^4\), using the convention that the first nonzero coordinate is \(1\). For each vector \(v\), form

\[
T_v=I+v(Jv)^T,
\]

with the standard symplectic form \(J=\begin{pmatrix}0&I\\-I&0\end{pmatrix}\). Then compute closure orders for every one-element and two-element transvection set.

## Result

All one-transvection closures have order

\[
\boxed{3^{40}}.
\]

All two-transvection closures have order histogram

\[
\boxed{9^{240},\quad 24^{540}}.
\]

Therefore

\[
\max |\langle T_v,T_w\rangle|=24\ll |Sp(4,3)|=51840.
\]

So no one- or two-transvection set can generate \(Sp(4,3)\).

## Consequence

BT1228 gave

\[
\boxed{4\text{ transvections generate }Sp(4,3)}.
\]

BT1230 now proves

\[
\boxed{\text{at least }3\text{ transvections are required}.}
\]

The only remaining exact-minimality gap is the three-transvection case:

\[
\boxed{3\;?\;4}.
\]

## Boundary

This is not a proof that four is minimal. It is a rigorous executable lower-bound certificate ruling out one and two transvections.

## Files

- Code: `analysis/bt1230_sp43_pair_bound.py`
- Result: `data/bt1230_sp43_pair_bound_summary.json`
