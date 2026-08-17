# Passes 5872–5879 — coherent closure, exact Radon sequence, all-field rank-metric graph, Clifford lift, and three outside-box probes

This packet starts from the collision-clean Pass5848–5855 matrix/Fourier carrier and the independently developed Pass5856–5862 doily/lattice packet. Every finite claim below is replayed from definitions by `analysis/w33_pass5872_5879_coherent_css_rankmetric_clifford_discriminant.py`; literature is used to identify established graph/code/Clifford contexts, not to inflate novelty.

## Pass 5872 — determinant-polar commutation plus unit difference closes to the 15-orbital O+(4,2) coherent configuration

Put `V=M2(F2)`, `q(X)=det X`, and polarize

\[
B(X,Y)=q(X+Y)+q(X)+q(Y).
\]

Start with the five ordered-pair colors determined by diagonal status, `q(X+Y)`, and `B(X,Y)`. One exact coherent/WL refinement produces 15 colors and the next refinement is stable:

\[
\boxed{5\longrightarrow15\longrightarrow15}.
\]

Independently enumerate all 20,160 elements of `GL4(2)`. Exactly 72 preserve determinant, giving `O^+(4,2)`. Its action on the 256 ordered pairs has exactly 15 orbitals, with sizes

\[
1,6,6,6,9,9,9,12,18,18,18,36,36,36,36,
\]

and the 15 coherent-refinement classes equal those orbitals objectwise. Thus the two relations recover the full orbital coherent configuration of the determinant stabilizer. Because the 16 vertices split into `{0}`, nine rank-one matrices, and six units, this is a three-fibre coherent configuration, not a homogeneous association scheme.

The orbital algebra has dimension 15 and center dimension 4. A generic central element has isotypic ranks `1,3,4,8`; the corresponding restricted commutant dimensions are `1,9,1,4`. Therefore over the complex numbers

\[
\boxed{\mathcal A\cong \mathbb C\oplus\mathbb C\oplus M_2(\mathbb C)\oplus M_3(\mathbb C)}.
\]

Equivalently the 16-point permutation module has multiplicity pattern

\[
\boxed{1^3\oplus\varepsilon\oplus V_{4,a}\oplus2V_{4,b}}.
\]

This is the clean representation-theoretic closure of the doily/rook pair.

## Pass 5873 — the local Reye code does not embed as a q=5 CSS check subcode

The local characteristic-two Reye kernel is

\[
C_R=[12,4,6],\qquad W_{C_R}(z)=1+12z^6+3z^8.
\]

The all-odd point-code theorem already gives, at `q=5`, the footprint check code

\[
C_F=[156,65,12]_2
\]

and CSS code

\[
[[156,26,6]]_2.
\]

Therefore a supported/zero-extended copy of `C_R` cannot lie in `C_F`: a weight-six Reye word would contradict `d(C_F)=12`.

There is a stronger shortening no-go. For any chosen 12 global coordinates, every nonzero word of the shortening of `C_F` to those coordinates has weight at least 12, hence must have the full 12-set as support. Thus such a shortening has dimension at most one, not four:

\[
\boxed{\dim\operatorname{Short}_{S}(C_F)\le1\quad(|S|=12).}
\]

This kills the most literal local-to-global CSS-check identification. It does **not** kill every possible relation to the logical normalizer `C_W`, whose q=5 minimum distance is also six; the repo still has no certified canonical map from the moving 12 cover labels to the 156 W(3,5) point coordinates. Pass5876 below supplies the actual exact local interface.

## Pass 5874 — the rook graph is the first member of an all-field rank-metric SRG family

For every finite field `F_r`, define a Cayley graph on `M2(F_r)` by

\[
X\sim Y\iff \det(X-Y)\ne0.
\]

This is the complement of the classical bilinear-forms graph `H_r(2,2)`, whose adjacency is rank-one difference. Fourier characters indexed by dual matrices split by rank 0/1/2 and give the exact spectrum

\[
\boxed{
 k^1,
 \quad r^{\,k},
 \quad[-r(r-1)]^{(r-1)(r+1)^2}},
\]

where

\[
k=r(r-1)^2(r+1)=|GL_2(r)|.
\]

Hence the graph is strongly regular with

\[
\boxed{
(v,k,\lambda,\mu)=
\bigl(r^4,
 r(r-1)^2(r+1),
 r(r^3-2r^2-r+3),
 r(r-1)(r^2-r-1)\bigr)}.
\]

The producer checks every additive character at prime anchors `r=2,3,5,7` using exact cyclotomic coefficient identities, not floating point. The first two examples are

\[
(16,6,2,2),\qquad(81,48,30,27).
\]

Thus Pass5854's `L2(4)` graph is precisely the binary member.

For the automorphism boundary, this is standard bilinear-forms-graph territory. Skresanov's Proposition 3.7, citing the classical distance-transitive graph literature, gives for `m=2`

\[
\operatorname{Aut}H_r(2,2)
=F_r^4\rtimes\Bigl(((GL_2(r)\circ GL_2(r))\rtimes\operatorname{Aut}F_r)\rtimes C_2\Bigr),
\]

with the final involution exchanging tensor factors. Complementation leaves the automorphism group unchanged. At `r=2` this has order 1152, recovering the affine determinant normalizer.

Prior-art anchor: S. V. Skresanov, *On 2-closures of rank 3 groups*, arXiv:2007.14696; bilinear-forms graphs themselves are classical distance-regular graphs.

## Pass 5875 — the 72 Pauli-label isometries lift to a Clifford-conjugate non-entangling subgroup

The 72 linear maps from matrix determinant geometry to the Saniga–Planat–Pracna Pauli quadratic frame form a torsor for the 72-element hyperbolic orthogonal group `O^+(4,2)`. The ambient symplectic group preserving Pauli commutation has order

\[
|Sp_4(2)|=720,
\]

so the ten hyperbolic quadrics form one orbit of size `720/72=10`.

To make the Clifford boundary explicit, introduce the standard tensor-factor quadratic

\[
q_{NE}=s(x_1,z_1)+s(x_2,z_2),
\qquad s(x,z)=x+z+xz.
\]

On the 15 nonzero Pauli labels, `q_NE=0` on the nine two-body Paulis and `q_NE=1` on the six one-body Paulis. Exhaustive `GL4(2)` search finds 72 isometries from the SPP quadratic to this standard form; one basis map is recorded in the certificate. Conjugation carries the SPP stabilizer exactly onto the standard 72-element stabilizer.

The projective two-qubit Pauli group contributes 16 elements, so the Clifford preimage has projective order

\[
\boxed{16\cdot72=1152}.
\]

Kubischta–Teixeira independently classify the non-entangling two-qubit Clifford group generated by local Clifford gates plus `SWAP` and list exactly projective order 1152. Therefore the lift obtained here is **Clifford-conjugate** to that non-entangling group. This does not assert that the original SPP coordinate frame is already the standard tensor-product frame.

Prior-art anchor: E. Kubischta and I. Teixeira, *Classification of the Subgroups of the Two-Qubit Clifford Group*, arXiv:2409.14624.

## Pass 5876 — the 2-primary firewall becomes an exact kernel/image/cokernel theorem

Let `T_R` be the saturated integral map induced by `R^T` between the common nine-dimensional lattices

\[
A_3^3\longrightarrow A_3\otimes A_3.
\]

The exact integer calculation sharpens dramatically:

\[
\boxed{T_R^T G_L T_R=4G_P},
\qquad
\det T_R=-64,
\qquad
\operatorname{SNF}(T_R)=1^5 2^2 4^2.
\]

Reduce modulo two. The four-dimensional kernel, mapped back into the ambient 12 point coordinates through the saturated `A3^3` basis, is **exactly** the complete Reye code:

\[
\boxed{\ker\bar T_R=C_R=[12,4,6]}
\]

objectwise, not just dimensionally. The five-dimensional image is exactly the radical of the mod-two line Gram form:

\[
\boxed{\operatorname{im}\bar T_R=\operatorname{Rad}(A_3\otimes A_3\pmod2)}.
\]

Hence

\[
\boxed{0\to C_R\to\mathbb F_2^9\xrightarrow{\bar T_R}\operatorname{Rad}(A_3\otimes A_3)\to0}.
\]

The remaining mod-two cokernel has dimension four. The even-lattice quadratic

\[
q_L(x)=\frac{x^TG_Lx}{2}\pmod2
\]

vanishes on the radical and therefore descends to that quotient. In the canonical greedy complement used by the verifier it is **literally**

\[
\boxed{q_L(a,b,c,d)=ad+bc=\det\begin{pmatrix}a&b\\c&d\end{pmatrix}}.
\]

Its 16 values split `10+6`; the nine nonzero isotropic classes and six anisotropic classes are exactly the determinant/Pauli `9+6` geometry.

This is the strongest bridge in the packet: the same integral Radon morphism places

- the Reye `[12,4,6]` code in its mod-two **kernel**,
- the five-dimensional lattice radical in its **image**, and
- the determinant/two-qubit plus-type four-space in its mod-two **cokernel**.

The integral cokernel remains `(Z/2)^2 x (Z/4)^2`; these three objects are related by the morphism and must not be collapsed into one another.

## Pass 5877 — outside-box arithmetic: quadratic determinant character is an all-odd Fourier eigenfunction

Let `r` be odd, let `chi` be the quadratic multiplicative character on `F_r` extended by `chi(0)=0`, and put

\[
f(X)=\chi(\det X).
\]

With Frobenius trace pairing on `M2(F_r)`, direct character-sum reduction gives

\[
\boxed{\widehat f(Y)=r^2\chi(-1)\chi(\det Y)}.
\]

In particular the transform vanishes on rank-zero and rank-one dual labels and is supported exactly on the units. Exact cyclotomic replays at `r=3,5,7` give scalar factors `-9,+25,-49` respectively.

This is not claimed as a new general theory: determinant is a relative invariant of a prehomogeneous vector space, and finite-field Fourier/character-sum functional equations of that type are established prior art. The useful result here is the explicit 2x2 formula and its fit to the repo's rank-stratified Fourier carrier.

Prior-art boundary: Kazhdan–Polishchuk, *Generalized character sums associated to regular prehomogeneous vector spaces*, arXiv:math/9906173; Cluckers–Herremans, *The Fundamental Theorem of prehomogeneous vector spaces modulo p^m*, arXiv:math/0408139.

## Pass 5878 — outside-box geometry: q=3 has a genuine nonlinear maximum-MRD orbit

For `Gamma_3` on the 81 matrices over `F3`, exhaustive maximal-clique enumeration gives

\[
\boxed{9072\text{ maximal }6\text{-cliques}+648\text{ maximum }9\text{-cliques}}.
\]

The maximum size nine is the MRD size for minimum rank distance two in `2x2` matrices. There are 130 linear two-planes in `F3^4`, of which exactly 18 are anisotropic: every nonzero matrix in the plane is invertible. Their nine affine cosets give

\[
18\cdot9=162
\]

affine-linear maximum cliques.

Under the full standard rank-isometry generators—translations, left/right `GL2(3)`, and transpose—the 648 maximum cliques split into exactly two orbits:

\[
\boxed{162+486}.
\]

Every clique in the first orbit has affine-span dimension two; every clique in the second has affine-span dimension four. Therefore the 486-object orbit consists of genuinely nonlinear maximum rank-distance sets.

This is an exact q=3 census, not an all-q classification. MRD codes and their connections to semifields/nonlinear constructions are established prior art; see J. Sheekey, *MRD Codes: Constructions and Connections*, arXiv:1904.05813.

## Pass 5879 — outside-box coding: the primal and dual minimum shells reconstruct both Reye configurations

The Reye code has dual

\[
C_R^\perp=[12,8,3]
\]

with exact weight enumerator

\[
1+16z^3+39z^4+48z^5+48z^6+48z^7+39z^8+16z^9+z^{12}.
\]

The 16 weight-three supports of `C_R^perp` are exactly the original 16 Reye triples. Meanwhile the 12 weight-six supports of `C_R` are exactly the heavy six-sets from Pass5849.

Across the `16 x 12=192` primal/dual minimum-shell pairs,

\[
|L\cap H|=0\quad(48\text{ pairs}),
\qquad
|L\cap H|=2\quad(144\text{ pairs}).
\]

Every triple is disjoint from three heavy words and every heavy word is disjoint from four triples. Thus the disjointness relation is itself a `12_4,16_3` Reye incidence—the second Reye copy of Pass5798.

So the pair `(C_R,C_R^perp)` is minimum-shell self-reconstructing:

\[
\boxed{
C_R^\perp\text{ min shell}=\text{original Reye lines},\quad
C_R\text{ min shell}=\text{heavies},\quad
\text{disjointness}=\text{dual Reye incidence}.}
\]

## Reproduction

```bash
python analysis/w33_pass5872_5879_coherent_css_rankmetric_clifford_discriminant.py
python -m pytest -q tests/test_w33_pass5872_5879_coherent_css_rankmetric_clifford_discriminant.py
```

## Evidence boundary

All promoted statements are exact finite algebra, coding theory, integral lattice theory, finite Fourier analysis, graph theory, or source-backed group identification. The two-qubit statement is a Clifford-conjugacy statement for Pauli-label geometry; it is not a physical embedding of the q=5 cover. The q=5 local code is explicitly **not** promoted to a CSS check subcode. No continuum dynamics, particle assignment, mass, coupling, threshold, or experimental prediction is inferred.
