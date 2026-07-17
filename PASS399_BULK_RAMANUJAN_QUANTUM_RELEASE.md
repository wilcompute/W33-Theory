# Pass 399 — The Heisenberg Bulk Cell Is a Ramanujan Network with a Quantum Revival Obstruction

**Status: certified.**  
Executable witness: `analysis/w33_pass399_bulk_ramanujan_quantum.py`  
Frozen certificate: `data/w33_pass399_bulk_ramanujan_quantum.json`

This pass concerns the `q^3`-vertex **bulk graph opposite one point** in
`W(3,q)`, not the full `(q+1)(q^2+1)`-vertex collinearity graph. Pass 394
proved that the bulk is an antipodal `q`-fold cover of `K_{q^2}`. Pass 399
diagonalizes that cover, proves its Ramanujan and Ihara properties, computes
its tree complexity, and closes an important photonic-control question:
the central phase fibres do not support any nontrivial exact continuous-time
fractional revival.

## 1. Coordinate law

Write a bulk point as

\[
v=(x,y,z)\in \mathbb F_q^3,
\]

with the central coordinate `z` parametrizing the phase fibre over
\((x,y)\in\mathbb F_q^2\). Pass 394 gives the adjacency law

\[
(x,y,z)\sim (x',y',z')
\quad\Longleftrightarrow\quad
(x,y)\ne(x',y')
\ \text{and}\ 
z'-z=yx'-xy'.
\]

Every vertex has one neighbour over each different base point, so the degree is

\[
k=q^2-1.
\]

The distance shells from a vertex are

\[
1,\quad q^2-1,\quad (q-1)(q^2-1),\quad q-1.
\]

The final shell is exactly the remainder of its central phase fibre.

## 2. Exact character diagonalization

Fourier transform in the central coordinate. For the trivial additive
character, the adjacency block is

\[
J_{q^2}-I_{q^2},
\]

with eigenvalues `q^2-1` once and `-1` with multiplicity `q^2-1`.

For a nontrivial additive character \(\chi_t\), define the symplectic Fourier
matrix

\[
H_t(u,v)=\chi_t(\omega(u,v)),
\qquad
u,v\in\mathbb F_q^2.
\]

It is Hermitian and satisfies

\[
H_t^2=q^2I.
\]

The corresponding adjacency block is \(H_t-I\). Since
\(\operatorname{tr}H_t=q^2\), the `+q` and `-q` eigenspaces of `H_t` have
dimensions

\[
\frac{q(q+1)}2,\qquad \frac{q(q-1)}2.
\]

There are `q-1` nontrivial central characters. Therefore the complete
adjacency spectrum is

\[
\boxed{
\operatorname{Spec}(A_q)=
\left\{
\begin{array}{rcl}
q^2-1 &:& 1,\\[2mm]
-1 &:& q^2-1,\\[2mm]
q-1 &:& \dfrac{q(q^2-1)}2,\\[3mm]
-q-1 &:& \dfrac{q(q-1)^2}2.
\end{array}
\right.
}
\]

The executable witness reconstructs the graphs at `q=3,5,7` and verifies the
spectrum numerically to integer precision.

For `q=3`, the 27-state register cell has

\[
\operatorname{Spec}(A_3)=
\{8^1,\,2^{12},\,(-1)^8,\,(-4)^6\}.
\]

This is distinct from the full W33 graph spectrum
\(\{12^1,2^{24},(-4)^{15}\}\).

## 3. An infinite Ramanujan family

The largest nontrivial adjacency magnitude is \(q+1\). Since

\[
(q+1)^2\le 4(q^2-2)
\qquad(q\ge3),
\]

every odd-order bulk graph is Ramanujan:

\[
\boxed{
\max_{\lambda\ne k}|\lambda|
=q+1
\le 2\sqrt{k-1}.
}
\]

The normalized random-walk contraction is even simpler:

\[
\boxed{
\frac{\max_{\lambda\ne k}|\lambda|}{k}
=\frac{q+1}{q^2-1}
=\frac1{q-1}.
}
\]

Thus the register cell becomes spectrally cleaner as the local alphabet grows:
`1/2` at `q=3`, `1/4` at `q=5`, and `1/6` at `q=7`.

## 4. Exact Hashimoto and Ihara data

Let \(m=q^3(q^2-1)/2\) and \(n=q^3\). Bass's determinant formula gives

\[
\zeta_q(u)^{-1}
=(1-u^2)^{m-n}
\prod_{\lambda\in\operatorname{Spec}(A_q)}
\left(1-\lambda u+(q^2-2)u^2\right)^{m_\lambda}.
\]

Explicitly,

\[
\boxed{
\begin{aligned}
\zeta_q(u)^{-1}
={}&(1-u^2)^{q^3(q^2-3)/2}
(1-(q^2-1)u+(q^2-2)u^2)\\
&\times(1+u+(q^2-2)u^2)^{q^2-1}\\
&\times(1-(q-1)u+(q^2-2)u^2)^{q(q^2-1)/2}\\
&\times(1+(q+1)u+(q^2-2)u^2)^{q(q-1)^2/2}.
\end{aligned}
}
\]

For every nontrivial adjacency eigenvalue, the two Hashimoto roots have modulus

\[
\boxed{\sqrt{q^2-2}}.
\]

Hence every nontrivial Ihara pole lies on

\[
|u|=\frac1{\sqrt{q^2-2}},
\]

the graph-theoretic Riemann circle.

## 5. Laplacian spectrum and routing complexity

With \(L=kI-A\),

\[
\boxed{
\operatorname{Spec}(L_q)=
\left\{
0^1,\,
(q^2)^{q^2-1},\,
[q(q-1)]^{q(q^2-1)/2},\,
[q(q+1)]^{q(q-1)^2/2}
\right\}.
}
\]

The matrix-tree theorem then gives the exact number of spanning trees:

\[
\boxed{
\tau_q=
q^{q^3+q^2-5}
(q-1)^{q(q^2-1)/2}
(q+1)^{q(q-1)^2/2}.
}
\]

For the qutrit register cell,

\[
\tau_3
=3^{31}2^{24}
=10\,362\,839\,986\,909\,376\,151\,552.
\]

This is the exact number of independent global routing backbones supported by
one 27-state Heisenberg cell.

## 6. Exact continuous-time quantum amplitudes

Let \(U(t)=e^{-itA_q}\), start at `(0,0,0)`, and let \(a_j(t)\) be the
entry amplitude to any vertex at distance `j`. Put

\[
E=e^{-iq^2t},\qquad c=\cos(qt),\qquad s=\sin(qt).
\]

Then

\[
\begin{aligned}
a_0(t)
&=\frac{e^{it}}q
\left[
1+\frac{E-1}{q^2}
+(q-1)\left(c-\frac{i}{q}s\right)
\right],\\
a_3(t)
&=\frac{e^{it}}q
\left[
1+\frac{E-1}{q^2}
-\left(c-\frac{i}{q}s\right)
\right],\\
a_1(t)
&=\frac{e^{it}}q
\left[
\frac{E-1}{q^2}
-\frac{i(q-1)}q s
\right],\\
a_2(t)
&=\frac{e^{it}}q
\left[
\frac{E-1}{q^2}
+\frac{i}{q}s
\right].
\end{aligned}
\]

The witness checks these formulas against direct matrix exponentiation.

## 7. Phase-fibre revival no-go

Exact evolution confined to the starting phase fibre requires

\[
a_1(t)=a_2(t)=0.
\]

Subtracting the two equations forces

\[
\sin(qt)=0.
\]

Substitution then forces

\[
e^{-iq^2t}=1.
\]

For odd `q`, these conditions imply

\[
t=\frac{2\pi r}{q}.
\]

At those times all four spectral phases coincide and

\[
\boxed{
U(2\pi r/q)=e^{2\pi ir/q}I.
}
\]

Therefore:

\[
\boxed{
\text{There is no nontrivial exact phase-fibre fractional revival or
perfect state transfer.}
}
\]

The graph has projective period \(2\pi/q\), but every exact return to the
phase fibre is merely scalar identity evolution. Any photonic protocol that
mixes or swaps the `q` central phase states must therefore add a control that
does not commute with native bulk adjacency; passive propagation through the
cell cannot perform that operation exactly.

## 8. Validation

The frozen certificate contains 30 passing checks:

- graph size, degree, spectrum, and distance shells at `q=3,5,7`;
- Ramanujan and normalized-radius formulas;
- nontrivial Hashimoto-circle checks;
- matrix-tree formula checks;
- closed quantum amplitudes against numerical exponentiation;
- projective-period checks.

The theorem proof uses only finite additive-character orthogonality and is
valid for every odd prime power. The executable checks use prime fields
`q=3,5,7`.

## 9. Claim boundary

The standard Bass/Hashimoto determinant machinery and the definition of a
Ramanujan graph are established graph theory. The project-specific content
here is the application to the Pass-394 Heisenberg bulk law, the resulting
closed spectrum and tree formula, and the exact phase-fibre revival
obstruction. This pass makes no claim that the full W33 graph and the
27-state bulk graph are the same object.
