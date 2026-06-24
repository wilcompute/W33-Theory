# BT1679 — Parity-Valid QSVT Phase Compiler Audit

## Purpose

BT1679 tests whether the BT1676 Chebyshev/QSVT projector candidates can be
implemented as single standard parity-constrained QSVT sequences.

Use the centered signal model

\[
x=2(L/\Lambda)-1.
\]

Standard single-sequence QSVT/QSP polynomials obey

\[
p(-x)=(-1)^d p(x).
\]

## Spectra

The clock spectrum becomes

\[
\{-1,-\sqrt2/3,\sqrt2/3,1\}.
\]

The matter spectrum becomes

\[
\{-1,3/5,1\}.
\]

## Obstruction

Endpoint selectors that distinguish \(-1\) from \(+1\) cannot be single parity
polynomials.

For example, \(P_{c,6}\) requires

\[
p(-1)=0,
\qquad
p(1)=1.
\]

Even parity would force

\[
p(-1)=p(1),
\]

and odd parity would force

\[
p(-1)=-p(1).
\]

Neither permits \(\{0,1\}\).  Therefore \(P_{c,6}\) is not a single-sequence
parity-valid QSVT polynomial in this centered model.

The same obstruction applies to:

\[
P_{c,0},
\qquad
P_{m,30}.
\]

## Positive case

The matter-24 projector has

\[
p(-1)=0,
\qquad
p(3/5)=1,
\qquad
p(1)=0.
\]

This is compatible with even parity and is certified by BT1680's even quartic.

## Required compiler route

The endpoint projectors require a two-sequence route:

\[
p(x)=p_{\rm even}(x)+p_{\rm odd}(x),
\]

implemented as an even/odd LCU or ancilla-selected QSVT construction.

For a target at \(x=1\), the endpoint pattern is

\[
p_{\rm even}(1)=1/2,
\qquad
p_{\rm odd}(1)=1/2,
\]

with

\[
p_{\rm even}(-1)=1/2,
\qquad
p_{\rm odd}(-1)=-1/2.
\]

## Conclusion

BT1679 does not emit a fake phase list.  It proves that no single
parity-constrained QSVT phase sequence exists for \(P_{c,6}\), \(P_{c,0}\), or
\(P_{m,30}\) under the centered signal model.  The correct route is a two-sequence
LCU/ancilla-selected compiler.

## Files

- `analysis/bt1679_parity_valid_qsvt_phase_compiler.py`
- `data/PART_BT1679_PARITY_VALID_QSVT_PHASE_COMPILER_results.json`
