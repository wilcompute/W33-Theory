# BT893 — Grade Yukawa Reflection Degeneracy Theorem

This finishes and corrects the CKM computation queued after BT891 and the failed first BT893 attempt in `ClaudeLastResponse.txt`.

## Input

BT891 gives the derived grade-selection rule for the cubic Yukawa skeleton:

\[
g_a+g_b+g_H\equiv 0\pmod 3.
\]

At the generation-grade level this gives one nonzero entry in every row and every column.

## Correction

The resulting support matrix is not a pure cyclic shift.  It is the shifted reflection

\[
Y_g[a,b]=1
\quad\Longleftrightarrow\quad
b\equiv -a-g\pmod 3.
\]

So the three Higgs-grade skeletons are the three reflections of

\[
D_3\cong S_3,
\]

not the three rotations.

Explicitly:

\[
Y_0=
\begin{pmatrix}
1&0&0\\
0&0&1\\
0&1&0
\end{pmatrix},\qquad
Y_1=
\begin{pmatrix}
0&0&1\\
0&1&0\\
1&0&0
\end{pmatrix},\qquad
Y_2=
\begin{pmatrix}
0&1&0\\
1&0&0\\
0&0&1
\end{pmatrix}.
\]

Each matrix is a symmetric involution:

\[
Y_g^T=Y_g,
\qquad
Y_g^2=I.
\]

Each has singular values

\[
1,1,1.
\]

## Product law

The product of two Higgs-grade reflections is a generation rotation:

\[
Y_{g_u}Y_{g_d}=R_{g_u-g_d}.
\]

The three reflections generate the full flavor group

\[
\langle Y_0,Y_1,Y_2\rangle\cong S_3,
\]

with order histogram

\[
1^1,
\quad 2^3,
\quad 3^2.
\]

Distinct Higgs-grade skeletons do not commute; their commutator Frobenius norm squared is always

\[
6.
\]

## Physics interpretation

This strengthens the honest boundary around BT891.

The exact grade skeleton fixes:

1. the allowed Yukawa support,
2. the three reflection axes of the flavor group,
3. the relative generation rotation between two Higgs-grade choices.

But it does **not** determine physical CKM/PMNS angles by itself. Since

\[
Y_gY_g^T=I
\]

for every grade skeleton, the grade-level left mass operator is triply degenerate. Thus the grade-level skeleton is maximally constrained but numerically angle-blind.

Therefore:

\[
\boxed{
\text{observable hierarchy and mixing must come from the within-grade }q^2=9\text{ Higgs profiles.}
}
\]

This is cleaner than the failed pure-shift assertion: the leading grade law gives an exact finite flavor/reflection skeleton, while the CKM/PMNS numbers live in the residual within-grade layer.

## Verified checks

The executable verifier `analysis/bt893_grade_yukawa_reflection_degeneracy.py` checks:

- T1: support is `b=-a-g mod 3`.
- T2: each `Y_g` is a symmetric involution with singular values `[1,1,1]`.
- T3: `Y_gu Y_gd = rotation(gu-gd)`.
- T4: the three skeletons generate `S3 ~= D3`.
- T5: distinct skeletons are noncommuting reflections.
- T6: the grade mass operator is the identity, so CKM/PMNS angles require the `q^2=9` within-grade profile.
