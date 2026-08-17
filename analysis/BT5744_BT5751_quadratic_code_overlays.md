# Passes 5744--5751 — quadratic code / symplectic-overlay frontier

## Executive result

The characteristic-3 collapse of the W33 non-collinearity matrix does **not** define a new classical code.  The underlying ternary code is prior art.  What the repo had not made explicit is the exact coordinate bridge and the resulting architecture split:

\[
\boxed{
\text{ambient quadratic code}
\quad+\quad
\text{selectable symplectic polarity}
\quad=\quad
\text{reconfigurable W33 routing overlay}.
}
\]

A single 40-coordinate ternary quadratic code supports exactly

\[
\boxed{234}
\]

distinct nondegenerate symplectic W33 overlays.  Changing the alternating form changes which 40 of the 130 projective lines are W33-native while leaving the 10-dimensional code space fixed.

That is the machine-level breakthrough of this packet.

## Prior-art firewall

Two earlier results absorb most of the raw coding-theory parameters.

1. **B. G. Rodrigues, 2008**, *Self-orthogonal designs and codes from the symplectic groups S4(3) and S4(4)*, Discrete Mathematics 308 (2008), 1941--1950, DOI 10.1016/j.disc.2007.04.047.  In the degree-40 representation, the orbit-27 design is the 2-(40,27,18) complement of the 2-(40,13,4) point/hyperplane design of PG(3,3).  Rodrigues proves that its ternary code is self-orthogonal [40,10,18]_3 and that its dual is [40,30,4]_3 with 260 weight-4 words.  The full design/code automorphism group is L4(3):2_1.

2. **K. Kaipa and P. Pradhan, 2024**, *Higher weight spectra of ternary codes associated to the quadratic Veronese 3-fold*, arXiv:2405.12011.  They define the quadratic Veronese code C3 as the second-order projective Reed--Muller code obtained by evaluating all ten degree-2 monomials on the 40 points of PG(3,3), and compute its ternary higher-weight spectra.

Accordingly, this packet does **not** claim novelty for [40,10,18]_3, its dual [40,30,4]_3, the 260 weight-4 dual words, projective Reed--Muller codes, or the Veronese embedding.

## Pass 5744 — exact W33-to-Veronese coordinate bridge

Let the 40 points be the projective points of \(PG(3,3)\), represented by nonzero vectors \(x\in\mathbb F_3^4\) modulo scalar.

Let

\[
V(x)=
(x_0^2,x_0x_1,x_0x_2,x_0x_3,x_1^2,x_1x_2,x_1x_3,x_2^2,x_2x_3,x_3^2)
\]

be the quadratic Veronese feature vector.  The resulting \(40\times10\) evaluation matrix has rank 10.

Choose the standard nondegenerate alternating form \(J\) on \(\mathbb F_3^4\).  W33 collinearity is

\[
x\sim y \iff x^TJy=0.
\]

Over \(\mathbb F_3\), every nonzero scalar squares to one.  Therefore the matrix

\[
C_J(x,y)=(x^TJy)^2
\]

is exactly the **non-collinearity adjacency matrix**: zero on the diagonal and W33 neighbors, one on non-neighbors.

For fixed \(x\), the row \(C_J(x,-)\) is the square of a linear form and therefore a quadratic evaluation word.  The verifier proves

\[
\operatorname{rank}_{\mathbb F_3} C_J=10
\]

and

\[
\boxed{
\operatorname{rowspan}_{\mathbb F_3}(C_J)
=
\operatorname{rowspan}_{\mathbb F_3}(V^T).
}
\]

Thus the W33 characteristic-3 non-collinearity module is exactly the known quadratic Veronese code, now with an explicit symplectic generator matrix.

The replayed ordinary weight distribution is

\[
0^1,
18^{1560},
24^{21060},
27^{18800},
30^{16848},
36^{780},
\]

so the code is [40,10,18]_3, consistent with the prior literature.

## Pass 5745 — a 40 -> 10 -> 40 finite-field compiler

The verifier constructs an exact factorization

\[
\boxed{C_J=V B_J V^T\pmod 3}
\]

for the selected symplectic polarity.  In the fixed quadratic-monomial basis, \(B_J\) is symmetric, invertible, and involutory:

\[
B_J^2=I_{10}.
\]

It has only 10 nonzero entries: exactly one nonzero entry in every row and column.

The direct 40x40 non-collinearity matrix has 1080 nonzero entries.  The two Veronese legs contain 216 nonzeros each, and the core contains 10, giving the structural coefficient count

\[
216+10+216=442.
\]

Hence the explicit factorization replaces 1080 direct coefficient incidences by 442 finite-field coefficient incidences, a ratio

\[
\boxed{1080/442\approx2.44344}.
\]

This is a finite-field compiler count, **not** a measured latency or photonic-loss speedup.

## Pass 5746 — square-zero generator and CSS consequence

The W33 complement is SRG(40,27,18,18), so over characteristic three its adjacency identity collapses to

\[
C_J^2=0.
\]

The verifier checks this directly.  Therefore

\[
\operatorname{rowspan}(C_J)\subseteq\operatorname{rowspan}(C_J)^\perp.
\]

Combining the known dimensions and the exact dual distance from the next pass gives the standard q-ary CSS consequence

\[
\boxed{[[40,20,4]]_3}.
\]

This quantum parameter set is recorded as a standard consequence of the known classical self-orthogonal code; it is not claimed as a new coding-theory family.

## Pass 5747 — minimum dual words are the 130 projective lines

PG(3,3) has exactly 130 projective lines, each containing four points.

For every line \(L\), its all-one incidence vector \(h_L\in\mathbb F_3^{40}\) satisfies

\[
h_L V=0.
\]

The verifier exhausts every support of size at most four and proves:

* no support of size 1, 2, or 3 supports a nonzero dual word;
* the dependent four-subsets are **exactly** the 130 projective lines.

Thus

\[
\boxed{d(C^\perp)=4}
\]

and the 260 nonzero weight-4 words are exactly the two scalar multiples of the 130 line-incidence rays.  This agrees with Rodrigues' 260 count and upgrades the repo representation to an explicit PG(3,3) support classification.

## Pass 5748 — thirteen three-query local repair groups per coordinate

The 130x40 projective-line incidence matrix \(H\) has row weight 4 and column weight 13.  Since \(HV=0\), every codeword obeys on every projective line

\[
\sum_{p\in L}x_p=0.
\]

Therefore any one coordinate on a line is reconstructed from the other three:

\[
\boxed{x_p=-\sum_{q\in L\setminus\{p\}}x_q\pmod3}.
\]

Every point lies on exactly 13 projective lines.  Relative to a selected W33 symplectic polarity, those 13 split uniformly as

\[
\boxed{13=4_{\rm W33\ isotropic}+9_{\rm ambient\ nonisotropic}}.
\]

So every symbol has thirteen distinct three-query local repair groups, four of which live entirely inside the currently selected W33 line geometry.

This is a classical-code repair statement.  In the CSS interpretation the weight-4 dual rays are minimum logical operators, so one must not confuse these repair checks with quantum stabilizer generators.

## Pass 5749 — the sparse line system is the whole classical dual

The 130x40 line-incidence matrix satisfies

\[
\boxed{\operatorname{rank}_{\mathbb F_3}H=30}.
\]

Since the quadratic code has dimension 10, the line rows span all of \(C^\perp\):

\[
\boxed{\operatorname{rowspan}(H)=C^\perp}.
\]

The same statement can be written as

\[
\ker H=C.
\]

Thus the ambient quadratic code has a completely local projective-line parity presentation with 130 weight-4 checks and column degree 13.

## Pass 5750 — minimum logical rays form a Grassmann SRG

For two distinct projective lines \(L,M\),

\[
h_L\cdot h_M=|L\cap M|\pmod3.
\]

Two lines in PG(3,3) are either disjoint or meet in one point.  Therefore the nonzero-dot-product graph of the minimum line rays is exactly the line-intersection Grassmann graph

\[
J_3(4,2).
\]

The verifier proves

\[
\boxed{J_3(4,2)=\operatorname{SRG}(130,48,20,16)}.
\]

For the selected W33 polarity, the 40 isotropic lines induce

\[
\boxed{\operatorname{SRG}(40,12,2,4)},
\]

while the 90 non-isotropic lines have induced degree 32.  The cross-incidence is biregular:

\[
40\cdot36=90\cdot16=1440.
\]

In the CSS reading, this 130-vertex graph is the commutation graph of the minimum projective logical rays.

## Pass 5751 — 234 symplectic W33 overlays on one fixed code

This is the new architectural synthesis.

An alternating 4x4 form over \(\mathbb F_3\) is determined by six coefficients.  Exhaustive enumeration gives 468 nondegenerate alternating forms.  Modulo the two nonzero scalar multiples, there are

\[
\boxed{234}
\]

projective symplectic polarities.

The same count is forced group-theoretically:

\[
|PGL(4,3)|=12{,}130{,}560,
\]

\[
|PGSp(4,3)|=51{,}840,
\]

and

\[
\boxed{[PGL(4,3):PGSp(4,3)]=234}.
\]

For each of the 234 polarity classes \(J\), the verifier builds

\[
C_J(x,y)=(x^TJy)^2.
\]

It finds:

\[
\boxed{234\text{ distinct }40\times40\text{ matrices }C_J},
\]

but for every one,

\[
\boxed{\operatorname{rowspan}(C_J)=C_{\rm Veronese}}.
\]

Every overlay selects 40 isotropic W33 lines out of the same 130 ambient projective lines.  Across the complete overlay family, every ambient line is selected exactly

\[
\boxed{72}
\]

times, since

\[
234\cdot40=130\cdot72=9360.
\]

### Architecture reading

The 40-coordinate quadratic memory layer and the W33 routing geometry are separable:

\[
\boxed{
\text{fixed code space}
\quad\times\quad
\text{234-way symplectic selector}
\quad\longrightarrow\quad
\text{selectable W33 native-line fabric}.
}
\]

This suggests a reconfigurable finite-geometry machine in which the stored code state does not have to be re-encoded when the symplectic routing polarity changes.  The selectable object is the **routing/incidence overlay**, not the underlying 10-dimensional code.

That is a finite combinatorial architecture statement.  Calling the selector a physical gauge field, spacetime degree of freedom, or fundamental interaction would require an additional physical model and experimental evidence that are not present here.

## Exact evidence

Executable verifier:

`analysis/w33_pass5744_5751_quadratic_code_overlays.py`

Frozen certificate:

`data/PART_W33_PASS5744_5751_QUADRATIC_CODE_OVERLAYS.json`

Focused regression:

`tests/test_w33_pass5744_5751_quadratic_code_overlays.py`

CI replay:

`.github/workflows/w33_pass5744_5751_quadratic_code_overlays.yml`
