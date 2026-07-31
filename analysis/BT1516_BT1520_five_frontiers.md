# Passes 1516–1520 — Relations, canonical Fourier form, atlas obstruction, arithmetic support, and equivariant Morita closure

**Status:** exact derived certificate complete.  
**Certificate SHA-256:** `603380fbc9370b97b08273a67785b43f9c52960610d84661f99228bbe020ab48`

This packet executes the five continuations left by Passes 1500–1504. It is deliberately derived from the frozen Passes 1370–1374 and 1500–1504 certificates: no expensive worker is silently replaced by a new implementation, and every inference boundary is explicit.

## Pass 1516 — The first exact relation layer beyond the Gabriel quiver

Let

\[
S=A/J,\qquad B=J/J^2.
\]

The Ext\(^1\) quiver identifies the split \(S\)-bimodule \(B\). Hence the canonical map

\[
T_S(B)\longrightarrow \operatorname{gr}_J(A)
\]

is surjective, and its homogeneous kernel dimensions are computable from the frozen quiver and Loewy data.

### Characteristic two

The weighted tensor-path dimensions in degrees \(0,1,2,3\) are

\[
38,\ 29,\ 45,\ 59,
\]

whereas the radical-graded dimensions are

\[
38,\ 29,\ 16,\ 0.
\]

Therefore the exact relation-space dimensions are

\[
0,\ 0,\ \boxed{29},\ 59.
\]

The Gabriel graph has six connected components:

\[
\{0,3,6\},\ \{1,9\},\ \{2,4\},\ \{5,12\},\ \{7,8,10\},\ \{11\}.
\]

The last is an isolated degree-\(3\) simple vertex, hence a semisimple \(M_3(\mathbb F_2)\) block of algebra dimension \(9\).

### Characteristic three

The weighted tensor-path dimensions in degrees \(0\) through \(6\) are

\[
11,\ 23,\ 92,\ 333,\ 1231,\ 4560,\ 16952,
\]

while the radical-graded dimensions are

\[
11,\ 23,\ 22,\ 13,\ 10,\ 4,\ 0.
\]

Thus the relation-space dimensions are

\[
0,\ 0,\ \boxed{70},\ 320,\ 1221,\ 4556,\ 16952.
\]

The characteristic-three quiver is connected. Its quadratic relation defect is already \(70\), compared with \(29\) in characteristic two.

**Boundary.** These are exact homogeneous kernels in the radical-associated graded algebra. They do not yet separate minimal cubic and higher generators from consequences of quadratic relations, and they are not represented as the complete Ext\(^2\) or Yoneda multiplication table.

## Pass 1517 — Coordinate-free selector Fourier theorem

Write the selector module as an \(H\)-module in the canonical isotypic form

\[
V\cong\bigoplus_{\chi} U_\chi\otimes W_\chi,
\qquad
U_\chi=\operatorname{Hom}_H(W_\chi,V).
\]

The fourteen multiplicity/irreducible-degree pairs are

\[
(1,1),(1,2),(1,2),(1,4),(1,4),(1,8),(1,8),
(2,1),(2,2),(3,4),(3,4),(3,8),(4,8),(5,1).
\]

They satisfy the three exact double-centralizer identities

\[
\sum_\chi m_\chi d_\chi=120,
\qquad
\sum_\chi m_\chi^2=83,
\qquad
\sum_\chi d_\chi^2=335.
\]

The first is the selector-module dimension; the second is the orbital commutant dimension; the third is the dimension of the dual semisimple image. The isotypic summands and evaluation map

\[
\bigoplus_\chi \operatorname{Hom}_H(W_\chi,V)\otimes W_\chi\longrightarrow V
\]

are basis-free. The Pass-1501 matrix \(U\) is one deterministic trivialization of these canonical tensor factors, not the invariant itself. Allowing bases in both factors gives a block-factorization gauge group of dimension

\[
83+335-14=404,
\]

where one scalar redundancy is removed in each of the fourteen blocks.

## Pass 1518 — Exact obstruction to a global rank-preserving \(D_4\) atlas action

The eight local masks form exactly two \(D_4\)-orbits, each of size four: the four weight-three masks and the four adjacent weight-two masks.

Assume a global \(D_4\)-action existed on the \(24=8\times3\) frozen sheets, projected to the standard mask action, and preserved sheet rank. Every sheet orbit would project onto one of the four-element mask orbits. Therefore every invariant rank level would have cardinality divisible by four.

But the exact sheet-rank distribution is

\[
70^4,\qquad 76^1,\qquad 81^{19}.
\]

The singleton rank-76 level gives an immediate contradiction. Hence

\[
\boxed{\text{no global rank-preserving }D_4\text{ lift exists on the frozen 24 sheets}.}
\]

After adjoining the four sign characters, the bridge counts become

\[
70^{16},\qquad76^4,\qquad81^{76},
\]

all divisible by four. Thus the obstruction is genuinely visible at the sheet level and is erased by the sign multiplicity at the level of rank counts alone.

The correct symmetry object is therefore chart-dependent: an action groupoid with a residual-label transport cocycle, or a transport that exits the frozen 24-sheet family.

**Boundary.** The cardinality theorem proves the nonexistence of the global lift. It does not compute the full rectangle-by-rectangle residual \(S_3\) cocycle.

## Pass 1519 — Maximal-order arithmetic: exact prime support and conductor bound

The containing maximal order has labeled split blocks

\[
\mathbb Z^7\oplus M_2(\mathbb Z)^2\oplus M_3(\mathbb Z)^3
\oplus M_4(\mathbb Z)\oplus M_5(\mathbb Z),
\]

of total \(\mathbb Z\)-rank \(83\). The exact index is

\[
[M_O:O]=2^{36}3^{113}.
\]

Consequently:

\[
\operatorname{length}_{\mathbb Z_2}(M_O/O)=36,
\qquad
\operatorname{length}_{\mathbb Z_3}(M_O/O)=113,
\]

and the orbital discriminant valuations are

\[
v_2(\operatorname{disc}O)=72,
\qquad
v_3(\operatorname{disc}O)=226.
\]

For every prime \(\ell\neq2,3\),

\[
O\otimes\mathbb Z_\ell=M_O\otimes\mathbb Z_\ell.
\]

Thus the conductor is supported only at \(2\) and \(3\). If

\[
N=2^{36}3^{113},
\]

then the finite quotient \(M_O/O\) is annihilated by \(N\), so

\[
N M_O\subseteq \mathfrak f,
\qquad
\mathfrak f=\{x\in M_O:xM_O\subseteq O\}.
\]

Componentwise, each labeled block \(M_n(\mathbb Z)\) has trivial locally free ideal class group by Morita equivalence with \(\mathbb Z\). Forgetting labels permits permutations of equal blocks, of order

\[
7!\,2!\,3!=60480,
\]

but this is a symmetry of the split maximal order, not an arithmetic ideal-class defect.

**Boundary.** Total index and discriminant do not determine the blockwise conductor exponents, Smith invariants of \(M_O/O\), or Bass/Eichler status. Those require the frozen transition matrix itself.

## Pass 1520 — The equivariant Morita obstruction vanishes after saturation

Let \(V\) be the \(120\)-dimensional selector module and \(W\) the signed \(81\)-dimensional Steinberg cycle module. Pass 1504 established the full corners

\[
A=\operatorname{End}_{\mathbb Q}(V)\cong M_{120}(\mathbb Q),
\qquad
B=\operatorname{End}_{\mathbb Q}(W)\cong M_{81}(\mathbb Q),
\]

and the saturated bridge bimodule of dimension

\[
120\cdot81=9720.
\]

Take

\[
X=\operatorname{Hom}_{\mathbb Q}(W,V),
\qquad
Y=\operatorname{Hom}_{\mathbb Q}(V,W).
\]

Composition gives the strict Morita pairings

\[
X\otimes_B Y\longrightarrow A,
\qquad
Y\otimes_A X\longrightarrow B.
\]

Surjectivity is literal on matrix units:

\[
E_{ij}=x_{i0}y_{0j},
\qquad
F_{ab}=y_{a0}x_{0b}.
\]

With the signed group representations \(\rho_V,\rho_W\), define

\[
g\cdot x=\rho_V(g)x\rho_W(g)^{-1}.
\]

The two composition pairings are equivariant. Therefore the full saturated context is a strict \(G\)-equivariant Morita equivalence, and its equivariant Brauer obstruction is zero.

This resolves the apparent contradiction with the earlier exact statement

\[
\operatorname{Hom}_G(W,V)=0.
\]

That vanishing says there is no **fixed bridge element**. It does not say the entire \(9720\)-dimensional \(G\)-module \(\operatorname{Hom}(W,V)\) fails to be an equivariant equivalence bimodule.

Thus the correct refinement of Pass 1504 is:

\[
\boxed{\text{the 75 apartment bridges are a gauge generating frame; their full corner saturation is canonically }G\text{-equivariant}.}
\]

**Boundary.** No individual apartment bridge becomes \(G\)-invariant, and there is no preferred fixed identification \(V\cong W\); their dimensions differ.

## Verification boundary

The release script recomputes every displayed integer from the frozen certificates and checks their hashes. It does not claim to have rerun the expensive Pass-1500 workers. The Pass-1516 higher-Yoneda boundary and the Pass-1518 residual-cocycle boundary remain explicit.
