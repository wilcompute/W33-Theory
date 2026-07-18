# Pass 438 — Finite-field versus residue-ring discrimination atlas

Let \(p\) be odd and compare two order-\(p^2\) coordinate systems:

\[
R_{m field}=GF(p^2),\qquad R_{m ring}=\mathbb Z/p^2\mathbb Z.
\]

Both produce Heisenberg groups of order \(p^6\), but their central characters have different conductor structure. That difference is visible simultaneously in the adjacency spectrum and the 2-primary critical group.

## Field model

All nontrivial central characters are primitive. Setting \(q=p^2\), the native graph has four eigenvalues:

\[
(q^2-1)^1,\quad
(q-1)^{q(q^2-1)/2},\quad
(-(q+1))^{q(q-1)^2/2},\quad
(-1)^{q^2-1}.
\]

Pass 435 gives

\[
K_{GF(p^2),(2)}\cong
(\mathbb Z/2^{
u_2(p^2-1)})^{p^2(p^2-1)}
\oplus
(\mathbb Z/2^{
u_2(p^4-1)})^{p^2(p^2-1)^2/2}.
\]

## Residue-ring model

Central characters of \(\mathbb Z/p^2\mathbb Z\) occur in three conductor classes:

- the trivial character;
- \(p-1\) characters of conductor \(p\);
- \(p^2-p\) primitive characters of conductor \(p^2\).

The conductor-\(p\) Fourier form has radical \(pR^2\), so it contributes a reduced \(GF(p)\) Fourier block plus a large unit block. Primitive characters contribute the \(q=p^2\) block. Hence the ring graph has six eigenvalues:

\[
egin{array}{c|c}
	ext{eigenvalue}&	ext{multiplicity}\ \hline
p^4-1&1\
p^3-1&rac{p(p^2-1)}2\
-(p^3+1)&rac{p(p-1)^2}2\
p^2-1&rac{(p^2-p)p^2(p^2+1)}2\
-(p^2+1)&rac{(p^2-p)p^2(p^2-1)}2\
-1&(p^4-1)+(p-1)(p^4-p^2).
\end{array}
\]

Its exact 2-primary Smith shape is

\[
oxed{
egin{aligned}
K_{\mathbb Z/p^2,(2)}\cong{}&
(\mathbb Z/2^{
u_2(p-1)})^{p(p-1)}\\
&\oplus
(\mathbb Z/2^{
u_2(p^2-1)})^{p(p-1)^2/2+p^3(p-1)}\\
&\oplus
(\mathbb Z/2^{
u_2(p^4-1)})^{p^3(p-1)(p^2-1)/2}.
\end{aligned}}
\]

## Atlas entries

### \(p=3\)

\[
K_{GF(9),(2)}=(\mathbb Z/8)^{72}\oplus(\mathbb Z/16)^{288},
\]

\[
K_{\mathbb Z/9,(2)}=(\mathbb Z/2)^6\oplus(\mathbb Z/8)^{60}\oplus(\mathbb Z/16)^{216}.
\]

The ring spectrum is

\[
80^1,26^{12},8^{270},(-1)^{224},(-10)^{216},(-28)^6.
\]

### \(p=5\)

\[
K_{GF(25),(2)}=(\mathbb Z/8)^{600}\oplus(\mathbb Z/16)^{7200},
\]

\[
K_{\mathbb Z/25,(2)}=(\mathbb Z/4)^{20}\oplus(\mathbb Z/8)^{540}\oplus(\mathbb Z/16)^{6000}.
\]

### \(p=7\)

\[
K_{GF(49),(2)}=(\mathbb Z/16)^{2352}\oplus(\mathbb Z/32)^{56448},
\]

\[
K_{\mathbb Z/49,(2)}=(\mathbb Z/2)^{42}\oplus(\mathbb Z/16)^{2184}\oplus(\mathbb Z/32)^{49392}.
\]

## Discriminator

The field model has one nontrivial conductor and two torsion periods. The residue-ring model has two nontrivial conductors and three torsion periods. The additional lowest-order period is the clean experimental feature used by Pass 439.
