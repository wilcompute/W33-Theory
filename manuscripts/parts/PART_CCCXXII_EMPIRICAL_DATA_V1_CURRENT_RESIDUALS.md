# Part CCCXXII — Empirical Data v1 / Current Residuals

**Date:** 2026-05-05  
**Status:** first current-source residual table for the W33 empirical program

---

## 1. Purpose

CCCXXI created the versioned target schema.

CCCXXII inserts the first current-source measured values and computes real residuals.

The data policy is strict: measured constants are external inputs, source-tagged, and versioned. They are not derived from W33.

---

## 2. External data used

The current-source values used are:

\[
m_e=0.51099895069\pm0.00000000016\ \mathrm{MeV},
\]

\[
m_\mu=105.6583755\pm0.0000023\ \mathrm{MeV},
\]

\[
m_\tau=1776.93\pm0.09\ \mathrm{MeV}.
\]

The weak-mixing reference value recorded is

\[
\sin^2\theta_{\mathrm{eff}}^{\mathrm{lept}}=0.23148\pm0.00012.
\]

Sources are recorded in `empirical_data_v1_current_residuals.json` as PDG/pdgLive entries accessed on 2026-05-05.

---

## 3. Koide residual

The charged-lepton Koide ratio is

\[
Q=
\frac{m_e+m_\mu+m_\tau}
{(\sqrt{m_e}+\sqrt{m_\mu}+\sqrt{m_\tau})^2}.
\]

Using the current masses above gives

\[
Q_{data}=0.6666644634026365.
\]

The W33 target is

\[
Q_{W33}=\frac23=0.6666666666666666\ldots
\]

Residual:

\[
Q_{data}-Q_{W33}
=
-2.2032640301\times10^{-6}.
\]

The propagated uncertainty is

\[
\sigma_Q\approx5.0809581952\times10^{-6}.
\]

So

\[
z\approx-0.4336315997.
\]

Therefore, under this mass scheme,

\[
\boxed{
Q=\frac23
\text{ is compatible with current charged-lepton masses at }<1\sigma.
}
\]

---

## 4. Weak mixing status

The W33 weak-mixing candidate is

\[
\sin^2\theta_W=\frac38.
\]

But this is a unification-boundary target.

The recorded measured value

\[
0.23148\pm0.00012
\]

is an effective leptonic weak angle at the Z pole.

A raw comparison gives a huge residual, but this is **not** a valid pass/fail test of the W33 target because no RG/unification map has been applied.

Therefore its status is:

\[
\boxed{
\text{RG required; not a direct Z-pole pass/fail test.}
}
\]

---

## 5. Result statuses

The residual table has two records:

1. `M1_KOIDE_CHARGED_LEPTON_PDGLIVE_2026`

\[
\text{PASS\_WITHIN\_1\_SIGMA\_UNDER\_THIS\_SCHEME}.
\]

2. `M1_SIN2_THETA_W_RAW_Z_POLE_NOT_RG_TEST`

\[
\text{RG\_REQUIRED\_NOT\_A\_DIRECT\_PASS\_FAIL\_TEST}.
\]

---

## 6. Theorem statement

**The first current-source empirical residual table confirms that the W33 Koide target**

\[
Q=\frac23
\]

**is compatible with current charged-lepton masses under the stated PDG/pdgLive mass scheme, with**

\[
z\approx-0.43.
\]

The weak-mixing target

\[
\frac38
\]

remains an RG-boundary claim, not a direct Z-pole prediction.

---

## 7. Honest boundary

Only Koide is evaluated here as a direct dimensionless comparison.

Weak mixing requires a specified RG/unification map before it can be used as pass/fail evidence for or against the W33 interpretation.

---

## 8. Regression status

The CCCXXII test file verifies:

1. Koide current residual,
2. weak mixing marked as RG-required,
3. residual record statuses,
4. audit-level consistency.

---

## 9. Final state of the empirical program

The repo now has:

\[
\text{exact finite theorem}
\to
\text{observable dictionary}
\to
\text{versioned targets}
\to
\text{current residual table}.
\]

The first direct physical residual is favorable:

\[
Q_{Koide}=\frac23
\quad
\text{within }1\sigma.
\]

The next unresolved empirical task is the RG map for

\[
\sin^2\theta_W=\frac38.
\]
