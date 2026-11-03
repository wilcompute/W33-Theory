# A27-coordinate common cover exists, with a sharp coupling tradeoff

This addendum follows the published eight-front packet `fa513b2ad`. It pursues
the common-cover question further after the313-coordinate induced compression.
It uses the original signed27 generators unchanged and the same enlarged
spinor Clifford generators. Neither the common-cover obstruction nor the
previous313 result claimed global minimality.

## Construction and exact order

Let L be the old signed native-cubic group, order30,720. Its six signed
generators act faithfully on54 signed coordinate symbols. Exact
Schreier-Sims and derived-subgroup computations show **L is perfect**.

Let K be the full linear spinor Clifford group, order46,080. Reduce the actual
matrices into GF(17) with i=4 and sqrt2=6. The orbit of e0 contains480 vectors,
including all four basis vectors, and the generated permutation group on this
orbit has order46,080. Since the original group has that same certified order,
this reduction is faithful.

Use paired generators (l_j,U_j) for the old six, and **(I27,U_new)** for the
new gate. Their action on the disjoint union of54+480 symbols is faithful.
The exact generated group order is

```
30,720 * 46,080 = 1,415,577,600.
```

The scalar cubic remains the original45-term native polynomial on **27**
coordinates. This is much smaller than the original induced common cover,
whose order was46,080*2^60, and uses fewer coordinates than313. It is a
different cover, not a quotient contradicting the induced-cover obstruction.

There is also a conceptual proof. K has a normal2-group P of order64 and
K/P is S6. A common quotient Q of L and K has3-part at most3, so Q/image(P)
cannot be S6. The proper quotients of S6 are1 and C2. Thus Q is a2-group,
but it is also perfect as a quotient of L. A finite perfect2-group is trivial.
By classical **Goursat's lemma**, the paired group is therefore exactly L×K.
For a statement of the lemma in current research, see
[Homomorphism extension problem for subdirect products](https://arxiv.org/abs/2603.17515),
Lemma2.1. The proof and the finite permutation calculation agree.

An independent GAP script checks the old group and its derived subgroup,
the480-vector Clifford image, the534-point paired group, the2-core quotient
S6, and the bilinear dimensions below. Its generated input permutations and
finite-field matrices are frozen alongside the Python certificate.

## The smaller carrier does not supply the desired mixed cubic

The earlier interaction calculation already owns a crucial constraint: the
old diagonal-kernel words act by±I4 on spinors and eliminate26 of27 possible
linear scalar coefficients. The sole allowed scalar-spinor-spinor tensor is

```
phi0 * psi^T Omega eta.
```

The addendum reconstructs every kernel word on the actual spinor matrices.
It independently checks that the six old bilinear constraints have nullity1,
spanned by Omega. The added gate instead gives U-transpose*Omega*U orthogonal
to Omega. Adding its constraint gives nullity **zero**, both exactly in
characteristic zero and independently modulo17 in GAP.

More strongly, this obstruction does **not** depend on choosing I27 for the
new scalar action. Any invariant in an unchanged old27 module must first lie
in the one-dimensional old invariant space. Applying an arbitrary linear new
scalar action and U_new to this rank-one scalar/bilinear tensor can preserve
it only if U_new-transpose*Omega*U_new is proportional to Omega. It is not.
Therefore **no extension retaining both prescribed old representations and
this new spinor gate admits a nonzero cubic linear in the scalar and bilinear
in the two4-spinors**, regardless of a larger abstract cover.

This does not rule out Hermitian, higher-degree, additional-field or changed
embedding interactions. The November2 nonmonomial27 construction explicitly
changes the old embedding and contains a six-dimensional bilinear covariant.
It remains a distinct constructive route. The present27-coordinate cover
preserves the old cubic but exposes the coupling price, rather than resolving
it by group-order matching.

## Reproduction and scope

Run `py -3 analysis/w33_20261103_product_cover_coupling_tradeoff.py`, then the
frozen GAP companion with `scripts/run_gap.sh` as documented in that wrapper.
The Python JSON exports the actual534-point paired permutations,480-vector
orbit, mod17 spinor matrices and the two bilinear forms. The GAP JSON records
the independent engine results. The publication receipt retains their actual
execution evidence and parent-input hashes.

The result is a finite common-cover construction and a specified interaction
no-go. It does not identify physical matter, choose a vacuum, prove a global
minimum cover order, or complete a TOE.

Five independent investigations: find covariant changed-embedding interactions;
stabilize the conditional ADS branch; compile all measurement branches with
feedforward; prove thermodynamic tunneling bounds; construct symmetric twisted
interfaces.
