# Passes 5840–5847 — Matrix determinant normalizer, two-qubit doily, and all-field Radon frontier

## Why this packet exists

The live `master` frontier moved rapidly through Passes 5792–5831:

- 5792–5799 identified the q=5 local 16-space with the **additive** matrix space `M2(F2)`, carrying the affine left/right unit action of order 576 and an outer transpose normalizer.
- 5816–5823 Fourier-diagonalized the 16-line carrier into `1 + W9 + V6`, where the nonzero Fourier labels split by matrix rank as `9 + 6`.
- 5824–5831 showed that the common rational `W9` has inequivalent integral realizations: `A3^3` on point/heavy carriers versus `A3 tensor A3` on the line carrier, with a purely 2-primary mismatch.

A parallel lane then landed a different theorem packet under the already-reserved 5832–5839 numbering. The current namespace file still records the earlier reservation, while theorem files from the parallel lane also use that range. This packet therefore **abandons 5832–5839 as contaminated** and continues at 5840–5847.

## Pass 5840 — full affine determinant normalizer

Enumerating all `|GL(4,2)|=20160` linear maps on `M2(F2)` gives exactly

\[
|\operatorname{Stab}_{GL(4,2)}(\det)|=72.
\]

The original left/right action contributes

\[
GL(2,2)\times GL(2,2),\qquad 6\cdot 6=36,
\]

and transpose supplies the disjoint second coset. Hence

\[
\boxed{O^+(4,2)\cong (GL(2,2)\times GL(2,2)):C_2}
\]

in this concrete matrix model, and the full affine determinant-preserving group is

\[
\boxed{2^4:O^+(4,2)},\qquad |G|=16\cdot72=1152.
\]

Its center is trivial.

## Pass 5841 — the 2-primary lattice shadow is now explicit

The rational `W9` equivalence does **not** survive integrally.

Point/heavy:

\[
L_{PH}=A_3^3,
\qquad
A_{L_{PH}}\cong (\mathbb Z/4)^3.
\]

Modulo two, the Gram form has rank six and radical dimension three.

Line:

\[
L_L=A_3\otimes A_3,
\qquad
A_{L_L}\cong (\mathbb Z/4)^4\times\mathbb Z/16.
\]

Modulo two, the Gram form has rank four and radical dimension five.

Thus the dimensions of the mod-2 radicals equal the 2-torsion ranks of the respective discriminant groups:

\[
\boxed{3\text{ versus }5}.
\]

The Walsh sublattice quotients sharpen the mismatch further:

\[
L_{PH}/W_{PH}\cong (\mathbb Z/2)^6,
\]

whereas

\[
L_L/W_L\cong (\mathbb Z/2)^4\times(\mathbb Z/4)^4.
\]

This is an exact code/lattice boundary: rational equivalence is not binary or integral equivalence.

## Pass 5842 — all-field matrix Fourier/Radon theorem

Let `T=M2(F_q)` over any finite field. The additive Fourier labels split by matrix rank:

\[
q^4
=
1+N_1+N_2,
\]

with

\[
\boxed{N_1=(q-1)(q+1)^2}
\]

rank-one labels and

\[
\boxed{N_2=q(q-1)^2(q+1)=|GL(2,q)|}
\]

rank-two labels.

For the point-fibre Fourier carrier, nontrivial pairs `(w,phi)` number

\[
(q^2-1)^2.
\]

Each rank-one matrix label has exactly `q-1` factorizations, so the Radon map has rank-one image dimension `N1` and kernel

\[
\boxed{(q-2)(q-1)(q+1)^2}.
\]

Therefore

\[
\boxed{q=2\text{ is the unique multiplicity-free case}.}
\]

At `q=2`, every nonzero `(w,phi)` gives a distinct rank-one Fourier label. For every larger field, the point-fibre Fourier sector contains a nonzero factorization kernel before it reaches the rank-one matrix sector.

This explains why the exact `W9` point/line identification is unusually sharp in the binary local model and should **not** be naively extrapolated to arbitrary field order.

## Pass 5843 — determinant-polar doily

On the four-dimensional binary vector space

\[
V=M_2(\mathbb F_2),
\]

define

\[
q(X)=\det X.
\]

Its polar form

\[
B(X,Y)=q(X+Y)+q(X)+q(Y)
\]

has matrix

\[
\begin{pmatrix}
0&0&0&1\\
0&0&1&0\\
0&1&0&0\\
1&0&0&0
\end{pmatrix}
\]

and rank four. It is therefore a nondegenerate alternating form.

The fifteen nonzero matrices are exactly the fifteen points of

\[
\boxed{W(3,2)}.
\]

The matrix-rank split is

\[
15=9+6.
\]

The nine rank-one matrices are the zero locus of `det`, hence the hyperbolic quadric

\[
\boxed{Q^+(3,2)\cong P^1(\mathbb F_2)\times P^1(\mathbb F_2)},
\]

which is the `3 x 3` grid. There are six isotropic lines contained entirely in the grid and nine remaining doily lines meeting the grid in one point each. The six invertible matrices form the complementary six points.

This is the exact incidence-level bridge to the standard two-qubit doily `9+6` decomposition.

### Object-level boundary

Saniga–Planat–Pracna use **15 projective-ring points** in a subconfiguration of `P1(M2(F2))`. The present theorem uses the **15 nonzero ring elements as vectors** in `PG(3,2)`. These are not literally the same objects. They are two coordinatizations of the same abstract `W(3,2)` geometry.

## Pass 5844 — grid stabilizer and transpose as ruling swap

The full symplectic group of the determinant polar form has

\[
|Sp(4,2)|=720.
\]

The determinant quadric/grid stabilizer has order

\[
72,
\]

so its orbit has size

\[
720/72=10.
\]

This matches the ten grid hyperplanes of `W(3,2)`.

The 36-element left/right matrix group preserves the two rulings separately. Transpose exchanges them. Thus

\[
\boxed{36\xrightarrow{\ +\ \mathrm{transpose}\ }72}
\]

is exactly the passage from ruling-preserving symmetry to the full grid stabilizer.

## Pass 5845 — the order-1152 `W(F4)` temptation is false

The affine determinant group has order

\[
1152.
\]

So does `W(F4)`. They are **not isomorphic**.

The verifier independently generates `W(F4)` from four standard simple-root reflections and finds

\[
|W(F4)|=1152,
\qquad
|Z(W(F4))|=2,
\]

with central `-I`.

The affine determinant group is centerless:

\[
|Z(2^4:O^+(4,2))|=1.
\]

Therefore

\[
\boxed{2^4:O^+(4,2)\not\cong W(F4)}.
\]

Shared order is numerology here, not a group identification.

## Pass 5846 — explicit mod-2 radical geometry

The 3-dimensional point/heavy radical is simply one fibre-constant parity vector in each of the three `A3` blocks.

For the line lattice,

\[
\operatorname{rad}(A_3\otimes A_3\bmod2)
=
\{\mathbf1\otimes a+b\otimes\mathbf1\},
\]

so

\[
\dim=3+3-1=5.
\]

This is an exact row-plus-column parity gauge structure on the `3 x 3` rank-one label grid. It is a finite 2-primary lattice defect only; no physical gauge-boson or error-syndrome interpretation is asserted.

## Pass 5847 — release boundary

The packet is intended to ship with byte-stable replay tests and an isolated CI workflow. Publication language must preserve four firewalls:

1. `M2(F2)` ring elements are not the same objects as projective-ring points.
2. Abstract `W(3,2)` incidence equivalence is not a physical two-qubit identification of the q=5 W33 carrier.
3. Rational `W9` equivalence is not integral or mod-2 equivalence.
4. Equal group order `1152` does not imply `W(F4)`.

## External prior art

Primary source used for the two-qubit boundary:

- M. Saniga, M. Planat, P. Pracna, *Projective Ring Line Encompassing Two-Qubits*, arXiv:quant-ph/0611063; later Theoretical and Mathematical Physics 155 (2008) 905–913.

That work identifies a 15-point projective-ring subconfiguration with the two-qubit Pauli commutation geometry `W(3,2)` and describes its `9+6` factorization. The determinant-polar coordinatization proved here is new repo work and is stated only as an isomorphism of the abstract finite geometry.
