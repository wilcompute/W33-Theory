# Part DCMLXXXVII (987) - Cyclotomic Local Euler Factor

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED LOCAL GENERATING-FUNCTION THEOREM

---

## Why this part exists

Part DCMLXXXVI promoted the defect set to a full \(p\)-adic valuation tree.  But
once the local valuation law is exact, it should also have an exact generating
function.

It does.

For each split prime \(p\equiv1\pmod3\), the valuation random variable

\[
V_p(q)=v_p\bigl(\Phi_3(q)\bigr)
\]

has a closed probability generating function, a closed Euler factor, and a very
cheeky moment law:

\[
\mathbb E[V_p]=\operatorname{Var}(V_p)=\frac{2}{p-1}.
\]

---

## The theorem

For a split prime \(p\equiv1\pmod3\), let \(V_p=v_p(\Phi_3(q))\) (equivalently
\(v_p(\Phi_6(q))\); the law is the same). Then:

\[
\Pr(V_p=0)=1-\frac{2}{p},
\qquad
\Pr(V_p=n)=\frac{2(p-1)}{p^{n+1}}\quad(n\ge1).
\]

Therefore the probability generating function is

\[
\boxed{
G_p(t)=\mathbb E[t^{V_p}]=\frac{p-2+t}{p-t}.
}
\]

Substituting \(t=p^{-s}\) gives the local Euler factor

\[
\boxed{
E_p(s)=\mathbb E[p^{-sV_p}]=\frac{p-2+p^{-s}}{p-p^{-s}}.
}
\]

Differentiating the PGF at \(t=1\) yields

\[
\boxed{
\mathbb E[V_p]=\frac{2}{p-1},
\qquad
\operatorname{Var}(V_p)=\frac{2}{p-1}.
}
\]

So mean and variance coincide exactly.

---

## Proof sketch

From Part DCMLXXXVI,

\[
\Pr(V_p\ge n)=\frac{2}{p^n} \qquad (n\ge1),
\]

because there are exactly two defect classes modulo \(p^n\).

Hence

\[
\Pr(V_p=n)=\Pr(V_p\ge n)-\Pr(V_p\ge n+1)
=\frac{2}{p^n}-\frac{2}{p^{n+1}}
=\frac{2(p-1)}{p^{n+1}}.
\]

Summing the geometric series gives

\[
G_p(t)=1-\frac{2}{p}+\sum_{n\ge1}\frac{2(p-1)}{p^{n+1}}t^n
=\frac{p-2+t}{p-t}.
\]

The moment formulas follow by differentiation.

---

## The first split-prime moments

For the first split primes:

\[
p=7: \quad \mathbb E[V_7]=\frac{2}{6}=\frac13=\frac1q;
\]

\[
p=13: \quad \mathbb E[V_{13}]=\frac{2}{12}=\frac16=\frac1{q!};
\]

\[
p=19: \quad \mathbb E[V_{19}]=\frac{2}{18}=\frac19=\frac1{q^2}.
\]

So the first three local valuation means land exactly on the reciprocals of the
substrate quantities

\[
q,\qquad q!,\qquad q^2.
\]

That is an unexpectedly rigid arithmetic shadow of the local defect process.

---

## What is now exact

The promoted exact statements are:

1. the local valuation PGF is \((p-2+t)/(p-t)\);
2. the local Euler factor is \((p-2+p^{-s})/(p-p^{-s})\);
3. mean and variance coincide at \(2/(p-1)\);
4. the first split-prime means are \(1/q,1/q!,1/q^2\).

---

## Correct status

\[
\boxed{
\text{The cyclotomic defect tree now has an exact local generating function and Euler factor.}
}
\]

What remains open is the global perfect-power theorem, not the local valuation
law.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_local_euler_factor.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_local_euler_factor.json`
- Result: `PART_DCMLXXXVII_cyclotomic_local_euler_factor_results.json`
