# BT569 — The 244 Spectral Moment and the Cubic Leakage Resonance

## Statement

The cubic leakage ratio found in BT562,

\[
\frac{E_1+E_3}{E_2}=\frac{244}{121},
\]

is not a fitted numerical accident.  Its numerator is an intrinsic moment ratio
of the W33 strongly regular graph spectrum, and its denominator is the square of
the Ihara non-backtracking outdegree.

## W33 spectral moment identity

For the W33 collinearity graph, use the nontrivial strongly regular spectrum

\[
12^1+2^{24}+(-4)^{15}.
\]

The third and fifth weighted spectral moments are

\[
M_3=1\cdot12^3+24\cdot2^3+15\cdot(-4)^3,
\]

\[
M_5=1\cdot12^5+24\cdot2^5+15\cdot(-4)^5.
\]

A direct calculation gives

\[
M_3=960,
\qquad
M_5=234240.
\]

Therefore

\[
\boxed{\frac{M_5}{M_3}=244.}
\]

The same integer has the W33 substrate form

\[
\boxed{244=40\cdot7-4\cdot9=v\Phi_6-\chi q^2.}
\]

## Ihara normalization

The W33 non-backtracking outdegree is

\[
p_{\rm Ih}=11,
\]

so

\[
\boxed{p_{\rm Ih}^2=121.}
\]

Thus the BT562 cubic leakage resonance is exactly

\[
\boxed{
\frac{244}{121}
=
\frac{M_5/M_3}{p_{\rm Ih}^2}.
}
\]

Equivalently,

\[
\boxed{
\frac{244}{121}=2+\frac{2}{121}.
}
\]

## Interpretation

The cubic leakage from the protected Levi cycle-frame sector is governed by a
global W33 spectral moment ratio, normalized by the square of the Ihara
non-backtracking scale.  This connects three previously separate layers:

1. the cubic Gegenbauer leakage calculation,
2. the W33 SRG spectral moment stack,
3. the non-backtracking/Ihara scale.

So the ratio \(244/121\) should be treated as a structural resonance:

\[
\boxed{
\text{cubic leakage resonance}
=
\text{W33 spectral moment ratio}/\text{Ihara square}.
}
\]
