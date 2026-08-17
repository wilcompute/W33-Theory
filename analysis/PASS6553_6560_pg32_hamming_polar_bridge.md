# Passes 6553–6560 — PG(3,2) Hamming-polar bridge

## Status

**PASS — exact finite binary geometry/coding theorem.** This packet explains the previously separate numbers
\[
35=15+20
\]
and
\[
20=2\cdot10
\]
inside one standard coding/projective mechanism.

## Pass 6553 — the simplex layer has the full Hamming code as dual

The Pass6533 code is
\[
C=S+\langle q_0\rangle,
\]
where
\[
S\cong[15,4,8]_2
\]
is the symplectic simplex code. Therefore
\[
\boxed{S^\perp\cong[15,11,3]_2},
\]
the binary length-15 Hamming code.

Because \(C\) is obtained from \(S\) by adjoining the quadratic word \(q_0\),
\[
\boxed{C^\perp=\{h\in S^\perp:\langle q_0,h\rangle=0\}},
\]
a codimension-one subcode of the Hamming code.

## Pass 6554 — the 35 Hamming minimum words are the 35 lines of PG(3,2)

The Hamming code has exactly 35 weight-three words. Under the standard nonzero-vector coordinate labeling of \(\mathbb F_2^4\), each has support
\[
\boxed{\{x,y,x+y\}},
\]
so these 35 supports are exactly all 35 projective lines of
\[
\boxed{PG(3,2)}.
\]
This gives a direct coding realization of the projective line carrier that repeatedly appears elsewhere in the repo.

## Pass 6555 — one quadratic parity bit selects the doily inside PG(3,2)

For any projective line \(L=\{x,y,x+y\}\), polarization gives
\[
\langle q_0,\mathbf1_L\rangle
=q_0(x)+q_0(y)+q_0(x+y)
=B(x,y).
\]
Therefore the codimension-one constraint defining \(C^\perp\) is exactly the symplectic-isotropy test:
\[
\boxed{\mathbf1_L\in C^\perp\iff B(x,y)=0.}
\]
Hence the 35 Hamming minimum supports split canonically as
\[
\boxed{35=15_{\rm isotropic}+20_{\rm nonisotropic}}.
\]
The 15 retained words are exactly the 15 doily lines already recovered in Pass6534.

## Pass 6556 — the 20 rejected Hamming lines are exactly the tricentric triads

If \(L\) is nonisotropic, its three points are pairwise noncollinear in the doily. Its symplectic orthogonal complement \(L^\perp\) is another nonisotropic projective line containing exactly three points, and those three points are precisely the common perpendiculars of the three points of \(L\).

Thus each rejected Hamming minimum support is a tricentric triad:
\[
\boxed{20_{\rm nonisotropic\ PG(3,2)\ lines}=20_{\rm tricentric\ doily\ triads}}.
\]
This gives the missing mechanism behind the Pass6543 split of the 35 all-perp Veldkamp lines.

## Pass 6557 — the 35 all-perp Veldkamp lines are the Hamming minimum shell

Let \(L=\{a,b,a+b\}\) be a Hamming/PG(3,2) line. The three simplex words
\[
s_a,\ s_b,\ s_{a+b}
\]
form an all-perp Veldkamp line. Their common zero core is
\[
\boxed{L^\perp}.
\]
If \(L\) is isotropic, \(L^\perp=L\), giving one of the 15 collinear cores. If \(L\) is nonisotropic, \(L^\perp\ne L\), giving one of the 20 tricentric cores. Therefore
\[
\boxed{35\text{ all-perp Veldkamp lines}=35\text{ Hamming weight-3 words}}
\]
with the exact internal split \(15+20\).

## Pass 6558 — polarity pairs the 20 tricentric lines into ten pairs

On the 20 nonisotropic PG(3,2) lines, symplectic polarity is fixed-point-free:
\[
L\longleftrightarrow L^\perp,
\qquad L\cap L^\perp=\varnothing.
\]
Hence
\[
\boxed{20=10\times2}
\]
polar pairs.

## Pass 6559 — the ten polar-pair unions are exactly the ten grid complements

Each polar pair consists of two disjoint three-point lines, so its union has six points. Exhaustive comparison with the Pass6533 code gives
\[
\boxed{
\{L\cup L^\perp:L\text{ nonisotropic}\}
=
\{\operatorname{supp}(c):c\in C,\ \mathrm{wt}(c)=6\}.
}
\]
There are ten of each. Consequently each six-point polar-pair union is the complement of one nine-point doily grid:
\[
\boxed{10\text{ polar pairs of nonisotropic PG(3,2) lines}
\leftrightarrow10\text{ doily grids}.}
\]
For the determinant word \(q_0\), this says its six units split into the two mutually polar nonisotropic projective lines complementary to the associated determinant grid.

## Pass 6560 — unified projective/code mechanism

The entire bridge is now:
\[
[15,4,8]\ \text{simplex}
\quad\perp\quad
[15,11,3]\ \text{Hamming}
\]
\[
\Downarrow\ +\langle q_0\rangle
\]
\[
[15,5,6]\ \text{doily hyperplane code}
\quad\perp\quad
[15,10,3]\ \text{isotropic-line subcode}.
\]
At minimum weight,
\[
\boxed{
35\ PG(3,2)\text{ lines}
=15\text{ doily lines}+20\text{ tricentric triads},
}
\]
and the rejected 20 lines pair under polarity into the ten six-point grid complements.

This is the precise connection between the repo's recurring PG(3,2), Hamming/simplex, doily, Veldkamp, determinant, and grid layers. It is a finite binary theorem; no continuum or physical claim is inferred.
