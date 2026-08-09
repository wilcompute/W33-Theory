# Part DCMXCIII (993) - Cyclotomic Completed Euler Product

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED COMPLETED PRODUCT THEOREM

---

## Why this part exists

Part DCMXCII showed that the global cutoff PGF decays like
\((\log X)^{-(1-t)}\). That means the raw split-prime product still carries a
logarithmic singularity. The natural next step is to remove that singularity
prime-by-prime and expose the genuinely convergent global object underneath.

---

## The theorem

Define the finite cutoff PGF

\[
G_X(t)=\prod_{\substack{p\le X\\ p\equiv1\ (3)}}\frac{p-2+t}{p-t}
\]

and the residue-class Mertens kernel

\[
M_X=\prod_{\substack{p\le X\\ p\equiv1\ (3)}}\left(1-\frac1p\right).
\]

Then the completed product

\[
\boxed{
\mathcal C_X(t)=G_X(t)\,M_X^{-2(1-t)}
}
\]

has local factors

\[
\boxed{
\left(\frac{p-2+t}{p-t}\right)\left(1-\frac1p\right)^{-2(1-t)}=1+O_t\!\left(\frac1{p^2}\right),
}
\]

so the infinite product

\[
\boxed{
\mathcal C(t)=\prod_{p\equiv1\ (3)}\left(\frac{p-2+t}{p-t}\right)\left(1-\frac1p\right)^{-2(1-t)}
}
\]

converges absolutely for each fixed \(t<1\).

---

## Factorization of the old shadow

The earlier normalized PGF shadow factorizes exactly as

\[
G_X(t)(\log X)^{1-t}=\mathcal C_X(t)\left(\sqrt{\log X}\,M_X\right)^{2(1-t)}.
\]

So the global decay theorem of Part DCMXCII is exactly the product of:

1. a convergent completed Euler product \(\mathcal C_X(t)\), and
2. the residue-class Mertens kernel for split primes.

---

## Numerical profile

At \(X=10^6\), the completed constants stabilize near

\[
\mathcal C(0)\approx 0.9583648561,
\qquad
\mathcal C(1/2)\approx 0.9803258953,
\qquad
\mathcal C(3/4)\approx 0.9902841393.
\]

The same run gives the split-prime Mertens constant estimate

\[
\sqrt{\log X}\,M_X \approx 1.4033699521.
\]

Multiplying these back exactly recovers the shadow constants of Part DCMXCII.

---

## What is now exact

1. the split-prime PGF has a completed Euler product with absolute convergence;
2. its logarithmic singularity is entirely carried by the residue-class Mertens kernel;
3. the normalized global shadow factors exactly into a completed constant times a Mertens constant;
4. the completed object is the genuine global cyclotomic product underneath the defect process.

---

## Correct status

\[
\boxed{
\text{The cyclotomic split-prime packet now has a true completed Euler product: a globally convergent object with the logarithmic singularity factored off prime-by-prime.}
}
\]

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_completed_euler_product.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_completed_euler_product.json`
- Result: `PART_DCMXCIII_cyclotomic_completed_euler_product_results.json`
