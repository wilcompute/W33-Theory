# Part CCCXLIV — Correlated Covariance Fit Compiler

**Date:** 2026-05-05  
**Status:** correlated covariance and generalized least-squares layer for anchor-free response fitting.

**Executable audit:** `exploration/PART_CCCXLIV_CORRELATED_COVARIANCE_FIT.py`  
**Results:** `PART_CCCXLIV_correlated_covariance_fit_results.json`  
**Regression tests:** `tests/test_correlated_covariance_fit_cccxliv.py`

---

## 1. Starting point

CCCXLIII upgraded the anchor-free identities to first-order independent uncertainty propagation.

It treated each channel as giving a squared-scale estimate

\[
X_i=f_i(y_i)
\]

with propagated uncertainty

\[
\sigma_{X_i}=\left|\frac{dX_i}{dy_i}\right|\sigma_{y_i}.
\]

CCCXLIV upgrades this to the realistic case where channels may have correlated errors.

---

## 2. Channel-value covariance

Let

\[
y=(m,g,H,T,R,\zeta)^T
\]

be the vector of measured channel values.

Let

\[
C_y
\]

be the full covariance matrix of the measured channel values.

This matrix may contain:

- independent statistical variances,
- channel-to-channel correlations,
- shared systematic components.

---

## 3. First-order covariance propagation

Each channel maps to a squared-scale estimate:

\[
X_i=f_i(y_i).
\]

The Jacobian is diagonal for the one-sector channel map:

\[
J_{ij}=\frac{\partial X_i}{\partial y_j}.
\]

At first order, the squared-scale covariance is

\[
\boxed{
C_X=JC_yJ^T.
}
\]

This is the correlated version of the independent propagation law from CCCXLIII.

---

## 4. Generalized least-squares scale estimate

All channels should estimate the same scale:

\[
X_i=X.
\]

Let

\[
\mathbf 1=(1,1,\dots,1)^T.
\]

The generalized least-squares estimator is

\[
\boxed{
\hat X=\frac{\mathbf 1^TC_X^{-1}X}{\mathbf 1^TC_X^{-1}\mathbf 1}.
}
\]

The estimator variance is

\[
\boxed{
\sigma_{\hat X}^2=\frac{1}{\mathbf 1^TC_X^{-1}\mathbf 1}.
}
\]

---

## 5. Correlated chi-square diagnostic

Residuals are

\[
r=X-\hat X\mathbf 1.
\]

The correlated chi-square is

\[
\boxed{
\chi^2=r^TC_X^{-1}r.
}
\]

Since one common scale is fit from \(N\) channels, the degrees of freedom are

\[
\boxed{
\nu=N-1.
}
\]

A simple diagnostic used by the compiler is

\[
\boxed{
\chi^2_\nu<3.
}
\]

where

\[
\chi^2_\nu=\frac{\chi^2}{\nu}.
\]

---

## 6. Synthetic validation

The compiler builds three packets:

1. **Clean packet:** all channels exactly agree and pass.
2. **Small noisy correlated packet:** small channel perturbations pass under the correlated covariance model.
3. **Bad packet:** a strongly perturbed channel fails the correlated chi-square test.

The compiler also verifies:

- covariance symmetry,
- scale covariance symmetry,
- inverse covariance correctness,
- positive quadratic form behavior,
- independent and correlated fits both recover the clean scale,
- correlated and independent fit uncertainties differ.

---

## 7. Architecture upgrade

CCCXLIII gave:

\[
\text{independent error propagation}.
\]

CCCXLIV gives:

\[
\boxed{
\text{correlated covariance propagation}
\to
\text{generalized least-squares consensus}
\to
\text{correlated chi-square test}.
}
\]

So the empirical layer is now covariance-ready.

---

## 8. Theorem statement

**Correlated Covariance Fit Theorem.**  
For a one-sector W33 response packet with correlated channel uncertainties, the measured channel covariance \(C_y\) propagates to squared-scale covariance

\[
C_X=JC_yJ^T.
\]

The common physical scale is optimally estimated by

\[
\hat X=\frac{\mathbf 1^TC_X^{-1}X}{\mathbf 1^TC_X^{-1}\mathbf 1},
\]

with variance

\[
\sigma_{\hat X}^2=\frac{1}{\mathbf 1^TC_X^{-1}\mathbf 1}.
\]

The one-sector model is tested by

\[
\chi^2=(X-\hat X\mathbf 1)^TC_X^{-1}(X-\hat X\mathbf 1)
\]

with \(N-1\) degrees of freedom.

---

## 9. Honest boundary

This is a covariance-ready fitting layer, but the covariance used in the executable audit is synthetic. Real empirical use requires experimentally justified covariance matrices, nuisance parameters, and systematic-error modeling.

The next bridge is:

\[
\boxed{
\text{correlated covariance fit}
\to
\text{nuisance/systematic parameter model}
\to
\text{real experimental likelihood}.}
\]
