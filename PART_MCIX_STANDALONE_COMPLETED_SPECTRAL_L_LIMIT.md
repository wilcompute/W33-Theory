# Part MCIX: Standalone Infinite-Cutoff Completed Spectral $L$-Limit

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED STANDALONE GLOBAL ANALYTIC OBJECT / CERTIFIED TAIL BOUNDS

---

## Why this part exists

Part MCVII showed that the odd Taylor coefficients of the completed spectral family converge absolutely as the split-prime cutoff $X\to\infty$, and Part MCVIII identified the corresponding deformation cumulants and free-energy functional. The natural next step is to stop talking only about the Taylor coefficients and define the **global completed spectral $L$-object itself**.

---

## The theorem

Fix real $s>0$ and a compact deformation disk $|\lambda|\le \rho<6$. For each split prime $p\equiv1\pmod3$, write
\[
K_p(s)=(p^{-s}-1)\left[\frac{1}{p-1}+\log\!\left(1-\frac1p\right)\right],
\qquad
x_p(s)=\frac{p^{-s}-1}{p-1}.
\]
Then the completed local spectral log splits as
\[
\log \Lambda_p^{\mathrm{def}}(s;\lambda)
=
2\lambda K_p(s)
+
2\sum_{m\ge1}\frac{\lambda^{2m+1}x_p(s)^{2m+1}}{2m+1}.
\]
Because $K_p(s)=O(p^{-2})$ and $|x_p(s)|<1/(p-1)$ on the positive real $s$-axis, one has the compact-disk majorant
\[
\left|\log \Lambda_p^{\mathrm{def}}(s;\lambda)\right|
\le
2\rho\,|K_p(s)|
+
\frac{2}{3}\,\frac{(\rho/(p-1))^3}{1-(\rho/(p-1))^2}.
\]
Both split-prime sums are absolutely convergent. Therefore
\[
\boxed{
\log \Lambda_\infty^{\mathrm{def}}(s;\lambda)
=
\sum_{p\equiv1\ (3)}\log \Lambda_p^{\mathrm{def}}(s;\lambda)
}
\]
converges absolutely and uniformly on every compact disk $|\lambda|\le\rho<6$, and hence defines a genuine analytic function there. Exponentiating gives the standalone global Euler product
\[
\boxed{
\Lambda_\infty^{\mathrm{def}}(s;\lambda)
=
\prod_{p\equiv1\ (3)}\Lambda_p^{\mathrm{def}}(s;\lambda),
\qquad |\lambda|<6.
}
\]
Moreover the finite-cutoff approximants carry certified tail bounds:
\[
\left|\log \Lambda_\infty^{\mathrm{def}}(s;\lambda)-\log \Lambda_X^{\mathrm{def}}(s;\lambda)\right|
\le B_X(\rho),
\qquad
\left|\frac{\Lambda_\infty^{\mathrm{def}}(s;\lambda)}{\Lambda_X^{\mathrm{def}}(s;\lambda)}-1\right|
\le e^{B_X(\rho)}-1,
\]
with a simple explicit choice
\[
B_X(\rho)
=
\frac{2\rho}{X_*}
+
\frac{\rho^3}{3\bigl(1-(\rho/X_*)^2\bigr)X_*^2},
\qquad X_*=\max\{X,6\}.
\]
Finally, the finite-cutoff reciprocity law passes to the limit:
\[
\Lambda_\infty^{\mathrm{def}}(s;\lambda)\,\Lambda_\infty^{\mathrm{def}}(s;-\lambda)=1.
\]

---

## Reading

This is the first point where the completed spectral package becomes a **standalone analytic object** rather than only a family of improving truncations. The odd Taylor tower from MCVI and the free-energy package from MCVIII are now seen as shadows of one honest global function.

There are three sharp consequences:

1. the global completed spectral family exists as a true Euler product on $|\lambda|<6$;
2. the physical slice $\lambda=1$ comes with certified finite-cutoff error bars;
3. reciprocity survives at infinite cutoff, so the centered odd structure is not an artifact of truncation.

---

## Numerical profile

At the verified physical slice $(s,\lambda)=(1,1)$, the $X=10^6$ cutoff already has an extremely small certified tail bound, and the corresponding relative multiplicative error is comparably tiny. The same remains true on the broader deformed slices $\lambda=2$ and $\lambda=5$, although the error bars naturally widen as one approaches the radius-six boundary.

---

## What is now exact

1. the completed spectral family is a genuine infinite-cutoff analytic object;
2. the finite-cutoff packets come with explicit certified log/value error bounds;
3. the infinite-cutoff object inherits the reciprocity law
   $\Lambda_\infty^{\mathrm{def}}(s;\lambda)\Lambda_\infty^{\mathrm{def}}(s;-\lambda)=1$.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_spectral_global_limit_object.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_spectral_global_limit_object.json`
- Result: `PART_MCIX_completed_spectral_global_limit_object_results.json`
