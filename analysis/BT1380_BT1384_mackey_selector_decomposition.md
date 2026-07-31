# Passes 1380–1384 — Exact Mackey decomposition of the selector algebra

## Collision-safe scope

The computation was first developed under a provisional 1375–1379 label. A parallel release claimed Passes 1375–1378 before merge, so this independent packet is canonically renumbered 1380–1384. The exhaustive implementation and remotely observed digest are retained byte-for-byte; only release labels and public artifact paths changed.

Let \(X\) be the 120 line-matching selectors of \(W(3,3)\), and let \(H\) be one selector stabilizer. Pass 1371 had proved from the literal permutation action that

\[
H\cong C_3^3\rtimes(D_8\times C_2).
\]

## Pass 1380 — Complete little-group character table

Writing \(N=O_3(H)\cong C_3^3\) and \(K=H/N\cong D_8\times C_2\), the action of \(K\) on \(\widehat N\) has six orbits:

\[
\boxed{1,2,4,4,8,8}.
\]

Their little groups have orders \(16,8,4,4,2,2\) and types

\[
D_8\times C_2,\quad D_8,\quad V_4,\quad V_4,\quad C_2,\quad C_2.
\]

Exact induction in \(\mathbb Z[\omega]\) constructs all 27 irreducible characters. Every character value is a rational integer, with degree census

\[
\boxed{1^8,\;2^6,\;4^9,\;8^4}.
\]

Thus

\[
\mathbb QH\cong
\mathbb Q^8\oplus M_2(\mathbb Q)^6\oplus
M_4(\mathbb Q)^9\oplus M_8(\mathbb Q)^4.
\]

## Pass 1381 — Selector permutation character

Exactly fourteen irreducibles occur in \(\mathbb Q^X\). Their degrees are

\[
1,1,1,2,2,2,4,4,4,4,8,8,8,8,
\]

and their multiplicities are

\[
1,1,1,1,1,1,1,2,2,3,3,3,4,5.
\]

Therefore

\[
\sum_i d_i m_i=120,
\qquad
\boxed{\sum_i m_i^2=83}.
\]

This derives the orbital-commutant dimension without orbital enumeration.

## Pass 1382 — Exact Mackey/Wedderburn identification

For every nonzero constituent, the exact character projector

\[
e_\chi=\frac{\chi(1)}{|H|}\sum_{h\in H}\chi(h^{-1})\rho_X(h)
\]

is literally equal to one of the fourteen rational orbital central projectors. Consequently

\[
\boxed{
\operatorname{End}_H(\mathbb Q^X)
\cong
\mathbb Q^7\oplus M_2(\mathbb Q)^2\oplus
M_3(\mathbb Q)^3\oplus M_4(\mathbb Q)\oplus M_5(\mathbb Q)
}
\]

and the matrix sizes are exactly the selector multiplicities.

## Pass 1383 — Character explanation of the Schur defect

The orbital center has fourteen sectors while the Terwilliger center has ten. Seven sectors are already separated; the remaining seven fuse into packets of sizes

\[
\boxed{2,2,3}.
\]

Hence

\[
\boxed{(2-1)+(2-1)+(3-1)=4=14-10=83-79}.
\]

The geometric splitter resolves these packets with scalar eigenvalue sets

\[
\{-3,3\},\qquad \{-3,0\},\qquad \{-4,-1,2\}.
\]

## Pass 1384 — Reproducibility and boundary

The corrected remote exact workflow completed successfully. The exhaustive implementation digest is

```text
dbcf6881622b3e1cdd694d1e345eadce309eae0550e23e348ba446ca603bee74
```

and the collision-safe canonical compact certificate digest is

```text
0ec8be0272896594c7013691a1f2516d08bdcc08cf97049297b69e594f953152
```

This is finite rational representation theory reconstructed from the literal permutation group. No database character table, floating eigensolver, particle identification, hardware claim, or laboratory claim is used.
