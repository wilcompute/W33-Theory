# Part MCI - Cyclotomic Reciprocity / Hessian Theorem

**Date:** 2026-05-19  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED CENTERED-RECIPROCITY / ODD-CUMULANT THEOREM

---

## Why this part exists

The completed split-prime Euler product already had a finite tangent at
\(t=1\). The next exact question is whether that point carries genuine local
curvature, or whether the completed packet has a sharper hidden symmetry.

---

## The theorem

For a split prime \(p\equiv1\pmod3\), write the completed local factor as

\[
\mathcal C_p(t)=\left(\frac{p-2+t}{p-t}\right)\left(1-\frac1p\right)^{-2(1-t)}.
\]

Set \(t=1+u\). Then

\[
\boxed{
\mathcal C_p(1+u)\,\mathcal C_p(1-u)=1.
}
\]

Therefore

\[
\log \mathcal C_p(1+u)
=
\log\!\left(\frac{p-1+u}{p-1-u}\right)+2u\log\left(1-\frac1p\right)
\]

is an odd function of \(u\). Hence every even derivative of
\(\log\mathcal C_p\) at \(t=1\) vanishes exactly.

More precisely,

\[
\boxed{
\left.\frac{d^{2m}}{dt^{2m}}\log \mathcal C_p(t)\right|_{t=1}=0
\qquad (m\ge1),
}
\]

while the odd derivatives are

\[
\boxed{
\left.\frac{d}{dt}\log \mathcal C_p(t)\right|_{t=1}
=
\frac{2}{p-1}+2\log\left(1-\frac1p\right),
}
\]

and for \(m\ge1\),

\[
\boxed{
\left.\frac{d^{2m+1}}{dt^{2m+1}}\log \mathcal C_p(t)\right|_{t=1}
=
\frac{2(2m)!}{(p-1)^{2m+1}}.
}
\]

---

## Global consequence

For the finite-cutoff completed product

\[
\mathcal C_X(t)=\prod_{\substack{p\le X\\ p\equiv1\ (3)}}\mathcal C_p(t),
\]

the same reciprocity holds exactly:

\[
\boxed{
\mathcal C_X(1+u)\,\mathcal C_X(1-u)=1.
}
\]

So the completed packet is centered-self-reciprocal at \(t=1\), its Hessian is
exactly zero for every cutoff \(X\), and the whole completed cumulant tower is
odd.

In particular,

\[
\boxed{
\left.\frac{d^2}{dt^2}\log \mathcal C_X(t)\right|_{t=1}=0
}
\]

for every finite cutoff, and the higher odd completed cumulants are the exact
split-prime sums

\[
\boxed{
\left.\frac{d^{2m+1}}{dt^{2m+1}}\log \mathcal C_X(t)\right|_{t=1}
=
2(2m)!\sum_{\substack{p\le X\\ p\equiv1\ (3)}}\frac{1}{(p-1)^{2m+1}}
\qquad (m\ge1).
}
\]

---

## Numerical profile

At the verified cutoff \(X=10^6\), the first few completed cumulants are

\[
\kappa_1\approx 0.038825320649,
\qquad
\kappa_3\approx 0.021882373868,
\]
\[
\kappa_5\approx 0.006394439992,
\qquad
\kappa_7\approx 0.005186664291.
\]

And the reciprocity check is numerically exact at machine precision, e.g.
for \(u=0.2\):

\[
\mathcal C_7(1+u)\mathcal C_7(1-u)=1+O(10^{-16}),
\]

with the same behaviour visible globally across the verified cutoffs.

---

## What is now exact

1. the completed cyclotomic packet is centered-self-reciprocal at \(t=1\);
2. the completed Hessian vanishes exactly, locally and globally;
3. every even completed cumulant is identically zero;
4. the odd completed cumulants form an explicit convergent split-prime tower.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_reciprocity_hessian.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_reciprocity_hessian.json`
- Result: `PART_MCI_cyclotomic_reciprocity_hessian_theorem_results.json`