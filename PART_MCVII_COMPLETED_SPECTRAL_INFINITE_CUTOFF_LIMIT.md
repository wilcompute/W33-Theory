# Part MCVII: Infinite-Cutoff Completed Spectral Taylor Limit

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED ABSOLUTE-CONVERGENCE / LIMITING ANALYTIC OBJECT

---

## Why this part exists

Part MCVI established that every finite-cutoff completed spectral package carries an odd Taylor tower in the deformation variable \(\lambda\) and is uniformly analytic for \(|\lambda|<6\). The next exact question is whether this is only a finite-cutoff phenomenon, or whether the tower survives the limit \(X\to\infty\).

---

## The theorem

For real \(s>0\), the linear Taylor coefficient may be written as
\[
\mathcal O_1^{(X)}(s)
=
2\sum_{\substack{p\le X\\ p\equiv1\ (3)}}
(p^{-s}-1)
\left[
\frac{1}{p-1}+\log\!\left(1-\frac1p\right)
\right].
\]
The bracket is \(O(p^{-2})\), so this coefficient converges absolutely as \(X\to\infty\).

For every higher odd coefficient \(2m+1\ge3\),
\[
\mathcal O_{2m+1}^{(X)}(s)
=
\frac{2}{2m+1}
\sum_{\substack{p\le X\\ p\equiv1\ (3)}}x_p(s)^{2m+1},
\qquad
x_p(s)=\frac{p^{-s}-1}{p-1},
\]
and because \(|x_p(s)|<1/(p-1)\), one has the absolute majorant
\[
\left|\mathcal O_{2m+1}^{(X)}(s)\right|
\le
\frac{2}{2m+1}
\sum_{\substack{p\le X\\ p\equiv1\ (3)}}\frac{1}{(p-1)^{2m+1}},
\]
which is summable. Therefore every odd Taylor coefficient converges absolutely.

By the Weierstrass \(M\)-test, the completed spectral Taylor tower passes to a genuine limiting analytic object:
\[
\boxed{
\log \Lambda_\infty^{\mathrm{def}}(s;\lambda)
=
\sum_{m\ge0}\mathcal O_{2m+1}^{(\infty)}(s)\,\lambda^{2m+1},
\qquad |\lambda|<6.
}
\]

---

## Reading

This upgrades the completed defect packet from a family of finite-cutoff models to a true limiting analytic object. The package is no longer merely stable numerically: it exists as a convergent odd Taylor tower on a uniform disk large enough to contain the physical slice \(\lambda=1\).

---

## Numerical profile

At the verified slice \(s=1\), the order-1 coefficient is already very stable by the \(10^6\) cutoff, and the tail majorants shrink exactly as expected. The higher odd coefficients converge even faster.

---

## What is now exact

1. the odd Taylor coefficients converge absolutely as \(X\to\infty\);
2. the finite-cutoff completed spectral package lifts to a genuine limiting analytic object;
3. the limiting object keeps the same odd/even collapse and the same radius-six analyticity disk.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_spectral_infinite_cutoff_limit.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_spectral_infinite_cutoff_limit.json`
- Result: `PART_MCVII_completed_spectral_infinite_cutoff_limit_results.json`
