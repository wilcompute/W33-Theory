# Passes 3635–3648 — Exact Monster/U4(2) completion, rank-24 algebra, and two chamber breakthroughs

## Release status

This packet executes the five open Monster fronts from Passes 3614–3627 and adds two outside-the-box constructions. The exact Python verifier reproduces frozen semantic certificate

`cf276859798326def36c2bdc0e9fb75dbdadbbc44d69ba61cae24b5c82f40271`.

The character-table restriction remains a separate GAP/CTblLib certificate. No concrete Monster-word embedding or degree-81 multiplicity is promoted before that artifact is generated.

## 1. Explicit abstract U4(2) carrier

The forty projective points of `F_3^4` are joined by symplectic orthogonality, giving

\[
W(3,3)=\operatorname{SRG}(40,12,2,4),
\qquad
A^2=8I-2A+4J.
\]

Four order-three symplectic transvections, based at

\[
(1,1,0,1),\ (0,1,2,2),\ (1,2,2,2),\ (1,2,1,2),
\]

generate a permutation group of order

\[
\boxed{25,920=|PSp(4,3)|=|U_4(2)|}.
\]

Its complete element-order census is

\[
1^1,\ 2^{315},\ 3^{800},\ 4^{3780},\ 5^{5184},\ 6^{5760},\ 9^{5760},\ 12^{4320}.
\]

An explicit compressed pair has orders

\[
|x|=2,\qquad |y|=5,\qquad |xy|=12,
\]

and generates the full order-25,920 group. This is a concrete certificate for the repo's abstract W33 symmetry. It is not yet a pair of serialized Monster words.

## 2. Degree-81 Monster restriction front

The GAP companion loads `U4(2)` and `M`, identifies the unique degree-81 U4(2) character, verifies its vanishing on all nonidentity classes of orders three and nine, and enumerates possible class fusions with decomposability initially disabled.

The 5B-containing screen imposes the documented constraints

\[
2\mapsto2B,\qquad 3\mapsto3B,\qquad 5\mapsto5B,
\]

plus the `4B -> 4D` constraint. The Monster degree-196883 character is then restricted along every surviving map. Only nonnegative integral decompositions are retained, and the complete set of possible Steinberg multiplicities is exported.

The workflow is fail-closed: character-table fusion is not treated as a concrete `mmgroup` embedding, and ambiguity is reported rather than resolved by preference.

## 3. The 2B-local linear algebra is already full

For the W33 eigenvalue-two projector numerator

\[
N=(12I-A)(A+4I),
\qquad
N^2=60N,
\qquad
\operatorname{rank}N=24,
\]

choose twenty-four independent columns to obtain forty carrier vectors in a 24-dimensional coordinate system.

Their symmetric tensors span

\[
\boxed{\dim\operatorname{Sym}^2(\mathbf Q^{24})=300},
\]

and their alternating tensors span

\[
\boxed{\dim\Lambda^2(\mathbf Q^{24})=276}.
\]

Therefore the combined carrier-generated linear space has dimension

\[
300+276=576=24^2,
\]

so it fills the entire matrix algebra

\[
\boxed{M_{24}(\mathbf Q)}
\]

at the linear-span level. This is a decisive local-algebra result: the W33 carrier is not deficient in bilinear operator directions. It does not prove that a particular Griess, Majorana, or VOA product is preserved.

## 4. Scalar Leech glue is impossible

The Smith nonzero invariants of the integral projector Gram form are

\[
2^1,\qquad 10^9,\qquad 30^6,\qquad 60^8.
\]

Consequently its discriminant has prime valuation profile

\[
\boxed{2^{32}3^{14}5^{23}}.
\]

The 5-adic exponent is odd. Multiplying a rank-24 form by any rational scalar changes every prime valuation by a multiple of 24, hence cannot change that parity. Therefore no scalar rescaling of this same rank-24 lattice can possess a unimodular overlattice.

\[
\boxed{\text{Scalar-rescaled W33 projector lattice }\not\rightsquigarrow\Lambda_{24}.}
\]

Any Leech route must first use non-scalar coupling, a quotient, a discriminant-form extension involving another lattice, or a multi-copy construction.

## 5. Exact graded modular completion

The rootless rank-24 theta numerator is

\[
\Theta_{\Lambda}(q)=E_4(q)^3-720\Delta(q),
\]

with initial coefficients

\[
1,\ 0,\ 196560,\ 16773120,\ 398034000,\ 4629381120.
\]

The 24-boson oscillator factor

\[
\prod_{n\ge1}(1-q^n)^{-24}
\]

begins

\[
1,\ 24,\ 324,\ 3200,\ 25650,\ 176256.
\]

Their exact product gives

\[
1,\ 24,\ 196884,\ 21493760,\ 864299970,\ 20245856256,
\]

namely the initial coefficients of `J+24` in the packet's shifted indexing.

This closes the earlier raw-moment no-go by identifying the minimum missing machinery: a rootless rank-24 modular numerator multiplied by the 24-oscillator denominator. W33 supplies an exact multiplicity-24 carrier, but incidence alone does not prove rootlessness or select the Leech numerator.

## BONKERS 1 — The complete A5/A6/S6 chamber geometry

The full group contains exactly

\[
\boxed{432}
\]

A5 subgroups, in two conjugacy orbits

\[
216+216.
\]

There are exactly

\[
\boxed{51,840}
\]

ordered `(2,3,5)` presentation pairs. Join two A5 subgroups when their intersection is a D10. The resulting graph has

\[
432\text{ vertices},\qquad 1296\text{ edges},\qquad k=6,
\]

and decomposes into

\[
\boxed{36K_{6,6}}.
\]

Every edge generates an A6 of order 360. Thus the 36 connected components are exactly 36 A6 chambers, and each chamber's normalizer in U4(2) has order

\[
\boxed{720},
\]

hence is S6.

This refines the Monster A5-amalgam program: a bare D10-sharing pair closes locally at A6. Reaching U4(2) requires the chamber normalizer or additional ambient gluing data, not merely the naked A5 pair.

## BONKERS 2 — A transvection tetrahedral amalgam

The four order-three transvections have pair-product orders

\[
3,6,6,6,6,6.
\]

Every three-generator face generates an order-648 subgroup and fixes exactly one W33 point. The four faces fix four distinct points:

\[
(1,0,1,2),\quad(1,2,2,0),\quad(0,1,0,1),\quad(0,1,1,2).
\]

Thus U4(2) is generated here by a tetrahedral amalgam of four point stabilizers:

\[
\boxed{648\ \overset{4\text{ faces}}{\longrightarrow}\ 25,920}.
\]

This gives a compact geometric presentation target for future Monster-word descent: search for four order-three Monster elements whose face subgroups reproduce these stabilizers and whose total closure is U4(2).

## Evidence boundary

### Proved by the exact Python certificate

- the explicit order-25,920 40-point group and its element-order census;
- the compressed `(2,5,12)` generating pair;
- the four order-648 point-stabilizer faces;
- all 432 A5 subgroups, both 216-orbits, all 1,296 D10 edges, and all 36 A6/S6 chambers;
- the full 300+276 tensor spans;
- the Smith profile and scalar Leech-glue obstruction;
- the initial modular-completion coefficients.

### Delegated or still open

- the completed GAP class-fusion census and resulting degree-81 multiplicity set;
- concrete `mmgroup` words for U4(2) inside the Monster;
- a unique Monster class fusion;
- a Griess, Majorana, or VOA multiplication map;
- a non-scalar Leech-lattice completion;
- any laboratory or physical interpretation.
