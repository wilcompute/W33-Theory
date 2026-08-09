# Part CCCXL — Anchor Prediction Table Compiler

**Date:** 2026-05-05  
**Status:** deterministic prediction-table layer conditional on one chosen calibration anchor.

**Executable audit:** `exploration/PART_CCCXL_ANCHOR_PREDICTION_TABLE.py`  
**Results:** `PART_CCCXL_anchor_prediction_table_results.json`  
**Regression tests:** `tests/test_anchor_prediction_table_cccxl.py`

---

## 1. Starting point

CCCXXXIX made the calibration layer falsifiable:

\[
\kappa_{\rm mass}
=
\kappa_{\rm heat}
=
\kappa_{\rm spinor}
=
\kappa_{\rm resolvent}
=
\kappa_{\rm zeta}.
\]

CCCXL turns this into prediction.

Once one valid anchor fixes \(\kappa\), every other response channel is determined.

---

## 2. Dimensionless kernel

The dimensionless mass shell remains

\[
M^2=\frac{5049}{4},
\qquad
M=\frac{\sqrt{5049}}{2}.
\]

The projective gap is

\[
\sqrt{5049}=2M.
\]

Thus

\[
\boxed{
\frac{\text{projective gap}}{M}=2.
}
\]

---

## 3. Prediction formulas

Once an anchor fixes \(\kappa\), the physical mass is

\[
\boxed{
M_{\rm phys}=\kappa M.
}
\]

The physical projective gap is

\[
\boxed{
\Delta_{\rm gap,phys}=2M_{\rm phys}.
}
\]

The heat trace is

\[
\boxed{
H(\tau)=2\exp(-\kappa^2M^2\tau).
}
\]

The spinor trace is

\[
\boxed{
T(t)=2\cosh(\kappa Mt).
}
\]

The resolvent trace is

\[
\boxed{
R(s)=\frac{2s}{s^2-\kappa^2M^2}.
}
\]

The zeta value is

\[
\boxed{
\zeta_{\rm phys}(p)=\kappa^{-2p}2(M^2)^{-p}.
}
\]

---

## 4. Anchor inversion

Any one of the channels can serve as an anchor.

### Mass anchor

\[
\kappa=\frac{M_{\rm phys}}{M}.
\]

### Heat anchor

\[
\kappa=\sqrt{\frac{-\log(H/2)}{M^2\tau}}.
\]

### Spinor-trace anchor

\[
\kappa=\frac{\operatorname{arcosh}(T/2)}{Mt}.
\]

### Resolvent anchor

\[
\kappa=\sqrt{\frac{s^2-2s/R}{M^2}}.
\]

### Zeta anchor

\[
\kappa=\left(\frac{\zeta_{\rm dimless}(p)}{\zeta_{\rm phys}(p)}\right)^{1/(2p)}.
\]

After inversion, every other channel becomes a prediction.

---

## 5. Round-trip consistency

The executable compiler builds prediction tables from five possible anchor choices:

- mass,
- heat trace,
- spinor trace,
- resolvent trace,
- zeta value.

For a self-consistent synthetic calibration, every anchor produces the same prediction table.

Thus:

\[
\boxed{
\text{anchor choice should not matter.}
}
\]

If different anchor choices produce different prediction tables, the one-sector interpretation fails.

---

## 6. Architecture upgrade

CCCXXXIX gave:

\[
\text{multi-anchor calibration consistency}.
\]

CCCXL gives:

\[
\boxed{
\text{one-anchor calibration}
\to
\text{full response-channel prediction table}.
}
\]

The architecture now has a direct empirical workflow:

\[
\boxed{
\text{choose anchor}
\to
\text{solve }\kappa
\to
\text{predict all other channels}
\to
\text{test consistency}.
}
\]

---

## 7. Theorem statement

**Anchor Prediction Table Theorem.**  
For the one-sector W33 unit map, any single valid anchor determines \(\kappa\). Once \(\kappa\) is fixed, the physical mass, projective gap, heat trace, spinor trace, resolvent trace, and zeta values are all fixed by closed formulas. Prediction tables generated from mass, heat, spinor-trace, resolvent, or zeta anchors must agree. Disagreement falsifies the one-sector physical interpretation.

---

## 8. Honest boundary

This compiler produces deterministic prediction tables conditional on a chosen anchor. It does not claim which physical observable should be used as the real anchor.

The next bridge is:

\[
\boxed{
\text{candidate real-world anchors}
\to
\text{prediction tables}
\to
\text{empirical comparison}.}
\]
