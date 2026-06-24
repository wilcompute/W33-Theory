# BT1680 — Analytic Sup-Norm Certificate

## Purpose

BT1676 used sampled bounded-Chebyshev checks.  The delicate case was
\(P_{m,24}\), whose sampled degree-5 candidate had

\[
\|p\|_\infty\approx1.000004174608004.
\]

BT1680 replaces that sampled near-pass with an exact analytic certificate.

## Certified polynomial

Use

\[
x=2(L_m/30)-1.
\]

The matter eigenvalues \(L_m\in\{0,24,30\}\) map to

\[
x\in\{-1,3/5,1\}.
\]

For the matter-24 projector, use the even quartic

\[
\boxed{
p(x)=-\frac{625}{256}x^4+\frac{225}{128}x^2+\frac{175}{256}.
}
\]

It satisfies

\[
p(-1)=0,
\qquad
p(3/5)=1,
\qquad
p(1)=0.
\]

## Sup-norm proof

The derivative factors as

\[
p'(x)=x\left(-\frac{625}{64}x^2+\frac{225}{64}\right).
\]

The only critical points in \([-1,1]\) are

\[
-3/5,
\qquad
0,
\qquad
3/5.
\]

The endpoint and critical values are

\[
p(-1)=p(1)=0,
\]

\[
p(-3/5)=p(3/5)=1,
\]

and

\[
p(0)=175/256.
\]

Therefore

\[
\boxed{\|p\|_{\infty,[-1,1]}=1.}
\]

## Chebyshev basis

In Chebyshev form,

\[
p(x)=\frac{1325}{2048}T_0(x)-\frac{175}{512}T_2(x)-\frac{625}{2048}T_4(x).
\]

The Chebyshev coefficient mass is

\[
1.2939453125.
\]

## Boundary

This certifies the scalar polynomial bound and QSVT parity for the matter-24
candidate. It does not yet synthesize the phase sequence.

## Files

- `analysis/bt1680_analytic_sup_norm_certificate.py`
- `data/PART_BT1680_ANALYTIC_SUP_NORM_CERTIFICATE_results.json`
