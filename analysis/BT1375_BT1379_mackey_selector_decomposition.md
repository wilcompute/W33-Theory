# Passes 1375–1379 — Exact Mackey decomposition of the selector algebra

## Scope

Let \(X\) be the 120 line-matching selectors of \(W(3,3)\), and let \(H\) be the stabilizer of one selector in

\[
G=\operatorname{PGSp}(4,3)\cong W(E_6).
\]

Pass 1371 proved directly from the literal permutation action that

\[
H\cong C_3^3\rtimes(D_8\times C_2).
\]

The present packet explains the complete rational decomposition of

\[
\mathbb Q^X
\]

and therefore the 83-dimensional orbital algebra

\[
\operatorname{End}_H(\mathbb Q^X)
\]

by exact Mackey/little-group theory.

## Pass 1375 — Complete little-group character table

Write

\[
N=O_3(H)\cong C_3^3,
\qquad
K=H/N\cong D_8\times C_2.
\]

The complement acts faithfully on \(N\cong\mathbb F_3^3\). Its action on the dual group \(\widehat N\) has exactly six orbits, of sizes

\[
\boxed{1,2,4,4,8,8}.
\]

The corresponding little groups have orders

\[
16,8,4,4,2,2
\]

and types

\[
D_8\times C_2,\quad D_8,\quad V_4,\quad V_4,\quad C_2,\quad C_2.
\]

Inducing every little-group irreducible gives all 27 irreducible characters of \(H\). Exact arithmetic in

\[
\mathbb Z[\omega],\qquad \omega^2+\omega+1=0,
\]

shows that all character values are rational integers. Their degree census is

\[
\boxed{1^8,\;2^6,\;4^9,\;8^4},
\]

and

\[
8\cdot1^2+6\cdot2^2+9\cdot4^2+4\cdot8^2=432=|H|.
\]

Thus the rational group algebra is split:

\[
\boxed{
\mathbb QH\cong
\mathbb Q^8\oplus M_2(\mathbb Q)^6\oplus
M_4(\mathbb Q)^9\oplus M_8(\mathbb Q)^4.
}
\]

## Pass 1376 — The 120-selector permutation character

The permutation character of \(H\curvearrowright X\) contains exactly 14 of the 27 irreducibles. Their degree profile is

\[
\boxed{1,1,1,2,2,2,4,4,4,4,8,8,8,8},
\]

and their multiplicity profile is

\[
\boxed{1,1,1,1,1,1,1,2,2,3,3,3,4,5}.
\]

The dimension identity is

\[
\sum_i d_i m_i=120,
\]

while Schur’s lemma gives

\[
\boxed{
\dim\operatorname{End}_H(\mathbb Q^X)
=\sum_i m_i^2
=83.
}
\]

This derives the orbital-algebra dimension directly from representation multiplicities rather than orbital enumeration.

## Pass 1377 — Exact Mackey/Wedderburn identification

For every nonzero constituent \(\chi\), the exact character projector

\[
e_\chi=
\frac{\chi(1)}{|H|}
\sum_{h\in H}\chi(h^{-1})\rho_X(h)
\]

was constructed in the 83-orbital coordinate basis. Each of the fourteen projectors is exactly equal—not merely conjugate or numerically close—to one of the rational primitive central projectors from Passes 1365–1374.

Consequently the matrix sizes in

\[
\boxed{
\operatorname{End}_H(\mathbb Q^X)
\cong
\mathbb Q^7\oplus M_2(\mathbb Q)^2\oplus
M_3(\mathbb Q)^3\oplus M_4(\mathbb Q)\oplus M_5(\mathbb Q)
}
\]

are precisely the multiplicities of the fourteen Mackey constituents.

## Pass 1378 — Why the Terwilliger center has dimension ten

The full orbital algebra has fourteen primitive central sectors, while the selector Terwilliger algebra has ten. Exact projector containment shows:

- seven Mackey sectors are already separated by the Terwilliger generators;
- the remaining seven sectors fuse into three scalar packets of sizes

\[
\boxed{2,2,3}.
\]

Therefore the center defect is

\[
\boxed{
(2-1)+(2-1)+(3-1)=4=14-10=83-79.
}
\]

The geometric splitter from Pass 1366 resolves these three packets. On the seven multiplicity-one orbital blocks it acts by scalar eigenvalues; on repeated constituents it is correctly retained as a non-scalar matrix in the multiplicity space.

## Pass 1379 — Boundary

This is an exact finite representation-theory theorem reconstructed from the literal 120-point permutation group. It uses no database character table, floating eigensolver, or numerical group-name inference.

The result does not identify particle multiplets, gauge fields, generations, cosmological sectors, optical components, or laboratory observables.
