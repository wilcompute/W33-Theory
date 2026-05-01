# Part CXL — RG Threshold Pinning of the W(3,3) k3 Rational Window

**Date:** 2026-05-01  
**Status:** inverse RG audit / threshold-naturalness theorem  
**Files:** `PART_CXL_RG_THRESHOLD_PINNING.py`, `PART_CXL_rg_threshold_pinning_results.json`, `tests/test_rg_threshold_pinning_cxl.py`

---

## 1. What CXL adds

CXXXIX inverted the corrected two-loop QCD RG map and found

\[
k_{3,\mathrm{eff}}=1.849461957178364
\]

for

\[
\alpha_{\rm unified}=\frac{1}{25},
\qquad
M_{\rm GUT}=\frac{13}{7}\cdot10^{16}\,\mathrm{GeV}.
\]

CXL asks the next sharper question:

> If W(3,3) wants a finite rational bare embedding factor such as \(24/13\) or \(13/7\), how large a GUT threshold correction is needed to pin that rational to the inverse target?

The threshold convention is

\[
\alpha_s(M_{\rm GUT})
=
\frac{\alpha_{\rm unified}}{k_{3,\rm bare}}(1+\delta_{\rm GUT}).
\]

Since

\[
\alpha_s(M_{\rm GUT})
=
\frac{\alpha_{\rm unified}}{k_{3,\rm eff}},
\]

we get the exact threshold formula

\[
\boxed{\delta_{\rm GUT}=\frac{k_{3,\rm bare}}{k_{3,\rm eff}}-1.}
\]

---

## 2. Main result

The inverse target lies between the two most structural W(3,3) rational candidates:

\[
\frac{24}{13}=1.846153846\ldots
<
1.849461957\ldots
<
\frac{13}{7}=1.857142857\ldots.
\]

Pinning either candidate requires only a sub-percent GUT threshold:

| bare candidate | without threshold | sigma | required \(\delta_{\rm GUT}\) | percent |
|---:|---:|---:|---:|---:|
| \(24/13=2k/\Phi_3\) | 0.119231857 | +1.37σ | −0.001788688 | −0.179% |
| \(37/20\) | 0.117802128 | −0.22σ | +0.000290919 | +0.029% |
| \(50/27\) | 0.117126298 | −0.97σ | +0.001291131 | +0.129% |
| \(13/7=\Phi_3/\Phi_6\) | 0.115238742 | −3.07σ | +0.004153046 | +0.415% |

So the two structural candidates straddle the inverse target, and the whole threshold span between them is only

\[
0.594\%.
\]

This is very small.  Expressed in natural one-loop units

\[
\frac{\alpha_{\rm unified}}{2\pi}
=
\frac{0.04}{2\pi},
\]

the thresholds are

\[
\delta(24/13)=-0.281\text{ loop-units},
\]

and

\[
\delta(13/7)=+0.652\text{ loop-units}.
\]

That is exactly the size one expects from a modest heavy-threshold packet, not a huge free correction.

---

## 3. Interpretation

CXL sharpens the RG problem into a finite-geometry problem:

> Do not fit \(k_3\) as an arbitrary real number.  Select a rational bare embedding from W(3,3), then derive the sub-percent GUT threshold from the heavy E8/Hashimoto sector.

The two rational candidates have different interpretations:

\[
\frac{24}{13}=\frac{2k}{\Phi_3}
\]

is built from the degree \(k=12\) and the same \(\Phi_3=13\) that appears in the two-loop QCD beta coefficient

\[
\beta_1=2\Phi_3.
\]

Meanwhile,

\[
\frac{13}{7}=\frac{\Phi_3}{\Phi_6}
\]

is the direct ratio of the Eisenstein/cyclotomic QCD beta sectors

\[
\beta_1/2=\Phi_3,
\qquad
\beta_0=\Phi_6.
\]

This makes the next derivation extremely concrete: determine whether the heavy-threshold sign comes from the \(\Phi_3\)-positive sector, the \(\Phi_6\)-negative sector, or the field-labeled Hashimoto split

\[
\mathbb Q(\sqrt{-\Phi_4(3)})
\oplus
\mathbb Q(\sqrt{-\Phi_6(3)}).
\]

---

## 4. Regression status

Local validation of the CXL test file:

```text
6 passed in 4.36s
```

The tests verify:

1. \(24/13\) needs a negative threshold and \(13/7\) needs a positive one.
2. \(k_{3,\rm eff}\) lies strictly between \(24/13\) and \(13/7\).
3. Both structural candidates need sub-percent thresholds.
4. \(37/20\) is a numerical near-hit needing only \(0.029\%\).
5. The structural thresholds are less than one natural loop unit.
6. The total threshold span is less than \(1\%\).

---

## 5. Next move

The next theorem to attempt is a **heavy-threshold sector derivation**:

\[
\delta_{\rm GUT}
\sim
\frac{\alpha_{\rm unified}}{2\pi}
\sum_i C_i\log\frac{M_i}{M_{\rm GUT}}.
\]

The CXL target tells us exactly what that sector must produce:

\[
-0.001788688
\quad\text{if }k_{3,\rm bare}=24/13,
\]

or

\[
+0.004153046
\quad\text{if }k_{3,\rm bare}=13/7.
\]

That is now a small, finite, testable target for the E8/W(3,3) heavy spectrum.
