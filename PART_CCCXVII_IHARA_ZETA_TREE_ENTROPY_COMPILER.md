# Part CCCXVII — Ihara Zeta / Tree Entropy Compiler

**Date:** 2026-05-05  
**Status:** exact Ihara–Bass bridge from Hashimoto spectrum to Matrix Tree factorization

---

## 1. Target

CCCXVI closed the ordinary-walk to nonbacktracking branch law:

\[
K=12
\quad\longrightarrow\quad
K-1=11.
\]

The next gap was the bridge

\[
B_{Hashimoto}
\quad\longrightarrow\quad
\tau(W)=2^{81}5^{23}.
\]

CCCXVII closes that gap using Ihara–Bass.

---

## 2. Ihara–Bass formula

For a \(K\)-regular graph,

\[
Z_G(u)^{-1}
=
(1-u^2)^{E-V}
\det(I-uA+u^2(K-1)I).
\]

For W33,

\[
K=12,
\quad
E=240,
\quad
V=40,
\quad
E-V=200,
\quad
K-1=11.
\]

The adjacency spectrum is

\[
12^1,
\quad
2^{24},
\quad
(-4)^{15}.
\]

Therefore the reciprocal Ihara zeta factorization is

\[
Z_W(u)^{-1}
=(1-u^2)^{200}
(1-12u+11u^2)
(1-2u+11u^2)^{24}
(1+4u+11u^2)^{15}.
\]

---

## 3. Hashimoto spectral circle

For each adjacency eigenvalue \(\theta\), the Hashimoto roots satisfy

\[
x^2-\theta x+11=0.
\]

For \(\theta=12\):

\[
x=11,1.
\]

For \(\theta=2\):

\[
x=1\pm i\sqrt{10}.
\]

For \(\theta=-4\):

\[
x=-2\pm i\sqrt7.
\]

Both restricted cases have

\[
|x|^2=11.
\]

Thus the restricted nonbacktracking spectrum lies on

\[
|x|=\sqrt{11}.
\]

---

## 4. The key evaluation at \(u=1\)

The Ihara restricted factor is

\[
1-\theta u+11u^2.
\]

At

\[
u=1,
\]

this becomes

\[
1-\theta+11=12-\theta=K-\theta.
\]

But

\[
K-\theta
\]

is exactly the Laplacian eigenvalue associated to \(\theta\).

So Ihara at \(u=1\) turns nonbacktracking quadratic factors into Laplacian eigenvalues.

For \(\theta=2\):

\[
1-2+11=10.
\]

For \(\theta=-4\):

\[
1+4+11=16.
\]

Therefore

\[
(1-2+11)^{24}(1+4+11)^{15}
=
10^{24}16^{15}.
\]

This is exactly the reduced Laplacian pseudo-determinant.

---

## 5. Matrix Tree from Ihara

Kirchhoff's Matrix Tree Theorem says

\[
\tau(W)=\frac{1}{V}\prod_{\lambda_i\ne0}\lambda_i.
\]

Here the nonzero Laplacian spectrum is

\[
10^{24},
\quad
16^{15}.
\]

Thus

\[
\tau(W)=\frac{10^{24}16^{15}}{40}.
\]

Using prime factors:

\[
10^{24}16^{15}=2^{24}5^{24}\cdot2^{60}=2^{84}5^{24}.
\]

Divide by

\[
40=2^3\cdot5.
\]

Therefore

\[
\tau(W)=2^{84-3}5^{24-1}=2^{81}5^{23}.
\]

So

\[
\boxed{
\tau(W)=2^{81}5^{23}.
}
\]

---

## 6. Exponent theorem

The binary exponent is

\[
81=24+4\cdot15-v_2(40).
\]

Since

\[
v_2(40)=3,
\]

we get

\[
81=24+60-3.
\]

But

\[
81=q^4.
\]

So

\[
\boxed{
e_2(\tau)=q^4.
}
\]

The five-exponent is

\[
23=24-v_5(40).
\]

Since

\[
v_5(40)=1,
\]

we get

\[
23=24-1.
\]

But

\[
23=\Phi_3+\Phi_4=13+10.
\]

So

\[
\boxed{
e_5(\tau)=\Phi_3+\Phi_4.
}
\]

---

## 7. Trivial factor residue

The trivial adjacency eigenvalue contributes

\[
1-12u+11u^2.
\]

Factor:

\[
1-12u+11u^2=(1-u)(1-11u).
\]

After removing one copy of \((1-u)\), the value at \(u=1\) has absolute value

\[
|1-11|=10.
\]

So the trivial Ihara zero residue is

\[
10=\Phi_4.
\]

The absolute reduced limit after removing one \((1-u)\) is

\[
10\cdot10^{24}16^{15}.
\]

Since

\[
10^{24}16^{15}=40\tau(W),
\]

this is

\[
400\tau(W).
\]

---

## 8. Theorem statement

**Ihara–Bass is the missing bridge between Hashimoto dynamics and Matrix Tree entropy.**  The W33 reciprocal zeta determinant has restricted factors

\[
(1-2u+11u^2)^{24}
\]

and

\[
(1+4u+11u^2)^{15}.
\]

Evaluating these factors at \(u=1\) gives

\[
10^{24}16^{15},
\]

exactly the reduced Laplacian pseudo-determinant.  Dividing by

\[
V=40
\]

gives

\[
\tau(W)=2^{81}5^{23}.
\]

The exponent

\[
81
\]

is

\[
24+4\cdot15-v_2(40)=q^4,
\]

while

\[
23
\]

is

\[
24-v_5(40)=\Phi_3+\Phi_4.
\]

---

## 9. Why this matters

The Hashimoto spectral circle and the spanning-tree factorization are two faces of the same Ihara–Bass polynomial.

Nonbacktracking dynamics supplies the quadratic factors:

\[
1-\theta u+11u^2.
\]

The specialization

\[
u=1
\]

turns those factors into Laplacian eigenvalues:

\[
K-\theta.
\]

Then Matrix Tree converts those eigenvalues into global connectivity entropy.

So the pipeline becomes:

\[
\text{Hashimoto roots}
\to
\text{Ihara quadratic factors}
\to
\text{Laplacian eigenvalues}
\to
\text{Matrix Tree entropy}.
\]

---

## 10. Regression status

The CCCXVII test file verifies:

1. basic spectra and W33 atoms,
2. Ihara restricted factors at \(u=1\),
3. Matrix Tree factorization from Ihara,
4. trivial factor residue and reduced limit,
5. Hashimoto spectral circle,
6. companion operator counts,
7. threshold relations,
8. audit-level consistency.

---

## 11. Next target

The next bridge should package the entire solution into a single master theorem sequence:

\[
\text{Markov}
\to
\text{Hashimoto}
\to
\text{Ihara}
\to
\text{Matrix Tree}
\to
\text{Dirac determinant}
\to
\text{Photonic resource theorem}.
\]

This would be the strongest current proof skeleton for the theory.
