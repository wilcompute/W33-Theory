# Part DCMXCIV (994) - Cyclotomic Tangent / Cumulant Constant at \(t=1\)

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED TANGENT THEOREM

---

## Why this part exists

The completed split-prime product

\[
\mathcal C_X(t)=G_X(t)M_X^{-2(1-t)}
\]

is the genuine global object underneath the packet. The natural next question is
its tangent at the special point \(t=1\), where all raw local factors become 1.

---

## The theorem

For each split prime \(p\equiv1\pmod3\), the completed local factor has
log-derivative at \(t=1\)

\[
\boxed{
\kappa_p
=\left.\frac{d}{dt}\log\Bigl[\left(\frac{p-2+t}{p-t}\right)(1-1/p)^{-2(1-t)}\Bigr]\right|_{t=1}
=\frac{2}{p-1}+2\log\left(1-\frac1p\right).
}
\]

Therefore the finite-cutoff completed tangent constant is

\[
\boxed{
\kappa_X=\sum_{\substack{p\le X\\ p\equiv1\ (3)}}\left(\frac{2}{p-1}+2\log\left(1-\frac1p\right)\right).
}
\]

Because each summand is \(O(1/p^2)\), the infinite tangent constant converges.

---

## Numerical profile

At the largest verified cutoff \(X=10^6\), the packet mean and Mertens term are

\[
\mathbb E[T_X]\approx 1.9868643295,
\qquad
2\log M_X \approx -1.9480390089,
\]

so the completed first cumulant has already stabilized near

\[
\boxed{\kappa_{\mathrm{cycl}}\approx 0.03882532065.}
\]

This is the exact tangent constant left over after removing the whole split-prime
logarithmic singularity.

---

## Relation to the old packet mean

Since

\[
\frac{d}{dt}\log G_X(t)\Big|_{t=1}=\mathbb E[T_X],
\]

one gets the exact factorization

\[
\boxed{
\kappa_X = \mathbb E[T_X] + 2\log M_X.
}
\]

So the divergent \(\log\log X\) packet mean becomes a convergent first cumulant
once the residue-class Mertens kernel is removed.

---

## What is now exact

1. the completed split-prime product is analytic at \(t=1\);
2. its exact first derivative/cumulant constant is the convergent split-prime sum above;
3. the global packet mean is precisely the singular part of the tangent;
4. the first cumulant of the completed object is finite and intrinsic.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_tangent_theory.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_tangent_theory.json`
- Result: `PART_DCMXCIV_cyclotomic_tangent_cumulant_constant_results.json`
