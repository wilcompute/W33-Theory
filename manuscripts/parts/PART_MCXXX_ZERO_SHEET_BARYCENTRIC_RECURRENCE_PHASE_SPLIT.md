# Part MCXXX: Zero-Sheet Barycentric Recurrence Phase Split

**Date:** 2026-05-20  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED FINITE CHARACTERISTIC-ROOT SPLIT FOR THE RECURRENCE LADDER

---

## Why this part exists

MCXXIX showed that the sampled entropy and concentration profiles admit short order-two
least-squares recurrences. The next invariant is the characteristic-root packet of those
recurrences.

This part stays finite: it classifies the sampled recurrence fits on the six-point ladder,
not an infinite dynamical system.

---

## The theorem

For an order-two fit
\[
x_n \approx a_2x_{n-2}+a_1x_{n-1},
\]
use the characteristic polynomial
\[
r^2-a_1r-a_2.
\]

On the MCXXIX ladder
\[
s\in\{0.5,1.0,1.5,2.0,2.5,3.0\}
\]
at cutoff \(10^5\), the entropy recurrence has coefficients
\[
[-0.7930288200175566,\ 1.7579250530757946],
\]
with discriminant
\[
-0.08181478783869123.
\]
So its roots are the complex-conjugate pair
\[
0.8789625265378973\pm0.14301642199297537i,
\]
both with modulus
\[
0.8905216561193539.
\]

The concentration recurrence has coefficients
\[
[-0.7838244705016053,\ 1.8194198703813187],
\]
with discriminant
\[
0.17499078273195323.
\]
So its roots are real:
\[
1.11886943338041,\qquad 0.7005504370009087.
\]

Thus the sampled recurrence ladder has a phase split:

1. entropy is a damped complex-conjugate recurrence;
2. concentration is a real split recurrence with one unit-exceeding root.

---

## Reading

MCXXIX found finite recurrence memory. MCXXX says the two memories are not of the same type.
Entropy carries a damped oscillatory root pair, matching the fact that entropy rises and then
falls around the shared resonance. Concentration carries a real two-mode split, matching its
dual trough behavior.

The result is deliberately local to the sampled ladder. It is a characteristic-root
classification of the finite recurrence fits, not a claim of asymptotic periodicity or a
continuum spectral theorem.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_zero_sheet_barycentric_recurrence_phase_split.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_zero_sheet_barycentric_recurrence_phase_split.json`
- Result: `PART_MCXXX_zero_sheet_barycentric_recurrence_phase_split_results.json`
