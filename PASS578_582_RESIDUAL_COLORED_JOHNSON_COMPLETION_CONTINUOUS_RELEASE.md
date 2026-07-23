# Passes 578–582 — residual collision symmetry, colored 600-cell packet module, Johnson quotient, cyclotomic completion, and continuous readout enclosure

This release executes the five directions opened after Pass 577 and incorporates the proposed 600-cell `12 + 1` interpretation as a falsifiable structural hypothesis.

## Pass 578 — classify the post-`C3` collision structure

The structured `F3^13` family has 797,162 sign-projective parameter words and 221,451 characteristic polynomials.  The hidden shear `C3` gives 266,450 projective orbits, leaving an orbit excess of 44,999.

Two exhaustive symmetry searches were performed.

1. The natural fibre-value relabelling group `S3 wr S4`, of order 31,104, has exactly three global projective spectral symmetries: the previously identified `C3`.  No global involution extends it to `S3`, `C3^2`, or a Heisenberg group inside this natural action.
2. On the 1,094-point fixed locus of the `C3`, all `2^7 7! = 645,120` monomial maps were exhausted.  The exact induced projective symmetry is `S3`, acting on three constant coordinates with a sign twist on odd permutations.

This fixed-locus `S3` closes 22 of the 23 exceptional three-point fibres as single `S3` orbits.  The remaining exceptional triple consists of three `S3`-fixed points.  Combining the global `C3` and fixed-locus `S3` reduces the residual orbit excess by 808, from 44,999 to **44,191**.

The no-extension claim is scoped to the exhausted natural wreath action and monomial fixed-locus action; arbitrary nonlinear transformations are not ruled out.

## Pass 579 — the colored 600-cell supplies the correct packet object

The icosahedral vertex figure has 20 triangular faces.  Exactly 25 eight-face subsets meet every icosahedron vertex twice.  Under the rotational `A5`, these split into orbits of sizes `5,10,10`.

The unique orbit of size five is the snub-octahedral coloring family:

- eight yellow faces;
- twelve blue faces;
- yellow faces paired into four opposite-face pairs;
- rotational stabilizer `A4` of order 12.

For every order-three element of the `A4` stabilizer:

- the eight yellow faces have cycle type `1^2 3^2`;
- the four opposite-yellow-face pairs have cycle type `1 3`;
- the combined twelve objects have cycle type `1^3 3^3`.

Over `F3`, this is exactly

`3 J3 + 3 J1`,

the Pass-573 Hjelmslev packet Jordan type.  The off-hyperplane 600-cell apex adds one more fixed direction, producing

`3 J3 + 4 J1`

on the full thirteen-object system.

Thus the correct twelve-object geometric model is **eight yellow faces plus four opposite-yellow-face pairs**, not the ordinary twelve icosahedron vertices.  A canonical coordinate intertwiner and full `A4` module equivalence remain open.

## Pass 580 — the Singer scheme has a Johnson quotient

The rank-nine association scheme on the 336 Singer normalizers has nonnegative real Krein parameters and exactly four symmetric fusions, of ranks `2,3,5,8`.

Its valency-five relation is an imprimitivity relation whose graph is

`56 disjoint K6`.

Quotienting by these six-cliques gives a rank-four scheme on 56 points with valencies

`1,15,10,30`.

An explicit graph isomorphism identifies it exactly with the Johnson scheme

`J(8,3)`.

Under this quotient:

- the 56-dimensional block-constant module is `1 + 7 + 20 + 28`, the `A8` permutation module on 3-subsets;
- the 280-dimensional within-block complement is `45 + conjugate(45) + 56 + 64 + 70`.

The basepoint Terwilliger algebra of the Johnson quotient has dimension 38 and center dimension 6 over the certificate prime 1,000,003.  No objectwise identification of the 280-dimensional complement with an `E6` module is asserted.

## Pass 581 — residue quotient and native adic completion

Pass 575 proved

`ker(residueMap) = (lambda)`.

The new Lean source applies the first isomorphism theorem to define

`O5 / (lambda) ≃+* ZMod 5`

and constructs the native completion

`AdicCompletion (lambda) O5`.

It also defines the algebra map into that completion and the completed image of the uniformizer.

The remaining formal boundary is explicit: establish the required local and Noetherian instances, derive the DVR structure and normalized valuation, and prove ramification index `e=4` and residue degree `f=1`.  No local Lean compilation is claimed unless hosted CI reports it.

## Pass 582 — continuous Blackwell dominance and strict one-step regions

The augmented readout MDP contains every baseline action, so its continuous-belief optimal value can never exceed the baseline value.

More strongly, every simultaneous action `J_k` has the same cost as its quartic action `Q_k`, and marginalizing the orientation output of `J_k` reproduces `Q_k` exactly.  Marginalizing the quartic output reproduces the orientation channel.  Hence `J_k` Blackwell-dominates `Q_k`.

At the uniform prior, the best explicit joint action beats every baseline one-step action by:

- conservative: **8.2037978464**;
- nominal: **20.9074990392**;
- aspirational: **45.5898964437**.

Global `L1` Lipschitz estimates certify strict one-step advantage on the following neighborhoods of the uniform prior:

- conservative radius: **0.0074512801**;
- nominal radius: **0.0159189580**;
- aspirational radius: **0.0309390990**.

This is the first continuous-simplex theorem in the readout chain.  It proves exact continuous non-worsening and strict one-step regions, while leaving strict infinite-horizon continuous improvement open.  The Pass-577 finite-grid Bellman results remain a separate stronger numerical certificate for conservative and nominal calibration.

## Validation boundary

The six executable certificates report **66/66 owner checks**, the aggregate release lock reports **18/18 checks**, and the focused suite reports **6/6 tests**.

Claims are exact for the declared natural symmetry searches, colored 600-cell face object, Singer association scheme and Johnson quotient, Lean source scaffold, and stochastic observation model.  No arbitrary nonlinear collision-group classification, full `A4` packet intertwiner, objectwise `E6` identification, completed local-field/DVR theorem, or strict infinite-horizon continuous Bayes theorem is asserted.
