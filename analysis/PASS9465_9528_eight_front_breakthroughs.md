# Passes 9465–9528 — unitary weld, centralizer fingerprint, all-rung root shadow, robust readout, and three outside-box attacks

## Scope and evidence boundary

This packet executes the five continuation targets from Pass9197–9260 plus three independent outside-box attacks.  The range was reserved on master at 2026-08-23T21:46:58Z, before the later conflicting Pass9481–9504 Bruhat–Tits reservation (21:55:59Z); under the repo's earliest-reservation convention this packet owns 9465–9528.  The parallel Bruhat–Tits mathematics is preserved but its later labels are noncanonical until rehomed.

Finite claims are represented by executable scripts `analysis/w33_pass9465_...` through `analysis/w33_pass9521_...` and frozen JSON certificates.  Standard classical-group identifications are labeled as such.  The optical section is a bounded finite transfer model, not a fabricated device Hamiltonian.

## 1. Pass9465–9472: the F9 structure closes to a unitary/Hermitian package, while the ordered glues become projectively rigid

From the transverse Golay glue `C_G` and E6-relative glue `C_E`, rebuild the Pass9237 operators `K,S,R` and set

`B = K R^T`.

The verifier proves:

- `K` is alternating and nondegenerate;
- `R^2=-I` and `R` is `K`-symplectic;
- `B` is symmetric, nondegenerate and plus type in dimension 12;
- `C_G` and `C_E` are mutually `B`-orthogonal;
- each restriction of `B` to `C_G` or `C_E` is nondegenerate minus type in dimension six;
- the same two spaces are maximal isotropic/Lagrangian for `K`;
- `S` preserves `B`, reverses `K`, and satisfies `SRS=-R`.

Consequently the standard semisimple-centralizer theorem gives

`C_{Sp(12,3)}(R) ~= U(6,3)`

with

`|U(6,3)| = 3^15 * product_{i=1}^6 (3^i-(-1)^i)`

`= 182699779456696320`.

The packet then exhausts the signed-coordinate monomial stabilizer of the ordered pair `(C_G,C_E)`.  The E6-relative code has signed monomial group order `62,208`, but the common stabilizer with ternary Golay is exactly

`{+I,-I}`.

So the ordered pair is **projectively rigid in the signed-monomial coordinate group**, despite living inside an enormous ambient unitary centralizer.

## 2. Pass9473–9480: orthogonal subtype helps the Suzuki weld, but R exposes a quantified transport obstruction

The existing Suzuki `Q+(5,3)` controller has 90 orbits on 7,371 nondegenerate two-space/W33 candidates: 62 hyperbolic orbits and 28 anisotropic orbits.  Thus fixing the orthogonal subtype is genuinely additional data but remains far from unique.

The stronger `R` datum cannot yet be attached invariantly.  The Niemeier `(K,R)` space and the Suzuki 12D symplectic module are independently constructed; no certified objectwise symplectic isometry between them exists.  The conjugacy orbit of a complex structure of this type has size

`[Sp(12,3):U(6,3)] = 78795564505342027200`.

Therefore choosing a transport arbitrarily amounts to choosing among about `7.88e19` conjugate `R` structures.  The Hall–Janko 416-carrier and its two-sheet Leech incidence cover are promising data for constructing a canonical transport, but they do not currently supply one.

This is an obstruction statement, not a proof that no canonical transport can exist.

## 3. Pass9481–9488: the complete rank-24 centralizer fingerprint

The three carriers now have exact projective quotient images:

| carrier | projective centralizer image | order | root-shadow meaning |
|---|---:|---:|---|
| `E8^3` | `PSp(4,3)` | `25,920` | all W33 points |
| `E6^4` | `3^3:S4` | `648` | full stabilizer of one W33 line |
| `A2^12` | `3^3:A4` | `324` | orientation-preserving stabilizer of one W33 line |

The A2 result is recomputed from the Golay lattice witness.  The signed Golay centralizer of the `3^4` carrier has 72 lifts; their exact 24D lattice actions induce an Sp-image of order 648 and a projective image of order 324.  The action on the four carrier cycles is exactly `A4`.

For E8, the repo-certified Springer theorem gives

`C_{W(E8)}(j3) = C3 x Sp(4,3)`

with the carrier `C3` itself as kernel on `E8/(I-j3)E8`.  A diagonal copy of this centralizer commutes with the rank-24 3-cycle lift and induces the same full `Sp(4,3)` quotient action, which is already maximal possible.

**New interpretation:** E6 selects an *unoriented* W33 line; A2/Golay selects the same type of line plus one orientation-parity bit.

## 4. Pass9489–9496: all-rung E8 root-shadow periodicity is now a formal theorem

For the one-step lift

`L(g)(x0,x1,x2) = (x2, g x0, x1)`,

the map

`[(x0,x1,x2)] -> [x0+x1+x2]`

is an explicit isomorphism

`coker(I-L(g)) ~= coker(I-g)`.

The kernel proof is constructive.  If

`z0+z1+z2=(I-g)t`,

then

`y=(t, t-z0-z2, t-z0)`

satisfies `(I-L(g))y=z`.

Iterating the block-sum isomorphism shows that a root in any leaf E8 factor maps to exactly its base E8 quotient class.  Since the base E8 shadow is six roots over each of the 40 W33 points, for every `m>=0`:

`rank = 8*3^m`,

`E8 factors = 3^m`,

`roots/W33 point = 6*3^m`,

`total roots = 240*3^m`.

This replaces the previous four-rung extrapolation by a dimension-independent induction.

## 5. Pass9497–9504: W33-native crosstalk and detector errors do not erase the rank-24 discriminator

Use an `n`-stage lazy W33 transfer kernel

`T_eta = (1-eta)I + eta A_W33/12`.

For a fixed W33 line, the partition `{4 line points, 36 off-line points}` is equitable: a line point has 3/12 neighbours on the line and an off-line point has 1/12.  Therefore an initially line-supported signal has exact line mass

`p_n = 1/10 + (9/10)(1-5 eta/6)^n`.

Allow arbitrary port gains in `[1-delta,1+delta]` with `delta=1/4`.  The delocalized E8 signal can fake at most `5/32` line mass.  A line carrier remains provably above that bound precisely when

`p_n > 25/106`,

or equivalently

`(1-5 eta/6)^n > 8/53`.

For one stage with `eta<=2/5`, the worst-case observed line lower bound is `7/12`, leaving exact gap `41/96` over the E8 upper bound.

For the dark monitor, under a binary-symmetric confusion model `d_obs=rho+(1-2rho)d` with `rho<=1/10`, the zero-dark E8/A2 carriers stay at or below `1/10`, while E6 remains at or above `1/4`: exact gap `3/20`.

So the two-observable carrier classifier survives substantial W33-native crosstalk and bounded detector error in this finite model.

# Three outside-box attacks

## 6. Pass9505–9512: a double-minus orthogonal polarization inside a plus-type 12D bulk

The compatible symmetric form has the exact decomposition

`(F3^12,B) = (C_G,B|G) orthogonal_sum (C_E,B|E)`

with bulk type `O+(12,3)` and both halves type `O-(6,3)`.

Each half therefore carries its own `Q-(5,3)`:

- 112 singular projective points;
- 3,640 degenerate two-spaces;
- 4,536 hyperbolic two-spaces;
- 2,835 anisotropic two-spaces;
- 7,371 nondegenerate two-spaces.

Simultaneously, both halves are Lagrangian for `K`.  `K` stabilizes the halves, while `S` and `R` exchange them; `S` acts as finite-field conjugation in the sense `SRS=-R`.

Thus the glue pair produces two orthogonal Q-minus selector spaces inside one O-plus bulk, with a simultaneous symplectic polarization.

## 7. Pass9513–9520: the tempting Hall–Janko/Q-minus 252 bridge is tested and the naive version is falsified

The parallel G2(4) fixed-edge partition is

`36 + 63 + 63 + 252`.

Meanwhile `Q-(5,3)` has

`112 singular + 126 norm-1 + 126 norm-2 = 364`

projective points.  Hence two striking count matches appear:

`252 = number of Q-minus nonsingular points`,

`63+63 = 126 = size of either Q-minus norm class`.

The natural graph test rejects both naive identifications.  Orthogonality on all 252 Q-minus nonsingular points has degree 81, while the G2 `D`-cell induced graph has average degree 66.  Within either 126-point Q-minus norm class the orthogonality degree is 45, while the G2 `B union C` induced graph has average degree 31.

So the count matches are real but **not** natural graph isomorphisms.  Any surviving Hall–Janko/Q-minus bridge has to use a different orbital of the rank-14 G2 edge association scheme.

## 8. Pass9521–9528: exact selector-information budget

The centralizer chain has a direct log-cardinality interpretation:

`25920 / 648 = 40` — choosing the E6 root-shadow line costs `log2 40 = 5.321928...` bits;

`648 / 324 = 2` — choosing the A2/Golay orientation parity costs **exactly one more bit**.

Thus the E8-to-A2 centralizer fingerprint carries `log2 80 = 6.321928...` bits of finite symmetry-breaking data.

For Suzuki, orthogonal subtype supplies only `log2(90/62)=0.538` bits in the hyperbolic case or `log2(90/28)=1.684` bits in the anisotropic case at controller-orbit level, consistent with its failure to select uniquely.

An arbitrary complex structure `R` among its Sp(12,3) conjugates would require

`log2 [Sp(12,3):U(6,3)] = 66.094748...` bits

to label.  The ordered transverse glues instead derive `R` algebraically.  This is a description-length statement, not thermodynamic entropy.

## Cross-track note: namespace and Bruhat–Tits lane

A later parallel reservation claimed Pass9481–9504 for a Bruhat–Tits-building interpretation of the Leech filtration.  Its mathematics is interesting and independent: the filtration is identified with a simplex and the measured depths with cyclotomic ramification indices.  However that reservation landed after the Pass9465–9528 reservation, so its pass labels collide under the repository's established earliest-reservation rule.  This packet does not delete or rewrite the parallel work; it records the collision so it can be rehomed cleanly.

## External provenance

Standard ingredients not claimed as repository discoveries include the order formula for finite unitary groups and the semisimple-centralizer description of symplectic groups.  The new content here is the explicit glue-derived `(K,B,R)` package, the common-monomial rigidity computation, the completed A2/E6/E8 quotient-centralizer comparison, the all-rung block-sum proof, the transfer/noise bounds, and the tested/falsified Hall–Janko count bridge.
