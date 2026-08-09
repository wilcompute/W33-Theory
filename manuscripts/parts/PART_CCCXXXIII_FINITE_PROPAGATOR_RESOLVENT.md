# Part CCCXXXIII — Finite Propagator / Resolvent Compiler

**Date:** 2026-05-05  
**Status:** finite Green's-function / propagator layer for the W33 RG spinor.

**Executable audit:** `exploration/PART_CCCXXXIII_FINITE_PROPAGATOR_RESOLVENT.py`  
**Results:** `PART_CCCXXXIII_finite_propagator_resolvent_results.json`  
**Regression tests:** `tests/test_finite_propagator_resolvent_cccxxxiii.py`

---

## 1. Starting point

CCCXXXII established the finite Dirac/Klein–Gordon factorization

\[
(D-G)(D+G)=D^2-\frac{5049}{4}I,
\]

where

\[
G=\begin{pmatrix}67/2&140\\1&-67/2\end{pmatrix}
\]

and

\[
G^2=\frac{5049}{4}I.
\]

CCCXXXIII turns this into the finite propagator/resolvent layer.

---

## 2. Resolvent identity

Since

\[
G^2=m^2I,
\qquad
m^2=\frac{5049}{4},
\]

we have

\[
(sI-G)(sI+G)=s^2I-G^2.
\]

Therefore

\[
(sI-G)(sI+G)=\left(s^2-\frac{5049}{4}\right)I.
\]

Thus the exact resolvent is

\[
\boxed{
(sI-G)^{-1}=\frac{sI+G}{s^2-5049/4}.
}
\]

This is the finite Green's-function identity for the RG spinor generator.

---

## 3. Branch projectors

Normalize

\[
J=\frac{G}{m}=\frac{2}{\sqrt{5049}}G.
\]

Then

\[
J^2=I.
\]

Define

\[
P_+=\frac{I+J}{2},
\qquad
P_-=\frac{I-J}{2}.
\]

They satisfy

\[
P_+^2=P_+,
\]

\[
P_-^2=P_-,
\]

\[
P_+P_-=0,
\]

\[
P_++P_-=I.
\]

---

## 4. Propagator decomposition

The spinor propagator is

\[
U(t)=e^{tG}.
\]

Using

\[
G^2=m^2I,
\]

we get the hyperbolic form

\[
\boxed{
e^{tG}=\cosh(mt)I+\frac{\sinh(mt)}{m}G.
}
\]

Using the branch projectors, the same propagator decomposes as

\[
\boxed{
e^{tG}=e^{mt}P_+ + e^{-mt}P_-.
}
\]

where

\[
m=\frac{\sqrt{5049}}{2}.
\]

Thus the finite propagator separates exactly into stable/unstable branch modes.

---

## 5. Semigroup law

The executable audit verifies

\[
e^{t_1G}e^{t_2G}=e^{(t_1+t_2)G}.
\]

This confirms that the branch propagator is a genuine finite flow object, not just a formal decomposition.

---

## 6. Architecture upgrade

CCCXXXII gave the finite Dirac factorization.

CCCXXXIII adds the Green's-function layer:

\[
\boxed{
\text{Dirac factorization}
\to
\text{resolvent}
\to
\text{branch propagator}.
}
\]

The chain now reads:

\[
\boxed{
\text{finite action}
\to
\text{Euler equation}
\to
\text{beta flow}
\to
\text{projective renderer}
\to
\text{Lorentzian spinor}
\to
\text{Dirac/Klein–Gordon factorization}
\to
\textbf{finite propagator/resolvent}.
}
\]

---

## 7. Theorem statement

**Finite Propagator / Resolvent Theorem.**  
Let

\[
G=\begin{pmatrix}67/2&140\\1&-67/2\end{pmatrix}
\]

with

\[
G^2=\frac{5049}{4}I.
\]

Then

\[
(sI-G)^{-1}=\frac{sI+G}{s^2-5049/4}.
\]

Moreover, defining

\[
P_\pm=\frac12\left(I\pm\frac{2G}{\sqrt{5049}}\right),
\]

one has

\[
e^{tG}=e^{mt}P_+ + e^{-mt}P_-,
\qquad
m=\frac{\sqrt{5049}}{2}.
\]

Therefore the W33 RG spinor admits an exact finite Green's-function and branch-propagator decomposition.

---

## 8. Honest boundary

This is a finite Green's-function/propagator layer for the RG spinor.  It is not yet a physical scattering amplitude or continuum QFT propagator.

The next bridge is:

\[
\boxed{
\text{finite propagator}
\to
\text{physical unit map / observable kernel}
\to
\text{continuum propagator or measured response}.}
\]
