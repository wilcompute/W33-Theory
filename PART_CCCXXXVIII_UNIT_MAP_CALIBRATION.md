# Part CCCXXXVIII — Unit Map / Calibration Compiler

**Date:** 2026-05-05  
**Status:** physical-unit calibration layer for the finite W33 RG spinor architecture.

**Executable audit:** `exploration/PART_CCCXXXVIII_UNIT_MAP_CALIBRATION.py`  
**Results:** `PART_CCCXXXVIII_unit_map_calibration_results.json`  
**Regression tests:** `tests/test_unit_map_calibration_cccxxxviii.py`

---

## 1. Starting point

CCCXXXVII gave a finite measurement protocol.  The architecture can now reconstruct:

\[
G,
\qquad
M^2=\frac{5049}{4},
\qquad
M=\frac{\sqrt{5049}}{2},
\]

along with its projectors, heat trace, spinor trace, resolvent, moment tower, and spectral measure.

But this still leaves one essential empirical issue:

> What physical unit does one finite RG/spinor unit represent?

CCCXXXVIII makes that bridge explicit.

---

## 2. Dimensionless kernel

The finite theory determines a dimensionless generator

\[
G=
\begin{pmatrix}
67/2 & 140\\
1 & -67/2
\end{pmatrix},
\]

with

\[
G^2=\frac{5049}{4}I.
\]

So the dimensionless mass shell is

\[
\boxed{
M^2=\frac{5049}{4},
\qquad
M=\frac{\sqrt{5049}}{2}.
}
\]

This is internally fixed by W33.

---

## 3. Calibration constant

Introduce a single physical calibration constant

\[
\boxed{\kappa}.
\]

For the one-sector RG spinor renderer, define

\[
\boxed{
G_{\rm phys}=\kappa G.
}
\]

Then

\[
\boxed{
M_{\rm phys}=\kappa M,
}
\]

and

\[
\boxed{
M_{\rm phys}^2=\kappa^2M^2.
}
\]

Thus the finite theory gives the dimensionless structure; empirical calibration fixes \(\kappa\).

---

## 4. Time and heat-time scaling

For spinor/RG time,

\[
\boxed{
t_{\rm dimless}=\kappa t_{\rm phys}.
}
\]

So

\[
\operatorname{tr}(e^{t_{\rm phys}G_{\rm phys}})
=
\operatorname{tr}(e^{t_{\rm dimless}G}).
\]

For heat time,

\[
\boxed{
\tau_{\rm dimless}=\kappa^2\tau_{\rm phys}.
}
\]

So

\[
\operatorname{tr}(e^{-\tau_{\rm phys}G_{\rm phys}^2})
=
\operatorname{tr}(e^{-\tau_{\rm dimless}G^2}).
\]

---

## 5. Resolvent scaling

Let

\[
s_{\rm dimless}=\frac{s_{\rm phys}}{\kappa}.
\]

Then

\[
\boxed{
(s_{\rm phys}I-G_{\rm phys})^{-1}
=
\kappa^{-1}
\left(s_{\rm dimless}I-G\right)^{-1}.
}
\]

So the resolvent scales with one inverse power of \(\kappa\).

---

## 6. Zeta scaling

For the spectral zeta values,

\[
\zeta_{G^2}(p)=2(M^2)^{-p}.
\]

Under physical scaling,

\[
M_{\rm phys}^2=\kappa^2M^2.
\]

Therefore

\[
\boxed{
\zeta_{\rm phys}(p)=\kappa^{-2p}\zeta_{\rm dimless}(p).
}
\]

---

## 7. Projector invariance

The branch projectors are

\[
P_\pm=\frac12\left(I\pm\frac{G}{M}\right).
\]

Under scaling,

\[
\frac{G_{\rm phys}}{M_{\rm phys}}
=
\frac{\kappa G}{\kappa M}
=
\frac{G}{M}.
\]

Therefore

\[
\boxed{
P_\pm\text{ are invariant under }\kappa.
}
\]

This is important: physical units change scale values, but not the branch decomposition.

---

## 8. Calibration recipes

A physical anchor fixes \(\kappa\).  Possible recipes:

### Mass anchor

If a physical mass scale \(M_{\rm phys}\) is assigned to the finite branch mass,

\[
\boxed{
\kappa=\frac{M_{\rm phys}}{M}.
}
\]

### Heat-trace sample

If a physical heat trace sample is measured,

\[
H=2e^{-\kappa^2M^2\tau_{\rm phys}},
\]

then

\[
\boxed{
\kappa=\sqrt{\frac{-\log(H/2)}{M^2\tau_{\rm phys}}}.
}
\]

### Spinor trace sample

If

\[
T=2\cosh(\kappa Mt_{\rm phys}),
\]

then

\[
\boxed{
\kappa=\frac{\operatorname{arcosh}(T/2)}{Mt_{\rm phys}}.
}
\]

### Resolvent sample

If

\[
R=\frac{2s}{s^2-\kappa^2M^2},
\]

then \(\kappa\) is recovered by solving

\[
\boxed{
\kappa^2=\frac{s^2-2s/R}{M^2}.
}
\]

---

## 9. Architecture upgrade

CCCXXXVII gave finite observability.

CCCXXXVIII gives physical calibration:

\[
\boxed{
\text{finite observability protocol}
\to
\text{unit map}
\to
\text{physical calibration constant }\kappa.
}
\]

The key distinction is:

\[
\boxed{
\text{finite architecture determines dimensionless structure;}
\quad
\text{empirical anchoring fixes absolute units.}
}
\]

---

## 10. Theorem statement

**Unit Map / Calibration Theorem.**  
The W33 RG spinor architecture determines the dimensionless kernel

\[
G^2=\frac{5049}{4}I.
\]

A one-sector physical unit assignment is obtained by choosing a calibration constant \(\kappa\) and setting

\[
G_{\rm phys}=\kappa G.
\]

Then masses scale by \(\kappa\), heat time by \(\kappa^2\), spinor/RG time by \(\kappa\), resolvents by \(\kappa^{-1}\) after frequency rescaling, zeta values by \(\kappa^{-2p}\), and branch projectors are invariant.  Thus one calibration constant is necessary and sufficient for the one-sector physical unit map.

---

## 11. Honest boundary

The finite architecture does not determine absolute physical units internally.  It determines dimensionless structure plus covariant scaling laws.  A physical anchor is required to set \(\kappa\).

The next bridge is:

\[
\boxed{
\text{unit map}
\to
\text{choice of empirical anchor}
\to
\text{testable physical predictions}.}
\]
