# Part DCMXCV (995) - Cyclotomic Completed Defect Dirichlet Series

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED DIRICHLET PACKAGE

---

## Why this part exists

The finite-adelic PGF and the completed split-prime product still leave one
obvious global analytic object to build: the genuine defect Dirichlet series.

---

## The theorem

For \(\Re(s)>0\), define the raw local factor

\[
D_p(s)=\frac{p-2+p^{-s}}{p-p^{-s}}.
\]

The completed local factor is

\[
\widehat D_p(s)=D_p(s)\,(1-1/p)^{-2(1-p^{-s})}.
\]

Hence the finite-cutoff completed defect Dirichlet product is

\[
\boxed{
\widehat D_X(s)=\prod_{\substack{p\le X\\ p\equiv1\ (3)}}\frac{p-2+p^{-s}}{p-p^{-s}}(1-1/p)^{-2(1-p^{-s})}.
}
\]

For fixed \(\Re(s)>0\), each completed local factor is

\[
1+O_s\!\left(\frac{1}{p^{1+\Re(s)}}+\frac1{p^2}\right),
\]

so the infinite completed defect Dirichlet product converges absolutely.

---

## Logarithmic derivative

The completed logarithmic derivative is

\[
\frac{d}{ds}\log\widehat D_X(s)
=\sum_{p\le X,\ p\equiv1\ (3)}
-z_p\log p\left(\frac1{p-2+z_p}+\frac1{p-z_p}+2\log\left(1-\frac1p\right)\right),
\]

with \(z_p=p^{-s}\). So the analytic package now includes both the global
completed product and its convergent logarithmic derivative.

---

## Numerical profile

At the verified cutoff \(X=10^6\), the completed values are already stable:

\[
\widehat D(1/2)\approx 0.9731105378,
\qquad
\widehat D(1)\approx 0.9637482610,
\qquad
\widehat D(2)\approx 0.9590920627.
\]

The corresponding completed logarithmic derivatives are

\[
\widehat D'(1/2)/\widehat D(1/2)\approx -0.03065507113,
\]
\[
\widehat D'(1)/\widehat D(1)\approx -0.01123351130,
\qquad
\widehat D'(2)/\widehat D(2)\approx -0.001509506658.
\]

---

## What is now exact

1. the split-prime defect process has a genuine global Dirichlet/Euler product;
2. its logarithmic singularity is removed by the same Mertens renormalization as the PGF;
3. the completed Dirichlet product converges absolutely for \(\Re(s)>0\);
4. the completed logarithmic derivative converges simultaneously.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_completed_dirichlet_series.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_completed_dirichlet_series.json`
- Result: `PART_DCMXCV_cyclotomic_completed_defect_dirichlet_series_results.json`
