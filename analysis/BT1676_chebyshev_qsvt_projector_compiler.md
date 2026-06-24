# BT1676 — Chebyshev/QSVT Projector Compiler Audit

## Purpose

BT1673 showed that raw monomial high-degree projectors become expensive after
block-encoding normalization. BT1676 tests whether a normalized Chebyshev/QSVT
basis can recover part of the high-degree advantage.

## Normalized spectra

Use

\[
H_c=L_c/6,
\qquad
H_m=L_m/30.
\]

The sampled spectra are

\[
\sigma(H_c)=\{0,0.26429773960448416,0.7357022603955158,1\},
\]

and

\[
\sigma(H_m)=\{0,0.8,1\}.
\]

## Candidate compiler

The bounded Chebyshev candidates are:

\[
P_{c,6}: d=3,\quad \ell_1=11.285714285714281,
\]

\[
P_{c,0}: d=3,\quad \ell_1=22.571428571428555,
\]

\[
P_{m,24}: d=5,\quad \ell_1=1.1038714135380872,
\]

\[
P_{m,30}: d=2,\quad \ell_1=9.000000000000007.
\]

Thus

\[
\|P_{\rm res}\|_{1,\rm Cheb}=12.459193236217543,
\]

and

\[
\|P_{\rm comp}\|_{1,\rm Cheb}=203.14285714285715.
\]

The combined candidate mass is

\[
\boxed{215.6020503790747.}
\]

## Comparison

BT1673's best monomial block-encoded mass was

\[
334.6461794019932.
\]

So the Chebyshev candidate ratio is

\[
\boxed{0.6442851332723987.}
\]

## Boundary

This is not yet a finished QSVT phase sequence. It is a sampled
bounded-Chebyshev audit. A true QSVT compiler must enforce parity constraints and
prove \(\|p\|_\infty\le1\) analytically.

## Files

- `analysis/bt1676_chebyshev_qsvt_projector_compiler.py`
- `data/PART_BT1676_CHEBYSHEV_QSVT_PROJECTOR_COMPILER_results.json`
