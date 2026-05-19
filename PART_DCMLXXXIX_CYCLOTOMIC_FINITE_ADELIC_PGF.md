# Part DCMLXXXIX (989) - Cyclotomic Finite-Adelic PGF

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED FINITE PRODUCT / MOMENT THEOREM

---

## Why this part exists

Part DCMLXXXVII identified the exact local valuation PGF for each split prime.
Part DCMLXXXVIII showed that finite sets of split primes combine exactly by CRT.

Those two facts should fuse into an exact finite-adelic generating function for
the total valuation packet. They do.

---

## The theorem

Let \(S\) be a finite set of split primes \(p\equiv1\pmod3\), and define the
total valuation packet

\[
T_S(q)=\sum_{p\in S} v_p\bigl(\Phi_3(q)\bigr).
\]

Then the exact finite-adelic PGF is

\[
\boxed{
G_S(t)=\mathbb E[t^{T_S}] = \prod_{p\in S}\frac{p-2+t}{p-t}.
}
\]

Equivalently, the finite Euler factor is

\[
\boxed{
E_S(s)=\mathbb E\!\left[\prod_{p\in S}p^{-s v_p(\Phi_3(q))}\right] = \prod_{p\in S}\frac{p-2+p^{-s}}{p-p^{-s}},
}
\]

interpreted factorwise over the primes in \(S\).

Because the finite-adelic packet is an exact product of independent local
valuation laws,

\[
\boxed{
\mathbb E[T_S]=\operatorname{Var}(T_S)=\sum_{p\in S}\frac{2}{p-1}.
}
\]

---

## Proof sketch

Each local valuation law has PGF

\[
G_p(t)=\frac{p-2+t}{p-t}.
\]

Part DCMLXXXVIII gives exact finite CRT factorization, so the local packets are
independent over any finite split-prime set. Therefore the total PGF is the
product of the local PGFs, and the mean/variance add.

---

## First three split primes

For

\[
S=\{7,13,19\},
\]

the total mean is

\[
\mathbb E[T_S]
=\frac13+\frac16+\frac19
=\frac{11}{18}.
\]

So the first three local contributions land exactly on

\[
\frac1q,\qquad \frac1{q!},\qquad \frac1{q^2},
\]

and the first three-prime packet mean is

\[
\boxed{\frac{11}{18}.}
\]

This is the cleanest moment-level shadow yet of the substrate's early split
prime tower.

---

## What is now exact

The promoted exact statements are:

1. finite split-prime valuation packets have exact PGF product law;
2. their finite Euler factors are exact products of the local factors;
3. the total packet mean and variance coincide and add linearly;
4. the first three split-prime means land on \(1/q,1/q!,1/q^2\).

---

## Correct status

\[
\boxed{
\text{The cyclotomic defect process now has exact local, finite-cutoff, and finite-adelic generating functions.}
}
\]

The next remaining frontier is the genuine global object: a completed global
Dirichlet series or zeta package built from these exact finite products.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_finite_adelic_pgf.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_finite_adelic_pgf.json`
- Result: `PART_DCMLXXXIX_cyclotomic_finite_adelic_pgf_results.json`
