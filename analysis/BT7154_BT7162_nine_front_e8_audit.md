# Passes 7154--7162 — nine-front q=9 / binary-column / E8 audit

## Scope

This packet executes the five post-Pass7153 attacks, three outside-box probes, and an explicit ninth E8 attack.  Exact finite statements are separated from queued exhaustive decisions.  In particular, neither `alpha(W(3,9))=51` nor an identification of the new `[248,6,51]_2` code with the 248-dimensional adjoint representation of E8 is asserted unless the required object-level map/certificate exists.

The prior E8 corpus matters here.  Pass1012 killed the specific W(E6)-equivariant 240-edge/240-root bijection for the E6 x A2 embedding by an orbit obstruction.  Pass1021 then found the correct surviving object: the 240 E8 roots carry a canonical Eisenstein Z6 fibration onto 40 blocks; the quotient is the W(3,3) *point* action with subdegrees `1,12,27` and SRG parameters `(40,12,2,4)`.  The present packet does not reopen the dead edge-root bijection.

Primary external anchors used only for standard E8 facts:

- Winter--van Luijk, *The action of the Weyl group on the E8 root system*, arXiv:1901.06945 — E8 root system / 240-root action.
- Hohm--Samtleben, *Exceptional Field Theory III: E8(8)*, arXiv:1406.3348 — the 248-dimensional adjoint representation.
- Planat, *Entangling gates in even Euclidean lattices such as the Leech lattice*, arXiv:1002.4287 — an explicit Construction-A presentation of E8 from the extended binary Hamming `[8,4,4]` code.

## Pass7154 — exact q=9 target-48 decision, parallelized

Pass7139 proved that a 52-point partial ovoid exists iff one of eight 512-state normalized Gram compatibility graphs contains a residual 48-clique.  The exact CaDiCaL encoding is now split into eight independent jobs (`analysis/w33_pass7154_parallel_48_case.py` and `.github/workflows/w33_pass7154_parallel_q9_48_decision.yml`).  Every case freezes a CNF hash and independently rechecks a SAT model against the GF(9) pairing law before aggregation.

**Boundary:** until `data/PART_W33_PASS7154_Q9_48_CLIQUE_DECISION.json` exists, the exact q=9 optimum is not changed.  The currently verified statement remains the 51-point witness plus the independent upper bound already carried by the repo.

A structural refinement is already exact.  The 512 normalized states

`(1,a,b,c)`,  `a,b,c in GF(9)^*`

may be reshaped as

`[[1,a],[b,c]]`.

They split by matrix rank as

`512 = 448 + 64`,

because singularity is exactly `c=ab`: 64 rank-one states and 448 invertible states.

## Pass7155 — the Gram state space meets PGL2(9) on a 448-state big cell

The 448 invertible normalized rows are precisely the all-entry-nonzero projective matrices with top-left entry normalized to 1.  They therefore inject into `PGL2(9)`.  The involution `D=diag(1,-1)` acts by

`(1,a,b,c) -> (1,a,-b,-c)`

and has no fixed points on this big cell, giving 224 D-orbits.  The full pair quotient from Pass7147 has

`|PGL2(9)/<D>| = 360`.

Hence the relationship is exact but not an equality:

- 224 quotient nodes occur in the all-entry-nonzero big cell;
- 136 quotient nodes lie outside that big cell;
- the remaining 64 Gram states are rank-one boundary matrices.

This is the requested Gram-to-PGL bridge and simultaneously a cardinality obstruction to identifying the full 512-state anchor graph with the 360-node involution quotient.

## Pass7156 — what the code forgets: one Hamiltonian C6 inside K3,3

The two complementary triple columns partition the six generators into two 3-sets.  The nine cross-pair column types are therefore the edges of `K3,3`, and

`Aut(K3,3) = S3 wr C2`, order 72,

which is exactly the outer column-pattern group of the code.

The ambient geometric group from Pass7149 is D12.  The actual induced product `AF` is the order-six rotation

`0 -> 1 -> 5 -> 4 -> 2 -> 3 -> 0`.

Its six edges form a Hamiltonian C6 in that K3,3.  The three omitted cross edges are a perfect matching.  K3,3 has exactly six perfect matchings, hence exactly six complementary Hamiltonian C6s.  The stabilizer of one such C6 inside `Aut(K3,3)` has order `72/6=12` and is D12.  Therefore:

**Lifting criterion.** A code-outer automorphism lifts to the ambient hexad geometry iff it preserves the selected Hamiltonian C6 (equivalently, the deleted perfect matching).

This resolves the former symmetry index `72/12=6` by naming the missing invariant.

## Pass7157 — the involution-pair theorem extends to W(2n-1,q)

Let `q` be odd and write a `2n`-dimensional symplectic space as `V=U+U*` with

`B((u,w),(u',w')) = u(w') - u'(w)`

and involution `D(u,w)=(u,-w)`.

Then:

- the fixed projective locus is `P(U) union P(U*)`, of size
  `2(q^n-1)/(q-1)`;
- the number of nonisotropic endpoint transversals is
  `q^(n-1)(q^n-1)/(q-1)`;
- each transversal carries `(q-1)/2` eligible D-pairs;
- hence the eligible pair-node count is
  `q^(n-1)(q^n-1)/2`.

For two eligible D-orbits represented by X and Y, the four possible cross pairings collapse to only two equations:

`B(X,Y)=0` or `B(X,DY)=0`.

Thus the two-channel factorization from rank two is an all-rank symplectic statement.  What is special to `n=2` is the extra `PGL2(q)` matrix/Schreier identification; that is not generalized here.

## Pass7158 — the witness orbit is a homogeneous hexagon bundle

With

`G=PΓSp(4,9)`, `H=Stab(S)=C2`, `K=Stab(hexad)=D12`,

there is the canonical G-map

`G/H -> G/K`.

The fiber is `K/H`, of size six, and is the natural six-vertex D12 hexagon.  Numerically,

- `|G/H| = 3,443,212,800` witnesses;
- `|G/K| = 573,868,800` hexads;
- `6 * 573,868,800 = 3,443,212,800`.

The order-six `AF` rotation supplies the C6 on every fiber by G-transport.  Thus the witness orbit is not merely partitioned into six-sets; it is a G-equivariant homogeneous hexagon bundle.

## Pass7159 — bonkers: the code-column complement is Fano x Fano minus a 3x3 grid

The 248 generator columns collapse to exactly 23 distinct nonzero vectors of `F2^6`:

- all six weight-one vectors;
- all fifteen weight-two vectors;
- two complementary weight-three vectors.

Let the two complementary triples split `F2^6=A+B`, each of dimension three.  Then the selected 23 projective points are exactly

`(A\{0}) union (B\{0}) union (basis(A) x basis(B))`,

so

`23 = 7 + 7 + 9`.

The 40-point complement in `PG(5,2)` is therefore canonically

`(7 x 7) \ (3 x 3)`,  so `40 = 49 - 9`.

This is much stronger than the bare equality `63-23=40`.  It carries the same abstract `S3 wr C2` that acts on the code-column pattern.  `analysis/w33_pass7159_fano40_w33_subgroup.g` now tests whether this exact 40-point permutation G-set is conjugate to an order-72 subgroup action on the *proved* W33 40-point quotient from Pass1021.  Until its frozen certificate exists, no W33 identification is claimed.

## Pass7160 — bonkers: the natural eight-coordinate Hamming/E8 puncture route is impossible

One might hope that the 23 distinct column types contain an affine 3-flat of eight points.  Restriction of the six linear coordinate functions to such a flat would produce `RM(1,3)`, equivalently the extended binary Hamming `[8,4,4]` code, providing a standard Construction-A route to E8.

There is no such affine 3-flat.

Let an affine 3-flat be `v+H`, and let `s` be the support size of H and `f` the number of fixed-one coordinates outside that support.  The sum of Hamming weights over the eight coset points is `4s+8f`.  The 23-set has only weights 1 and 2, apart from the two complementary weight-three words.  An affine flat cannot contain both complementary triples: their difference is `111111` in H, which would pair each point with its complement and force forbidden weight-4/5 points.  Thus the total weight is at most 17.

Since `dim H=3`, `s>=3`.  If `f=1`, then `4s+8>=20`, impossible.  Hence `f=0`.  The case `s=3` would make H the full 3-space on its support, putting `v` in H and 0 in the coset, impossible.  Therefore `s=4`.

Now H is a hyperplane of `F2^4`.  If the defining normal has Hamming weight `r=1,2,3,4`, the nonzero coset weight distributions `(n1,n2,n3,n4)` are respectively

- `(1,3,3,1)`,
- `(2,4,2,0)`,
- `(3,3,1,1)`,
- `(4,0,4,0)`.

Every case either contains a weight-four word or at least two weight-three words.  On any four-coordinate support our 23-set contains no weight-four word and at most one of its two complementary weight-three words.  Contradiction.

So this natural local `[8,4,4] -> E8` path is exactly obstructed.

## Pass7161 — bonkers: the full [248,6,51] code does not produce E8 by the standard binary Construction-A mechanism

The generator Gram matrix satisfies

`GG^T = I6 (mod 2)`.

Therefore the code is not self-orthogonal.  It also contains odd-weight (weight 51) words, so it is not doubly even.  In particular the full `[248,6,51]_2` code is not the self-dual doubly-even code input that underlies the standard Type-II binary Construction-A presentation of E8.

This does not say the 248-code has no lattice interpretation; it rejects the direct E8 Construction-A inference.

## Pass7162 — ninth attack: E8, tested at object level rather than by 248 alone

Standard E8 bookkeeping is

`dim(e8) = 248 = 240 root spaces + 8 Cartan directions`.

The 248-code's full coordinate-permutation automorphism group has four coordinate orbits of sizes

`192, 36, 18, 2`.

Every invariant coordinate subset must be a union of those orbits.  Their subset sums are

`0,2,18,20,36,38,54,56,192,194,210,212,228,230,246,248`.

Neither 8 nor 240 occurs.  Hence there is no full-code-symmetry-invariant `240+8` coordinate split that could canonically mean roots plus Cartan.  Likewise neither 78 nor 81 occurs, so the standard dimension pattern

`248 = 78 + 8 + 81 + 81`

associated with the E6 x A2 branching cannot be realized as a full-code-symmetry-invariant coordinate partition either.

This complements the older repo result rather than replacing it:

- Pass1012: the old edge/root E6 x A2 equivariant bijection is obstructed;
- Pass1021: E8 roots instead fiber canonically `240 -> 40` with six-root Eisenstein fibers, and the 40 quotient is W33;
- Pass7159: the new code independently manufactures a structured 40-point binary complement `(7x7)\(3x3)`, with an exact subgroup-conjugacy test now attached;
- Pass7162: the *248 coordinates themselves* do not carry a canonical roots+Cartan split under their own full code symmetry.

That leaves a credible E8 frontier: test whether the new binary 40-point complement is the same 40-point G-set that already occurs as the E8 root-fibration base.  This is a map problem, not a matching-integer argument.

A separate replay (`w33_pass7162_e8_outer_character_audit.py`) also compares the code's `S3 wr C2` coordinate action with several natural coordinate-permutation extensions on the standard 240-root + 8-axis E8 model.  It is intentionally not promoted until its certificate is frozen.

## Publication boundary

The theorem-grade statements in Passes7155--7158 and 7160--7162 are exact algebraic consequences of the prior frozen q=9/hexad certificates plus the proofs above.  Pass7154 (target-48 SAT) and the stronger Pass7159 subgroup-conjugacy decision remain queued exact computations and are not silently interpreted as solved.
