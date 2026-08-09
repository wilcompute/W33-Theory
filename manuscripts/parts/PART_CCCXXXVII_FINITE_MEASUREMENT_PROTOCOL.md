# Part CCCXXXVII — Finite Measurement Protocol Compiler

**Date:** 2026-05-05  
**Status:** finite observability and measurement protocol for the W33 RG spinor architecture.

**Executable audit:** `exploration/PART_CCCXXXVII_FINITE_MEASUREMENT_PROTOCOL.py`  
**Results:** `PART_CCCXXXVII_finite_measurement_protocol_results.json`  
**Regression tests:** `tests/test_finite_measurement_protocol_cccxxxvii.py`

---

## 1. Starting point

CCCXXXVI proved that the moment tower reconstructs the spectral measure:

\[
\mu_G=\delta_{+\sqrt{5049}/2}+\delta_{-\sqrt{5049}/2}.
\]

CCCXXXVII turns that inverse-spectral theorem into an explicit finite measurement protocol.

The goal is to answer:

> What finite samples are sufficient to reconstruct the branch spectrum, mass shell, weights, and projectors?

---

## 2. Tier A — Minimal moment reconstruction

Measure the first three moments:

\[
m_0,\quad m_1,\quad m_2.
\]

For the W33 RG spinor:

\[
m_0=2,
\qquad
m_1=0,
\qquad
m_2=\frac{5049}{2}.
\]

Then

\[
M^2=\frac{m_2}{m_0}.
\]

Therefore

\[
\boxed{
M^2=\frac{5049}{4}.
}
\]

The condition

\[
m_1=0
\]

certifies branch symmetry. Under the two-branch symmetric assumption,

\[
w_+=w_-=1.
\]

So Tier A recovers:

\[
\boxed{
\text{symmetry},\quad M^2=5049/4,
\quad w_+=w_-=1.
}
\]

---

## 3. Tier B — Hankel rank and recurrence certificate

Measure

\[
m_0,m_1,m_2,m_3,m_4.
\]

Build Hankel matrices.  The executable audit verifies:

\[
\det(H_2)=5049\neq0,
\]

and

\[
\det(H_3)=0.
\]

Thus the Hankel rank is exactly two:

\[
\boxed{
\operatorname{rank}_{\rm Hankel}=2.
}
\]

Tier B also verifies the recurrence

\[
\boxed{
m_{n+2}=\frac{5049}{4}m_n.
}
\]

In particular,

\[
m_4=\frac{5049}{4}m_2.
\]

So Tier B certifies:

\[
\boxed{
\text{two-atom spectrum}+	ext{mass-shell recurrence}.
}
\]

---

## 4. Tier C — Independent spectral response sample

Any one of the following response measurements independently recovers the same mass shell.

### Resolvent trace sample

For one value of \(s\), measure

\[
R(s)=\operatorname{tr}((sI-G)^{-1}).
\]

Since

\[
R(s)=\frac{2s}{s^2-M^2},
\]

we recover

\[
\boxed{
M^2=s^2-\frac{2s}{R(s)}.
}
\]

### Heat trace sample

For one positive \(\tau\), measure

\[
H(\tau)=\operatorname{tr}(e^{-\tau G^2}).
\]

Since

\[
H(\tau)=2e^{-M^2\tau},
\]

we recover

\[
\boxed{
M^2=-\frac{1}{\tau}\log\left(\frac{H(\tau)}{2}\right).
}
\]

### Spinor trace sample

For one value of \(t\), measure

\[
T(t)=\operatorname{tr}(e^{tG}).
\]

Since

\[
T(t)=2\cosh(Mt),
\]

we recover

\[
\boxed{
M=\frac{1}{t}\operatorname{arcosh}\left(\frac{T(t)}{2}\right).
}
\]

Thus Tier C provides an independent consistency check against the moment-reconstructed value.

---

## 5. Tier D — Projector reconstruction

Once \(G\) and \(M\) are known, reconstruct the branch projectors:

\[
\boxed{
P_\pm=\frac12\left(I\pm\frac{G}{M}\right).
}
\]

The executable audit verifies:

\[
P_+^2=P_+,
\]

\[
P_-^2=P_-,
\]

\[
P_+P_-=0.
\]

So Tier D reconstructs the stable/unstable branch sectors.

---

## 6. Protocol summary

| Tier | Samples | Recovers |
|---|---|---|
| A | \(m_0,m_1,m_2\) | symmetry, \(M^2=m_2/m_0\), equal branch weights |
| B | \(m_0,\dots,m_4\) | Hankel rank two, recurrence, two-atom certificate |
| C | one resolvent OR heat OR spinor trace sample | independent mass-shell check |
| D | \(G\) plus recovered \(M\) | branch projectors \(P_\pm\) |

---

## 7. Architecture upgrade

CCCXXXVI gave inverse-spectral reconstruction.

CCCXXXVII gives finite observability:

\[
\boxed{
\text{inverse spectral measure}
\to
\text{finite measurement protocol}
\to
\text{branch projector reconstruction}.
}
\]

The architecture chain now reaches:

\[
\boxed{
\text{finite spectral action}
\to
\text{moment tower}
\to
\text{inverse-spectral reconstruction}
\to
\textbf{finite observability protocol}.
}
\]

---

## 8. Theorem statement

**Finite Measurement Protocol Theorem.**  
The W33 RG spinor architecture is finitely observable. The samples

\[
m_0,m_1,m_2
\]

recover the symmetric two-branch mass shell

\[
M^2=\frac{5049}{4}
\]

and equal branch weights. The samples

\[
m_0,m_1,m_2,m_3,m_4
\]

certify Hankel rank two and the recurrence

\[
m_{n+2}=\frac{5049}{4}m_n.
\]

One resolvent, heat-trace, or spinor-trace sample independently recovers the same mass shell, and \(G\) plus recovered \(M\) reconstructs the branch projectors

\[
P_\pm=\frac12\left(I\pm\frac{G}{M}\right).
\]

---

## 9. Honest boundary

This is a finite mathematical measurement protocol. Mapping these samples to laboratory measurements requires a physical observable/unit assignment.

The next bridge is:

\[
\boxed{
\text{finite protocol}
\to
\text{physical observable map}
\to
\text{experimental/empirical predictions}.
}
\]
