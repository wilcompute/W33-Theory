# 2026-10-11 — Soft-supertrace essential hierarchy off the Witting vacuum

Producer: `analysis/w33_20261011_soft_supertrace_hierarchy.py`
Certificate: `data/w33_20261011_soft_supertrace_hierarchy.json`

## Result

Consider the dimensionless mixed spectral selector

\[
V_r=F+rG,\qquad
F=\sum_i e_i^2\log e_i,\qquad
G=\sum_i e_i\log e_i,
\]

on the normalized Vinberg Cartan.  \(F\) is the bosonic Coleman--Weinberg
shape of Pass 11884; \(G\) is the soft-mass shape isolated in Pass 11892.
The relative coefficient \(r\) is supplied here.  It is not yet a UV
prediction.

At a Witting ray choose the displayed stabilizer tangent.  The 24 massless
gauge modes split to leading order as

\[
0^4,\qquad (t^2/3)^{18},\qquad (t^2)^2 .
\]

Hence the sum of the opening coefficients is exactly eight in the numerical
certificate, and the two spectral functions have different nonanalyticities:

\[
F(t)-F(0)
 =\frac{\kappa_{\rm CW}}2\,t^2
 +4t^4\log(t^2)+O(t^4),
\]

\[
G(t)-G(0)
 =8t^2\log(t^2)+4t^2+o(t^2),
\]

with

\[
\kappa_{\rm CW}=7.21108\ldots .
\]
## A zero-threshold bifurcation

This sharpens the Witting-displacement firewall without violating it.
The \(G_{32}\)-invariant loop potential still has zero first projective
derivative at the Witting ray.  Indeed \(t^2\log t^2\) has derivative zero at
the origin.

Its second variation is singular.  For every \(r>0\),

\[
8r\,t^2\log(t^2)
\]

eventually dominates every finite positive \(t^2\) curvature as
\(t\rightarrow0\).  Therefore the Witting ray remains stationary but is no
longer a local minimum for any positive \(r\).  There is no finite spinodal
threshold.  The finite threshold inferred from a fixed-step numerical
Hessian is a regulator artefact.

Balancing the positive Coleman--Weinberg curvature against the logarithmic
soft term gives

\[
\boxed{
\log t_*=
-\frac{\kappa_{\rm CW}}{32r}
-\frac34+o(1)
}
\]

on the displayed tangent.  Direct minimization verifies the asymptotic law:

| \(r\) | direct \(\log t_*\) | asymptotic | error |
|---:|---:|---:|---:|
| 0.035 | -7.188362 | -7.188463 | \(1.0\times10^{-4}\) |
| 0.040 | -6.383198 | -6.383655 | \(4.6\times10^{-4}\) |
| 0.050 | -5.253940 | -5.256924 | \(3.0\times10^{-3}\) |
| 0.060 | -4.495951 | -4.505770 | \(9.8\times10^{-3}\) |

Thus an arbitrarily weak positive soft-supertrace admixture generates an
exponentially small projective displacement.
## Weld to the hierarchy law

Pass 11891 independently established

\[
\epsilon\propto\delta
\]

near the Witting cusp.  Identifying the projective displacement with the
small branch radius \(\delta\sim t_*\) gives the effective scaling

\[
\boxed{
\epsilon\ \propto\
\exp\!\left[-\frac{\kappa_{\rm CW}}{32r}\right]
}
\]

up to a non-universal prefactor.

This is an essential-scaling / dimensional-transmutation-like mechanism:
a modest dimensionless supertrace imbalance can generate a parametrically
small hierarchy without inserting that hierarchy as a small polynomial
coefficient.  The statement is about this declared effective potential,
not yet about the measured quark hierarchy.

## The angular direction is not forced to either W(3,3) endpoint

Pass 11925 identifies the local flavour-qutrit endpoints:

* the 12 collinear directions are stabilizer states, \(M_2=0\), and retain
  the charm--up lock;
* the 9 projected non-collinear directions are Strange/Hesse-SIC states,
  \(M_2=\log2\), and give the exact theta-zero spectrum \((1,1,0)\).

The logarithmic term has an angular finite coefficient \(C_G\).  At
\(t=2\times10^{-4}\) the certificate gives

\[
C_G({\rm Strange})=5.04650,\quad
C_G({\rm stabilizer})=4.00000,\quad
C_G(T)=3.74212.
\]

An explicit intermediate-magic direction gives

\[
C_G=3.70444,\qquad M_2=0.48015,
\]

and therefore beats all three named endpoint/resource directions
asymptotically.  In the common even-\(g\) Yukawa it has trivial projective
\(\Delta(54)\) residual symmetry and normalized singular values

\[
(1,\ 0.87638,\ 0.67737),
\]

so the protected degenerate pair is genuinely unlocked.
This is a witness, not a proof that the displayed direction is the global
minimum on \(\mathbb{CP}^2\).  Full six-real-dimensional branch optimization
independently finds an intermediate-magic angle near \(M_2\simeq0.4700\) at
small \(r\), consistent with the same conclusion.

## Physical boundary

The mechanism does **not** yet determine \(r\).  In exact \(N=1\) the
one-loop flat-direction potential cancels; Pass 11892 already established
that pure positive soft \(m^2G\) selects the \(C_{10}\) point globally, while
negative soft mass selects Witting.  The mixed \(F+rG\) selector studied
here describes a partially uncancelled bosonic contribution plus a soft
supertrace term.

A physical claim therefore still requires:

* the actual SUSY-breaking spectrum and the resulting coefficient \(r\);
* a complete gauge/Goldstone/ghost inventory;
* a renormalisation prescription and Nielsen-identity consistency;
* the compactification operator connecting the selected tangent direction
  to the observed Yukawa data.

Within that boundary, the new result is sharp: the loop spectrum itself
provides a zero-threshold, exponentially scaled escape from a Witting ray,
and the preferred angular sector can lie exactly in the intermediate-magic,
reflection-breaking region independently identified by the flavour no-gos.
