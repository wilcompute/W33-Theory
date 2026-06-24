# BT1682 — Two-Sequence Even/Odd QSVT Compiler

## Purpose

BT1679 proved that the clock endpoint selectors and the matter-30 endpoint
selector are not single parity-QSVT polynomials in the centered signal model

\[
x=2(L/\Lambda)-1.
\]

BT1682 gives explicit bounded even/odd decompositions for those endpoint
selectors.

## Clock endpoint selectors

The clock spectral points are

\[
\{-1,-\sqrt2/3,\sqrt2/3,1\}.
\]

Let

\[
a^2=2/9.
\]

Define the even component

\[
e_c(x)=\frac{9}{14}x^2-\frac17
=\frac{5}{28}T_0(x)+\frac{9}{28}T_2(x),
\]

and the odd component

\[
o_c(x)=\frac{9}{14}x^3-\frac17x
=\frac{19}{56}T_1(x)+\frac{9}{56}T_3(x).
\]

Both are bounded by

\[
\|e_c\|_\infty=\|o_c\|_\infty=1/2.
\]

Then

\[
P_{c,6}=e_c+o_c,
\]

and

\[
P_{c,0}=e_c-o_c.
\]

Each uses total two-sequence mass

\[
1/2+1/2=1.
\]

## Matter-30 endpoint selector

For matter,

\[
x\in\{-1,3/5,1\}.
\]

Use

\[
e_{30}(x)=\frac54x^2-\frac34
=-\frac18T_0(x)+\frac58T_2(x),
\]

and

\[
o_{30}(x)=x/2=\frac12T_1(x).
\]

Then

\[
P_{m,30}=e_{30}+o_{30},
\]

with values

\[
0,0,1
\]

at

\[
-1,3/5,1.
\]

The two-sequence mass is

\[
3/4+1/2=1.25.
\]

## Matter-24 single-sequence case

BT1680 gives the certified even quartic

\[
P_{m,24}(x)=-\frac{625}{256}x^4+\frac{225}{128}x^2+\frac{175}{256},
\]

with

\[
\|P_{m,24}\|_\infty=1,
\]

and Chebyshev mass

\[
1.2939453125.
\]

## Two-port logical LCU cost

Thus the resonance port has mass

\[
1\cdot1.2939453125=1.2939453125,
\]

and the companion port has mass

\[
1\cdot1.25=1.25.
\]

The combined two-port logical mass is

\[
\boxed{2.5439453125.}
\]

This is a large improvement over BT1676's sampled bounded-Chebyshev combined mass

\[
215.6020503790747.
\]

## Boundary

This gives exact bounded scalar polynomials and a two-sequence LCU routing rule.
It does not yet list hardware QSP phase angles for each bounded component.

## Files

- `analysis/bt1682_two_sequence_qsvt_compiler.py`
- `data/PART_BT1682_TWO_SEQUENCE_QSVT_COMPILER_results.json`
