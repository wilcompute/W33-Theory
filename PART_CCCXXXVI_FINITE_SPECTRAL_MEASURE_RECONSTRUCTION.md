# Part CCCXXXVI — Finite Spectral Measure Reconstruction Compiler

**Date:** 2026-05-05  
**Status:** finite inverse-spectral reconstruction layer for the W33 RG spinor.

**Executable audit:** `exploration/PART_CCCXXXVI_FINITE_SPECTRAL_MEASURE_RECONSTRUCTION.py`  
**Results:** `PART_CCCXXXVI_finite_spectral_measure_reconstruction_results.json`  
**Regression tests:** `tests/test_finite_spectral_measure_reconstruction_cccxxxvi.py`

---

## 1. Starting point

CCCXXXV organized the finite moment tower:

\[
\operatorname{tr}(G^{2r+1})=0,
\]

\[
\operatorname{tr}(G^{2r})=2\left(\frac{5049}{4}\right)^r.
\]

CCCXXXVI proves this tower is self-reconstructing: the observed moments alone recover the two branch atoms and their weights.

---

## 2. Moment recurrence

Let

\[
M^2=\frac{5049}{4}.
\]

The moment sequence is

\[
m_n=\operatorname{tr}(G^n).
\]

The first terms are

\[
m_0=2,
\qquad
m_1=0,
\qquad
m_2=\frac{5049}{2},
\qquad
m_3=0.
\]

The recurrence is

\[
\boxed{
m_{n+2}=M^2m_n=\frac{5049}{4}m_n.
}
\]

This recurrence is exactly the spectral shadow of

\[
G^2=M^2I.
\]

---

## 3. Minimal polynomial

The recurrence

\[
m_{n+2}=M^2m_n
\]

corresponds to the denominator

\[
\lambda^2-M^2.
\]

Therefore the minimal polynomial recovered from the moments is

\[
\boxed{
\lambda^2-\frac{5049}{4}.
}
\]

Its roots are

\[
\boxed{
\lambda_+=+\frac{\sqrt{5049}}{2},
\qquad
\lambda_-=-\frac{\sqrt{5049}}{2}.
}
\]

---

## 4. Hankel rank

Build the Hankel matrices from the moments:

\[
H_2=\begin{pmatrix}
m_0&m_1\\
m_1&m_2
\end{pmatrix}.
\]

Since

\[
m_0=2,
\quad
m_1=0,
\quad
m_2=\frac{5049}{2},
\]

we get

\[
\det(H_2)=5049\neq0.
\]

But the \(3\times3\) Hankel determinant vanishes:

\[
\det(H_3)=0.
\]

Therefore the moment sequence has Hankel rank two:

\[
\boxed{
\operatorname{rank}_{\rm Hankel}=2.
}
\]

This proves the measure has exactly two spectral atoms.

---

## 5. Branch weights

Let the two atoms be

\[
+M,
\qquad
-M.
\]

Let their weights be

\[
w_+,
\qquad
w_-.
\]

Using

\[
m_0=w_++w_-=2,
\]

and

\[
m_1=M(w_+-w_-)=0,
\]

we obtain

\[
\boxed{
w_+=1,
\qquad
w_-=1.
}
\]

Thus the reconstructed spectral measure is

\[
\boxed{
\mu_G=\delta_{+\sqrt{5049}/2}+\delta_{-\sqrt{5049}/2}.
}
\]

---

## 6. Stieltjes transform

The Stieltjes transform of the reconstructed measure is

\[
S(z)=\frac{1}{z-M}+\frac{1}{z+M}.
\]

Therefore

\[
\boxed{
S(z)=\frac{2z}{z^2-M^2}.
}
\]

Substituting

\[
M^2=\frac{5049}{4},
\]

gives

\[
\boxed{
S(z)=\frac{2z}{z^2-5049/4}.
}
\]

Its large-\(z\) expansion is exactly the resolvent trace expansion from CCCXXXV:

\[
S(z)=\sum_{r\ge0}2(M^2)^rz^{-(2r+1)}.
\]

---

## 7. Architecture upgrade

CCCXXXV gave the moment tower.

CCCXXXVI proves the tower is inverse-spectral:

\[
\boxed{
\text{moment tower}
\to
\text{minimal polynomial}
\to
\text{spectral atoms}
\to
\text{branch weights}
\to
\text{Stieltjes transform}.
}
\]

So the action-flow chain now reads:

\[
\boxed{
\text{finite spectral action}
\to
\text{finite moment tower}
\to
\textbf{finite inverse-spectral reconstruction}.
}
\]

---

## 8. Theorem statement

**Finite Spectral Measure Reconstruction Theorem.**  
The W33 RG spinor moment sequence satisfies

\[
m_{n+2}=\frac{5049}{4}m_n.
\]

Its Hankel rank is two, its minimal polynomial is

\[
\lambda^2-\frac{5049}{4},
\]

and the unique symmetric two-atom spectral measure is

\[
\mu_G=\delta_{+\sqrt{5049}/2}+\delta_{-\sqrt{5049}/2}.
\]

The corresponding Stieltjes transform is

\[
S(z)=\frac{2z}{z^2-5049/4}.
\]

Thus the finite moment tower reconstructs the branch spectrum without direct reference to the original matrix generator.

---

## 9. Honest boundary

This is a finite inverse-spectral reconstruction theorem.  It does not yet supply a continuum scaling limit or a physical measurement protocol for reconstructing the same spectral measure experimentally.

The next bridge is:

\[
\boxed{
\text{finite inverse spectral measure}
\to
\text{scaling family / observable measurement map}.
}
\]
