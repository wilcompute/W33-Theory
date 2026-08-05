# Passes 3701–3714 — D4/F4 triality, 45 octad axes, Lagrangian contexts, and polarization

**Status:** exact source packet complete; semantic certificate

`17e8e1caaa48587b8feb5678963358b1a18961efd933858f677ca42e5713c644`.

This packet executes the five open fronts after Passes 3670–3686 and two independent outside-the-box constructions. It preserves Passes 3694–3700 as prior art: that parallel packet constructed the 36-spread ETF and its Norton algebra, proved the first unbranched-panel obstruction, and retained Monster words and class fusion as fail-closed targets. The present packet works on the distinct 45-object octad carrier and strengthens the panel, triality, axial, and lattice conclusions.

## 1. Binary resolution of the ternary panels

An unbranched rank-preserving cover cannot change a three-chamber panel into a two-chamber panel: the local residue cardinality is inherited by every sheet. A nontrivial resolution must therefore alter the rank or the local exchange group.

The exact outer extension

\[
U_4(2){:}2\cong O^-_6(2)
\]

contains 576 outer involutions. For each of the four exact order-three generators \(g_i\), exactly 108 outer involutions satisfy

\[
s g_i s=g_i^{-1}.
\]

There is no involution that inverts all four simultaneously. Thus the four ternary colors admit no common-sheet rank-five Coxeterization.

A more permissive lift writes each color as a product of two involutions,

\[
g_i=a_i b_i.
\]

For every pair of colors, exhaustive comparison of all \(108^2\) choices gives at least two cross-color noncommuting pairs. Including one noncommuting pair within each color, any eight-involution realization has at least

\[
4+6\cdot2=16
\]

noncommuting edges. A rank-eight string diagram has only seven adjacent pairs. Therefore no color-split string-Coxeter lift preserves the exact four-generator target.

This is stronger than the first thickness obstruction: it blocks both a common outer sheet and every separated two-involution-per-color string construction.

## 2. The 135 frames are three-qubit Lagrangian contexts

Model \(U_4(2)\) as the derived subgroup of \(O^-_6(2)\) on the 36 anisotropic points of a minus quadratic form on \(\mathbb F_2^6\). The symplectic polar space \(W(5,2)\) has exactly 135 Lagrangian three-spaces. Every such seven-point commuting heptad splits as

\[
3\text{ singular}+4\text{ anisotropic}.
\]

The four anisotropic points are exactly one maximal \(K_4\) in the 36-chamber graph. Hence the previously found 135 chamber frames are not an isolated clique census:

\[
\boxed{
\{135\text{ chamber }K_4\text{s}\}
=
\{135\text{ Lagrangian three-spaces of }W(5,2)\}.
}
\]

This supplies a direct three-qubit Pauli-context interpretation of the chamber frames.

### The incidence code

Let \(M\) be the \(135\times36\) binary frame–anisotropic-point incidence matrix. Exact row reduction gives

\[
\operatorname{rank}_{\mathbb F_2}M=29.
\]

Its seven-dimensional dual has weight enumerator

\[
\boxed{1+63z^{16}+63z^{20}+z^{36}.}
\]

Objectwise, the dual is exactly the restriction to \(q(x)=1\) of every affine-linear function

\[
x\longmapsto B(a,x)+c.
\]

The 27 nonzero singular labels yield weight 16; the 36 anisotropic labels yield weight 20; complementation exchanges the two halves.

## 3. Three frames per octad: the 45-object quotient

For each maximal chamber \(K_4\), its order-192 stabilizer acts on the forty W33 points with orbits

\[
8+32.
\]

The small orbit is an octad. Across all 135 frames there are exactly 45 distinct octads, with exactly three frames over each octad:

\[
\boxed{135=45\cdot3.}
\]

The three frames over an octad are pairwise disjoint and their twelve chamber points induce

\[
3K_4.
\]

Two octads intersect in either zero or two W33 points. The census is

\[
270\text{ disjoint pairs},\qquad720\text{ pairs meeting in two points}.
\]

Disjointness gives

\[
\boxed{\operatorname{SRG}(45,12,3,3)},
\]

with spectrum

\[
12^1\oplus3^{20}\oplus(-3)^{24}.
\]

This is the exact degree-45 rank-three \(U_4(2)\) carrier, now reached by an objectwise frame-to-octad quotient rather than by matching parameters.

## Bonkers I — a 45-vector two-distance tight frame

Associate to each octad \(O\) the centered projector vector

\[
u_O(i)=
\begin{cases}
48,&i\in O,\\
-12,&i\notin O.
\end{cases}
\]

Then

\[
\langle u_O,u_O\rangle=23040,
\]

and for distinct octads

\[
\langle u_O,u_{O'}\rangle=
\begin{cases}
-5760,&O\cap O'=\varnothing,\\
1440,&|O\cap O'|=2.
\end{cases}
\]

The \(45\times45\) Gram matrix has spectrum

\[
43200^{24}\oplus0^{21}.
\]

Thus the 45 octad axes form an exact rank-24 two-distance tight frame. This is a second, inequivalent finite frame beside the 36-spread ETF of Passes 3694–3700.

## 4. The order-192 group is exactly the D4 Weyl group

A frame stabilizer \(H\) has order 192. Its action on the four frame points is the full \(S_4\); the kernel has order eight, is elementary abelian, and there is an explicit order-24 complement. Hence

\[
H\cong C_2^3\rtimes S_4\cong W(D_4).
\]

The order census is

\[
1^1\,2^{43}\,3^{32}\,4^{84}\,6^{32}.
\]

The center has order two. For the central quotient extension, the exact section cocycle equation \(\delta f=c\) over \(\mathbb F_2\) has coefficient rank 95 but augmented rank 96. Therefore the central quotient does not split. This gives the previously observed non-split tomotope lift a precise cohomological certificate.

## 5. The triality normalizer and full F4 closure

The three \(D_4\) frames over one octad have common normalizer of order 576 in \(U_4(2)\). It permutes the three frames and is the kernel of the sign of the induced frame permutation inside the full \(F_4\) Weyl action.

Passing to the outer extension \(U_4(2){:}2\) doubles the octad stabilizer to order 1152. Its faithful 24-point orbit was compared orbital by orbital with the action of the standard reflection group on the 24 short roots of \(F_4\). A colored orbital isomorphism conjugates the two permutation groups exactly. Consequently

\[
\boxed{
W(D_4)\;(192)
<
W(F_4)_{\mathrm{even\ frame}}\;(576)
<
W(F_4)\;(1152).
}
\]

The three chamber \(K_4\)s over an octad are the three triality frames.

## 6. Axial constraints on the 45 canonical lines

Let \(m_0\) and \(m_1\) be the two basis products of the complete
\(U_4(2)\)-equivariant commutative Frobenius envelope from Passes 3670–3686. For a canonical octad vector \(u\),

\[
m_0(u,u)=36u,
\qquad
m_1(u,u)=-216u.
\]

For \(m_t=m_0+t m_1\), the normalized axis exists for \(t\ne1/6\). The simultaneous left-multiplication eigenpairs are

\[
(36,-216)^1,
\quad
(28,152)^6,
\quad
(-12,-168)^8,
\quad
(-12,72)^9.
\]

The three non-axis Peirce eigenvalues are therefore

\[
\frac{28+152t}{36-216t},
\quad
\frac{-12-168t}{36-216t},
\quad
\frac{-12+72t}{36-216t}.
\]

Exhaustive exact rational comparison with the Monster 2A Majorana target

\[
\left\{0,\frac14,\frac1{32}\right\}
\]

finds no parameter \(t\). Thus the entire two-dimensional equivariant product plane fails the 2A Peirce spectrum on these 45 canonical axes. This is a no-go for this axis family, not a rejection of nonassociative axial algebra in general.

## 7. Monster search refinement

The four-parabolic target remains fail-closed: no serialized `mmgroup` words were found in the checked maximal-subgroup database or documentation. That database targets maximal Monster subgroups, whereas \(U_4(2)\) is non-maximal.

The internal candidate fingerprint is now much stronger. Any concrete Monster embedding must transport:

- 135 subgroups of type \(W(D_4)\);
- 45 octad normalizers with inner order 576 and outer order 1152;
- the degree-45 rank-three action with suborbits \(1+12+32\);
- the \(\operatorname{SRG}(45,12,3,3)\) intersection carrier;
- the three-frame triality partition over every octad.

This packet does not promote a subgroup embedding without Monster words and an independent image-order/class-fusion certificate.

## 8. Polarizations of \(II_{24,24}\)

Write the indefinite even-unimodular Gram matrix as

\[
\mathcal G=
\begin{pmatrix}
G&I\\
I&0
\end{pmatrix}.
\]

The graph of an integral matrix \(B\) has Gram matrix

\[
\boxed{G+B+B^\mathsf T.}
\]

For any even integral symmetric rank-24 matrix \(H\), choose

\[
B_{ii}=\frac{H_{ii}-G_{ii}}2,
\qquad
B_{ij}=H_{ij}-G_{ij}\;(i<j),
\qquad
B_{ji}=0.
\]

Then \(G+B+B^\mathsf T=H\). Hence \(II_{24,24}\) is a universal graph-polarization container for every even integral rank-24 lattice.

An explicit executable choice \(H=E_8^3\) gives a positive-definite unimodular child with determinant one. Using the standard external theorem that the Leech lattice is even, unimodular, rootless, and rank 24, the same formula proves that a primitive rootless graph section exists as well. No explicit Leech basis is frozen here.

### Symmetry firewall

The rank-24 carrier is irreducible, so a \(U_4(2)\)-equivariant rational polarization is scalar:

\[
B=mI.
\]

For \(m\ge0\), \(G+2mI\) has determinant greater than one. At \(m=-1\), the leading \(15\times15\) principal minor equals

\[
-171492398337997406208,
\]

so the form is not positive definite; smaller \(m\) cannot repair it. Therefore

\[
\boxed{
\text{no }U_4(2)\text{-equivariant positive-definite unimodular graph polarization exists.}
}
\]

The universal existence of a Leech section is consequently not W33-specific. A meaningful bridge must identify a canonical symmetry-breaking polarization or a weaker surviving subgroup.

## Evidence boundary

### Exact here

- strengthened common-sheet and rank-eight string Coxeterization no-go;
- 135 Lagrangian contexts and their seven-dimensional affine code;
- exact 135-to-45 triality quotient;
- \(\operatorname{SRG}(45,12,3,3)\) and rank-24 tight frame;
- explicit \(W(D_4)\), nontrivial central cocycle, order-576 triality normalizer, and full \(W(F_4)\) closure;
- 45-axis 2A Majorana spectrum no-go;
- graph-polarization universality, explicit \(E_8^3\) child, and equivariant unimodularity no-go.

### Still open

- a regular abstract-polytope cover of the ternary chamber system;
- concrete Monster words and observed image order;
- an explicit frozen Leech basis and canonical Leech section;
- a Majorana, Griess, or VOA realization;
- remote CI/PDF evidence;
- any physical or laboratory claim.
