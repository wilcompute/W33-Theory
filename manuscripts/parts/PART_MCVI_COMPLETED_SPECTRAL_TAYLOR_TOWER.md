# Part MCVI: Completed Spectral Odd Taylor Tower and Radius-Six Analyticity

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED ODD TAYLOR TOWER / UNIFORM ANALYTICITY PACKAGE

---

## Why this part exists

Part MCV promoted the completed defect packet to a full spectral \(L\)-family in the deformation variable \(\lambda\). The next exact question is whether that family is merely formal, or whether it carries a genuine analytic domain with a closed Taylor tower.

---

## The theorem

For every split prime \(p\equiv1\pmod3\), define the centered spectral coordinate
\[
 x_p(s)=\frac{p^{-s}-1}{p-1}.
\]
Then the completed local spectral family is
\[
\Lambda_p^{\mathrm{def}}(s;\lambda)
=
\left(\frac{1+\lambda x_p(s)}{1-\lambda x_p(s)}\right)
\exp\!\left(2\lambda\,(p^{-s}-1)\log\!\left(1-\frac1p\right)\right).
\]
Its logarithm has the exact odd expansion
\[
\boxed{
\log \Lambda_X^{\mathrm{def}}(s;\lambda)
=
\sum_{m\ge0}\mathcal O_{2m+1}^{(X)}(s)\,\lambda^{2m+1},
}
\]
with
\[
\boxed{
\mathcal O_1^{(X)}(s)
=
2\sum_{\substack{p\le X\\ p\equiv1\ (3)}}
\left[
 x_p(s)+(p^{-s}-1)\log\!\left(1-\frac1p\right)
\right],
}
\]
and for \(m\ge1\),
\[
\boxed{
\mathcal O_{2m+1}^{(X)}(s)
=
\frac{2}{2m+1}
\sum_{\substack{p\le X\\ p\equiv1\ (3)}} x_p(s)^{2m+1}.
}
\]
So every even Taylor coefficient vanishes exactly.

---

## Radius-six analyticity

On the positive real \(s\)-axis one has \(0<p^{-s}<1\), hence
\[
|x_p(s)|=\frac{|p^{-s}-1|}{p-1}<\frac{1}{p-1}\le\frac16,
\]
because the smallest split prime is \(7\). Therefore the completed spectral family is uniformly analytic in \(\lambda\) on the disk
\[
\boxed{|\lambda|<6}
\]
for every finite cutoff \(X\), and the odd Taylor tower converges absolutely there.

The first split prime controls the sharp lower bound: as \(s\to\infty\), the local radius at \(p=7\) approaches exactly \(6\).

---

## Reading

This upgrades Part MCV in two ways:

1. the completed spectral package is not just odd under \(\lambda\mapsto-\lambda\); it has a fully explicit odd Taylor tower;
2. the tower converges on a uniform disk large enough to contain the physical slice \(\lambda=1\) with room to spare.

So the completed packet is now an honest analytic family, not merely a product with good numerics.

---

## What is now exact

1. every even \(\lambda\)-coefficient of the completed spectral log vanishes;
2. every odd \(\lambda\)-coefficient is an explicit split-prime sum;
3. the positive-real \(s\)-axis carries a uniform analyticity radius of at least \(6\);
4. the completed Dirichlet packet at \(\lambda=1\) sits inside a genuinely convergent odd Taylor tower.

---

## Numerical profile

At the verified slice \(s=1\) and cutoff \(X=10^5\), the first two global odd coefficients are already stable:
\[
\mathcal O_1^{(10^5)}(1)\approx -0.034499090239,
\qquad
\mathcal O_3^{(10^5)}(1)\approx -0.002400282230.
\]
The executable profile also confirms that the truncated odd Taylor tower converges rapidly to the exact completed spectral log on the tested real slices \(s=1/2,1,2\).

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_completed_defect_spectral_taylor_tower.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_completed_defect_spectral_taylor_tower.json`
- Result: `PART_MCVI_completed_defect_spectral_taylor_tower_results.json`
