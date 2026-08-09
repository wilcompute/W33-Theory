# Part CXLIII — Branch Selection: the Φ₆-Polar QCD Threshold

**Date:** 2026-05-01  
**Status:** branch-selection theorem for the RG threshold program  
**Files:** `PART_CXLIII_BRANCH_SELECTION_PHI6_POLAR.py`, `PART_CXLIII_branch_selection_phi6_polar_results.json`, `tests/test_branch_selection_phi6_polar_cxliii.py`

---

## 1. Problem

CXLII reduced the RG embedding correction to two ppm-close branches:

| branch | bare \(k_3\) | threshold | interpretation |
|---|---:|---|---|
| Φ₆-polar | \(24/13\) | \(\log\sqrt{\mu/\Phi_6}\) | local to \(-2\pm i\sqrt7\) |
| radial q-clock | \(13/7\) | \(\log\sqrt{(k-1)/q}\) | global Ihara/Ramanujan shell |

Both branches are numerically excellent.  The remaining question is which one should be used for the QCD/SU(3) threshold.

---

## 2. Selection principle

The correction being pinned is not an arbitrary universal correction.  It is the SU(3)\(_c\)/QCD threshold.

Therefore the selected branch should be localized in the same finite sector that carries the QCD beta atom

\[
\beta_0=\Phi_6(3)=7.
\]

From CXXXVIII/CXLII, the \(\Phi_6\) sector is precisely the negative Hashimoto field

\[
x=-2\pm i\sqrt{\Phi_6}=-2\pm i\sqrt7.
\]

Its polar ratio is

\[
\frac{|\operatorname{Re}x|}{|\operatorname{Im}x|}
=\sqrt{\frac{\mu}{\Phi_6}}.
\]

So the QCD-local branch is

\[
\boxed{
 k_{3,\rm bare}=\frac{24}{13},
 \qquad
 \tau_{\rm GUT}=\log\sqrt{\frac{\mu}{\Phi_6}}.
}
\]

---

## 3. Branch score audit

The audit scores each branch by color-locality criteria:

1. Does the branch live in the \(\Phi_6\) sector carrying \(\beta_0\)?
2. Does it explicitly use the \(\Phi_6\) field?
3. Does it use the color-specific polar real/imaginary ratio?
4. Does it merely use the global radial/q-clock ratio?

The result:

| branch | QCD locality | uses Φ₆ | polar ratio | global radial | score | decision |
|---|---:|---:|---:|---:|---:|---|
| \(24/13\) Φ₆-polar | 1 | 1 | 1 | 0 | 3 | selected |
| \(13/7\) radial q-clock | 0 | 0 | 0 | 1 | −1 | rejected for QCD threshold |

The \(13/7\) branch is not mathematically false.  It remains useful as a universal Ihara-clock threshold candidate.  It is simply not the correct color-local QCD threshold branch.

---

## 4. Selected effective model

The selected model is:

\[
k_{3,\rm bare}=\frac{24}{13},
\]

with

\[
\tau_{\rm GUT}
=\log\sqrt{\frac{\mu}{\Phi_6}}
=\log\frac{2}{\sqrt7}.
\]

This gives

\[
k_{3,\rm eff}^{\rm template}=1.849448291286928,
\]

compared to the inverse RG target

\[
k_{3,\rm eff}^{\rm RG}=1.849461957178364.
\]

The residual is

\[
-7.39\ \mathrm{ppm}.
\]

Thus the QCD-local model is already within ppm-scale precision before adding multi-heavy or higher-loop threshold refinements.

---

## 5. Theorem statement

**Sector-locality selects the Φ₆-polar branch.**  Since the QCD beta atom \(\beta_0=\Phi_6\) lives in the negative Hashimoto field \(x=-2\pm i\sqrt{\Phi_6}\), the corresponding color-local GUT threshold is the polar ratio of that field:

\[
\tau=\log\sqrt{\frac{\mu}{\Phi_6}}.
\]

Together with the finite bare embedding

\[
k_{3,\rm bare}=\frac{24}{13},
\]

this produces the observed RG embedding factor to ppm accuracy.

---

## 6. Regression status

Local validation of the CXLIII test file:

```text
6 passed in 4.61s
```

The tests verify:

1. the selected branch is the \(\Phi_6\)-polar branch,
2. the selected bare factor is \(24/13\),
3. the radial \(13/7\) branch is rejected only for QCD-locality,
4. the selected branch scores strictly above the radial branch,
5. the selected branch is ppm-close to the inverse RG target,
6. the audit records \(\beta_0=\Phi_6\) as the selection principle.

---

## 7. Next move

Now that the QCD-local branch is selected, the next step is to wire this into the RG pipeline as a named option:

\[
\texttt{model='W33-Phi6-polar'}
\]

with

\[
\alpha_s(M_{\rm GUT})
=
\frac{\alpha_{\rm unified}}{24/13}
\left(1+\frac{\alpha_{\rm unified}}{2\pi}\log\sqrt{\frac{\mu}{\Phi_6}}\right).
\]

Then the V42 mass pipeline can be rerun with the selected threshold instead of the provisional \(k_3=1\) baseline.
