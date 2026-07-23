# Pass 595 — Johnson Triangle Holonomy Curvature

Pass 594 constructed a reversible six-state Singer connection over the Johnson graph

\[
J(8,3),\qquad |V|=\binom83=56,\qquad k=15,
\]

with fibre the six Sylow-5 subgroups of the complementary five-set and full holonomy

\[
S_5\cong PGL(2,5)
\]

in its exceptional degree-six action. Pass 595 computes the complete gauge-invariant conjugacy-class census of the elementary triangle holonomies.

## Exact triangle census

The Johnson graph has

\[
840=56\cdot15
\]

unordered triangles. They split into the two standard Johnson geometries:

- **top triangles:** intersection size 2, union size 5; count 560;
- **tetrahedral triangles:** intersection size 1, union size 4; count 280.

The Pass-594 connection separates these geometries sharply:

\[
\begin{array}{c|c|c|c}
\text{triangle geometry}&\text{degree-six cycle type}&\text{order}&\text{count}\\\hline
\text{top}&1^6&1&112\\
\text{top}&2^2 1^2&2&112\\
\text{top}&3^2&3&336\\
\text{tetrahedral}&2^3&2&280
\end{array}
\]

Thus every tetrahedral triangle has fixed-point-free involutory holonomy, while the top triangles split in the exact ratio

\[
1:1:3
\]

among flat, double-transposition, and order-three holonomy.

Equivalently,

\[
840=112+112+336+280=56(2+2+6+5).
\]

## Augmentation Wilson trace

The six-point permutation fibre decomposes as

\[
\mathbf 1\oplus V_5,
\]

where \(V_5\) is the irreducible five-dimensional icosahedral augmentation module from Pass 593. Its character is

\[
\chi_{V_5}(g)=\#\operatorname{Fix}_6(g)-1.
\]

Therefore the four triangle populations contribute

\[
5,\quad 1,\quad -1,\quad -1
\]

respectively, and the integrated Wilson trace is

\[
\boxed{
112\cdot5+112\cdot1-336-280=56.
}
\]

So the total augmentation curvature equals the number of base vertices:

\[
\boxed{
\sum_{\triangle}\chi_{V_5}(\operatorname{Hol}(\triangle))
=|V(J(8,3))|=56.
}
\]

For the full six-point permutation character the corresponding identity is

\[
\boxed{
896=840+56,
}
\]

i.e. the invariant line contributes one per base triangle and the augmentation fibre contributes the residual 56.

Counting triangle incidences at vertices gives the discrete integrated identity

\[
\frac13\sum_{v\in V(J(8,3))}
\sum_{\triangle\ni v}
\chi_{V_5}(\operatorname{Hol}(\triangle))
=56.
\]

The average incident augmentation trace is 3 per base vertex. It is not pointwise constant because Pass 594's canonical edge transporter uses the two smallest points outside an exchanged pair and therefore is not vertex-transitive. The global conjugacy census and Wilson sum are nevertheless gauge invariant under arbitrary vertex-wise fibre relabelling.

## Boundary

This is a finite combinatorial Wilson/Gauss–Bonnet identity for the specific Pass-594 connection. It is not a continuum curvature theorem, and the equality 56 does not define a canonical identification with the 40-point W33 geometry.
