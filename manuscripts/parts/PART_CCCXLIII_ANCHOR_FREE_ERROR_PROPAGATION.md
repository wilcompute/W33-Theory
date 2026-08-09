# Part CCCXLIII — Anchor-Free Error Propagation Compiler

**Date:** 2026-05-05  
**Status:** first-order uncertainty propagation and residual-test layer for anchor-free response identities.

**Executable audit:** `exploration/PART_CCCXLIII_ANCHOR_FREE_ERROR_PROPAGATION.py`  
**Results:** `PART_CCCXLIII_anchor_free_error_propagation_results.json`  
**Regression tests:** `tests/test_anchor_free_error_propagation_cccxliii.py`

---

## 1. Starting point

CCCXLII gave the exact anchor-free response identity

\[
 m^2
=
(g/2)^2
=
-\log(H/2)/\tau
=
(\operatorname{arcosh}(T/2)/t)^2
=
s^2-2s/R
=
(2/\zeta_p)^{1/p}.
\]

CCCXLIII makes this usable under measurement uncertainty.

Each channel estimates the same squared scale \(X\).  The question becomes:

> Do the channel estimates agree within propagated uncertainty?

---

## 2. Channel estimators

Define the channel scale estimators:

\[
X_m=m^2,
\]

\[
X_g=(g/2)^2,
\]

\[
X_H=-\frac{\log(H/2)}{\tau},
\]

\[
X_T=\left(\frac{\operatorname{arcosh}(T/2)}{t}\right)^2,
\]

\[
X_R=s^2-\frac{2s}{R},
\]

\[
X_\zeta=\left(\frac{2}{\zeta_p}\right)^{1/p}.
\]

---

## 3. Sensitivity derivatives

For first-order uncertainty propagation:

\[
\sigma_X=\left|\frac{dX}{dy}\right|\sigma_y.
\]

The channel derivatives are:

\[
\boxed{
\frac{dX_m}{dm}=2m.
}
\]

\[
\boxed{
\frac{dX_g}{dg}=\frac{g}{2}.
}
\]

\[
\boxed{
\frac{dX_H}{dH}=-\frac{1}{\tau H}.
}
\]

\[
\boxed{
\frac{dX_T}{dT}=
\frac{\operatorname{arcosh}(T/2)}{t^2\sqrt{(T/2)^2-1}}.
}
\]

\[
\boxed{
\frac{dX_R}{dR}=\frac{2s}{R^2}.
}
\]

\[
\boxed{
\frac{dX_\zeta}{d\zeta_p}=-\frac{X_\zeta}{p\zeta_p}.
}
\]

---

## 4. Weighted consensus estimator

Each channel gives an estimate

\[
X_i
\]

with propagated uncertainty

\[
\sigma_i.
\]

Use weights

\[
w_i=\frac{1}{\sigma_i^2}.
\]

The weighted consensus scale is

\[
\boxed{
\bar X=\frac{\sum_i w_iX_i}{\sum_iw_i}.
}
\]

Its uncertainty is

\[
\boxed{
\sigma_{\bar X}=\sqrt{\frac{1}{\sum_iw_i}}.
}
\]

---

## 5. Residual z-scores

For each channel:

\[
r_i=X_i-\bar X.
\]

The channel residual z-score is

\[
\boxed{
z_i=\frac{X_i-\bar X}{\sigma_i}.
}
\]

A simple diagnostic is

\[
\boxed{
\max_i |z_i|\le3.
}
\]

The compiler also computes

\[
\chi^2=\sum_i z_i^2
\]

and reduced chi-square

\[
\chi^2_\nu=\frac{\chi^2}{N-1}.
\]

---

## 6. Synthetic validation

The executable compiler builds three packets:

1. **Clean packet:** all channels exactly consistent.
2. **Small noisy packet:** channels perturbed within uncertainty; it passes the 3-sigma channel test.
3. **Bad packet:** one channel is strongly perturbed; it fails the 3-sigma channel test.

It also verifies every analytic sensitivity derivative against a finite-difference estimate.

---

## 7. Architecture upgrade

CCCXLII gave exact identities.

CCCXLIII gives empirical diagnostics:

\[
\boxed{
\text{anchor-free identities}
\to
\text{uncertainty propagation}
\to
\text{weighted consensus}
\to
\text{residual z-score / chi-square test}.
}
\]

This is the first measurement-ready layer of the one-sector observable model.

---

## 8. Theorem statement

**Anchor-Free Error Propagation Theorem.**  
For the one-sector W33 response packet, every channel estimates the same squared scale \(X\). First-order uncertainty propagation gives

\[
\sigma_X=|dX/dy|\sigma_y
\]

for each channel. Therefore the channel estimates define a weighted consensus scale and residual z-score test. A response packet passes the one-sector model only if the channel estimates agree within propagated uncertainty.

---

## 9. Honest boundary

This is first-order Gaussian-style propagation. Real experimental use must replace synthetic uncertainties with actual measurement models, systematic errors, and correlations.

The next bridge is:

\[
\boxed{
\text{error propagation}
\to
\text{correlated covariance model}
\to
\text{real experimental fitting}.}
\]
