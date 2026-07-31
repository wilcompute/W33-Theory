# W33 frame-graph Hoffman resolution theorem

## Executive result

The unresolved nine-cover resolution problem is not merely a large exact-cover search. It is an equality-case spectral coloring problem.

Let `M` be the canonical `540 x 240` frame/edge incidence matrix: every row is the four-edge cross-matching attached to one unordered pair of disjoint totally isotropic lines of `W(3,3)`, and every W33 edge occurs in nine rows. Let `H` be the graph on the 540 frames, with two frames adjacent exactly when their cross-matchings share an edge.

The independent verifier rebuilds `W(3,3)` directly from `PG(3,3)` and proves

\[
\boxed{H+4I_{540}=MM^{\mathsf T}.}
\]

It then proves the exact spectrum

\[
\boxed{
\operatorname{spec}(H)=
32^1\oplus14^{44}\oplus8^{15}\oplus4^{81}\oplus2^{84}\oplus(-4)^{315}.
}
\]

Consequently the Hoffman bounds are sharp at precisely the cover scale:

\[
\boxed{\chi(H)\ge 1-\frac{32}{-4}=9,}
\]

\[
\boxed{\alpha(H)\le 540\frac{4}{32+4}=60.}
\]

Every exact cover is an independent set of size 60, and every independent set of size 60 is an exact cover. Therefore

\[
\boxed{
\text{nine-cover resolution}
\iff
\text{Hoffman 9-coloring of }H.
}
\]

This does **not** decide whether the resolution exists. It replaces the unconstrained search by a rigid equality-case problem with a forced quotient matrix and a regular-simplex certificate.

## Construction

The script `analysis/w33_frame_hoffman_resolution_theorem.py` performs the following from scratch.

1. Build the 40 projective points of `PG(3,3)`.
2. Use the standard nondegenerate alternating form to build the W33 collinearity graph, verifying degree 12 and 240 edges.
3. Enumerate the 40 totally isotropic four-point lines.
4. Enumerate the 540 unordered disjoint line pairs.
5. For every pair, use the generalized-quadrangle axiom to obtain the unique point-to-point collinearity matching between the two lines. This gives four W33 edges.
6. Build `M`; verify row sum 4 and column sum 9.
7. Verify that two distinct frame matchings share either zero or one edge, so the off-diagonal part of `MM^T` is exactly the adjacency matrix `H`.

The resulting graph has 540 vertices, 8,640 edges, and degree 32.

## Exact spectral certificate

The verifier checks the integer matrix identity

\[
(H-32I)(H-14I)(H-8I)(H-4I)(H-2I)(H+4I)=0.
\]

Equivalently, the annihilator has coefficient vector

```text
1, -56, 908, -4320, -7616, 83456, -114688.
```

The exact trace moments are

\[
\operatorname{tr}(H^k)_{k=0}^{5}
=
(540,0,17280,146880,2903040,57473280).
\]

Solving the six-by-six Vandermonde system over the rationals gives the multiplicities

\[
(1,44,15,81,84,315)
\]

for eigenvalues

\[
(32,14,8,4,2,-4).
\]

In particular,

\[
\boxed{\ker(M^{\mathsf T})=E_{-4}(H),\qquad \dim E_{-4}=315,}
\]

and

\[
\boxed{\operatorname{rank}_{\mathbb Q}M=225.}
\]

This independently reproduces the previously frozen rank while identifying the entire frame-graph spectrum around it.

## Equality structure: every cover is perfect

Let `x` be the indicator vector of an exact cover. Then

\[
M^{\mathsf T}x=\mathbf 1_{240}.
\]

Because every row of `M` has weight four, `x` has weight 60. Since every edge column is hit once, the selected frames are pairwise nonadjacent in `H`. Thus exact covers are 60-cocliques.

Conversely, a 60-coclique consists of 60 pairwise edge-disjoint four-edge matchings. It contains 240 distinct W33 edges and therefore covers all 240 exactly once. Hence it is an exact cover.

Equality in Hoffman's independence bound forces

\[
\boxed{Hx=4(\mathbf 1-x).}
\]

So every frame outside an exact cover has exactly four neighbors inside it. Each exact cover is therefore a perfect two-cell equitable partition with quotient matrix

\[
\boxed{
\begin{pmatrix}
0&32\\
4&28
\end{pmatrix}.
}
\]

## What a resolution would have to look like

If `X=[x_1|...|x_9]` is a nine-cover resolution, then

\[
\boxed{HX=X\,4(J_9-I_9).}
\]

Thus every frame has exactly four neighbors in each of the other eight color classes. The quotient spectrum is

\[
32^1\oplus(-4)^8.
\]

Center the nine indicators:

\[
y_i=x_i-\frac19\mathbf 1.
\]

Then

\[
M^{\mathsf T}y_i=0,
\qquad
Hy_i=-4y_i,
\]

and

\[
\langle y_i,y_i\rangle=\frac{160}{3},
\qquad
\langle y_i,y_j\rangle=-\frac{20}{3}\quad(i\ne j).
\]

After normalization, the pairwise inner product is

\[
\boxed{-\frac18.}
\]

Therefore a resolution is equivalent to a regular 8-simplex of nine binary affine-fiber points inside the 315-dimensional `-4` eigenspace:

\[
\boxed{
M^{\mathsf T}x_i=\mathbf1,
\quad
x_i\in\{0,1\}^{540},
\quad
x_i^{\mathsf T}x_j=0\ (i\ne j).
}
\]

This is the correct reduced search target.

## Literature check

The equality language is standard Hoffman-coloring theory. A recent structural treatment is A. Abiad, W. Bosma, and T. van Veluw, *Hoffman colorings of graphs*, Linear Algebra and its Applications 710 (2025), 129–150, DOI `10.1016/j.laa.2025.01.036`. A 2026 equality-case treatment of the chromatic and independence bounds explicitly records that a maximum Hoffman coclique in a regular graph has exactly `|lambda_min|` neighbors from every outside vertex. The W33 frame graph supplies a new concrete equality-scale instance; the theorem here is the exact identification of its cover problem with that framework.

## Evidence boundary

- The spectrum, Hoffman bounds, exact-cover equivalence, equitable quotient, and simplex identities are exact and machine-verified.
- The existence of a nine-coloring remains open.
- The known four-cover packing is a partial regular simplex; the previously certified failure to add a fifth cover applies only to that selected packing.
- No physical interpretation follows from the graph-coloring theorem alone.
