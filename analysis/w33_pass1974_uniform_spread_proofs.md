# Pass 1974 — proof promotion for the surviving spread statements

This pass separates four levels: an unconditional incidence proof, an
unconditional candidate subfamily supplied by a linewise involution, an exact
counting theorem under the candidate-orbit property, and the remaining
arbitrary-spread classification problem.

## 1. The spread seed and its residual support

Let `S` be a spread of `W(q,q)`. It has `q^2+1` pairwise disjoint isotropic
lines, each with `q+1` points, and these lines partition the points.

### Proposition 1 — spread pairs form an independent seed

For each unordered pair `{L,M}` of lines in `S`, the generalized-quadrangle
axiom gives a unique point of `M` collinear with each point of `L`. These
`q+1` collinear pairs form the canonical cross-matching of the frame `{L,M}`.

An edge in that matching has one endpoint on `L` and one on `M`. Since the
spread line through each endpoint is unique, that edge identifies the unordered
pair `{L,M}`. Therefore different spread pairs have disjoint matching-edge
sets. The `C(q^2+1,2)` spread frames form an independent set in the frame graph.

Every collinear pair whose endpoints lie on two different spread lines occurs in
exactly one such matching. Hence the spread seed covers precisely the edges not
lying inside a spread line. The residual set is exactly the union of the edges
inside the spread lines and has size

`(q^2+1) C(q+1,2) = (q^2+1)q(q+1)/2`.

This proposition is uniform and does not require a special spread.

### Correction at `q=3`

The 45 spread frames are **not maximal independent**. The exact census gives 15
frames whose four matching edges lie entirely in the 60-edge residual set. Each
is nonadjacent to all 45 seed frames and can be adjoined individually.

What is exact is the completion obstruction: the 15 candidates collectively
touch only 20 residual edges, so 40 residual edges occur in no candidate frame.
No selection of candidates can complete the seed to a 60-frame exact cover.
This holds for all 36 spreads of `W(3,3)`.

## 2. What a linewise fixed-point-free involution proves by itself

Assume a spread `S` admits a collineation `sigma` with:

1. `sigma^2=1` projectively;
2. `sigma` fixes every line of `S` setwise;
3. `sigma` has no fixed point;
4. no line outside `S` is fixed setwise.

Let `A` be a line outside `S`. It meets `q+1` distinct spread lines, one at each
of its points. Because `sigma` fixes each spread line, `sigma(A)` meets the same
spread lines at the paired points. The canonical cross-matching between `A` and
`sigma(A)` is

`{ {x,sigma(x)} : x in A }`,

so every matching edge lies inside a spread line. Thus every two-element line
orbit `{A,sigma(A)}` is a residual candidate frame.

There are `q(q^2+1)` lines outside `S`, and none is fixed. Therefore the
involution supplies exactly

`q(q^2+1)/2`

candidate frames. Their union is supported on the `(q+1)/2` involution edges in
each spread line, hence on

`(q^2+1)(q+1)/2`

distinct residual edges. Each such edge `{x,sigma(x)}` occurs in the candidate
arising from each of the `q` non-spread lines through `x`, so its multiplicity in
this involution-generated subfamily is exactly `q`.

This proves a **candidate subfamily** of the measured size and support. It does
not, from the four involution axioms alone, exclude additional residual
candidate frames.

## 3. The candidate-orbit property and the exact `1/q` law

Define the **candidate-orbit property** for `(S,sigma)`:

> every residual candidate frame is one of the line orbits
> `{A,sigma(A)}`.

The property is verified by literal enumeration for the repository's `q=3,5,7`
examples. Under this additional property, the involution-generated subfamily is
the entire candidate set, and the following formulas are exact:

- candidates: `q(q^2+1)/2`;
- supported residual edges: `(q^2+1)(q+1)/2`;
- residual edges: `(q^2+1)q(q+1)/2`;
- supported fraction: `1/q`;
- multiplicity of every supported edge: `q`.

Thus the measured ratios `20/60`, `78/390`, and `200/1400` share one counting
mechanism. The finite computations prove the candidate-orbit property in those
cases; a general proof for every associated spread is not silently assumed.

### Even characteristic

A fixed-point-free involution on a spread line would partition `q+1` points into
2-cycles. When `q` is even, `q+1` is odd, so this is impossible. This explains
why the involution mechanism cannot exist in even characteristic and is
consistent with the measured zero-candidate `q=2` case. It does not alone prove
that every conceivable even-characteristic spread has zero residual candidates.

## 4. The nonsquare similitude construction

Let `q` be odd, choose a nonsquare `mu in F_q`, and let `K=F_q(alpha)` with
`alpha^2=mu`. Regard the four-dimensional `F_q` space as a two-dimensional
`K` space. Multiplication by `alpha` defines an `F_q`-linear map `g` satisfying

`g^2 = mu I`.

Choose the standard trace construction of the alternating form so that
multiplication by `alpha` is a symplectic similitude. The one-dimensional
`K`-subspaces are two-dimensional `F_q`-subspaces and form the associated
Desarguesian symplectic spread. Multiplication by `alpha` fixes each such spread
line setwise.

Projectively, `g` has order two because `g^2` is scalar. A projective fixed point
would give an `F_q` eigenvalue `lambda` with `lambda^2=mu`, impossible because
`mu` is nonsquare. Hence the projective involution is fixed-point-free.

This proves existence of the linewise involution for the associated Desarguesian
symplectic spread for every odd `q`. It does not by itself prove the
candidate-orbit property for all `q`; that converse remains a separate geometric
statement.

## 5. What remains open

- Prove the candidate-orbit property uniformly for the associated Desarguesian
  symplectic spread, or find a counterexample beyond the checked `q=3,5,7` cases.
- Determine which arbitrary, including non-Desarguesian, symplectic spreads admit
  the linewise involution.
- Uniqueness of the nontrivial linewise stabilizer is exact at `q=3`; no uniform
  uniqueness theorem is promoted here.
- The exact `q=3` `36/270` nonsquare/square multiplier split remains a certified
  finite result with no located literature reference.
- `chi(H)=9` remains open.

## Prior-art boundary

Regular spreads, spreads of symmetry, and symplectic-spread coordinatizations are
standard finite-geometry topics. De Bruyn's coordinatization work and the
Thas--Payne spread literature are relevant background. This pass claims the
proof organization and explicit scope separation above for the repository's
objects, not novelty for the standard framework.
