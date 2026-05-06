# Part CCCXLV — Nuisance/Systematic Parameter Fit Compiler

**Date:** 2026-05-06  
**Status:** nuisance/systematic-template extension of the correlated covariance fit.

**Executable audit:** `exploration/PART_CCCXLV_NUISANCE_PARAMETER_FIT.py`  
**Results:** `PART_CCCXLV_nuisance_parameter_fit_results.json`  
**Regression tests:** `tests/test_nuisance_parameter_fit_cccxlv.py`

---

## 1. Starting point

CCCXLIV upgraded the anchor-free response fit to a full correlated covariance model:

\[
C_X=JC_yJ^T.
\]

It then fit a single common squared scale \(X\) using generalized least squares.

CCCXLV adds explicit nuisance/systematic parameters.

---

## 2. Nuisance-template model

Instead of modeling channel scale estimates as only

\[
X_i=X+\epsilon_i,
\]

we allow a known systematic template direction \(b_i\):

\[
\boxed{
X_i=X\cdot 1_i+\theta b_i+\epsilon_i.
}
\]

Here:

- \(X\) is the common physical squared scale,
- \(b_i\) is a known systematic template across channels,
- \(\theta\) is the nuisance amplitude,
- \(\epsilon_i\) is residual noise.

---

## 3. Design matrix

Define the design matrix

\[
\boxed{
A=[\mathbf 1,b].
}
\]

More generally, with multiple nuisance templates:

\[
A=[\mathbf 1,b_1,b_2,\dots].
\]

The parameter vector is

\[
\beta=(X,\theta)^T.
\]

---

## 4. Generalized least-squares estimator

With scale covariance matrix \(C\), the GLS estimator is

\[
\boxed{
\hat\beta=(A^TC^{-1}A)^{-1}A^TC^{-1}X.
}
\]

Its covariance is

\[
\boxed{
\operatorname{Cov}(\hat\beta)=(A^TC^{-1}A)^{-1}.
}
\]

---

## 5. Nuisance-aware chi-square

The fitted values are

\[
\hat X=A\hat\beta.
\]

Residuals are

\[
r=X-A\hat\beta.
\]

The nuisance-aware chi-square is

\[
\boxed{
\chi^2=r^TC^{-1}r.
}
\]

The degrees of freedom are

\[
\boxed{
\nu=N-\operatorname{rank}(A).
}
\]

---

## 6. Synthetic validation

The executable audit verifies three cases:

### Clean packet

No nuisance is present.  The fit recovers

\[
X=6872.25
\]

and

\[
\theta\approx0.
\]

### Coherent systematic packet

A known systematic template is injected with

\[
\theta=0.02.
\]

Without the nuisance parameter, the packet fails the reduced chi-square test.

With the nuisance parameter, the fit recovers

\[
\theta=0.02
\]

and passes.

### Bad packet

A residual is added outside the nuisance-template subspace.

Even with the nuisance parameter, the packet fails.

This proves that nuisance fitting does not merely hide any discrepancy.  It only absorbs discrepancies lying in the modeled systematic direction.

---

## 7. Architecture upgrade

CCCXLIV gave:

\[
\text{correlated covariance fit}.
\]

CCCXLV gives:

\[
\boxed{
\text{correlated covariance fit}
\to
\text{explicit nuisance/systematic templates}
\to
\text{nuisance-aware residual test}.
}
\]

---

## 8. Theorem statement

**Nuisance/Systematic Parameter Fit Theorem.**  
For a one-sector W33 response packet with known systematic templates, the common scale and nuisance amplitudes are estimated by generalized least squares with design matrix

\[
A=[\mathbf 1,b_1,b_2,\dots].
\]

A coherent systematic lying in the nuisance-template subspace is absorbed without falsifying the model. Residuals outside that subspace still produce a chi-square failure.

---

## 9. Honest boundary

The nuisance template in this audit is synthetic. Real empirical use must derive nuisance templates from actual detector, calibration, or modeling systematics.

The next bridge is:

\[
\boxed{
\text{nuisance templates}
\to
\text{profile likelihood}
\to
\text{model comparison / evidence}.}
\]
