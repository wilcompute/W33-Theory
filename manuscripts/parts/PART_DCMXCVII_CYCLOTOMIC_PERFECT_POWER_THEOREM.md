# Part DCMXCVII (997) - Cyclotomic Perfect-Power Theorem

**Date:** 2026-05-19
**Series:** W(3,3) Theory of Everything
**Status:** VERIFIED GLOBAL PERFECT-POWER THEOREM

---

## Why this part exists

The scan up to \(q\le10^5\) found only one nontrivial perfect-power value on the
whole packet:

\[
\Phi_3(18)=\Phi_6(19)=343=7^3.
\]

The remaining task was to show this is not just a computational accident.

---

## The theorem

The two cyclotomic branches satisfy the exact identities

\[
4\Phi_3(q)-3=(2q+1)^2,
\qquad
4\Phi_6(q)-3=(2q-1)^2.
\]

Therefore, if either branch is a perfect power

\[
\Phi_3(q)=y^n \quad \text{or} \quad \Phi_6(q)=y^n
\qquad (q\ge3,\ n>1),
\]

then one obtains a solution of the classical Ljunggren equation

\[
\boxed{x^2+3=4y^n}
\]

with \(x=2q+1\) or \(x=2q-1\).

Using the classical Ljunggren theorem that the only nontrivial positive
solution with \(y>1\), \(n>1\) is

\[
(x,y,n)=(37,7,3),
\]

one gets the exact cyclotomic consequence:

\[
\boxed{
\Phi_3(18)=7^3,
\qquad
\Phi_6(19)=7^3,
}
\]

and there are no other nontrivial perfect powers on either branch for
\(q\ge3\).

---

## What is now exact

1. the empirical isolation of \(343=7^3\) is promoted to a global theorem;
2. the cyclotomic perfect-power problem is identified exactly with the Ljunggren equation;
3. the only nontrivial positive-q solutions are \(q=18\) on \(\Phi_3\) and \(q=19\) on \(\Phi_6\).

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_cyclotomic_perfect_power_theorem.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_cyclotomic_perfect_power_theorem.json`
- Result: `PART_DCMXCVII_cyclotomic_perfect_power_theorem_results.json`
