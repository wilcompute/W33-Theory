# The Steiner atlas closes the monomial Qpsi normalizer question

The preceding address/operator compiler left a precise question: could a
different trinification chart make a non-FI power of the anchored Qpsi clock
normalize the landed two-qutrit execution algebra?  The answer is no throughout
the complete Weyl-compatible monomial atlas:

\[
\boxed{\langle D_{12}\rangle\cap
N\!\left(I_9\otimes M_9(\mathbb C)\right)
=\langle D_{12}^{4}\rangle\cong C_3.}
\]

In particular, matter parity \(D_{12}^{6}\) does not normalize the execution
algebra in any of the 51,840 charts.  This strengthens the earlier fixed-chart
commutant calculation: changing the Steiner/trinification monomial gauge cannot
rescue the parity operation.

## 1. The cubic itself recovers the 40 Steiner partitions

Let \(C\) be the \(45\times27\) zero-one incidence matrix whose rows are the
supports of the 45 monomials of the Cartan cubic.  Exact row reduction gives

\[
\operatorname{rank}_{\mathbb F_3}C=21,
\qquad \dim_{\mathbb F_3}\ker C=6.
\]

The executable certificate exhausts all \(3^6=729\) kernel words.  Of these,
510 use each symbol exactly nine times.  Exactly 240 have the stronger cubic
support split

\[
45=18\ \hbox{monochromatic determinant terms}
   +27\ \hbox{rainbow trace terms}.
\]

The six permutations of the three symbols label the same unordered
\(9+9+9\) partition, so the 240 words give exactly 40 partitions.  The program
then reconstructs the repository's previously certified 120 Steiner nonets
from the double-sixes and proves set equality between these 40 kernel
partitions and the prior 40 triads of nonets.  This is an equality of explicit
point sets, rather than a count match.

The 120 Steiner trihedral pairs and their grouping into 40 triads are classical
and already owned by
`analysis/w33_e6_120_steiner_trihedral_pairs.py`,
`manuscripts/parts/PART_MCCCXCVI_E6_120_STEINER_TRIHEDRAL_PAIRS.md`, and
Pass 4870.  Manivel describes the 27-dimensional \(E_6\) module, its 45 cubic
monomials, and the \(\mathfrak{sl}_3^3\) triple-system decomposition in
[Configurations of lines and models of Lie algebras](https://arxiv.org/abs/math/0507118).
The new increment is the executable kernel recovery and its use as a complete
coordinate atlas for the Qpsi test.

## 2. One conservation code contains the 36-40-45 triangle

The full kernel is a ternary code with parameters

\[
\boxed{K_{\rm cub}=[27,6,12]_3}
\]

and exact weight enumerator

\[
W_K(z)=1+72z^{12}+510z^{18}+144z^{21}+2z^{27}.
\]

This is a ternary code on the cubic-surface lines.  It is distinct from the
repository's earlier binary \([27,6,12]_2\) code arising from line/double-six
incidence.

The constant word belongs to \(K_{\rm cub}\), because every cubic support has
three entries.  Quotient by that invariant line and projectivize:

\[
\mathbb P\!\left(K_{\rm cub}/\langle\mathbf1\rangle\right)
\cong PG(4,3),\qquad
\frac{3^5-1}{3-1}=121.
\]

Each projective ray has six lifts in the original code: three constant
translates and their two scalar orientations.  The exact \(W(E_6)\) action on
these rays is faithful of order 51,840 and has three orbits,

\[
\boxed{121=36+40+45.}
\]

All three orbits now have objectwise cubic-surface meanings:

- The 72 weight-12 words occur in opposite pairs with 36 distinct supports.
  Those supports equal the 36 previously certified double-sixes.
- The 240 balanced words with 18 monochromatic cubics give, after the six
  colour relabellings, the 40 prior Steiner triads.
- The remaining 270 balanced words have 12 monochromatic and 33 rainbow
  cubics.  Their 45 colour-free partitions map bijectively to the 45
  tritangents: the 12 monochromatic cubics are exactly the 12 other
  tritangents meeting the distinguished one.

Solving the invariant-form equations on the induced five-dimensional module
produces a nondegenerate quadratic form over \(\mathbb F_3\).  With its scale
fixed by the prior convention, the norm classes are

\[
Q=0:\ 40\ {\rm Steiner\ triads},\qquad
Q=1:\ 45\ {\rm tritangents},\qquad
Q=2:\ 36\ {\rm double\!-\!sixes}.
\]

Passes 4863--4864 already owned the abstract \(PG(4,3)\) norm-class sizes
\(40,45,36\) and identified the 36-class with the double-six graph.  The
representation-level identity \(40+36+45=121\) was also already recorded.
The increment here is the single conservation code and the two missing
objectwise identifications of its 40- and 45-orbits.

There is also a dual chain-level connection.  For the same incidence map
\(R:\mathbb F_3^{45}\to\mathbb F_3^{27}\),

\[
\dim\ker R^{T}=6,\qquad \dim\ker R=24.
\]

The six-dimensional point kernel is the charge/chart code used here.  The
24-dimensional line kernel is the cubic-holonomy space from the earlier
Pass 7364 lane; quotienting its certified 14-dimensional boundary span leaves
the prior ten-dimensional global holonomy sector.  Charge conservation and
cubic holonomy are therefore the two null spaces of one matrix.

## 3. Forty partitions expand to one regular 51,840-chart atlas

For each Steiner partition, order its three nonets as the sectors

\[
(3,\bar3,1),\qquad(1,3,\bar3),\qquad(\bar3,1,3).
\]

Pairwise rainbow incidence splits the points into the three shared
three-valued factor coordinates.  There are six sector assignments and
\(6^3\) independent relabellings of those shared coordinates.  Hence each
partition supports

\[
6\cdot 6^3=1296
\]

labelled tensor charts, and the full atlas has

\[
40\cdot1296=51840
\]

distinct charts.  The exact Weyl permutations generated from the minuscule
27 have order 51,840.  Acting on one chart produces the entire atlas with no
repetition.  Thus the atlas is a regular \(W(E_6)\)-torsor, while an unordered
partition has stabilizer order 1,296.  Dolgachev records the same classical
index-40 \(A_2^3\) subgroup structure in
[Classical Algebraic Geometry](https://sites.lsa.umich.edu/idolga/wp-content/uploads/sites/1334/2024/08/CAG.21.pdf).

For every one of the \(27\cdot40=1080\) anchor/partition pairs, the Qpsi
charges have the same nonet profile.  The nonet containing the anchor has

\[
\{4^1,-2^4,1^4\},
\]

and each other nonet has \(\{-2^3,1^6\}\).

## 4. A factorization lemma turns normalization into finite arithmetic

A labelled chart identifies the 27 weights with \((m,q)\), where
\(m\in\{0,\ldots,8\}\) is the multiplicity address and
\(q\in\mathbb F_3\) is the internal active coordinate.  The external active
coordinate \(p\in\mathbb F_3\) is invisible to Qpsi.  Thus

\[
D_{12}^{k}|m,q,p\rangle
=\zeta_{12}^{\,kQ(m,q)}|m,q,p\rangle .
\]

Every unitary normalizer of \(I_9\otimes M_9(\mathbb C)\) factors as
\(A\otimes B\): conjugation induces an inner automorphism on the matrix
factor, and removing it leaves an element of the commutant
\(M_9\otimes I_9\).  If the normalizer is diagonal in the displayed product
basis, both factors are diagonal.  Consequently the exponent table must be
additively separable modulo 12,

\[
kQ(m,q)=\alpha_m+\beta_q\pmod {12},
\]

or equivalently every anchored \(2\times2\) additive minor must vanish.
This criterion is necessary and sufficient for these diagonal clock powers.

Exhausting all 51,840 charts gives the number of normalizing charts for powers
\(k=0,\ldots,11\):

\[
(51840,0,0,0,51840,0,0,0,51840,0,0,0).
\]

Weyl equivariance carries the calculation from the checked anchor to all 27
anchors.  The only normalizing powers are therefore \(0,4,8\), exactly the
scalar FI/common-H27 \(C_3\) already found in the commutant.

## 5. The obstruction is sharply one cell in the best gauges

For matter parity, reduce the \(9\times3\) charge table modulo two.  There are
2,048 distinct separable binary tables \(a_m+b_q\), after fixing the one-bit
global gauge redundancy.  The exact minimum Hamming-distance census over the
atlas is

\[
\begin{array}{c|ccc}
\text{distance}&1&5&6\\\hline
\text{charts}&5760&34560&11520.
\end{array}
\]

For one fixed chart the 27 anchors split as \(3+18+6\) across those same
distances.  The certificate stores an explicit best chart.  Its parity table
differs from a separable normalizer in one \((m,q)\) cell.  Because Qpsi is
independent of the external coordinate, that cell lifts to the three basis
states

\[
(m,q,p_0),\quad(m,q,p_1),\quad(m,q,p_2)
\]

in Matter81.  So the smallest diagonal correction has support three on the
81-state carrier.  This is an exact interface cost; it does not prove that the
correction is generated dynamically or fault tolerantly.

## 6. Computational meaning and boundary

The result removes a chart ambiguity from the virtual machine.  No
Weyl-compatible monomial relabelling turns matter parity into a legal tensor
normalizer of the current Pauli243 execution algebra.  A compiler has two
honest options: restrict the native Qpsi clock to its \(C_3\) subgroup, or add
an address-conditioned phase interface.  The best gauges reduce that interface
to one \((m,q)\) condition, repeated over the external qutrit.

The theorem does not choose a physical Steiner chart or vacuum, prove that the
repair gate is physically available, or identify observed particles with
individual minuscule weights.  Parallel representation audits sharpen the
root-gauge boundary: an H27-equivariant map has maximum rank 9 in dimension
27, and a full K-equivariant compiler has maximum rank 27 in dimension 81.
An invertible equivariant conjugacy is therefore impossible.  The later
K-Fourier-coordinate compiler closes the finite conversion with exactly 54
representation retypings, saturating the lower bound.  Materializing its
composition with the frozen root/address and operator bases, and realizing the
retypings dynamically, remain open.  The present theorem exhausts the finite
monomial chart family and the diagonal powers of the anchored Qpsi clock
independently of that physical realization.

## Reproducible artifacts

- Producer: `analysis/w33_steiner_trinification_qpsi_normalizer.py`
- Frozen certificate: `data/w33_steiner_trinification_qpsi_normalizer.json`
- Regression test: `tests/test_w33_steiner_trinification_qpsi_normalizer.py`
