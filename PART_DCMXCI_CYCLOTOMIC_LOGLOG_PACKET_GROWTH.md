# Part DCMXCI (991) - Cyclotomic Log-Log Packet Growth

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED GLOBAL GROWTH LAW

---

## Why this part exists

Part DCMLXXXIX gave the exact finite-adelic PGF for a finite set of split
primes. Once Part DCMXC shows that the whole packet is already supported on the
split-prime side, the next natural question is global:

> How does the total split-prime valuation packet grow as the prime cutoff rises?

It grows with exact local formulas but only logarithmically at the global level.
More precisely, its mean and variance have **unit log-log slope**.

---

## The theorem

Let

\[
T_X(q)=\sum_{\substack{p\le X\\ p\equiv1\ (3)}} v_p\bigl(\Phi_3(q)\bigr).
\]

Then for every finite cutoff \(X\):

\[
\boxed{
\mathbb E[T_X]=\operatorname{Var}(T_X)=\sum_{\substack{p\le X\\ p\equiv1\ (3)}}\frac{2}{p-1}.
}
\]

By the prime number theorem in arithmetic progressions,

\[
\sum_{\substack{p\le X\\ p\equiv1\ (3)}}\frac{1}{p} = \frac12\log\log X + B_3 + o(1),
\]

so the exact packet mean obeys

\[
\boxed{
\mathbb E[T_X]=\operatorname{Var}(T_X)=\log\log X + C_{\mathrm{cycl}} + o(1).
}
\]

Thus the cyclotomic split-prime packet has exact **leading coefficient 1** in its
log-log growth law.

---

## First packets

For the first split primes \(7,13,19\):

\[
\mathbb E[T_{19}] = \frac13 + \frac16 + \frac19 = \frac{11}{18}.
\]

So the first three local means are exactly

\[
\frac1q,\qquad \frac1{q!},\qquad \frac1{q^2},
\]

and the three-prime packet lands on

\[
\boxed{\frac{11}{18}.}
\]

At the next split prime \(31\), the mean is

\[
\mathbb E[T_{31}] = \frac{61}{90}.
\]

---

## Numerical profile

The executable profile gives:

- \(X=19\): \(\mathbb E[T_X]=11/18\approx0.61111\);
- \(X=31\): \(\mathbb E[T_X]=61/90\approx0.67778\);
- \(X=10^3\): \(\mathbb E[T_X]\approx1.29960\);
- \(X=10^4\): \(\mathbb E[T_X]\approx1.58413\);
- \(X=10^5\): \(\mathbb E[T_X]\approx1.80503\);
- \(X=10^6\): \(\mathbb E[T_X]\approx1.98686\).

Subtracting \(\log\log X\) gives a stable constant estimate near

\[
\boxed{C_{\mathrm{cycl}}\approx -0.63893.}
\]

---

## What is now exact

1. the finite-cutoff packet mean and variance are exact split-prime sums;
2. the first packets land on \(1/q,1/q!,1/q^2\);
3. the global packet grows like \(\log\log X\) with exact leading coefficient 1;
4. the packet is globally thin but not bounded: its total split-prime valuation
   depth grows slowly and inexorably.

---

## Correct status

\[
\boxed{
\text{The finite-adelic cyclotomic packet globalizes into a unit-slope log-log valuation law over the split-prime tower.}
}
\]

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_loglog_packet_growth.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_loglog_packet_growth.json`
- Result: `PART_DCMXCI_cyclotomic_loglog_packet_growth_results.json`
