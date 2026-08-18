# Passes 7146--7153 — exact q=9 closure attack, PGL2 quotient theorem, hexad and code anatomy

## Scope firewall

Everything in this packet is finite symplectic geometry, finite-group representation theory, finite-field matrix algebra, graph theory, SAT certification, or binary coding theory.  Nothing here identifies the finite objects with particles, couplings, continuum fields, laboratory hardware, or a physical theory.  Pass7146 becomes an optimality theorem only if the separately replayed eight-case SAT certificate is present and says that every residual 512-state compatibility graph has clique number at most 47.

## Pass7146 — eight exact 512-state decisions

Pass7139 proved that a hypothetical 52-point partial ovoid in W(3,9), after choosing a nonsingular four-anchor block and quotienting projective/Frobenius gauge, must lie in one of exactly eight anchor types

```
(1,1,2) (1,1,3) (1,1,4) (1,1,5)
(1,2,3) (1,2,4) (1,3,4) (1,3,5).
```

For each type there are exactly 512 normalized residual rows `(1,a,b,c)`, with `a,b,c != 0`.  Pass7146 encodes incompatibility by binary clauses and the target clique size by a totalizer cardinality constraint.  Every SAT model is independently checked against the GF(9) rank-four Gram pairing law.  Each final UNSAT query is frozen together with a SHA256 of the generated CNF.  The certificate lives in `data/PART_W33_PASS7146_EXACT_EIGHT_CLIQUES.json`; no q=9 optimality statement is to be promoted unless that file exists and replays.

A useful additional invariant is that all eight sparse *conflict* graphs have least real eigenvalue `-10=-(q+1)` (multiplicity 101 at q=9), despite three different degree classes.  This is recorded as a search hint rather than used as an unsupported clique upper bound.

## Pass7147 — the C2 pair quotient is a PGL2 involution Schreier graph

Work in the dual-Lagrangian normal form

`V = E_+ ⊕ E_-`, `g(u,w)=(u,-w)`, `B((u,w),(u',w'))=u·w'-w·u'`.

For an eligible nonfixed orbit, `u·w != 0`.  Define

```
M(u,w) = [[u1,u2],[w2,-w1]].
```

Then `det M = -u·w`, hence `M` is invertible.  Projective rescaling sends `M -> cM`, while the involution sends `M -> D M` with `D=diag(1,-1)`.  Therefore the eligible pair-orbits are canonically

`G/H`, with `G=PGL2(q)` and `H=<D>`.

The count is immediate:

`|G/H| = q(q^2-1)/2`,

exactly the pair-node count found geometrically.

Let `I` be the complete projective involution class of `G`; for odd q it has `q^2` elements.  On `G/H`, let

`W = sum_{t in I} rho(t)`.

Because `I` is a conjugacy class, `W` is central in the permutation algebra.  The standard PGL2(q) character calculation on `Ind_H^G(1)` gives

- `q^2`, multiplicity 1;
- `+q`, multiplicity `(q+1)(q^2-q-4)/4`;
- `-q`, multiplicity `q(q-1)^2/4`;
- `1`, multiplicity `q(q+1)/2`.

`W` is weighted: the diagonal contribution is the unique involution in a vertex stabilizer, and a second involution can reach the same adjacent H-coset exactly when the two stabilizer involutions lie in the same split-torus normalizer.  Let `R` mark these doubled off-diagonal entries.  The normalizer fibers give

`R = disjoint union of q(q+1)/2 copies of K_{h,h}`, `h=(q-1)/2`.

Thus the simple pair graph is exactly

`A_pair = W - I - R`.

The class sum commutes with `R`.  Decomposing each split-normalizer fiber into its `+h,-h,0` eigenspaces and intersecting with the four central W-isotypic pieces gives the pair spectrum

- `(2q^2-q-1)/2`, multiplicity 1;
- `q-1`, multiplicity `q(q-3)(q+1)/4`;
- `-(q+1)`, multiplicity `q(q-3)(q-1)/4`;
- `(q-1)/2`, multiplicity `(q-1)(q+2)/2`;
- `-(q+3)/2`, multiplicity `q(q-1)/2`;
- `0`, multiplicity `q(q-3)/2`;
- `-(q-1)/2`, multiplicity `q`.

The exact producer independently rebuilds the PGL2 coset operator at q=3,5,7 and checks `W`, `R`, `[W,R]=0`, and the simple-graph spectra.

### Adding the two fixed generator lines

The fixed block consists of two `(q+1)`-point generator lines.  After matching the unique cross-line orthogonal partners,

`A_F = [[J-I,I],[I,J-I]]`.

The cross-incidence matrix C from fixed nodes to pair nodes satisfies

`C C^T = [[q h I, h(J-I)],[h(J-I),q h I]]`, `h=(q-1)/2`.

The fixed/pair partition is equitable with quotient matrix

```
[[q+1, q(q-1)/2],
 [2,   (2q^2-q-1)/2]].
```

Hence two simple eigenvalues are the roots of

`2x^2-(2q^2+q+1)x+(2q^3-q^2-1)=0`.

On the four orthogonal fixed-space sectors (constant symmetric, constant antisymmetric, and the two `(q)`-dimensional zero-sum symmetric/antisymmetric sectors), the known singular values of C and the pair-graph eigenvalues give the remaining two-by-two blocks.  The full quotient spectrum is therefore, for every odd q:

- `q-1`, multiplicity `(q+1)(q^2-3q+4)/4`;
- `-(q+1)`, multiplicity `q(q-3)(q-1)/4`;
- `-(q+3)/2`, multiplicity `q(q+1)/2`;
- `(q-1)/2`, multiplicity `(q-1)(q+2)/2`;
- `0`, multiplicity `q(q-3)/2`;
- `-(q-1)`, multiplicity `q`;
- the two simple roots above.

This upgrades the Pass7141 q=3,5,7,9 pattern from CONJECTURE to THEOREM.  The PGL2/cross-ratio association-scheme setting is standard; the particular involution-support fusion and its identification with the C2 partial-ovoid quotient are the repo-derived step.

## Pass7148 — compatibility entirely in M2(Fq)

For pair nodes represented by invertible matrices M,N, set `R=M N^{-1}`.  Direct expansion shows that the two diagonal entries of `M adj(N)` are, up to the same nonzero scalar,

`-u·w'` and `-w·u'`.

The two C2 orbits conflict iff at least one of the four representative pairings vanishes, hence iff

`R_11 = +R_22` or `R_11 = -R_22`.

Equivalently,

`tr(R)=0` or `tr(DR)=0`.

For 2x2 projective matrices in odd characteristic, trace zero is precisely the nontrivial projective-involution condition.  Thus pair conflict is a pure relative-matrix statement: **R or DR is a projective involution**.  The q=9 producer verifies this objectwise over all `C(360,2)=64620` pair-node pairs.

## Pass7149 — exact D12 hexad stabilizer and unique-hexad theorem

Pass7131 proved the stabilizer of one 51-witness S in PΓSp(4,9) is exactly C2.  Pass7144 constructed a D12 acting on a hexad H of six such witnesses.  If an ambient semilinear symplectic map stabilizes H setwise, it sends a chosen S to one of the six members.  For each target there are at most `|Stab(S)|=2` such maps.  Hence

`|Stab(H)| <= 6*2 = 12`.

The known D12 already has order 12, so

`Stab_{PΓSp(4,9)}(H) = D12`.

With `|PΓSp(4,9)|=6,886,425,600`,

`#hexads = 6,886,425,600/12 = 573,868,800`.

The witness orbit has

`6,886,425,600/2 = 3,443,212,800`

members.  Since

`573,868,800 * 6 = 3,443,212,800`,

every witness in this orbit belongs to **exactly one** D12 hexad.

The 248 union coordinates have the following six-bit membership-column multiset:

- the six singleton columns, each multiplicity 32;
- six weight-2 columns internal to a distinguished `3+3` partition, each multiplicity 3;
- nine weight-2 cross-block columns, each multiplicity 4;
- two complementary weight-3 columns, each multiplicity 1.

The abstract automorphism group of this membership multiset is `S3 wr C2` of order 72, verified by exhaustive S6 permutation.

## Pass7150 — [248,6,51] code anatomy

The dual distance is exactly 2 because repeated nonzero columns occur.  The exact number of weight-two dual words is

`sum_c binom(m_c,2) = 3048`.

A MacWilliams transform gives the low dual coefficients

`A0=1, A1=0, A2=3048, A3=56790, A4=5006140, A5=146155716, A6=6113331833, A7=179798854824, A8=5351507131762, A9=136090424710256, A10=3226214403894780`.

Because the six singleton columns have the unique maximal multiplicity 32, any GL(6,2) stabilizer of the column multiset must permute the six basis vectors.  The multiplicity-3/4 pair pattern then forces preservation of the unordered `3+3` partition.  Thus the outer linear/column-pattern group is exactly

`S3 wr C2`, order 72.

Within repeated coordinate classes, arbitrary permutations act trivially on the code.  Hence the full coordinate-permutation automorphism group is

`((S_32)^6 x (S_4)^9 x (S_3)^6) semidirect (S3 wr C2)`,

of factored order

`72*(32!)^6*(4!)^9*(3!)^6`.

No nonzero weight shell is a 1-design on all 248 coordinates; the regular object is instead the membership-pattern stratification.  This prevents a tempting but false design overclaim.

As an F2[D12]-module, the six generator words carry the natural hexagon permutation module.  For a six-cycle r,

`x^6-1=(x+1)^2(x^2+x+1)^2` over F2.

Thus the 6-dimensional module has a 2-dimensional `(x+1)^2` primary piece and a 4-dimensional `(x^2+x+1)^2` primary piece, with composition factors `1,1,V2,V2`.  Equivalently `im(I+r^3)=ker(I+r^3)` is a 3-dimensional invariant submodule and both it and the quotient have factors `1+V2`.

## Pass7151 — bonkers: the quotient quartic factorizes into two symplectic channels

Writing X=(u,w), Y=(u',w') in the normal form,

`Delta_D(X,Y)=(u·w')^2-(w·u')^2`

factorizes as

`Delta_D = -(B(X,Y)) (B(X,DY))`

up to the fixed sign convention for D.  So the C2 quotient conflict law is not an irreducible quartic condition: it is the union of the original symplectic orthogonality divisor and its D-twist.  This is a finite-algebra statement only.

## Pass7152 — bonkers: exact code/geometric symmetry gap

The hexad has ambient geometric stabilizer D12 of order 12 but abstract code/membership outer group `S3 wr C2` of order 72.  Therefore

`[Aut_outer(code pattern) : Aut_geometric(hexad)] = 6`.

The extra six cosets are exact code-only symmetries: they preserve the 248-column multiset but are not induced by ambient PΓSp(4,9) transformations of the hexad.

## Pass7153 — bonkers: one puncture breaks the block swap, two restore it

The two multiplicity-one weight-3 columns are complementary and occur at ambient points 50 and 80.  Puncturing point 50 produces a `[247,6,50]` code.  The surviving unique triple column distinguishes one side of the `3+3` partition, so the outer group drops from order 72 to `S3 x S3`, order 36.

Puncturing **both** 50 and 80 produces a `[246,6,50]` code.  With both distinguished triple columns removed, the unordered `3+3` partition again admits its block swap, restoring `S3 wr C2`, order 72.

Thus a second puncture restores a symmetry destroyed by the first.  This is exact combinatorics, not a physical symmetry-breaking claim.

## Literature interface

Hollmann--Xiang's PGL2 conic work and Ma--Wang's sharply 3-transitive/cross-ratio schemes establish the standard association-scheme setting in which PGL2 orbitals and fusions are treated.  The repo result here is the explicit identification of the C2 partial-ovoid quotient with the split-involution coset action, the involution-support operator `W`, and the normalizer correction `R`.
