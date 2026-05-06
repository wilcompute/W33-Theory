# Part CCCXXVIII — Canonical Beta Flow Compiler

**Date:** 2026-05-05  
**Status:** finite RG-like beta-flow object extracted from the inverse-scale fixed-point law.

**Executable audit:** `exploration/PART_CCCXXVIII_CANONICAL_BETA_FLOW.py`  
**Results:** `PART_CCCXXVIII_canonical_beta_flow_results.json`  
**Regression tests:** `tests/test_canonical_beta_flow_cccxxviii.py`

---

## 1. From fixed point to beta flow

CCCXXVII derived the inverse-scale fixed-point law

\[
y=67+\frac{140}{y}.
\]

Define

\[
F(y)=67+\frac{140}{y}.
\]

The rational finite beta function is

\[
\beta(y)=F(y)-y=67+\frac{140}{y}-y.
\]

Multiplying by \(y\) gives the polynomial beta numerator

\[
\boxed{
B(y)=y\beta(y)=67y+140-y^2.
}
\]

The fixed points are the zeros of

\[
B(y)=0,
\]

which is equivalent to

\[
y^2-67y-140=0.
\]

---

## 2. W33 coefficient forms

The linear beta coefficient is

\[
67=2v-\Phi_3.
\]

The constant beta coefficient is

\[
140=\frac{v}{2}\Phi_6.
\]

So

\[
\boxed{
B(y)=(2v-\Phi_3)y+\frac{v}{2}\Phi_6-y^2.
}
\]

At W33:

\[
B(y)=67y+140-y^2.
\]

---

## 3. Fixed points and factorization

The discriminant is

\[
\Delta=5049=q^3(k-1)(\Phi_4+\Phi_6).
\]

The fixed points are

\[
y_+=\frac{67+\sqrt{5049}}{2},
\qquad
y_-=\frac{67-\sqrt{5049}}{2}.
\]

The beta numerator factors as

\[
\boxed{
B(y)=-(y-y_+)(y-y_-).
}
\]

The exact fixed-point identities are

\[
y_++y_-=67,
\]

\[
y_+y_-=-140.
\]

---

## 4. Branch derivatives

The beta numerator derivative is

\[
B'(y)=67-2y.
\]

At the fixed points:

\[
B'(y_+)=-\sqrt{5049},
\]

\[
B'(y_-)=+\sqrt{5049}.
\]

The fixed-point iteration derivative is

\[
F'(y)=-\frac{140}{y^2}.
\]

Therefore:

\[
|F'(y_+)|<1,
\]

so the positive branch is attracting, while

\[
|F'(y_-)|>1,
\]

so the negative branch is repelling.

---

## 5. Basin signs

Because

\[
B(y)=67y+140-y^2
\]

is a downward-opening quadratic, the sign structure is:

\[
y<y_- \quad\Rightarrow\quad B(y)<0,
\]

\[
y_-<y<y_+ \quad\Rightarrow\quad B(y)>0,
\]

\[
y>y_+ \quad\Rightarrow\quad B(y)<0.
\]

In architecture language:

\[
\boxed{
\text{below }y_-: \text{ decreasing-scale},
\quad
\text{between roots}: \text{ increasing-scale},
\quad
\text{above }y_+: \text{ decreasing-scale}.
}
\]

---

## 6. Architecture upgrade

CCCXXVI gave the finite Euler equation.

CCCXXVII gave the inverse-scale fixed-point law.

CCCXXVIII packages this as a beta-flow object:

\[
\boxed{
\beta(y)=67+\frac{140}{y}-y,
\qquad
B(y)=67y+140-y^2.
}
\]

So the architecture now contains a bona fide finite flow layer:

\[
\boxed{
\text{unique finite action kernel}
\to
\text{finite Euler equation}
\to
\text{inverse-scale fixed point}
\to
\textbf{canonical finite beta flow}
\to
\text{RG/scaling renderer}.
}
\]

---

## 7. Theorem statement

**Canonical Beta Flow Theorem.**  
The inverse-scale fixed-point law

\[
y=67+\frac{140}{y}
\]

induces the finite beta numerator

\[
B(y)=67y+140-y^2.
\]

Its fixed points are

\[
y_\pm=\frac{67\pm\sqrt{5049}}{2},
\]

with discriminant

\[
5049=q^3(k-1)(\Phi_4+\Phi_6).
\]

The derivative spectrum is

\[
B'(y_\pm)=\mp\sqrt{5049},
\]

and the fixed-point map has an attracting positive branch and a repelling negative branch.  Thus the W33 finite action architecture contains a canonical beta-flow object before any continuum approximation is taken.

---

## 8. Honest boundary

This is not yet a physical renormalization group in the continuum QFT sense.  It is a finite beta-flow for the inverse-scale coordinate \(y\).

The next bridge is a unit/scaling map:

\[
\boxed{
y
\to
\text{physical RG coordinate}
\to
\text{energy/length/coupling observable}.
}
\]
