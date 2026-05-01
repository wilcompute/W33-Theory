# Part CXLIV — Two-Sector QCD Coupling Compiler

**Date:** 2026-05-01  
**Status:** deeper structural compiler theorem behind the Φ₆-polar RG branch  
**Files:** `PART_CXLIV_TWO_SECTOR_QCD_COUPLING_COMPILER.py`, `PART_CXLIV_two_sector_qcd_coupling_results.json`, `tests/test_two_sector_qcd_coupling_cxliv.py`

---

## 1. Why this matters

The Φ₆-polar RG branch solves the numerical QCD running problem:

\[
\alpha_s(M_Z)=0.11800503473579949,
\]

which is only

\[
0.0056\sigma
\]

from the PDG input \(0.1180\pm0.0009\).

But the deeper question is: **why does the formula have exactly that shape?**

CXLIV gives the structural answer:

> The selected QCD coupling is a two-sector Hashimoto object.

It is compiled from both nontrivial Bass fields:

\[
\mathbb Q(\sqrt{-10})
\quad\text{and}\quad
\mathbb Q(\sqrt{-7}).
\]

---

## 2. The positive sector supplies the bare carrier

The positive adjacency sector is

\[
\lambda=2,
\qquad
m_r=24,
\qquad
x=1\pm i\sqrt{\Phi_4}=1\pm i\sqrt{10}.
\]

This sector supplies the bare SU(3)\(_c\) embedding:

\[
k_{3,\rm bare}
=\frac{m_r}{\Phi_3}
=\frac{24}{13}.
\]

This explains why the bare factor is not arbitrary.  It is the positive-sector multiplicity divided by the \(\Phi_3\) generation/cyclotomic denominator.

---

## 3. The negative sector supplies the QCD-local threshold

The negative adjacency sector is

\[
\lambda=-4,
\qquad
m_s=15,
\qquad
x=-2\pm i\sqrt{\Phi_6}=-2\pm i\sqrt7.
\]

Here

\[
(-2)^2=4=\mu,
\]

and

\[
7=\Phi_6.
\]

So the QCD-local polar threshold is

\[
\tau
=
\log\frac{|\operatorname{Re}x|}{|\operatorname{Im}x|}
=
\log\sqrt{\frac{\mu}{\Phi_6}}.
\]

This is exactly the selected CXLIII branch.

---

## 4. Compiled coupling formula

The final compiled GUT-scale coupling is therefore

\[
\alpha_s(M_{\rm GUT})
=
\frac{\alpha_{\rm unified}}{m_r/\Phi_3}
\left(
1+rac{\alpha_{\rm unified}}{2\pi}
\log\sqrt{\frac{\mu}{\Phi_6}}
\right).
\]

With

\[
\alpha_{\rm unified}=\frac1{25},
\qquad
m_r=24,
\qquad
\Phi_3=13,
\qquad
\mu=4,
\qquad
\Phi_6=7,
\]

this gives

\[
k_{3,\rm bare}=1.8461538461538463,
\]

\[
\tau=-0.27980789396771133,
\]

\[
\delta_{\rm GUT}=-0.0017813123776437676,
\]

\[
k_{3,\rm eff}=1.849448291286928,
\]

and

\[
\alpha_s(M_{\rm GUT})=0.021628071565151053.
\]

Running this through the live two-loop RG pipeline gives

\[
\alpha_s(M_Z)=0.11800503473579949.
\]

---

## 5. Structural interpretation

The QCD coupling is not simply “the \(\Phi_6\) branch.”  More precisely:

| Hashimoto sector | field | role |
|---|---|---|
| \(r=2\), multiplicity 24 | \(\mathbb Q(\sqrt{-\Phi_4})=\mathbb Q(\sqrt{-10})\) | bare visible carrier \(24/13\) |
| \(s=-4\), multiplicity 15 | \(\mathbb Q(\sqrt{-\Phi_6})=\mathbb Q(\sqrt{-7})\) | QCD-local threshold \(\log\sqrt{\mu/\Phi_6}\) |

This matters because it reveals a hidden **two-field compiler**:

\[
\boxed{
\mathbb Q(\sqrt{-10})\ \text{sets the carrier,}
\qquad
\mathbb Q(\sqrt{-7})\ \text{sets the threshold.}
}
\]

That is deeper than fitting \(k_3\).  The color coupling is the interaction of the two nontrivial Hashimoto fields.

---

## 6. Regression status

Local validation of the CXLIV test file:

```text
7 passed in 0.08s
```

The tests verify:

1. the positive sector supplies \(24/13\),
2. the negative sector supplies \(\log\sqrt{\mu/\Phi_6}\),
3. the threshold is a negative sub-percent one-loop correction,
4. the compiled effective \(k_3\) matches the selected pipeline value,
5. the compiled \(\alpha_s(M_{\rm GUT})\) matches the selected pipeline value,
6. the two roles correspond to distinct Hashimoto fields,
7. the full audit recovers \(\alpha_s(M_Z)\) to less than \(0.01\sigma\).

---

## 7. Next move

The deeper program should now search for the same two-sector compiler pattern in the other couplings:

- electroweak: identify which Hashimoto sector supplies the bare carrier and which supplies the threshold,
- Yukawa: test whether generation ratios are carrier/threshold decompositions across \(\mathbb Q(\sqrt{-10})\) and \(\mathbb Q(\sqrt{-7})\),
- neutrino: test whether the seesaw scale is a radial/q-clock branch rather than a \(\Phi_6\)-polar branch.

This is likely the real architecture: **observables are not attached to single invariants; they are compiled from paired sector roles.**
