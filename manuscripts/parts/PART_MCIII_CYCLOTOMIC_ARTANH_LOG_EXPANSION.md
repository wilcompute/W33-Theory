# Part MCIII - Cyclotomic Global Artanh Log Expansion

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED CLOSED-FORM LOG PACKAGE

---

## Why this part exists

The odd/even collapse of Part MCI was derived derivative-by-derivative. The next
upgrade is to package the whole completed defect product into a single exact
closed-form logarithm.

---

## The theorem

For each split prime \(p\equiv1\pmod3\), set \(z=p^{-s}\) and
\(u=z-1\). Then the completed local factor satisfies
\[
\widehat D_p(z)=\left(\frac{p-2+z}{p-z}\right)\left(1-\frac1p\right)^{-2(1-z)}.
\]
Its logarithm has the exact artanh form
\[
\boxed{
\log \widehat D_p(z)
=

2\operatorname{artanh}\!\left(\frac{z-1}{p-1}\right)
+2(z-1)\log\left(1-\frac1p\right).
}
\]
Hence for the finite-cutoff completed Dirichlet package,
\[
\boxed{
\log \widehat D_X(s)
=

2\sum_{\substack{p\le X\\ p\equiv1\ (3)}}
\left[
\operatorname{artanh}\!\left(\frac{p^{-s}-1}{p-1}\right)
+
(p^{-s}-1)\log\left(1-\frac1p\right)
\right].
}
\]

Since \(|p^{-s}-1|<2<p-1\) for every split prime \(p\ge7\) and every \(\Re(s)>0\),
this yields the absolutely convergent odd-power series
\[
\boxed{
\log \widehat D_X(s)
=

2\sum_{\substack{p\le X\\ p\equiv1\ (3)}}
\left[
\sum_{m\ge0}\frac{(p^{-s}-1)^{2m+1}}{(2m+1)(p-1)^{2m+1}}
+
(p^{-s}-1)\log\left(1-\frac1p\right)
\right].
}
\]

---

## Reading

This is the closed-form global object underneath the whole cumulant tower.
All even derivatives vanish because the artanh series is odd in the centered
spectral variable \(u_p=p^{-s}-1\).

So the completed package is no longer just a product with stable numerics. It now
has a canonical logarithm with a fully explicit odd-power expansion.

---

## Numerical profile

At the verified cutoff \(X=10^6\), the exact and truncated artanh logs agree to
very high precision on the tested real slices \(s=1/2,1,2\), with small errors
already after eight odd-power terms.

---

## What is now exact

1. the completed Dirichlet package has an explicit closed-form logarithm;
2. that logarithm is an artanh-type split-prime sum;
3. the entire odd cumulant tower is encoded in one global series rather than recovered term-by-term.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_artanh_log_expansion.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_artanh_log_expansion.json`
- Result: `PART_MCIII_cyclotomic_artanh_log_expansion_results.json`
