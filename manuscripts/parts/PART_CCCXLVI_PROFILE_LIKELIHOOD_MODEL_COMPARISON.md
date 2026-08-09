# Part CCCXLVI — Profile Likelihood / Model Comparison Compiler

**Date:** 2026-05-06  
**Status:** profile-likelihood and model-comparison layer for the one-sector response fit.

**Executable audit:** `exploration/PART_CCCXLVI_PROFILE_LIKELIHOOD_MODEL_COMPARISON.py`  
**Results:** `PART_CCCXLVI_profile_likelihood_model_comparison_results.json`  
**Regression tests:** `tests/test_profile_likelihood_model_comparison_cccxlvi.py`

---

## 1. Starting point

CCCXLV introduced nuisance/systematic-template fitting:

\[
X_i=X\cdot 1_i+\theta b_i+\epsilon_i.
\]

CCCXLVI turns this into a model-comparison engine.

---

## 2. Competing models

The compiler compares three models.

### M0 — common scale only

\[
\boxed{X_i=X+
oise_i.}
\]

### M1 — common scale plus nuisance template

\[
\boxed{X_i=X+	heta b_i+
oise_i.}
\]

### M2 — broken/free-channel model

\[
\boxed{X_i=\alpha_i+
oise_i.}
\]

M2 is the saturated alternative: every channel is allowed its own independent scale. It represents breakdown of the one-sector identity structure.

---

## 3. Profile GLS likelihood

For a Gaussian covariance model, the profiled negative log-likelihood is controlled by

\[
\chi^2=(X-A\hat\beta)^TC^{-1}(X-A\hat\beta).
\]

The GLS estimator is

\[
\boxed{
\hat\beta=(A^TC^{-1}A)^{-1}A^TC^{-1}X.
}
\]

---

## 4. Information criteria

The compiler reports:

\[
\boxed{\mathrm{AIC}=\chi^2+2k,}
\]

and

\[
\boxed{\mathrm{BIC}=\chi^2+k\log N.}
\]

where \(k\) is the number of fitted parameters and \(N\) is the number of response channels.

For nested models, it also reports

\[
\boxed{\Delta\chi^2=\chi^2_{\rm simpler}-\chi^2_{\rm richer}.}
\]

---

## 5. Synthetic validation

The compiler validates three cases.

### Clean packet

No systematic is present.

BIC prefers the common-scale model \(M0\), because the nuisance parameter is unnecessary.

### Coherent systematic packet

A coherent nuisance-template systematic is injected.

The nuisance model \(M1\) is selected and recovers

\[
\theta=0.02.
\]

### Bad/off-template packet

A residual is added outside the nuisance subspace.

The nuisance model fails, while the saturated/free-channel model is selected by AIC.

This means the model comparison distinguishes:

\[
\boxed{
\text{clean one-sector}
\quad vs\quad
\text{one-sector plus modeled systematic}
\quad vs\quad
\text{broken/free-channel behavior}.}
}
\]

---

## 6. Architecture upgrade

CCCXLV gave nuisance fitting.

CCCXLVI gives model comparison:

\[
\boxed{
\text{nuisance fit}
\to
\text{profile likelihood}
\to
\text{AIC/BIC/LR model comparison}.}
\]

---

## 7. Theorem statement

**Profile Likelihood / Model Comparison Theorem.**  
The one-sector W33 response model can be compared as nested Gaussian GLS models. A coherent modeled systematic should select the nuisance model over the no-nuisance model. Residuals outside the nuisance-template subspace should force rejection or selection of the broken/free-channel alternative.

---

## 8. Honest boundary

The likelihoods here use synthetic covariance and Gaussian residual assumptions. Real use requires experimentally justified covariance, priors, and nuisance templates.
