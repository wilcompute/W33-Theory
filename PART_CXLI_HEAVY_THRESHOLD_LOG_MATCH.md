# Part CXLI — Heavy-Threshold Log Match for the W(3,3) RG Window

**Date:** 2026-05-01  
**Status:** heavy-threshold diagnostic / ppm-scale log-template match  
**Files:** `PART_CXLI_HEAVY_THRESHOLD_LOG_MATCH.py`, `PART_CXLI_heavy_threshold_log_match_results.json`, `tests/test_heavy_threshold_log_match_cxli.py`

---

## 1. Why CXLI matters

CXL showed that the two-loop inverse RG target

\[
k_{3,\mathrm{eff}}=1.849461957178364
\]

lies between the two structural W(3,3) rational candidates

\[
\frac{24}{13}<k_{3,\mathrm{eff}}<\frac{13}{7}.
\]

It also showed that pinning either rational requires only a sub-percent GUT threshold:

\[
\delta_{\rm GUT}(24/13)=-0.001788688,
\]

or

\[
\delta_{\rm GUT}(13/7)=+0.004153046.
\]

CXLI asks whether these small thresholds look like natural one-loop heavy-threshold logarithms built from W(3,3) invariants.

The threshold convention is

\[
\alpha_s(M_{\rm GUT})
=
\frac{\alpha_{\rm unified}}{k_{3,\rm bare}}(1+\delta_{\rm GUT}),
\]

with

\[
\delta_{\rm GUT}
=
\frac{\alpha_{\rm unified}}{2\pi}\tau.
\]

Thus \(\tau\) is the threshold measured in natural one-loop units.

---

## 2. Primitive square-root threshold matches

For the \(24/13\) branch:

\[
\tau_{\rm target}=-0.280966506\ldots
\]

while the primitive W(3,3) square-root log gives

\[
\log\sqrt{\frac{\mu}{\Phi_6}}
= -\frac12\log\frac{7}{4}
= -0.279807894\ldots
\]

This yields

\[
\delta_{\rm template}=-0.001781312,
\]

with residual

\[
\delta_{\rm target}-\delta_{\rm template}
=-7.38\times10^{-6}.
\]

The induced effective-\(k_3\) error is only

\[
-7.39\ \mathrm{ppm}.
\]

For the \(13/7\) branch:

\[
\tau_{\rm target}=+0.652358888\ldots
\]

while the primitive W(3,3) square-root log gives

\[
\log\sqrt{\frac{k-1}{q}}
=\frac12\log\frac{11}{3}
=0.649641492\ldots
\]

This yields

\[
\delta_{\rm template}=+0.004135746,
\]

with residual

\[
+1.73\times10^{-5},
\]

and effective-\(k_3\) error

\[
+17.23\ \mathrm{ppm}.
\]

That is a legitimate crack: the required thresholds are not random. They are almost exactly single square-root logarithms of W(3,3) atoms.

---

## 3. Scanner result

The half-log scanner searches templates of the form

\[
\frac12\log\frac{a}{b}
\]

where \(a,b\) are W(3,3) atoms:

\[
q,
\mu,
\Phi_6,
\Phi_4,
k-1,
k,
\Phi_3,
v-
\mu+1,
v,
E,
137.
\]

The best catalog matches are:

| branch | best scanner template | induced effective-\(k_3\) error |
|---|---:|---:|
| \(24/13\) | \(\log\sqrt{137/E}=\frac12\log(137/240)\) | −4.07 ppm |
| \(13/7\) | \(\log\sqrt{(v-\mu+1)/\Phi_4}=\frac12\log(37/10)\) | −11.46 ppm |

These are even closer numerically, but the primitive templates are cleaner conceptually:

\[
\sqrt{\frac{\mu}{\Phi_6}}
\qquad\text{and}\qquad
\sqrt{\frac{k-1}{q}}.
\]

The presence of \(137/E\) is still meaningful: it ties the Gaussian alpha integer to the 240-edge W(3,3) carrier, exactly the same carrier supporting the Hashimoto operator.

---

## 4. Interpretation

CXLI does not prove a heavy spectrum yet.  It narrows the search to a very specific form.

A one-loop heavy threshold usually has the schematic structure

\[
\delta_{\rm GUT}
\sim
\frac{\alpha}{2\pi}
\sum_i C_i\log\frac{M_i}{M_{\rm GUT}}.
\]

CXLI says a single quadratic-field mass ratio almost closes the problem:

\[
\frac{M_i}{M_{\rm GUT}}
\approx
\sqrt{\frac{\mu}{\Phi_6}}
\]

on the \(24/13\) branch, or

\[
\frac{M_i}{M_{\rm GUT}}
\approx
\sqrt{\frac{k-1}{q}}
\]

on the \(13/7\) branch.

This is exactly the kind of object expected from the CXXXVIII Hashimoto field split:

\[
\mathbb Q(\sqrt{-\Phi_4(3)})
\oplus
\mathbb Q(\sqrt{-\Phi_6(3)}).
\]

The threshold target is now small enough and structured enough that the next step should be to derive the heavy mass ratios from the field-labeled Hashimoto sectors rather than continue fitting RG numbers.

---

## 5. Regression status

Local validation of the CXLI test file:

```text
6 passed in 4.55s
```

The tests verify:

1. primitive templates pin \(k_3\) at ppm scale,
2. the threshold signs match the required branch signs,
3. the scanner finds \(137/E\) for the \(24/13\) branch,
4. the scanner finds \((v-\mu+1)/\Phi_4\) and \((k-1)/q\) for the \(13/7\) branch,
5. the audit emits both primitive and catalog templates,
6. the loop unit is the expected one-loop scale \(\alpha/(2\pi)\).

---

## 6. Next move

The next theorem to attempt is a **Hashimoto heavy-spectrum derivation**:

1. start with the two quadratic sectors
   \[
   x=1\pm i\sqrt{\Phi_4},
   \qquad
   x=-2\pm i\sqrt{\Phi_6},
   \]
2. define candidate heavy masses from their real/imaginary norms,
3. compute the threshold sum
   \[
   \sum_i C_i\log(M_i/M_{\rm GUT}),
   \]
4. test whether it selects either
   \[
   \log\sqrt{\mu/\Phi_6}
   \]
   or
   \[
   \log\sqrt{(k-1)/q}.
   \]

That would turn the current ppm-scale diagnostic into an actual derivation.
