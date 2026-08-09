# Part MCXXVIII: Zero-Sheet Barycentric Dispersion Turning Law

**Date:** 2026-05-20  
**Series:** W(3,3) Theory of Everything  
**Status:** VERIFIED FINITE TURNING LAW FOR BARYCENTRIC GAP ENTROPY/CONCENTRATION

---

## Why this part exists

MCXXVII established a directed wallward flow of barycentric witness coordinates along a finite
real-slice ladder. The natural next question is how the *distribution* of barycentric gaps behaves:
does it sharpen monotonically, spread monotonically, or turn?

---

## The theorem (finite ladder form)

Fix cutoff $X=10^5$ and the sampled ladder
\[
 s\in\{0.5,1.0,1.5,2.0,2.5,3.0\}.
\]
Let $g_i(s)$ be the five positive barycentric gaps and define
\[
H(s)=-\sum_i g_i(s)\log g_i(s),
\qquad
C(s)=\sum_i g_i(s)^2.
\]
In the generated packet:

1. the dominant gap is always the interior-to-softening gap;
2. the wall gap decreases strictly at every step;
3. entropy follows the sign pattern
   \[
   (+,+,+,-,-),
   \]
   so it rises up to $s=2.0$ and then falls;
4. concentration follows the dual sign pattern
   \[
   (-,-,-,+,+),
   \]
   so it falls up to $s=2.0$ and then rises.

Hence the sampled ladder has a finite dispersion turning point at
\[
s=2.0,
\]
with maximal barycentric entropy and minimal quadratic concentration.

---

## Reading

MCXXVII gave direction (wallward drift). MCXXVIII adds shape: the barycentric gap distribution is
most spread near the middle of this sampled ladder and becomes more concentrated again for larger
sampled $s$.

So the finite zero-sheet barycentric dynamics now has two verified components:

1. **transport direction** (witnesses move wallward, wall gap shrinks), and
2. **dispersion geometry** (entropy up then down; concentration down then up).

This is a finite, sampled-law result, not a full asymptotic claim in $s$.

---

## Executable artifact

- Module: `w33/cyclotomic.py`
- Analysis: `analysis/w33_zero_sheet_barycentric_dispersion_turning.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_zero_sheet_barycentric_dispersion_turning.json`
- Result: `PART_MCXXVIII_zero_sheet_barycentric_dispersion_turning_results.json`
