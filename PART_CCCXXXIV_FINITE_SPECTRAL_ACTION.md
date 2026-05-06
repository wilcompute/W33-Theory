# Part CCCXXXIV — Finite Spectral Action / Heat Kernel Compiler

**Date:** 2026-05-05  
**Status:** finite spectral-action and heat-kernel layer for the W33 RG spinor.

**Executable audit:** `exploration/PART_CCCXXXIV_FINITE_SPECTRAL_ACTION.py`  
**Results:** `PART_CCCXXXIV_finite_spectral_action_results.json`  
**Regression tests:** `tests/test_finite_spectral_action_cccxxxiv.py`

---

## 1. Starting point

CCCXXXIII gave the finite propagator/resolvent layer:

\[
(sI-G)^{-1}=\frac{sI+G}{s^2-5049/4},
\]

and

\[
e^{tG}=e^{mt}P_+ + e^{-mt}P_-,
\qquad
m=\frac{\sqrt{5049}}{2}.
\]

CCCXXXIV extracts the finite spectral action data.

---

## 2. Spectrum

Since

\[
G^2=\frac{5049}{4}I,
\]

the eigenvalues of \(G\) are

\[
\boxed{
\operatorname{spec}(G)=\left\{+\frac{\sqrt{5049}}{2},-\frac{\sqrt{5049}}{2}\right\}.
}
\]

The squared operator has spectrum

\[
\boxed{
\operatorname{spec}(G^2)=\left\{\frac{5049}{4},\frac{5049}{4}\right\}.
}
\]

So the KG/mass-shell multiplicity is two.

---

## 3. Characteristic determinant

The characteristic determinant is

\[
\det(sI-G)=s^2-\frac{5049}{4}.
\]

Thus

\[
\boxed{
\det(sI-G)=s^2-m^2,
\qquad
m^2=\frac{5049}{4}.
}
\]

This is the spectral denominator already appearing in the resolvent.

---

## 4. Resolvent trace

The resolvent is

\[
(sI-G)^{-1}=\frac{sI+G}{s^2-5049/4}.
\]

Because

\[
\operatorname{tr}(G)=0,
\]

we get

\[
\boxed{
\operatorname{tr}\big((sI-G)^{-1}\big)
=
\frac{2s}{s^2-5049/4}.
}
\]

This is the finite Green's trace.

---

## 5. Spinor propagator trace

The spinor propagator is

\[
e^{tG}=e^{mt}P_+ + e^{-mt}P_-.
\]

Taking trace gives

\[
\operatorname{tr}(e^{tG})=e^{mt}+e^{-mt}.
\]

Therefore

\[
\boxed{
\operatorname{tr}(e^{tG})=2\cosh\left(\frac{\sqrt{5049}}{2}t\right).
}
\]

---

## 6. Klein–Gordon heat trace

The heat trace of \(G^2\) is

\[
\operatorname{tr}(e^{-\tau G^2}).
\]

Since \(G^2=(5049/4)I\),

\[
\boxed{
\operatorname{tr}(e^{-\tau G^2})=2e^{-(5049/4)\tau}.
}
\]

This is the finite heat-kernel response of the RG mass shell.

---

## 7. Spectral zeta function

For positive integer \(p\), define

\[
\zeta_{G^2}(p)=\operatorname{tr}\left((G^2)^{-p}\right).
\]

Then

\[
\boxed{
\zeta_{G^2}(p)=2\left(\frac{5049}{4}\right)^{-p}.
}
\]

In particular,

\[
\zeta_{G^2}(1)=\frac{8}{5049},
\]

and

\[
\zeta_{G^2}(2)=\frac{32}{5049^2}.
\]

---

## 8. Sharp cutoff spectral action

For a sharp cutoff \(\Lambda^2\), the finite spectral action is simply the number of \(G^2\)-modes below the cutoff:

\[
S_\Lambda=\#\{\lambda\in\operatorname{spec}(G^2):\lambda\leq\Lambda^2\}.
\]

Since both squared eigenvalues equal

\[
\frac{5049}{4},
\]

we get

\[
\boxed{
S_\Lambda=
\begin{cases}
0,&\Lambda^2<5049/4,\\
2,&\Lambda^2\ge 5049/4.
\end{cases}
}
\]

---

## 9. Architecture upgrade

CCCXXXIII gave the propagator and resolvent.

CCCXXXIV gives the finite spectral-action layer:

\[
\boxed{
\text{propagator/resolvent}
\to
\text{determinant}
\to
\text{resolvent trace}
\to
\text{heat trace}
\to
\text{zeta function}
\to
\text{spectral cutoff action}.
}
\]

The action-flow chain now reads:

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
\text{finite propagator/resolvent}
\to
\textbf{finite spectral action}.
}
\]

---

## 10. Theorem statement

**Finite Spectral Action Theorem.**  
The finite RG spinor generator has spectrum

\[
\left\{+\frac{\sqrt{5049}}{2},-\frac{\sqrt{5049}}{2}\right\}.
\]

Therefore

\[
\det(sI-G)=s^2-\frac{5049}{4},
\]

\[
\operatorname{tr}\big((sI-G)^{-1}\big)=\frac{2s}{s^2-5049/4},
\]

\[
\operatorname{tr}(e^{tG})=2\cosh\left(\frac{\sqrt{5049}}{2}t\right),
\]

\[
\operatorname{tr}(e^{-\tau G^2})=2e^{-(5049/4)\tau},
\]

and

\[
\zeta_{G^2}(p)=2\left(\frac{5049}{4}\right)^{-p}.
\]

Thus the W33 RG spinor admits a closed finite spectral-action/heat-kernel package.

---

## 11. Honest boundary

This is a finite spectral-action/heat-kernel layer for the RG spinor. It is not yet the continuum spectral action of a physical Dirac operator on spacetime.

The next bridge is:

\[
\boxed{
\text{finite spectral action}
\to
\text{continuum spectral action / physical observable expansion}.
}
\]
