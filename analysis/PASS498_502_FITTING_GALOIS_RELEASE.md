# Passes 498–502 — Fitting, product-ring, Galois-cycle, and small-ring release

This release executes the five directions opened after Pass 497.

## Pass 498 — Fitting mechanism and the minimum-law reduction

For a DVR `R` with uniformizer `lambda`, a finite cyclic torsion module

`M = R/(lambda^d)`

has

`length(M)=d` and `Fitt_0(M)=(lambda^d)`.

If `M` is a common quotient of the arithmetic budget module
`R/(lambda^a)` and the Hjelmslev budget module `R/(lambda^g)`, then

`d <= min(a,g)`.

If the final permitted graded layer survives, then

`d=min(a,g)`.

This gives the exact commutative-algebra mechanism that could explain the
higher-conductor depth law. It also gives a no-go: treating both filtrations as
divisibility lower bounds yields `max(a,g)`, not `min(a,g)`. The remaining proof
obligation is now precise: construct the determinant-gap cokernel, prove the two
quotient maps, and prove survival of the last allowed layer.

## Pass 499 — exact product-ring discriminator

For

`R=(Z/9) x F_9`,

we have

`|R|=81`, `v_lambda(|R|)=24`, and `|P^1(R)|=12*10=120`.

A separable tensor slice is too symmetric: exact depths `60,66,96` occur and do
not see the generic minimum.

The full one-pair family is nevertheless exactly reducible. The flat block is

`F=81 P-I`,

and changing only the pair `±(0,b)` is diagonal away from parity. The determinant
therefore factors into one `1 x 1` block and forty `2 x 2` blocks.

The exact witness

`b=(0,tau)`, `c=(1,0)`

attains

`v_lambda(det B-det F)=24`.

This is the seventh higher-conductor exact point and selects the arithmetic
budget over the projective budget by a factor of five.

## Pass 500 — Galois phase-cycle compiler overlay

Write

`t=zeta_9+zeta_9^{-1}`,

so `t^3-3t+1=0` and every real determinant gap has a unique representation

`A+B t+C t^2`.

The three real embeddings indexed by `u=1,2,4 mod 9` produce a `3 x 3`
Vandermonde system. The compiler overlay reserves BT1653 guard-page time bins

`2032,2033,2034`

for those phase settings and

`2035,2036,2037`

for matched references.

The reconstruction order is essential:

1. measure the three real embeddings;
2. reconstruct and round the integer coefficients `(A,B,C)`;
3. compute the exact relative norm;
4. recover lambda-depth as twice the `3`-valuation of the relative norm.

Bounded-noise synthetic tests recover depths `8,12,18,24` exactly. The actual
product-ring witness also reconstructs depth `24`. However, its coefficients
have 153 digits, so direct analog rounding would require roughly 156 significant
digits. The overlay is therefore an exact algebraic compiler, not a claim of
current experimental feasibility. A practical implementation requires digital
or modular accumulation.

## Pass 501 — small Frobenius-ring census

A declared standard-family catalogue of 40 odd p-primary commutative Frobenius
rings and products of size at most 81 was assembled. It is explicitly not
represented as the complete all-rings isomorphism classification.

The decisive collision pair is

`F_3[x]/(x^4)`

and

`F_3[x,y]/(x^2,y^2)`.

They are nonisomorphic: their embedding dimensions are 1 and 2. But they have
identical size, character order, residue field, ramification budget, projective
budget, and predicted depth. Exact parity-block determinants give

`depth=12`

for both. Thus the low-conductor law is insensitive to substantial multiplication
geometry in this sharp comparison.

## Pass 502 — Lean formal support

Two theorem-backed pieces are formalized without importing the conjectural
sharp-attainment step:

- the Gram matrix of a canonical uniform `p`-sheeted incidence cover is `p I`;
- if selected embedding values are fixed by the involution, the product over
  conjugate pairs is the square of the half-orbit product.

The Python support certificate checks finite Gram instances, paired-product
identities, source custody, theorem names, and absence of `sorry`. The GitHub
Lean workflow is the authoritative compile test.

## Validation boundary

Exact determinant and arithmetic certificates are complete for the selected
families. The higher-conductor minimum law remains a conjecture. Pass 498 reduces
its proof to explicit module-theoretic hypotheses; it does not assert those
hypotheses without construction.
