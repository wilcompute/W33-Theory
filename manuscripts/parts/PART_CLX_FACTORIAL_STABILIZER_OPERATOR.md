# Part CLX — Factorial Stabilizer Operator

**Date:** 2026-05-02  
**Status:** seed-to-global closure theorem

---

## 1. Starting point

The original finite seed is

\[
q! = 2q.
\]

At \(q=3\), this gives

\[
3! = 6 = 2q.
\]

CLX identifies this same number as the local rank seed:

\[
2q=6=\operatorname{rank}(E_6).
\]

---

## 2. Global factorial lift

Now take the factorial lift of the rank seed:

\[
(2q)! = 6! = 720.
\]

But CLVIII showed that the E6 root stabilizer is

\[
qE=3\cdot240=720.
\]

Therefore

\[
\boxed{(2q)! = qE.}
\]

So the global stabilizer is the factorial lift of the original seed.

---

## 3. Descendants of the global lift

The W(3,3) edge carrier is

\[
E=\frac{(2q)!}{q}=\frac{720}{3}=240.
\]

The directed-edge carrier is

\[
a_0=2E=\frac{2(2q)!}{q}=480.
\]

The E6 root orbit is

\[
|\Phi(E_6)|=\frac{(2q)!}{\Phi_4}=\frac{720}{10}=72.
\]

The Weyl group order is

\[
|W(E_6)|=\frac{(2q)!^2}{\Phi_4}=\frac{720^2}{10}=51840.
\]

Thus

\[
|W(E_6)|=|\Phi(E_6)|\cdot(2q)!.
\]

---

## 4. The seed-to-global ladder

The full ladder is:

\[
q! = 2q = 6
\]

\[
\Downarrow
\]

\[
(2q)! = 720
\]

\[
\Downarrow
\]

\[
E=(2q)!/q=240
\]

\[
\Downarrow
\]

\[
a_0=2(2q)!/q=480
\]

\[
\Downarrow
\]

\[
|\Phi(E_6)|=(2q)!/\Phi_4=72
\]

\[
\Downarrow
\]

\[
|W(E_6)|=(2q)!^2/\Phi_4=51840.
\]

---

## 5. Theorem statement

**The original seed \(q!=2q\) has a global factorial lift.** At \(q=3\),

\[
q!=2q=6
\]

is the E6 Cartan rank, while

\[
(2q)!=720
\]

equals the q-lifted W(3,3) edge carrier \(qE\) and hence the E6 root stabilizer. Consequently,

\[
E=(2q)!/q,
\]

\[
a_0=2(2q)!/q,
\]

\[
|\Phi(E_6)|=(2q)!/\Phi_4,
\]

and

\[
|W(E_6)|=(2q)!^2/\Phi_4.
\]

---

## 6. Why this matters

This closes the seed-to-global loop.

The same factorial identity that selects \(q=3\) locally expands to the E6 Weyl stabilizer globally.  The edge carrier, directed-edge spectral coefficient, root orbit, and Weyl order are all factorial descendants of

\[
q!=2q.
\]

The original seed is therefore not only a selection rule; it is the first rung of the stabilizer ladder.

---

## 7. Regression status

Local validation of the CLX test file:

```text
5 passed in 0.04s
```

The tests verify:

1. the local seed is the Cartan rank,
2. the global lift is the root stabilizer,
3. edge/directed-edge carriers come from the global lift,
4. E6 roots and Weyl order come from the factorial lift,
5. audit-level consistency.

---

## 8. Next move

The next target is to test whether the global stabilizer

\[
(2q)! = 720
\]

also acts as the denominator/normalizer for the observable grammar:

\[
C=8/13,
\qquad
T=5/13,
\qquad
D=3/13,
\qquad
P(A)=A/\Phi_3.
\]

If so, the final form may be a single stabilizer-normalized observable algebra.
