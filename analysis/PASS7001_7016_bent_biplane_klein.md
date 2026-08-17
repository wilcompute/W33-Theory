# Passes 7001–7016 — the doily code is a point-derived bent biplane

## Executive result

The `[15,5,6]_2` quadratic-evaluation code from Pass6533 is not an isolated 15-coordinate object.  Reinsert the missing zero vector of `F_2^4` and adjoin the affine constant.  The result is

\[
D=\langle RM(1,4),q_0\rangle,\qquad q_0=x_0x_1+x_2x_3,
\]

a self-orthogonal binary `[16,6,6]` code with

\[
W_D(y)=1+16y^6+30y^8+16y^{10}+y^{16}.
\]

Its sixteen weight-six supports form a symmetric

\[
\boxed{2-(16,6,2)}
\]

biplane.  Fixing the reinserted zero coordinate recovers the complete doily Veldkamp hyperplane split: the ten nonincident blocks shorten to the ten grid-complement words, the six incident blocks delete to the six ovoids, and the thirty weight-eight words form fifteen complementary pairs whose zero-coordinate representatives shorten to the fifteen perp words.

This gives a single 16-point design containing the repo's `10+15+6` hyperplane taxonomy.

## Pass7001 — intrinsic coding invariants of C

For

\[
C=\{(B(a,x)+tq_0(x))_{x\ne0}:a\in\mathbb F_2^4,\ t\in\mathbb F_2\},
\]

the independent enumerator confirms

\[
C=[15,5,6]_2,\qquad
W_C=1+10y^6+15y^8+6y^{10}.
\]

Moreover \(C\subset C^\perp\), so the code is self-orthogonal.  Its generalized Hamming weights are

\[
\boxed{(d_1,d_2,d_3,d_4,d_5)=(6,10,12,14,15)}
\]

and its covering radius is six.

The dual is `[15,10,3]` with weight enumerator

\[
1+15y^3+45y^4+96y^5+160y^6+195y^7+195y^8+160y^9+96y^{10}+45y^{11}+15y^{12}+y^{15}.
\]

## Pass7002 — the bent extension

Extending to all sixteen points and adding the constant affine function gives

\[
D=\langle RM(1,4),q_0\rangle=[16,6,6]_2.
\]

The quadratic \(q_0\) is a nondegenerate quadratic/bent function for the standard symplectic polar form.  The exact weight enumerator is

\[
\boxed{W_D=1+16y^6+30y^8+16y^{10}+y^{16}}.
\]

The code remains self-orthogonal.  Its dual is `[16,10,4]` with

\[
W_{D^\perp}=1+60y^4+256y^6+390y^8+256y^{10}+60y^{12}+y^{16}.
\]

The generalized Hamming weights are

\[
\boxed{(6,10,12,14,15,16)},
\]

and the covering radius is again six.

## Pass7003 — the sixteen minimum words are a biplane

Let the sixteen weight-six supports be the blocks.  Direct enumeration gives:

- 16 points and 16 blocks;
- each block has size 6;
- each point lies on 6 blocks;
- each pair of points lies on exactly 2 blocks;
- any two distinct blocks meet in exactly 2 points.

Hence the minimum shell is the symmetric biplane

\[
\boxed{2-(16,6,2)}.
\]

Equivalently, for the 16-by-16 block incidence matrix \(N\),

\[
NN^T=4I+2J.
\]

## Pass7004 — one point derives the doily `10+6`

Choose the coordinate corresponding to \(0\in\mathbb F_2^4\).

Exactly ten biplane blocks avoid that point.  Deleting the distinguished coordinate from those ten incidence vectors gives exactly the ten weight-six words of \(C\), previously identified as grid complements.

Exactly six biplane blocks contain the distinguished point.  Deleting that point from those blocks produces exactly the six five-point zero sets of the weight-ten words of \(C\), i.e. the six ovoids.

Thus the biplane point stabilizer sees the exact split

\[
\boxed{10+6}.
\]

## Pass7005 — the fifteen perps are the middle shell

The thirty weight-eight words of \(D\) occur in complementary pairs.  Exactly fifteen have zero in the distinguished coordinate.  Shortening those fifteen words gives exactly the fifteen weight-eight words of \(C\), hence exactly the fifteen perp hyperplanes.

The point-derived biplane therefore contains all three doily Veldkamp point classes:

\[
\boxed{10\text{ grids}+15\text{ perps}+6\text{ ovoids}=31}.
\]

## Pass7006 — full automorphism group

All 720 matrices of `Sp(4,2)` preserve \(q_0\) up to an affine-linear correction and hence preserve the biplane after allowing translations.  The affine symplectic group

\[
2^4:\!Sp(4,2)
\]

therefore acts as a biplane automorphism group of order

\[
16\cdot720=11520.
\]

This is the full automorphism group.  Indeed, the stabilizer of a point acts on the remaining fifteen coordinates and preserves the ten nonincident blocks.  Those ten binary incidence vectors span the full `[15,5,6]` code \(C\); hence the point stabilizer embeds in `Aut(C)=Sp(4,2)` of order 720.  Therefore

\[
|Aut(\mathcal B)|\le16\cdot720,
\]

and the affine symplectic subgroup attains the bound:

\[
\boxed{Aut(\mathcal B)=2^4:\!Sp(4,2)\cong2^4:\!S_6}.
\]

## Pass7007 — the 35 PG(3,2) lines are the Klein quadric

Write the Plücker coordinates of a projective line as

\[
(p_{01},p_{02},p_{03},p_{12},p_{13},p_{23}).
\]

The 35 lines of `PG(3,2)` map bijectively to the 35 `F_2`-rational points of the Klein quadric

\[
\boxed{p_{01}p_{23}+p_{02}p_{13}+p_{03}p_{12}=0}.
\]

For the repo's standard symplectic form,

\[
B(x,y)=p_{01}+p_{23}.
\]

Therefore symplectic isotropy is not another quadratic condition in Klein space: it is the hyperplane section

\[
\boxed{p_{01}+p_{23}=0}.
\]

That hyperplane cuts the 35 Klein points into exactly

\[
\boxed{15+20},
\]

the 15 doily lines and the 20 nonisotropic projective lines.

## Pass7008 — the ten polar pairs are the ten biplane-derived blocks

Symplectic polarity is fixed-point-free on the 20 nonisotropic lines and pairs them into ten unordered pairs.  Each line is skew to its polar mate, so every pair has a six-point union in `PG(3,2)`.

Those ten six-point unions are exactly the ten weight-six supports of \(C\), i.e. the ten grid complements.

Even more rigidly, any two of the ten unions intersect in exactly two points.  If \(M\) is their `10 x 15` incidence matrix, then

\[
\boxed{MM^T=4I_{10}+2J_{10}},
\]

with spectrum

\[
\boxed{24^1\oplus4^9},
\]

and every doily point lies in exactly four of the ten unions.

This explains why the ten polar pairs looked unexpectedly uniform in Pass6553: they are literally the ten nonincident blocks of the 16-point biplane seen from one distinguished point.

## Pass7009–7016 — status and boundary

The code/design/Klein statements above are finite exact statements.  They sharpen the earlier doily/Veldkamp and `PG(3,2)` results without introducing a physical interpretation.

The most useful conceptual diagram is now

\[
\text{bent }q_0
\longrightarrow [16,6,6]\text{ biplane code}
\xrightarrow{\text{fix a point}}
[15,5,6]\text{ doily code}
\longrightarrow
10+15+6,
\]

while independently

\[
35\text{ lines of }PG(3,2)
\cong Q^+(5,2)(\mathbb F_2),
\qquad
H_B\cap Q^+(5,2)=15,
\]

and the 20 exterior points pair under polarity to the same ten grid-complement blocks.

**Boundary:** no quantum, particle, spacetime, or gauge-theory identification follows from these finite incidences alone.
