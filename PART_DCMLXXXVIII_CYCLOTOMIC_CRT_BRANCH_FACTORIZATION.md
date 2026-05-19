# Part DCMLXXXVIII (988) - Cyclotomic CRT Branch Factorization

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED FINITE ADELIC FACTORIZATION THEOREM

---

## Why this part exists

Parts DCMLXXXV--DCMLXXXVII identified the cyclotomic defect classes locally:

- exact lifted residue classes modulo \(p^2\);
- full \(p\)-adic valuation trees;
- exact local Euler factors.

The remaining exact finite step is to show that these local pieces combine by
the Chinese remainder theorem with no loss.  They do, and the result is the
finite-cutoff/global shadow of the density law.

---

## The theorem

Let \(S\) be a finite set of split primes \(p\equiv1\pmod3\), and define

\[
M_S=\prod_{p\in S} p^2.
\]

At square depth \(p^2\), each split prime contributes exactly two local
cyclotomic defect classes for \(\Phi_3\), and likewise two for \(\Phi_6\).

By the Chinese remainder theorem:

\[
\boxed{
\#\mathcal R_S(\Phi_3)=\#\mathcal R_S(\Phi_6)=2^{|S|}
}
\]

modulo \(M_S\), where \(\mathcal R_S\) is the simultaneous defect-class set.

The exact simultaneous density is therefore

\[
\boxed{
\mu_S^{\mathrm{sim}}=\prod_{p\in S}\frac{2}{p^2}.
}
\]

The exact avoidance density is

\[
\boxed{
\mu_S^{\mathrm{avoid}}=\prod_{p\in S}\left(1-\frac{2}{p^2}\right),
}
\]

and the exact union density is

\[
\boxed{
\mu_S^{\mathrm{union}}=1-\prod_{p\in S}\left(1-\frac{2}{p^2}\right).
}
\]

So the global density product is already exact at every finite cutoff.

---

## Proof sketch

For each \(p\in S\), Part DCMLXXXV gives exactly two classes modulo \(p^2\).
Since the moduli \(p^2\) are pairwise coprime, the Chinese remainder theorem
identifies simultaneous classes with independent choices of one local class at
each prime.

Hence the class count multiplies:

\[
2\times2\times\cdots\times2 = 2^{|S|}.
\]

Dividing by \(M_S\) yields the simultaneous density.  The avoidance and union
density formulas follow from the same finite independence.

---

## First nontrivial example: \(S=\{7,13\}\)

For \(\Phi_3\), the local classes are

\[
\{18,30\}\pmod{49},
\qquad
\{22,146\}\pmod{169}.
\]

Combining them by CRT gives exactly four simultaneous classes modulo

\[
49\cdot169=8281:
\]

\[
\boxed{\{2174,3019,5261,6106\}\pmod{8281}.}
\]

Thus

\[
\mu_{\{7,13\}}^{\mathrm{sim}}=\frac{4}{8281}=\frac{2}{49}\cdot\frac{2}{169}.
\]

For \(\Phi_6\), the simultaneous classes are the corresponding negative-branch
CRT lifts.

---

## Three-prime packet

For \(S=\{7,13,19\}\), the class count is

\[
2^3=8
\]

modulo

\[
49\cdot169\cdot361.
\]

So even the first three split primes already exhibit the exact finite adelic
product structure.

---

## What is now exact

The promoted exact statements are:

1. finite sets of split primes combine by exact CRT branch factorization;
2. the simultaneous class count is exactly \(2^{|S|}\);
3. the finite-cutoff simultaneous density is exactly \(\prod 2/p^2\);
4. the finite-cutoff avoidance density is exactly \(\prod (1-2/p^2)\);
5. the global density product is the direct limit of these exact finite
   cutoff formulas.

---

## Correct status

\[
\boxed{
\text{The cyclotomic defect Euler product is not merely asymptotic; it is the exact CRT factorization law at every finite cutoff.}
}
\]

This is the finite adelic shadow of the local valuation-tree theorem.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_crt_branch_factorization.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_crt_branch_factorization.json`
- Result: `PART_DCMLXXXVIII_cyclotomic_crt_branch_factorization_results.json`
