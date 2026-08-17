# Passes 7065–7080 — the bent biplane is the abstract Kummer configuration

## Executive result

The `[16,6,6]` bent-function code from Pass7001 is not merely another biplane with the same parameters as a Kummer configuration.  Its sixteen minimum supports admit an **explicit linear coordinate change over `F_2`** to the classical `4 x 4` row/column model of the Kummer `16_6` configuration.

Thus the internal finite theorem is

\[
\boxed{\text{Pass7001 biplane}\cong\text{abstract Kummer }16_6\text{ configuration}.}
\]

This produces the first rigorous K3-adjacent route in the current lane: classical Kummer quartics have 16 nodes and 16 tropes in this incidence pattern, and their minimal resolutions are K3 surfaces.  The bridge is presently **incidence-level**.  A particular projective quartic and a chain map into the repo's 45-point curvature precomplex remain open.

## Pass7065 — the sixteen code blocks are translates of one quadratic support

For

\[
q_0(x)=x_0x_1+x_2x_3
\]

on `F_2^4`, its support has size six.  The sixteen minimum words in

\[
D=\langle RM(1,4),q_0\rangle
\]

have supports

\[
\mathcal B_a=\{x:q_0(x+a)=1\},\qquad a\in\mathbb F_2^4.
\]

Hence the biplane is translation-developed from a single six-set.

## Pass7066 — explicit conversion to the classical 4x4 model

Split a target vector as two binary pairs, interpreted as a row label and column label in a `4 x 4` array.  The standard cross at the origin consists of the three nonzero points in row zero together with the three nonzero points in column zero.

The matrix

\[
M=
\begin{pmatrix}
1&1&0&1\\
1&1&1&0\\
1&0&1&1\\
1&1&0&0
\end{pmatrix}
\in GL(4,2)
\]

sends the six-point support of `q0` exactly onto that cross.  Since `M` is linear,

\[
M(\mathcal B_a)=M(\mathcal B_0)+Ma,
\]

which is precisely the set of the other three points in the row of `Ma` plus the other three points in its column.

The verifier checks this equality for **all sixteen blocks**.  This gives an explicit labelled isomorphism rather than a parameter comparison.

## Pass7067 — literature identification with the Kummer 16_6

The row/column `4 x 4` realization is the classical combinatorial model of the Kummer configuration.  Independently, Catanese's treatment of Kummer quartics recalls that their sixteen singular points and sixteen tropes form a nondegenerate `(16_6,16_6)` configuration; every such projective Kummer configuration has the characteristic six-by-six incidence and the minimal resolution of a Kummer quartic is a K3 surface.

Even more relevant to the present repo, Liu and Manivel recover the Kummer `16_6` directly from the sixteen half-spin weights and identify its automorphism group as

\[
W_{Kum}\simeq W(D_6)/\{\pm1\}.
\]

Its order is

\[
\frac{|W(D_6)|}{2}=\frac{2^5\,6!}{2}=11520,
\]

exactly the full automorphism-group order independently obtained for our biplane:

\[
2^4:\!Sp(4,2)\cong2^4:\!S_6.
\]

The agreement is now structural, because the explicit `GL(4,2)` incidence isomorphism is already in hand.

## Pass7068 — fixing one Kummer node reproduces the doily split

A distinguished biplane point has six incident blocks and ten nonincident blocks.  Under the Pass7001 shortening:

- the six incident blocks, after deleting the distinguished point, become the six doily ovoids;
- the ten nonincident blocks become the ten doily grid-complement supports;
- the remaining fifteen nonzero differences from the distinguished point are naturally the fifteen coordinates of the doily code.

Thus the earlier `10+6` split acquires a classical Kummer reading:

\[
\boxed{10\text{ nonincident tropes}+6\text{ incident tropes}.}
\]

The fifteen perp words continue to occupy the middle weight-eight shell of the code; no claim is made here that they are themselves tropes.

## Pass7069 — the translation group is the correct 2-torsion-sized carrier

The point set is an affine `F_2^4` torsor and the biplane contains the full translation subgroup `2^4`.  This is exactly the finite group size appearing classically in the sixteen-node Kummer construction.  Catanese's projective description likewise organizes the sixteen nodes as a `(Z/2)^4` orbit.

This is significantly stronger than the previous K3 lane's 2,428-row dimensional analogy: the finite set, group action, and incidence design are now all the correct Kummer type.

## Pass7070 — the Levi graph is the folded six-cube

The 32-vertex node/trope incidence graph of the biplane is explicitly isomorphic to the antipodal quotient

\[
Q_6/\{x\sim x+111111\},
\]

the folded six-cube.

The verifier freezes a concrete bijection from the sixteen point vertices and sixteen block vertices to the 32 antipodal classes and checks every edge and nonedge.  Its parameters are

\[
|V|=32,\qquad |E|=96,\qquad k=6,
\]

with adjacency spectrum

\[
\boxed{6^1\oplus2^{15}\oplus(-2)^{15}\oplus(-6)^1}.
\]

This is a new, exact bridge to the repo's longstanding hypercube program: the Kummer incidence object lives naturally one dimension above the familiar folded-cube/Clebsch layer, rather than being connected to the hypercube only by the number sixteen.

## Pass7071 — the recent spinor-tenfold paper makes the E8/Kummer direction concrete

Liu–Manivel's 2025 work is unusually relevant to this project.  It studies codimension-four linear sections of the spinor tenfold, proves that their GIT moduli agree with Kummer-surface moduli, and derives the picture through a cyclic grading of `e8` involving a half-spin representation.  In the same construction the sixteen half-spin weights recover the Kummer configuration.

This gives a legitimate research program linking three structures already present in this repo:

\[
\boxed{\text{Kummer }16_6\quad\leftrightarrow\quad D_6\text{ half-spin combinatorics}\quad\leftrightarrow\quad E_8\text{ grading}.}
\]

It does **not** yet identify that E8 grading with the repo's particular `E6 x A2` grading, so that comparison remains a falsifiable next step.

## Pass7072 — what this does to the K3 evidence boundary

Pass7041 concluded that the repo had a real finite 45-point curved precomplex but no actual K3 realization.  The present result does not magically produce the missing chain map, but it improves the external side of the problem substantially.

We now have a canonical K3-related finite source object:

\[
\text{our bent code}\to\text{Kummer }16_6\to\text{nodes/tropes of a Kummer quartic}\to\text{K3 minimal resolution}.
\]

The missing part is no longer “find any K3-looking matrix.”  It is:

> choose/projectively realize the explicit Kummer configuration, lift its node/trope incidence or divisor lattice to the K3 resolution, and construct a functor/chain map from that geometric lattice into the repo's 45-point transport precomplex.

That is a precise geometric target.

## Pass7073–7080 — strict boundary

What is closed:

- explicit `GL(4,2)` isomorphism from the code biplane to the standard row/column Kummer model;
- exact Kummer `16_6` incidence parameters;
- full `11520` automorphism group from the internal code calculation;
- exact folded-six-cube Levi graph;
- point-derived `10+6` doily split.

What remains open:

- coordinates of a specific quartic in `P^3` whose node/trope labels are fixed to our binary labels;
- the associated K3 Picard/Neron–Severi lattice in those labels;
- an explicit comparison between that lattice and the 45-point transport precomplex;
- any statement identifying the finite rank-36 curvature block with K3 curvature or a K3 differential.

The correct promotion is therefore

\[
\boxed{\text{abstract Kummer configuration identified; projective K3/curvature realization open}.}
\]
