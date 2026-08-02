# Pass 1974 — proof promotion for the surviving spread statements

This pass separates three levels: unconditional incidence proofs, a uniform
proof for spreads carrying the certified linewise involution, and the remaining
arbitrary-spread question.

## 1. The spread seed and its residual support

Let `S` be a spread of `W(q,q)`.  It has `q^2+1` pairwise disjoint isotropic
lines, each with `q+1` points, and these lines partition the points.

### Proposition 1 — spread pairs form an independent seed

For each unordered pair `{L,M}` of lines in `S`, the generalized-quadrangle
axiom gives a unique point of `M` collinear with each point of `L`.  These
`q+1` collinear pairs form the canonical cross-matching of the frame `{L,M}`.

An edge in that matching has one endpoint on `L` and one on `M`.  Since the
spread line through each endpoint is unique, that edge identifies the unordered
pair `{L,M}`.  Therefore different spread pairs have disjoint matching-edge
sets.  The `C(q^2+1,2)` spread frames form an independent set in the frame graph.

Every collinear pair whose endpoints lie on two different spread lines occurs in
exactly one such matching.  Hence the spread seed covers precisely the edges not
lying inside a spread line.  The residual set is exactly the union of the edges
inside the spread lines and has size

`(q^2+1) C(q+1,2) = (q^2+1)q(q+1)/2`.

This proposition is uniform and does not require a special spread.

### Correction at `q=3`

The 45 spread frames are **not maximal independent**.  The exact census gives 15
frames whose four matching edges lie entirely in the 60-edge residual set.  Each
is nonadjacent to all 45 seed frames and can be adjoined individually.

What is exact is the completion obstruction: the 15 candidates collectively
touch only 20 residual edges, so 40 residual edges occur in no candidate frame.
No selection of candidates can complete the seed to a 60-frame exact cover.
This holds for all 36 spreads of `W(3,3)`.

## 2. The `1/q` law from a linewise fixed-point-free involution

Assume now that a spread `S` admits a collineation `sigma` with the following
properties:

1. `sigma^2=1` projectively;
2. `sigma` fixes every line of `S` setwise;
3. `sigma` has no fixed point;
4. the only lines fixed setwise by `sigma` are the lines of `S`.

These are exactly the properties certified for the q=3 spread involutions and
for the constructed examples at q=5,7.

### Theorem 2 — candidates are the line orbits `{A,sigma(A)}`

Let `A` be a line outside `S`.  It meets `q+1` distinct spread lines, one at each
of its points.  Because `sigma` fixes each spread line, `sigma(A)` meets the same
spread lines at the paired points.  The canonical cross-matching between `A`
and `sigma(A)` is therefore

`{ {x,sigma(x)} : x in A }`,

and every matching edge lies inside a spread line.  Thus `{A,sigma(A)}` is a
residual candidate frame.

Conversely, let `{A,B}` be a frame whose canonical matching lies entirely in the
residual edges.  For each `x in A`, its matched point `y in B` lies with `x` on a
spread line.  On that line the certified residual pairing is the `sigma`-pair,
so `y=sigma(x)`.  Therefore `B=sigma(A)`.

The candidate frames are exactly the two-element `sigma`-orbits on lines outside
`S`.

### Corollary 2.1 — candidate count

`W(q,q)` has `(q+1)(q^2+1)` lines.  Removing the `q^2+1` spread lines leaves
`q(q^2+1)` lines.  By assumption none is fixed by `sigma`, hence

`number of candidates = q(q^2+1)/2`.

### Corollary 2.2 — support and multiplicity

On each spread line, the fixed-point-free involution partitions its `q+1` points
into `(q+1)/2` edges.  Across all spread lines the distinct candidate support is

`(q^2+1)(q+1)/2`.

The residual set has `(q^2+1)q(q+1)/2` edges, so the supported fraction is
exactly `1/q`.

Fix a supported edge `{x,sigma(x)}`.  There are exactly `q` lines through `x`
other than its spread line.  Each such line `A` produces the candidate
`{A,sigma(A)}`, and these are all candidates containing the edge.  Thus every
supported edge occurs with multiplicity exactly `q`.

This proves the measured `20/60`, `78/390`, and `200/1400` ratios in one
argument whenever the linewise involution exists.

### Even characteristic

A fixed-point-free involution on a spread line would partition `q+1` points into
2-cycles.  When `q` is even, `q+1` is odd, so this is impossible.  The measured
zero-candidate q=2 case is therefore the parity branch of the same mechanism.

## 3. The nonsquare similitude construction

Let `q` be odd, choose a nonsquare `mu in F_q`, and let `K=F_q(alpha)` with
`alpha^2=mu`.  Regard the four-dimensional `F_q` space as a two-dimensional
`K` space.  Multiplication by `alpha` defines an `F_q`-linear map `g` satisfying

`g^2 = mu I`.

Choose the standard trace construction of the alternating form so that
multiplication by `alpha` is a symplectic similitude.  The one-dimensional
`K`-subspaces are two-dimensional `F_q`-subspaces and form the associated
Desarguesian symplectic spread.  Multiplication by `alpha` fixes each such spread
line setwise.

Projectively, `g` has order two because `g^2` is scalar.  A projective fixed point
would give an `F_q` eigenvalue `lambda` with `lambda^2=mu`, impossible because
`mu` is nonsquare.  Hence the projective involution is fixed-point-free.

This proves existence of `sigma_S` for the associated Desarguesian symplectic
spread for every odd q.

## 4. What remains open

- The proof above does not show that every arbitrary symplectic spread admits the
  linewise involution.  The repository has exhaustive q=3 evidence and explicit
  constructed q=5,7 examples, not a classification for all spreads and all q.
- Uniqueness of the nontrivial linewise stabilizer is exact at q=3; no uniform
  uniqueness theorem is promoted here.
- The exact q=3 `36/270` nonsquare/square multiplier split remains a certified
  finite result with no located literature reference.
- `chi(H)=9` remains open.

## Prior-art boundary

Regular spreads, spreads of symmetry, and symplectic-spread coordinatizations are
standard finite-geometry topics.  De Bruyn's coordinatization work and the
Thas--Payne spread literature are relevant background.  This pass claims the
proof organization above for the repository's objects, not novelty for the
standard framework.
