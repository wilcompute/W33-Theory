# Part CXLII — Hashimoto Heavy-Spectrum Threshold Derivation

**Date:** 2026-05-01  
**Status:** spectral derivation of the CXL/CXLI threshold templates  
**Files:** `PART_CXLII_HASHIMOTO_HEAVY_SPECTRUM_DERIVATION.py`, `PART_CXLII_hashimoto_heavy_spectrum_results.json`, `tests/test_hashimoto_heavy_spectrum_cxlii.py`

---

## 1. What CXLII proves

CXLI found that the GUT threshold logs needed to pin the RG embedding factor are almost exactly

\[
\log\sqrt{\frac{\mu}{\Phi_6}}
\]

on the \(24/13\) branch, and

\[
\log\sqrt{\frac{k-1}{q}}
\]

on the \(13/7\) branch.

CXLII explains where those square roots come from: they are not fitted logs. They are already encoded in the Hashimoto/Ihara spectrum of W(3,3).

From CXXXVIII, the two nontrivial Bass sectors are

\[
\lambda=2:
\qquad
x=1\pm i\sqrt{\Phi_4}=1\pm i\sqrt{10},
\]

and

\[
\lambda=-4:
\qquad
x=-2\pm i\sqrt{\Phi_6}=-2\pm i\sqrt7.
\]

Both have norm

\[
|x|^2=k-1=11.
\]

---

## 2. The \(24/13\) branch: the \(\Phi_6\)-sector polar ratio

In the negative adjacency sector,

\[
x=-2\pm i\sqrt7.
\]

The real-square is

\[
(-2)^2=4=\mu,
\]

and the imaginary-square is

\[
7=\Phi_6.
\]

Therefore the polar real/imaginary ratio is

\[
\frac{|\operatorname{Re}x|}{|\operatorname{Im}x|}
=
\frac{2}{\sqrt7}
=
\sqrt{\frac{\mu}{\Phi_6}}.
\]

Taking the one-loop threshold log gives

\[
\tau_{24/13}
=
\log\sqrt{\frac{\mu}{\Phi_6}}
=
-0.27980789396771133.
\]

Applied to the bare embedding

\[
k_{3,\rm bare}=\frac{24}{13},
\]

this gives

\[
k_{3,\rm eff}^{\rm template}=1.849448291286928,
\]

compared with the inverse RG target

\[
k_{3,\rm eff}^{\rm RG}=1.849461957178364.
\]

The error is only

\[
-7.39\ \mathrm{ppm}.
\]

---

## 3. The \(13/7\) branch: the Ramanujan radial/q-clock ratio

Every nontrivial Hashimoto root lies on the Ramanujan circle

\[
|x|=\sqrt{k-1}=\sqrt{11}.
\]

Comparing this shell radius to the internal q-clock

\[
\sqrt q=\sqrt3
\]

gives the radial ratio

\[
\frac{|x|}{\sqrt q}
=
\sqrt{\frac{k-1}{q}}.
\]

Thus

\[
\tau_{13/7}
=
\log\sqrt{\frac{k-1}{q}}
=
0.6496414920651304.
\]

Applied to the bare embedding

\[
k_{3,\rm bare}=\frac{13}{7},
\]

this gives

\[
k_{3,\rm eff}^{\rm template}=1.8494938201265572,
\]

with error

\[
+17.23\ \mathrm{ppm}.
\]

---

## 4. Interpretation

CXLII upgrades CXLI from a numerical threshold coincidence into a spectral derivation:

| branch | bare \(k_3\) | threshold source | template | ppm error |
|---|---:|---|---:|---:|
| polar \(\Phi_6\) branch | \(24/13\) | \(-2\pm i\sqrt7\) real/imaginary ratio | \(\log\sqrt{\mu/\Phi_6}\) | −7.39 ppm |
| radial q-clock branch | \(13/7\) | Ramanujan radius over q-clock | \(\log\sqrt{(k-1)/q}\) | +17.23 ppm |

This means the remaining issue is **branch selection**, not threshold discovery.

The two branches have different physical flavor:

- \(24/13\) uses the \(\Phi_6\)-sector itself, so it is the more QCD/confinement-natural branch.
- \(13/7\) uses the global Ramanujan shell radius against the q-clock, so it is the more universal/Ihara-clock branch.

Both are extremely close before including any multi-heavy correction.

---

## 5. Regression status

Local validation of the CXLII test file:

```text
6 passed in 4.45s
```

The tests verify:

1. the \(\Phi_6\) sector has real-square \(\mu=4\) and imaginary-square \(\Phi_6=7\),
2. the sector ratio is exactly \(\sqrt{\mu/\Phi_6}\),
3. every nontrivial sector has norm \(k-1=11\),
4. the radial/q-clock ratio is \(\sqrt{(k-1)/q}\),
5. the derived branches are ppm-close to the RG inverse target,
6. the audit emits the exact derivation identities.

---

## 6. Next move

The next theorem should decide the branch.

A natural criterion is: because QCD is the sector being corrected, and because \(\beta_0=\Phi_6\), the preferred heavy-threshold branch may be the \(\Phi_6\)-polar branch:

\[
k_{3,\rm bare}=\frac{24}{13},
\qquad
\tau=\log\sqrt{\frac{\mu}{\Phi_6}}.
\]

But the \(13/7\) branch has the elegance of the global Ramanujan/q-clock ratio:

\[
k_{3,\rm bare}=\frac{\Phi_3}{\Phi_6},
\qquad
\tau=\log\sqrt{\frac{k-1}{q}}.
\]

The next audit should test branch selection against the V42 Yukawa/mass pipeline and the Section 5 Langlands/Frobenius generation structure.
