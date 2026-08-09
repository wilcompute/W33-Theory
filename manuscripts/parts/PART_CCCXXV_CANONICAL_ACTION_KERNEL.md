# Part CCCXXV — Canonical Action Kernel Compiler

**Date:** 2026-05-05  
**Status:** exact uniqueness theorem for the finite determinant/action layer of the TOE architecture.

**Executable audit:** `exploration/PART_CCCXXV_CANONICAL_ACTION_KERNEL.py`  
**Results:** `PART_CCCXXV_canonical_action_kernel_results.json`  
**Regression tests:** `tests/test_canonical_action_kernel_cccxxv.py`

---

## 1. What CCCXXIV left open

CCCXXIV closed the runtime architecture:

\[
\text{qutrit Pauli memory}
\to
\text{photonic hardware}
\to
\text{Clifford compiler}
\to
\text{critical fusion}
\to
\text{Hashimoto scheduler}
\to
\text{determinant/action compression}
\to
\text{RG renderer}.
\]

But it still left a question:

> Is the determinant/action layer merely a nice compression, or is it forced?

CCCXXV answers: it is forced by three finite action constraints.

---

## 2. The centered coupling triple

The determinant previously appeared as

\[
Z(x)=(1-5x)^{10}(1+x)^{16}(1+7x)^6.
\]

The coupling coefficients are

\[
(5,-1,-7).
\]

These are not arbitrary. They are the centered W33 triple

\[
\boxed{
(-1+2q,\,-1,\,-1-2q)
}
\]

with

\[
q=3.
\]

So:

\[
(-1+2q,\,-1,\,-1-2q)=(5,-1,-7).
\]

Architecturally, the determinant spectrum is centered at \(-1\), with symmetric spacing \(2q=6\):

\[
5=-1+6,
\qquad
-7=-1-6.
\]

This is the coupling spine.

---

## 3. The three action constraints

Let the three unknown sector dimensions be

\[
(d_+,d_0,d_-).
\]

The finite runtime imposes three constraints.

### Constraint 1 — total runtime degree

The total determinant degree must be the spinor/runtime degree

\[
d_+ + d_0 + d_- = 2^{q+\lambda}=2^5=32.
\]

### Constraint 2 — triangle-trace product

The product of sector dimensions must compress the W33 triangle trace:

\[
d_+d_0d_- = \operatorname{tr}(A^3)=6T=960.
\]

### Constraint 3 — signed imbalance

The signed first moment against the centered coupling triple must be the W33 imbalance

\[
(5)d_+ + (-1)d_0 + (-7)d_- = -2^q=-8.
\]

Equivalently:

\[
5d_+ - d_0 - 7d_- = -8.
\]

---

## 4. Uniqueness theorem

The executable audit enumerates all positive integer triples satisfying the constraints.

There is exactly one solution:

\[
\boxed{
(d_+,d_0,d_-)=(10,16,6).
}
\]

And these are exactly

\[
10=\Phi_4=q^2+1,
\]

\[
16=(q+1)^2,
\]

\[
6=2q.
\]

Therefore:

\[
\boxed{
(d_+,d_0,d_-)
=
(\Phi_4,(q+1)^2,2q).
}
\]

This proves that the determinant exponents are forced by the finite runtime constraints.

---

## 5. The determinant is now derived

Substituting the unique sector dimensions gives

\[
Z(x)
=
(1-5x)^{10}(1+x)^{16}(1+7x)^6.
\]

So this determinant should no longer be presented as an ansatz.  It is the unique positive-integer three-sector kernel compatible with:

\[
\text{centered W33 coupling triple},
\]

\[
\text{spinor/runtime degree},
\]

\[
\text{triangle trace},
\]

and

\[
\text{signed imbalance}.
\]

---

## 6. Moment checks

The signed first moment is

\[
10(5)+16(-1)+6(-7)
=
50-16-42
=
-8
=
-2^q.
\]

The second moment is

\[
10(5^2)+16(1)+6(7^2)
=
250+16+294
=
560.
\]

But

\[
560=
\Phi_6(q^4-1)
=
7\cdot80.
\]

The determinant value at one is

\[
Z(1)=(-4)^{10}2^{16}8^6.
\]

Therefore

\[
Z(1)=2^{20}2^{16}2^{18}=2^{54}=2^{2q^3}.
\]

---

## 7. Architecture upgrade

CCCXXIV said:

\[
Z(x)\quad\text{compresses the action/operator stack}.
\]

CCCXXV upgrades this to:

\[
\boxed{
Z(x)\quad\text{is the unique finite action kernel compatible with the runtime constraints.}
}
\]

That is a deeper statement.

The architecture is now:

\[
\boxed{
\text{qutrit Pauli memory}
\to
\text{photonic cluster runtime}
\to
\text{Clifford compiler}
\to
\text{critical fusion}
\to
\text{Hashimoto scheduler}
\to
\textbf{unique finite action kernel}
\to
\text{RG renderer}.
}
\]

---

## 8. Final theorem statement

**Canonical Action Kernel Theorem.**  
Let the W33 coupling triple be

\[
(-1+2q,-1,-1-2q)=(5,-1,-7),
\]

and let the unknown sector dimensions be positive integers \((d_+,d_0,d_-)\).  If the sector dimensions satisfy

\[
d_+ + d_0 + d_- = 2^{q+\lambda}=32,
\]

\[
d_+d_0d_- = \operatorname{tr}(A^3)=960,
\]

and

\[
5d_+ - d_0 - 7d_- = -2^q=-8,
\]

then the unique positive integer solution is

\[
(d_+,d_0,d_-)=(10,16,6)=(\Phi_4,(q+1)^2,2q).
\]

Therefore the determinant

\[
Z(x)=(1-5x)^{10}(1+x)^{16}(1+7x)^6
\]

is the canonical finite action kernel of the W33 runtime architecture.

---

## 9. Honest boundary

CCCXXV proves uniqueness of the finite action kernel.  It still does not by itself give the full continuum Standard Model Lagrangian.

The next required bridge is:

\[
\boxed{
\text{finite action kernel}
\to
\text{Euler/variation principle}
\to
\text{scaling/RG continuum field theory}.
}
\]

That is the next architecture target.
