# Part DCMXC (990) - Cyclotomic Split-Prime Support Law

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED SUPPORT THEOREM

---

## Why this part exists

Parts DCMLXXXV--DCMLXXXIX identified the split-prime defect classes, their
Hensel lifts, the local Euler factors, and the exact finite-adelic packet. But
there is an even simpler structural question underneath all of that:

> Why are the relevant primes split in the first place?

The answer is that the whole cyclotomic packet already lives on the split-prime
side before any squarefree or defect refinement is imposed.

---

## The theorem

For every integer \(q\ge 3\):

\[
\boxed{
 p\mid \Phi_3(q)=q^2+q+1 \implies p=3 \text{ or } p\equiv 1 \pmod 3,
}
\]

and

\[
\boxed{
 p\mid \Phi_6(q)=q^2-q+1 \implies p=3 \text{ or } p\equiv 1 \pmod 6.
}
\]

So every nontrivial prime divisor of the \(\Phi_3\) packet lies in the split
ternary class, and every nontrivial prime divisor of the \(\Phi_6\) packet lies
in the even sharper split-hexic class.

---

## Proof sketch

If \(p\mid q^2+q+1\), then

\[
q^3-1=(q-1)(q^2+q+1)
\]

shows \(q^3\equiv 1\pmod p\). For \(p\neq 3\), we cannot have \(q\equiv1\pmod p\),
because then \(q^2+q+1\equiv 3\pmod p\). So for \(p\neq 3\), the order of \(q\)
modulo \(p\) is exactly \(3\), hence \(3\mid p-1\), i.e. \(p\equiv1\pmod3\).

If \(p\mid q^2-q+1\), then

\[
q^3+1=(q+1)(q^2-q+1)
\]

shows \(q^6\equiv1\pmod p\). For \(p\neq 3\), one rules out orders \(1,2,3\)
by the same congruence checks, so the order is exactly \(6\). Therefore
\(6\mid p-1\), i.e. \(p\equiv1\pmod6\).

---

## Verified scan

The executable audit on \(3\le q\le 20000\) finds:

- \(\Phi_3\) exact support: **True**;
- \(\Phi_6\) exact support: **True**.

The first support primes seen on both branches are

\[
3,7,13,19,31,37,43,61,67,73,79,97.
\]

So the split-prime support is not just a defect phenomenon; it is the native
support law of the full cyclotomic packet.

---

## What is now exact

1. the \(\Phi_3\) packet is supported on \(p=3\) and \(p\equiv1\pmod3\);
2. the \(\Phi_6\) packet is supported on \(p=3\) and \(p\equiv1\pmod6\);
3. the split-prime defect theory sits on top of an already split-prime packet;
4. the earlier discriminant-\(-3\) observations are now explained at the
   prime-support level, not just the repeated-factor level.

---

## Correct status

\[
\boxed{
\text{The cyclotomic packet does not merely prefer split primes at its defects; it is globally supported on them from the start.}
}
\]

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_split_prime_support.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_split_prime_support.json`
- Result: `PART_DCMXC_cyclotomic_split_prime_support_results.json`
