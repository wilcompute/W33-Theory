# Part CCCXXXII — Finite Dirac Factorization Compiler

**Date:** 2026-05-05  
**Status:** finite Dirac/Klein–Gordon factorization of the Lorentzian RG spinor flow.

**Executable audit:** `exploration/PART_CCCXXXII_FINITE_DIRAC_FACTORIZATION.py`  
**Results:** `PART_CCCXXXII_finite_dirac_factorization_results.json`  
**Regression tests:** `tests/test_finite_dirac_factorization_cccxxxii.py`

---

## 1. Starting point

CCCXXXI identified the RG renderer as a Lorentzian spinor generator

\[
G=
\begin{pmatrix}
67/2 & 140\\
1 & -67/2
\end{pmatrix}
\]

with

\[
G^2=\frac{5049}{4}I.
\]

CCCXXXII extracts the finite Dirac/Klein–Gordon factorization implied by this identity.

---

## 2. Finite spinor transport

Define the finite spinor transport equation

\[
\boxed{
\frac{d\psi}{dt}=G\psi.
}
\]

This is the first-order spinor equation for the RG renderer.

Differentiating once more gives

\[
\frac{d^2\psi}{dt^2}=G\frac{d\psi}{dt}=G^2\psi.
\]

Since

\[
G^2=\frac{5049}{4}I,
\]

we obtain

\[
\boxed{
\frac{d^2\psi}{dt^2}=\frac{5049}{4}\psi.
}
\]

This is the finite Klein–Gordon/mass-shell equation for the RG spinor.

---

## 3. Finite Dirac factorization

Let

\[
D=\frac{d}{dt}.
\]

Then

\[
(D-G)(D+G)=D^2-G^2.
\]

Because

\[
G^2=\frac{5049}{4}I,
\]

we get

\[
\boxed{
(D-G)(D+G)=D^2-\frac{5049}{4}I.
}
\]

Similarly,

\[
(D+G)(D-G)=D^2-\frac{5049}{4}I.
\]

Therefore the finite mass-shell operator factors into first-order Dirac operators:

\[
\boxed{
D^2-m^2=(D-G)(D+G),
\qquad
m=\frac{\sqrt{5049}}{2}.
}
\]

---

## 4. W33 mass form

The mass squared is

\[
m^2=\frac{5049}{4}.
\]

But

\[
5049=q^3(k-1)(\Phi_4+\Phi_6).
\]

So

\[
\boxed{
m^2=\frac{q^3(k-1)(\Phi_4+\Phi_6)}{4}.
}
\]

and

\[
\boxed{
m=\frac{1}{2}\sqrt{q^3(k-1)(\Phi_4+\Phi_6)}.
}
\]

At W33:

\[
m=\frac{\sqrt{5049}}{2}.
\]

---

## 5. Architecture upgrade

CCCXXXI gave the Lorentzian spinor generator.

CCCXXXII gives the finite Dirac square-root of the mass shell:

\[
\boxed{
\text{Lorentzian spinor generator}
\to
\text{finite Dirac equation}
\to
\text{finite Klein–Gordon equation}.
}
\]

The full action-flow chain is now:

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
\textbf{Dirac/Klein–Gordon factorization}.
}
\]

---

## 6. Theorem statement

**Finite Dirac Factorization Theorem.**  
Let

\[
G=\begin{pmatrix}67/2&140\\1&-67/2\end{pmatrix}.
\]

Then

\[
G^2=\frac{5049}{4}I.
\]

Thus the first-order spinor equation

\[
\frac{d\psi}{dt}=G\psi
\]

implies the second-order mass-shell equation

\[
\frac{d^2\psi}{dt^2}=\frac{5049}{4}\psi.
\]

Equivalently,

\[
(D-G)(D+G)=D^2-\frac{5049}{4}I.
\]

Therefore the W33 RG renderer admits a finite Dirac/Klein–Gordon factorization with mass

\[
m=\frac{\sqrt{5049}}{2}.
\]

---

## 7. Honest boundary

This is a finite Dirac/Klein–Gordon factorization for the RG spinor flow.  It is not yet a continuum relativistic field equation on physical spacetime.

The next bridge is:

\[
\boxed{
\text{finite Dirac factorization}
\to
\text{physical spin bundle / continuum Dirac operator}.
}
\]
