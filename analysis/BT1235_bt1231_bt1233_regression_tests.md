# BT1235 -- BT1231--BT1233 Regression Tests

## Purpose

BT1235 converts the latest Clifford/R3 artifacts into executable regression coverage.

## Protected claims

The test file protects three claims:

1. BT1231: the exact minimal projective-transvection count for `Sp(4,3)` is four.
2. BT1232: the R3 validator is fail-closed and does not promote a near-candidate.
3. BT1233: the compressed `Sp(4,3)` word metric has the fixed sphere and ball fingerprints.

## Exact asserted values

BT1231 asserts:

\[
\binom{40}{3}=9880,
\qquad
\max_{m\le 3}|\langle g_1,\ldots,g_m\rangle|=648,
\qquad
m_{\min}=4.
\]

BT1232 asserts:

\[
\texttt{near\_candidate\_promoted}=\texttt{false},
\qquad
\texttt{certified\_candidate\_promoted}=\texttt{true}.
\]

BT1233 asserts:

\[
|G|=51840,
\qquad
\operatorname{diam}=14,
\qquad
(|B_4|,|B_8|,|B_{12}|,|B_{14}|)=(534,14994,51803,51840).
\]

## File

- Test: `tests/test_bt1231_bt1233.py`

## Boundary

This is regression coverage for already-built witness scripts. It does not replace independent hardware tomography or K3 metric certification.
