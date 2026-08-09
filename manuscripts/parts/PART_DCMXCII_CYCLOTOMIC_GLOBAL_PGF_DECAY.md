# Part DCMXCII (992) - Cyclotomic Global PGF Decay

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED GLOBAL DECAY LAW

---

## Why this part exists

Part DCMXCI shows that the total split-prime valuation packet has mean and
variance growing like \(\log\log X\) with unit leading coefficient. The next
natural question is what this does to the finite-cutoff probability generating
function itself.

It turns out the PGF decays with a clean logarithmic power dictated exactly by
\(1-t\).

---

## The theorem

For fixed \(t<1\), define the finite split-prime cutoff PGF

\[
G_X(t)=\prod_{\substack{p\le X\\ p\equiv1\ (3)}}\frac{p-2+t}{p-t}.
\]

Then

\[
\log G_X(t)=-(1-t)\log\log X + C(t) + o(1),
\]

so equivalently

\[
\boxed{
G_X(t)\,(\log X)^{1-t} \to \mathcal C(t)
}
\]

for a stable constant shadow \(\mathcal C(t)\).

---

## Why the exponent is exactly \(1-t\)

For large split primes,

\[
\frac{p-2+t}{p-t}=1-\frac{2(1-t)}{p-t}=1-\frac{2(1-t)}{p}+O\!\left(\frac{1}{p^2}\right).
\]

Taking logs and summing over split primes gives

\[
\log G_X(t) = -2(1-t)\sum_{\substack{p\le X\\p\equiv1\ (3)}}\frac1p + O(1).
\]

The prime number theorem in arithmetic progressions contributes the factor
\(\tfrac12\log\log X\), so the coefficient becomes exactly \(1-t\).

---

## Numerical profile

The executable profile on \(X=10^3,10^4,10^5,10^6\) shows stabilization of the
normalized packet:

- for \(t=0\), \(G_X(0)\log X\) approaches a stable constant;
- for \(t=1/2\), \(G_X(1/2)\sqrt{\log X}\) approaches a stable constant;
- for \(t=3/4\), \(G_X(3/4)(\log X)^{1/4}\) approaches a stable constant.

So the decay exponent is not just qualitative: it is exactly the linear shadow
of the packet parameter \(t\).

---

## What is now exact

1. the finite split-prime PGF has explicit cutoff product law;
2. its global decay is logarithmic rather than exponential or power-of-\(X\);
3. the decay exponent is exactly \(1-t\);
4. the normalized PGF isolates a stable constant shadow \(\mathcal C(t)\).

---

## Correct status

\[
\boxed{
\text{The cyclotomic split-prime packet has an exact logarithmic PGF decay law whose exponent interpolates linearly as }1-t.
}
\]

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_global_pgf_decay.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_global_pgf_decay.json`
- Result: `PART_DCMXCII_cyclotomic_global_pgf_decay_results.json`
