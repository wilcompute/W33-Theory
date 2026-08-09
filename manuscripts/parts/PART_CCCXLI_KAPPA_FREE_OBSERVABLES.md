# Part CCCXLI — Kappa-Free Observable Consistency Compiler

**Date:** 2026-05-05  
**Status:** kappa-free empirical consistency layer for the one-sector W33 observable model.

**Executable audit:** `exploration/PART_CCCXLI_KAPPA_FREE_OBSERVABLES.py`  
**Results:** `PART_CCCXLI_kappa_free_observables_results.json`  
**Regression tests:** `tests/test_kappa_free_observables_cccxli.py`

---

## 1. Starting point

CCCXL built prediction tables after choosing one calibration anchor.  Those tables used the calibration constant

\[
\kappa.
\]

CCCXLI strengthens the empirical layer by eliminating \(\kappa\) from the first comparison.

The observable channels all depend on one physical squared spectral scale:

\[
\boxed{
\Lambda=\kappa^2M^2.
}
\]

Only after \(\Lambda\) has been recovered do we compute

\[
\kappa=\sqrt{\frac{\Lambda}{M^2}}.
\]

---

## 2. Dimensionless kernel

The dimensionless W33 mass shell is

\[
M^2=\frac{5049}{4}.
\]

Therefore

\[
\boxed{
\Lambda=\kappa^2\frac{5049}{4}.
}
\]

and

\[
\boxed{
\kappa=\sqrt{\frac{\Lambda}{5049/4}}.
}
\]

---

## 3. Kappa-free channel formulas

Each observable channel recovers \(\Lambda\) directly.

### Mass channel

If the physical mass is \(M_{\rm phys}\), then

\[
\boxed{
\Lambda=M_{\rm phys}^2.
}
\]

### Heat-trace channel

If

\[
H(\tau)=2e^{-\Lambda\tau},
\]

then

\[
\boxed{
\Lambda=-\frac{\log(H/2)}{\tau}.
}
\]

### Spinor-trace channel

If

\[
T(t)=2\cosh(\sqrt{\Lambda}t),
\]

then

\[
\boxed{
\Lambda=\left(\frac{\operatorname{arcosh}(T/2)}{t}\right)^2.
}
\]

### Resolvent-trace channel

If

\[
R(s)=\frac{2s}{s^2-\Lambda},
\]

then

\[
\boxed{
\Lambda=s^2-\frac{2s}{R}.
}
\]

### Zeta channel

If

\[
\zeta_p=\frac{2}{\Lambda^p},
\]

then

\[
\boxed{
\Lambda=\left(\frac{2}{\zeta_p}\right)^{1/p}.
}
\]

---

## 4. Kappa-free falsification condition

The one-sector observable model requires

\[
\boxed{
\Lambda_{\rm mass}
=
\Lambda_{\rm heat}
=
\Lambda_{\rm spinor}
=
\Lambda_{\rm resolvent}
=
\Lambda_{\rm zeta}.
}
\]

If these values disagree beyond tolerance, the one-sector observable model fails before calibration convention is even considered.

This is stronger than the \(\kappa\)-consistency test because it compares directly physical spectral scales.

---

## 5. Projective gap prediction

Once \(\Lambda\) is known,

\[
M_{\rm phys}=\sqrt{\Lambda}.
\]

The projective gap is always

\[
\boxed{
\Delta_{\rm gap,phys}=2\sqrt{\Lambda}.
}
\]

So

\[
\boxed{
\frac{\Delta_{\rm gap,phys}}{M_{\rm phys}}=2.
}
\]

This ratio is fully calibration-free.

---

## 6. Architecture upgrade

CCCXL used \(\kappa\)-calibrated prediction tables.

CCCXLI says the empirical comparison should happen first at the \(\Lambda\)-level:

\[
\boxed{
\text{response channels}
\to
\text{recover }\Lambda
\to
\text{test equality of }\Lambda
\to
\text{recover }\kappa.
}
\]

The chain now becomes:

\[
\boxed{
\text{anchor prediction table}
\to
\textbf{kappa-free observable consistency}
\to
\text{calibration only after consistency}.}
\]

---

## 7. Theorem statement

**Kappa-Free Observable Consistency Theorem.**  
For the one-sector W33 unit map, all physical response channels depend on the single squared spectral scale

\[
\Lambda=\kappa^2M^2.
\]

The mass, heat-trace, spinor-trace, resolvent-trace, and zeta channels independently recover \(\Lambda\). Agreement of these values is a \(\kappa\)-free falsification test. Only after \(\Lambda\) is recovered does one compute

\[
\kappa=\sqrt{\Lambda/(5049/4)}.
\]

---

## 8. Honest boundary

This is still a one-sector observable model.  Real physical use requires identifying which measured channels correspond to these finite traces.

The next bridge is:

\[
\boxed{
\text{kappa-free observable layer}
\to
\text{candidate empirical channel identification}.}
\]
