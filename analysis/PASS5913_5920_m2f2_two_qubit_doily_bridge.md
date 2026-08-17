# Passes 5913–5920 — object-level M2(F2) / two-qubit doily bridge

## Executive theorem

The `1+9+6` Fourier/rank stratification already present in the q=5 matrix carrier is not merely numerically reminiscent of two-qubit geometry. On the underlying 4-dimensional binary matrix space there is an explicit symplectic isomorphism.

For

\[
M=\begin{pmatrix}a&b\\c&d\end{pmatrix}\in M_2(\mathbb F_2),
\]

define

\[
\Phi(M)=(a,d,b,c)=(x_1,z_1,x_2,z_2).
\]

Then

\[
\det M=ad+bc=x_1z_1+x_2z_2=q_0(\Phi(M)),
\]

and polarization gives

\[
\det(M+N)+\det M+\det N
=
\langle\Phi(M),\Phi(N)\rangle_{\rm sp}.
\]

Thus determinant polarization is exactly the standard two-qubit Pauli commutation form.

## Pass5913 — symplectic isometry

The map `Phi` is a bijection from the 16-element additive space `M2(F2)` to `F2^4`. The determinant becomes the standard plus-type quadratic form

\[
q_0(x)=x_1z_1+x_2z_2.
\]

Two nonzero matrices are orthogonal under the determinant polarization iff the corresponding two-qubit Pauli classes commute.

## Pass5914 — the 15 nonzero matrices are a doily model

Deleting the zero matrix leaves 15 points. Their commuting graph has exact parameters

\[
\boxed{\operatorname{SRG}(15,6,1,3)},
\]

which is the point graph of the generalized quadrangle `W(3,2)`, the two-qubit doily.

This is an object-level finite symplectic identification, not just a matching cardinality.

## Pass5915 — the rank split is the 9+6 grid/complement split

Among the 15 nonzero matrices:

- 9 have determinant zero, hence rank one;
- 6 have determinant one, hence are the units `GL2(2)`.

The rank-one sector is literally

\[
\{uv^T:0\ne u,v\in\mathbb F_2^2\},
\]

so it is a `3 x 3` grid. Two rank-one matrices commute iff they share the same left factor or the same right factor. Its induced graph is

\[
\operatorname{SRG}(9,4,1,2),
\]

the rook graph / hyperbolic quadric `Q+(3,2)=GQ(2,1)`.

The six units induce `K3,3`. Cross commutation is biregular:

\[
9\cdot2=6\cdot3=18.
\]

So the full doily decomposes exactly as the 9-point grid plus its six-point complementary/dual packet.

## Pass5916 — explicit match to Saniga–Planat–Pracna's displayed 9-grid

The 2007 `Geometry of Two-Qubits` source identifies the 15 Pauli classes with a 15-point subconfiguration of `P1(M2(GF(2)))` and states that its 9+6 factorization is the split into a grid and its dual.

Using their displayed operator assignment `C1,...,C15`, the particular nine-point grid `C7,...,C15` is the zero set

\[
q_0(x)+x_2=0.
\]

Now apply the local phase Clifford on qubit 2,

\[
S_2:(x_1,z_1,x_2,z_2)\mapsto(x_1,z_1,x_2,z_2+x_2).
\]

It is symplectic and obeys

\[
q_0(S_2x)=q_0(x)+x_2.
\]

Therefore

\[
\boxed{S_2(\{C_7,\ldots,C_{15}\})=\{M\ne0:\det M=0\}.}
\]

This closes the coordinate gap explicitly: the source grid and the determinant/rank-one grid are locally Clifford-conjugate.

## Pass5917 — the complete doily hyperplane census

All quadratic forms with the same symplectic polarization are

\[
q_v(x)=q_0(x)+\langle v,x\rangle.
\]

Enumerating `v in F2^4` gives:

- 10 plus-type forms, each with 9 nonzero zeros: the ten grids;
- 6 minus-type forms, each with 5 nonzero zeros: the six ovoids;
- 15 symplectic perp sets `p^perp\setminus{0}`, one for each nonzero point.

For every minus-type form, the 5-point zero set is an ovoid (no commuting pair) and the 10-point complement induces the Petersen graph.

Thus the matrix determinant model reproduces exactly the classical doily hyperplane census quoted in the two-qubit source:

\[
\boxed{10\text{ grids},\quad6\text{ ovoids},\quad15\text{ perp-sets}.}
\]

## Pass5918 — closing the Pass5876 Radon quotient

Pass5876 produced a 4-dimensional mod-2 quotient carrying the determinant quadratic form with value distribution

\[
10+6.
\]

The present theorem identifies that quotient completely:

- zero class + 9 nonzero `q=0` classes;
- 6 `q=1` classes;
- nonzero classes form `W(3,2)`;
- the `q=0` shell is the 9-grid;
- the `q=1` shell is the six-point complement.

So the mod-2 Radon discriminant quotient is not an anonymous 4-space anymore; it is a canonical two-qubit doily geometry up to the explicit finite symplectic coordinate choice.

## Pass5919 — ring-line boundary

The source emphasizes that `M2(F2)` has 16 ring elements: six units and ten zero-divisors. Our affine split is therefore exactly

\[
1+9+6
=
\{0\}
+\{\text{nonzero zero-divisors}\}
+\{\text{units}\}.
\]

However, the 15 nonzero ring elements are **not literally** the source's 15 projective-ring-line points `C1,...,C15`; those are equivalence classes of admissible pairs in `P1(M2(F2))`. What is proven is stronger and cleaner than a literal identification: both coordinate systems realize the same `W(3,2)` commutation geometry, and an explicit local Clifford maps the displayed source grid to the determinant grid.

## Pass5920 — evidence boundary

This sharpens the old Pass5797 boundary from a `9+6` analogy to an object-level finite symplectic theorem.

It does **not** imply that the q=5 W33 carrier is physically a two-qubit Hilbert space, that its six-unit sector is an entanglement class, or that any continuum/particle/hardware identification follows. The certified statement is the finite quotient geometry only.

## External source alignment

The source used for the comparison is:

Metod Saniga, Michel Planat and Petr Pracna, *Geometry of Two-Qubits* (2007 talk / associated projective-ring-line work).

The source explicitly states:

- `M2(GF(2))` has six units and ten zero-divisors;
- the relevant two-qubit configuration has 15 Pauli operators;
- the `9+6` factorization is a grid plus its dual;
- `W(2)` / `W(3,2)` has 15 points and 15 lines;
- the geometric hyperplanes consist of 6 ovoids, 15 perp-type hyperplanes and 10 grids;
- the `10+5` factorization is an ovoid plus a Petersen-graph complement.

The verifier independently reconstructs each finite-geometric statement needed for the bridge.
