# March 2026 Frontier Note

## Scope

This note records the current exact, reproducible frontier of the project. It is deliberately narrower than the full historical site. Claims below are split by evidence level:

- `Verified`: directly reproduced by scripts, artifacts, and targeted tests in this repo.
- `Conjectural`: physics interpretation that fits the verified structure but is not yet a theorem.
- `Historical`: older broad project claims preserved elsewhere in the repo and site archive.

## New synthesis

The strongest repo-native closure is best described as a **finite spectral-exceptional skeleton**, not yet a finished continuum-dynamical TOE. The cleanest reading is a three-shell reading: bare/internal formulas such as `1/4` or `3/8`, dressed/projective formulas such as `3/13`, and global/spectral formulas such as `137 + 40/1111`, `122`, or shell-dependent Euler counts should not be conflated.

## Verified

### Geometry and linear-algebra backbone

The finite geometry layer remains stable:

- `W(3,3)` point graph is `SRG(40,12,2,4)`.
- The collinearity graph has `240` edges and `160` filled triangles.
- The triangle-filled complex has first Betti number `b1 = 81`.
- The `L1` spectrum splits as `0^81 4^120 10^24 16^15`.
- The `E8` `Z3` grading fingerprint is `86 + 81 + 81 = 248`, with the `81` sector matching the `27 x 3` matter split.

These are historical core invariants of the repo and remain part of the live program.

### Exact PMNS cyclotomic route

The exact PMNS formulas currently promoted at verified status are the cyclotomic ones in [PMNS_CYCLOTOMIC.py](./PMNS_CYCLOTOMIC.py):

- `sin^2(theta_12) = (q+1)/Phi_3 = 4/13`
- `sin^2(theta_23) = Phi_6/Phi_3 = 7/13`
- `sin^2(theta_13) = (q-1)/(Phi_3 Phi_6) = 2/91`

with

- `q = 3`
- `lambda = q - 1 = 2`
- `mu = q + 1 = 4`
- `Phi_3(q) = q^2 + q + 1 = 13`
- `Phi_6(q) = q^2 - q + 1 = 7`

The numerators are therefore not arbitrary:

- `4` comes from the SRG/GQ parameter `mu = q + 1`
- `2` comes from the SRG/GQ parameter `lambda = q - 1`
- `7` comes from the cyclotomic partner `Phi_6(3)`

The angle-only Jarlskog magnitude is

- `J_max ~= 0.03336`

but the physical invariant remains phase-dependent:

- `J = J_max sin(delta)`

So `0.03336` should be read as `J_max`, not as a phase-independent prediction for `J`.

### PMNS incidence-theorem derivation (Phase LVI)

The cyclotomic PMNS formulas above now have a direct incidence-geometry derivation from `W(3,3)` (62 tests, T801–T815):

- **Cyclotomic decomposition**: `Phi_3 = mu + Phi_6 + lambda`, i.e., `(q+1) + (q^2-q+1) + (q-1) = q^2+q+1`. This is an algebraic identity for all `q`.
- **Three-sector partition**: At `q=3`, the 13 points of `PG(2,3)` split into collinear (`mu=4`), transversal (`Phi_6=7`), and tangent (`lambda=2`) sectors.
- **Mixing angles as sector ratios**: `sin^2(theta_ij)` is the sector fraction of `PG(2,3)`.
- **Hierarchy mechanism**: `theta_13` is second-order because the tangent sector (`lambda=2`) couples through the transversal, introducing a `1/Phi_6` suppression.
- **Three-flavor sum rule**: `s12 + s23 + s13*Phi_6 = 1`, equivalent to sector completeness. Holds for all `q >= 2`.
- **Cyclotomic tower**: Level-1 denominators = `Phi_3 = 13`, Level-2 = `Phi_3*Phi_6 = 91 = Phi_3(q^2)`.
- **GQ(3,3) spread structure**: 10 disjoint lines of 4 points partition all 40. Spread overlap matrix `R/(q+1)` is doubly stochastic. Line-adjacency within a spread is uniform: `4*(J_10 - I_10)`.
- **Unified mixing picture**: Weinberg angle `sin^2(theta_W) = g/v = 3/8` and PMNS angles are all W(3,3) incidence ratios.

### Exact CE2 / L-infinity frontier

The live algebra frontier is the dual `g1,g2,g2` closure in [scripts/ce2_global_cocycle.py](./scripts/ce2_global_cocycle.py) and [tools/build_linfty_firewall_extension.py](../tools/build_linfty_firewall_extension.py).

Verified in this pass:

- The `a = (0,1,0)` anchor is fully closed.
- The `a = (0,0,1)` anchor is fully closed.
- The dual predictor now cancels the whole `(21,*)` anchor orbit through explicit sparse `1/54` line families and `1/108` overlap families.
- The first `a = (0,0,2)` witness package is now promoted into the dual predictor:
  - `((22,0),(1,0),(16,1)) -> W = -E_(16,0) / 54`
  - `((22,0),(1,1),(16,0)) -> V = -E_(1,0) / 54`
  - `((22,0),(1,1),(23,0)) -> U = -g1(15,2) / 108`, `V = E_(1,2) / 108`
  - `((22,0),(1,2),(23,0)) -> U = g1(15,1) / 108`, `V = E_(1,2) / 108`
  - `((22,0),(4,0),(13,1)) -> W = E_(13,0) / 54`

The current first unresolved anchor is now:

- `a = (0,0,2)` / basis `(22,*)`

Representative rows already promoted from that anchor:

- `((22,0),(1,0),(16,1)) -> W = -E_(16,0) / 54`
- `((22,0),(1,1),(23,0)) -> U = -g1(15,2) / 108`, `V = E_(1,2) / 108`
- `((22,0),(4,0),(13,1)) -> W = E_(13,0) / 54`

Remaining uncovered rows still begin on that same `a = (0,0,2)` anchor; this is a genuine narrowing, not full closure.

The certified coefficient hierarchy still looks layered rather than random:

- `1/54`: transport line branch
- `1/108`: overlap / phase branch
- `1/12`: transport-plus-gauge companion
- `1/18`: diagonal / source compensation
- `1/6`: large reflected transport branch

### Exact Yukawa nonlinear frontier

The Yukawa frontier is now compressed further than “one unknown last packet”:

- On the replicated diagonal `l6` seed, the exact bottleneck is `response rank = 9`, `augmented rank = 10`.
- Inside the native unit `A2` mixed-seed family, the minimal exact rank-lift seeds are `[8,246]`, `[8,247]`, `[9,246]`, `[9,247]`; these raise the ranks to `11` and `12`.
- The minimal full-activation seeds are the two fans `[8,9]` and `[246,247]`; one exact nonlinear closure step turns each fan into a full `3x3`-support mixed seed with a slotwise isotropic off-diagonal shell.
- After the exact `V4`, unipotent, Kronecker, and Gram reductions, the remaining nontrivial packet is already a finite `240^2`-shell problem: exact scalar channels `169`, `275`, `323`, plus residual blocks `[[367,-55],[-55,175]]` and `[[323,275],[275,659]]`.
- Equivalently, the unresolved base spectrum is exactly two radical pairs with trace/determinant data `(542, 61200)` and `(982, 137232)`.

The strongest conservative read is therefore:

- the remaining Yukawa packet is not currently a missing linear `l6` mode;
- it is the remaining nonlinear internal spectral data carried by those reduced blocks.

### Exact Yukawa generation flag

The reduced generation algebra now has a cleaner exact finite structure too:

- The two universal generation matrices have nilpotent parts of rank `2`, share the same rank-`1` square, and satisfy `N^3 = 0`.
- That common square defines a shared exact flag in `C^3`:
  - line `L = span(1,1,0)`
  - plane `P = {x = y} = span((1,1,0),(0,0,1))`
- Both universal generation matrices preserve that line and that plane exactly.

So the repo-native finite side already carries a common `1 ⊂ 2 ⊂ 3` flag before any continuum family model is chosen.

### Exact finite family normal form

The exact family packet is now sharper than just “there is a flag”:

- The six ordered `l6` generation-transfer modes are the complete oriented three-generation graph.
- On the replicated seed, the active quartet is exactly the star at generation `2`:
  - `[0,2]`, `[2,0]`, `[1,2]`, `[2,1]`
- The dormant pair is the opposite bidirectional edge:
  - `[0,1]`, `[1,0]`
- In the exact basis
  - `u = (1,1,0)`
  - `v = (0,0,1)`
  - `w = (1,-1,0)`
  the two universal generation matrices become
  - `C_(+-) = [[1,1,-2],[0,1,2],[0,0,1]]`
  - `C_(-+) = [[1,-1,-2],[0,1,-2],[0,0,1]]`
- Their nilpotent parts have the same nonzero square:
  - `N_(+-)^2 = N_(-+)^2 = 2 E_13`

So the current exact family/Yukawa packet already has a canonical one-versus-two upper-unitriangular normal form before any continuum orbit language is added.

### Exact quadratic shadow

The same normal form now gives a sharper nonlinear statement too:

- Write the active simple-root packet as
  - `A_(+-) = E_12 + 2 E_23`
  - `A_(-+) = -E_12 - 2 E_23`
- Then the first nonlinear closure is exact:
  - `A_(+-)^2 = A_(-+)^2 = 2 E_13`
  - equivalently `2 E_13 = [E_12, 2 E_23]`
- The universal generation nilpotents are exactly
  - `N_(+-) = A_(+-) - 2 E_13`
  - `N_(-+) = A_(-+) - 2 E_13`

So the first nonlinear family packet is not an independent extra mode. It is the exact quadratic central shadow of the active simple-root packet already present in the finite family normal form.

### Exact A4 entry point

The local product-heat bridge also sharpens the continuum bottleneck:

- `A0 = 81 a0`
- `A2 = -459 a0 + 81 a2`
- so both `A0` and `A2` are family-blind
- the first family correction is
  - `ΔA4 = 81 ε^2 a0 = 1209 a0 / 9194`

So the honest continuum wall is now more specific than “derive gravity somehow”:

- the remaining family/continuum problem is the refined `A4` density
- not the leading `Λ^4` or `Λ^2` coefficients

### Exact two-channel refined action

The refined continuum side now compresses one step further too:

- On both `CP2_9` and `K3_16` refinement towers,
  - `A0_density(n) = fixed + C20/20^n + C120/120^n`
- The first family-sensitive density is not a new external mode:
  - `ΔA4_density(n) = ε^2 A0_density(n)`
  - `ε^2 = 403/248238`
- So `ΔA4_density` inherits exactly the same `20^-n` and `120^-n` modes as `A0_density`.

Equivalently, through first family order the refined truncated action is still only a two-channel external packet:

- `S_n = (2 f4 Λ^4 + ε^2 f0) A0_density(n) + 2 f2 Λ^2 A2_density(n)`

So the first family-sensitive step renormalizes the geometric `A0` channel rather than creating a third external refinement channel.

### Exact local A4 normalization

The local bridge packet is now normalized sharply enough to state a stronger conservative theorem:

- The relevant product heat coefficient is exactly
  - `A4*B0 + A2*B2 + A0*B4`
- Explicit 4D Euclidean gamma matrices give the universal twisted-Dirac gauge factor
  - `a4_gauge(x) = (4 pi)^(-2) * (1/12) Tr(F_{mu nu} F^{mu nu})`
- For the twisted Dirac gauge endomorphism,
  - `tr_S(E_F) = 0`
- So this packet does not shift the `A2` / Einstein-Hilbert channel; it is purely an `A4` packet.
- On a self-dual branch that universal factor becomes
  - `1 / (96 pi^2)` per curved copy
- The exact repo-native A4-entry theorem already fixes the finite multiplier:
  - `Delta A4 = 81 epsilon^2 a0 = 1209 a0 / 9194`

### Holographic transport-twisted lift localization

The clean holographic continuation now compresses the post-`CCCLXXII` wall one
step further.

- The central image-side family channel localizes to the head-compatible line.
- The first family-sensitive `A4` packet has minimal canonical external carrier
  plane `U1`.
- Exact transport completion uses the avatar shell `81 -> 162 -> 81`.
- The external realization wall is already localized to a
  carrier-preserving transport-twisted K3 lift of that fixed package.

So the honest remaining theorem is no longer a generic continuum or K3
enhancement problem. It is the refined external `A4` density on the nested
support ladder

- `head line ⊂ U1 ⊂ 81 -> 162 -> 81 ⊂ transport-twisted K3 lift`

with the finite entry coefficient already locked at

- `Delta A4 = 81 epsilon^2 a0 = 1209 a0 / 9194`.
- Rank-1 external branches kill the packet automatically, while rank-2 activation is quartic:
  - `C -> t C` gives scaling `t^4`
- So before the already-isolated universal rank-2 factor `2`, the reduced local prefactor is
  - `27 / (32 pi^2)`
- And after that factor `2`, the reduced local prefactor is
  - `27 / (16 pi^2)`

So the honest open step is no longer the local coefficient. It is the global branch-counting / orientation theorem over the actual refinement tower.

### Exact external exceptional quanta

The promoted residue dictionary now fixes the external exceptional quanta too:

- Internal exceptional ranks are already promoted as
  - `(40, 6, 8)`
- The continuum coefficients are already exact on the live surface:
  - `c_EH = 320 = 40 * 8`
  - `c_6 = 12480`
  - `a2 = 2240`
- So the external quanta are forced:
  - `Q_curv = c_6 / (40 * 6) = 52`
  - `Q_top = a2 / 40 = 56`
- The same data satisfy the promoted ratio locks:
  - `9 c_EH / c_6 = 3 / 13`
  - `a2 / c_EH = 7`

So the remaining ambiguity is not the local external normalization. It is which primitive external branches actually activate, with what sign and multiplicity, on the refined tower.

### Selected-point q-cyclotomic master lock

The promoted finite and curved packages now compress one step further at the selected point `q = 3`:

- Internal blocks align as
  - `81 = q^4`
  - `6 = 2q`
  - `8 = q^2 - 1`
  - `86 = q^4 + 2q - 1`
  - `248 = 3q^4 + 2q - 1`
- Curved coefficients align as
  - `320 = v(q) (q^2 - 1)` with `v(q) = (q+1)(q^2+1)`
  - `2240 = Phi_6(q) * 320`
  - `12480 = q Phi_3(q) * 320`
- So the promoted curved Weinberg lock is a direct corollary:
  - `9 c_EH / c_6 = q / Phi_3(q) = 3 / 13`

This is a selected-point master theorem, not yet a proof that the whole global bridge is finished. But it does mean the live `81 / 6 / 8`, `320 / 2240 / 12480`, and `3/13` package is now best read as one `q = 3` cyclotomic dictionary rather than three unrelated residue facts.

### Balanced rank-2 bridge selector

There is now also a clean exact selector on the active `2x2` bridge branch:

- For singular-value squares `x, y >= 0`,
  - `tr(C^* C) = x + y`
  - `|det C|^2 = x y`
  - `4 |det C|^2 = tr(C^* C)^2 - (x - y)^2 <= tr(C^* C)^2`
- Equality holds iff the two singular-value squares agree:
  - `x = y`
- So at fixed branch radius the quartic bridge packet is uniquely maximized on the balanced rank-2 branch.
- In the reduced branch action
  - `V(C) = -mu tr(C^* C) + u tr(C^* C)^2 - v A |det C|^2`
  the shape dependence rewrites exactly as
  - `V = -mu r^2 + (u - A v / 4) r^4 + (A v / 4) (x - y)^2`
  with `r^2 = x + y`
- The nonzero stationary point is therefore forced to be balanced:
  - `x = y = mu / (4u - vA)`
- The Hessian at that point is exact:
  - `H = [[2u, 2u-vA], [2u-vA, 2u]]`
  - radial eigenvalue `lambda_radial = 4u - vA` on `(1,1)`
  - shape eigenvalue `lambda_shape = vA` on `(1,-1)`
- Hence if `mu > 0` and `4u > Av`, the nonzero balanced stationary radius is
  - `r_*^2 = 2 mu / (4u - A v)`

This does **not** finish the bridge theorem. The checked local `V29_output_q_stiffness/summary.json` is numerically near-isotropic at quadratic order (`diag_cv ~= 0.024`, `offdiag_rms_ratio ~= 0.0077`, `eig_std_ratio ~= 0.088`), and the companion `V29_output_q_stiffness_validate/summary.json` keeps the finite-difference mean relative error near `0.017`, which is consistent with the reduced selector picture, but only as observation. The exact open step is still the actual branch-realization / orientation theorem on the refinement tower.

### External H2 host split

The explicit curved seeds now sharpen that remaining external step more than the older wording admitted:

- `CP2_9` has Betti profile `(1,0,1,0,1)` and signature `+1`
- `K3_16` has Betti profile `(1,0,22,0,1)` and signature `-16`
- So the harmonic `H^2` capacities split exactly as
  - `CP2_9`: `b2 = 1`, hence `(b2^+, b2^-) = (1,0)`
  - `K3_16`: `b2 = 22`, hence `(b2^+, b2^-) = (3,19)`
- Therefore `CP2_9` cannot by itself host a genuine rank-2 harmonic bridge branch, while `K3_16` is the first exact seed in the repo that can.
- The seed-level curvature sign is already sharp too:
  - `six_mode(CP2_9) = 156/19`
  - `six_mode(K3_16) = -880/19`
- Those signs match the recorded seed signatures `+1` and `-16`.

So the common exact part of the external bridge is the universal local `120`-mode law, not a common seed-level `H^2` host. The remaining global ambiguity is narrower: it is the actual selection, counting, and orientation of the relevant rank-2 harmonic plane inside the refined `K3` tower.

### Middle-degree qutrit bridge

That same host theorem now lands directly on the exact matter packet:

- The finite W33 qutrit sector has exact dimension `81`
- Tensoring with middle harmonic cohomology gives
  - `CP2_9`: `81 * 1 = 81`
  - `K3_16`: `81 * 22 = 1782`
- The K3 middle-degree channel splits exactly by sign as
  - positive: `81 * 3 = 243`
  - negative: `81 * 19 = 1539`

So the relevant exact bridge host is not just “the K3 side somewhere.” It is the concrete middle-degree package

- `81 ⊗ H^2(K3)`

rather than the coarser total-harmonic lift. This still does **not** fix the final global branch theorem, but it does mean the branch now has a sharply localized exact qutrit host before any continuum interpretation is added.

### Harmonic qutrit degree split

The older protected-harmonic totals now separate cleanly into universal endpoints plus the live middle packet:

- On both explicit seeds, `b0 = b4 = 1`
- So the endpoint qutrit channel is always
  - `81 b0 + 81 b4 = 162`
- The full protected-harmonic qutrit counts therefore split as
  - `CP2_9`: `243 = 162 + 81`
  - `K3_16`: `1944 = 162 + 1782`

So all external growth is already concentrated in the middle-degree channel `81 x H^2`, not in the endpoint topological lines. Equivalently, the full seed-to-seed harmonic gap is

- `1944 - 243 = 1782 - 81 = 1701`

which is entirely middle-degree.

### K3 rank-2 qutrit plane types

The K3 middle-degree host now supports exact minimal rank-2 branch types:

- positive rank-2 plane `(2,0)`
- mixed rank-2 plane `(1,1)`
- negative rank-2 plane `(0,2)`

Because the qutrit matter packet has dimension `81`, tensoring any such rank-2 plane gives

- total branch size `81 * 2 = 162`

and the mixed branch splits exactly as

- `81 + 81`

### Chain-level H2 cup form

The explicit curved chain complexes now carry the actual middle-degree cup form. Using the propagated fundamental class and the simplicial cup pairing on harmonic `H^2`:

- `CP2_9` recovers signature `(1,0)`
- `K3_16` recovers signature `(3,19)`

So the old `H^2` host split is no longer only a Betti/signature bookkeeping statement. It is already visible on the explicit chain model.

### Canonical mixed K3 plane

On `K3_16`, the lexicographically first harmonic triangle already has both positive and negative harmonic projections. That determines a canonical ordered mixed plane:

- positive line
- negative line

and tensoring it with the qutrit packet gives a split external branch package

- `81 + 81 = 162`

### Transport shadow obstruction

That same result sharpens the transport comparison. The internal transport sector is still the exact non-split extension

- `0 -> 81 -> 162 -> 81`

but the canonical mixed `K3` plane is already split by construction. So the current exact statement is:

- exact size-shadow match
- exact split-versus-nonsplit obstruction

not an exact identification of extension objects.

### Local A4 resolution

The chain-level mixed plane also settles the old local coefficient tension:

- total external branch size: `162`
- exact finite multiplier in `Delta A4 = 81 epsilon^2 a0`: `81`
- missing factor: universal external rank-2 activation `2`

### First refinement persistence

The canonical mixed K3 selector plane now survives the first barycentric pullback exactly:

- seed restricted cup form: mixed and nondegenerate
- first refinement restricted form: `120` times the seed form
- normalized mixed signature: unchanged
- determinant scaling: `120^2`

So the rank-2 selector is not just a seed artifact; it survives `sd^1(K3_16)` after normalization.

### Integral K3 lattice

The explicit `K3_16` simplicial cochain complex now yields an actual integral `H^2(K3,Z)` basis by Smith reduction:

- Smith data on the cocycle/exact quotient: `0^22, 1^105`
- integral rank: `22`
- cup-form determinant: `-1`
- diagonal parity: even
- signature: `(3,19)`

So the explicit seed already realizes the full even unimodular K3 lattice. Inside that same lattice there is a deterministic primitive hyperbolic plane:

- Gram matrix: `[[0,1],[1,0]]`
- primitive minor gcd: `1`

This is a genuine lattice-level rank-2 bridge host, not only a real-signature shadow.

More sharply, the same explicit integral lattice already contains three pairwise orthogonal primitive hyperbolic planes:

- the resulting block Gram matrix is exactly `3U`
- a unit `6 x 6` minor witnesses that this `3U` block is primitive in the ambient lattice
- therefore the orthogonal complement is forced to be an even unimodular negative-definite rank-16 lattice

So the explicit `K3` host now carries a full hyperbolic core, not merely one isolated primitive plane.

### Selector plane versus the 3U core

The canonical mixed harmonic selector is now separated from that lattice core cleanly.

In harmonic `H^2` coordinates, projecting the selector plane cup-orthogonally onto the primitive `3U` block gives a positive-definite `2 x 2` form, while the residual plane in the orthogonal rank-16 complement is negative-definite.

So the selector plane is not itself one of the primitive `U` factors, and it is not contained entirely in the negative complement either. It genuinely straddles both exact K3 lattice pieces.

### Refinement persistence of the selector/core split

That selector/core split itself now survives the first exact refinement step.

- On `sd^1(K3_16)`, the selector plane, its positive-definite `3U` shadow, and its negative-definite rank-16 residual all scale by the same exact factor `120 = 5!`.
- So the normalized selector/core/complement decomposition is already refinement-invariant at first barycentric order.
- The `3U` shadow stays positive-definite and the residual stays negative-definite after pullback, so the seed-level split is not a one-off artifact of the unrefined triangulation.

### Refinement persistence of the full 3U core

The same refinement law is now known on the whole explicit hyperbolic core, not only on the selector-derived shadows.

- Restricting the first barycentric pullback to the six explicit `3U` cochain vectors gives exactly `120 * 3U`.
- So the normalized hyperbolic core itself is already refinement-invariant at `sd^1`.
- In particular, the primitive K3-side `3U` host is not merely present on the seed; it already survives the first exact refinement step as one coherent block.

### First-refinement rigidity of the full K3 lattice split

The explicit `K3` host now goes one step further again.

- Taking the integral kernel complement of the primitive `3U` block gives an exact orthogonal rank-16 negative-definite lattice `N16`.
- That full complement also scales by the same exact factor `120` under first barycentric pullback.
- In the combined split basis `3U (+) N16`, the full `22 x 22` restricted cup form stays block-diagonal and is carried exactly to `120` times itself.

So the normalized full lattice split `H^2(K3,Z) = 3U (+) N16` is already refinement-invariant at `sd^1` on the explicit seed.

### Naming the rank-16 complement

The negative-definite complement is no longer just an unnamed `N16`.

- The explicit complement has exactly `480` norm-2 roots.
- Those roots span the full rank-16 lattice with Smith index `1`.
- So, under the standard rank-16 even-unimodular classification, the explicit complement is `E8(-1) (+) E8(-1)`, not `D16^+(-1)`.

So the explicit `K3` host now carries a named exact split:

- `H^2(K3,Z) = 3U (+) E8(-1) (+) E8(-1)`.

### Constructive `E8(-1) (+) E8(-1)` split

That naming step is now constructive on the actual seed, not just forced by classification.

- The explicit norm-2 root graph of the negative complement already splits into two connected `120`-representative packets.
- After adjoining antipodes, that becomes two full `240`-root packets.
- Each packet admits a deterministic simple-root basis with exact negative `E8` Cartan Gram.
- The two simple-root systems are exactly orthogonal.
- Together the `16` simple roots form a unimodular change of basis of the explicit complement.

So the explicit complement is not merely abstractly of type `E8(-1) (+) E8(-1)`. The two `E8` factors are already concretely present in the current cochain-level bridge host.

### Named refinement theorem

That constructive exceptional split is now refinement-rigid too.

- The first explicit `E8(-1)` factor is carried by barycentric pullback to exactly `120` times its negative `E8` Cartan form.
- The second explicit `E8(-1)` factor does the same.
- The two factors remain exactly orthogonal after pullback.
- Together with the earlier `3U -> 120 * 3U` theorem, the full named split
  `3U (+) E8(-1) (+) E8(-1)` is carried exactly to `120` times itself.

So the K3 host is no longer only rigid in the coarse basis `3U (+) N16`. It is already rigid at the fully named `3U (+) E8(-1) (+) E8(-1)` level.

### Selector plane versus the two `E8` factors

The selector/core theorem now resolves further against the named exceptional blocks.

- The selector still has a positive-definite `3U` shadow.
- Its projection onto the first explicit `E8(-1)` factor is nonzero and negative-definite.
- Its projection onto the second explicit `E8(-1)` factor is also nonzero and negative-definite.
- The `3U`, `E8_1`, and `E8_2` pieces are pairwise cup-orthogonal and reconstruct the selector exactly.

So the canonical selector is not only a bridge between hyperbolic core and unnamed negative complement. It already bridges `3U` and both named `E8` blocks on the explicit seed.

### Reduced global A4 coupling

On that canonical oriented primitive K3 plane:

- seed oriented cup quantum: `+1`
- first refined quantum: `+120`
- local reduced prefactor: `27/(16 pi^2)`
- external curvature quantum: `Q_curv = 52`

Therefore the reduced normalized external bridge coefficient is fixed as

- `351/(4 pi^2)`

with raw `sd^1` mass

- `10530/pi^2`

Honest caveat:

- this does not yet prove that the primitive lattice plane is exactly the same 2-plane as the earlier harmonic-selector plane
- it does prove that the explicit K3 seed now carries both a canonical real selector plane and a canonical integral primitive plane, and that the reduced external sign/count coupling is already fixed on the latter

So `162` is branch dimension, not a replacement for the finite trace multiplier `81`.

### Primitive plane inside the `3U` core

The relation between the global primitive plane and the hyperbolic core is no longer open on the explicit seed.

- The canonical primitive lattice plane is exactly the first explicit `U` factor of the `3U` block.
- The selector's positive `3U` shadow decomposes orthogonally across all three explicit `U` factors.
- Each `U` factor carries nonzero selector support.

So the locked `351/(4 pi^2)` plane is a distinguished exact hyperbolic factor, but it is not the whole selector-positive channel.

### Selector-side `A4` split on the named lattice pieces

Keeping the already-fixed scalar coefficient `351/(4 pi^2)`, the selector-side external packet now decomposes directly over the full named K3 split:

- one positive-definite `3U` piece
- one negative-definite `E8_1` piece
- one negative-definite `E8_2` piece

and those three contributions add back to the selector form exactly.

So the reduced selector-side `A4` geometry is not carried by the hyperbolic core alone, and it is not carried by just one exceptional block either. On the explicit seed it is already tri-supported across `3U (+) E8(-1) (+) E8(-1)`.

### Fine selector-side `A4` split

The selector-side packet can now be resolved one step further inside the hyperbolic core.

- The positive `3U` packet reconstructs exactly as `U1 + U2 + U3`.
- Keeping the same locked scalar `351/(4 pi^2)`, the full selector-side reduced packet reconstructs exactly as
  `U1 + U2 + U3 + E8_1 + E8_2`.
- The `U1`, `U2`, and `U3` packet pieces are each mixed-sign `2 x 2` forms.
- The `E8_1` and `E8_2` packet pieces are each negative-definite.
- All five packet pieces are nonzero.

So the canonical global plane `U1` is a genuine packet carrier, but it does not exhaust the local selector-side bridge geometry.

### Fine selector-side refinement rigidity

The finer five-factor split is not a seed-only phenomenon.

- On the explicit `K3_16` chain model, the restricted form on each of `U1`, `U2`, `U3`, `E8_1`, and `E8_2` is carried by first barycentric pullback to exactly `120` times itself.
- The normalized restricted form of each packet piece is therefore refinement-invariant at `sd^1`.
- The three `U`-factor packet pieces stay mixed-sign, while the two `E8` pieces stay negative-definite.

So the selector-side packet is already first-refinement rigid down to its current finest named decomposition.

### Minimal `U1` carrier of the family `A4` entry

The strongest conservative K3-to-family coupling theorem is now:

- the internal family spurion is blind at `A0` and `A2` and first enters at `A4` with
  `Delta A4 = 1209 a0 / 9194`
- the reduced local bridge prefactor is already exact
- the reduced global external coupling is already fixed on the canonical primitive plane
- and that canonical primitive plane is exactly `U1`, the first explicit `U` factor of the `3U` core

So the minimal canonical external carrier of the first family-sensitive packet is now explicit: `Delta A4` on `U1`.

What is not yet proved is stronger:

- the full local selector packet does not collapse to `U1`
- the internal one-versus-two family flag `span(1,1,0) < {x=y}` is not yet identified exactly with the external `U1` plane
- the split external `81 + 81` package is still obstructed from exact identification with the non-split internal transport `81 -> 162 -> 81` extension

### Isotropic-line obstruction inside `U1`

The current `U1` carrier theorem does not yet select an external family line.

- In the canonical integral basis, `U1` already has two primitive isotropic line generators.
- Those two lines have unit hyperbolic pairing.
- Swapping them leaves the seed form `[[0,1],[1,0]]` unchanged.
- The same swap also leaves the first-refinement form and the reduced global prefactor unchanged.

So the current K3-side data are still line-blind inside `U1`: they fix the hyperbolic carrier plane, not a distinguished internal family line.

### Fine selector-packet weight hierarchy

The five-factor split is not only exact; it is highly uneven.

- Within the hyperbolic packet, the Frobenius-norm order is `U3 > U1 > U2`.
- `U3` carries a little over `80%` of the hyperbolic packet weight.
- Within the exceptional packet, the order is `E8_2 > E8_1`.
- `E8_2` carries about `89.4%` of the exceptional packet weight.

Since each packet piece scales by exact factor `120` at `sd^1`, that normalized hierarchy is already refinement-invariant.

### Transport filtered split shadow

The transport comparison is now sharper than a size match and sharper than a bare graded shadow, but still weaker than object identity.

- The internal transport packet is a non-split `81 -> 162 -> 81` extension.
- The external canonical mixed K3 packet is a split `81 (+) ⊕ 81 (-)` object.
- So externally there is already a canonical ordered split filtration
  `81(+) -> 162 -> 81(-)`.
- The exact common invariant is therefore not only the graded shadow
  `81 ⊕ 81`,
  but also the ordered filtered dimension pattern
  `81 -> 162 -> 81`.

So the current bridge identifies a canonical ordered split filtered shadow exactly, but not the full extension class.

### Transport nilpotent-glue obstruction

The remaining transport wall is now sharper than an abstract split-versus-nonsplit slogan.

- Internally, the transport `162` already carries a canonical square-zero rank-`81` glue operator.
- Its image and kernel are both exactly `81`.
- Externally, the current K3 filtered shadow is split, so its extension class is zero.

So the present bridge reaches head, middle, tail, and ordering, but not the nontrivial nilpotent glue that binds the internal transport packet.

### Global carrier versus local packet dominance

The bridge now separates two exact notions that should not be conflated.

- Globally, the first family-sensitive packet has canonical minimal external carrier `U1`.
- Locally, the selector-side packet is dominated by `U3` on the hyperbolic side and by `E8_2` on the exceptional side.
- The exact Frobenius-norm ratios are `U3/U1 ≈ 4.8741` and `E8_2/E8_1 ≈ 8.4712`.

So `U1` is the canonical global carrier, but it is not the dominant local packet piece. That separation is already exact and refinement-invariant.

### Canonical line candidate inside `U1`

The carrier-only theorem is not yet the whole external story.

- The metric carrier data on `U1` are still symmetric under swapping the two primitive isotropic lines.
- But the canonical ordered selector basis already projects to `U1` with unequal isotropic-line weights:
  about `0.29249917` versus `0.220630996`.
- The exact dominance ratio is therefore `1.3257392335`.
- The same ordered positive/negative selector basis now sign-orders the two `U1` null lines:
  the dominant line has larger positive-selector weight, smaller negative contamination,
  and larger positive-minus-negative gap than the recessive line.
- That line selection is invariant under the natural sign/swap ambiguities of the selector basis.
- And it survives first barycentric refinement, because both the `U1` carrier form and the `U1` selector packet form scale by exact factor `120`.

So the full current external packet already selects a unique rigid dominant isotropic-line candidate inside `U1`, and the filtered-shadow sign basis already orders that choice, even though the carrier metric alone is line-blind.

### Family-flag visibility obstruction

The finite family flag is now sharper than the current external bridge.

- Internally, the reduced Yukawa side has exact line-plane data
  `span(1,1,0) < {x = y}`.
- Externally, the current K3 bridge fixes the carrier plane `U1`.
- The full external packet now also picks a canonical dominant isotropic-line candidate inside `U1`, ordered by the positive/negative filtered-shadow basis.
- And on the transport side, the exact match now reaches a canonical filtered split shadow
  `81 -> 162 -> 81`,
  but not the internal rank-`81` nilpotent glue.

So the present bridge fixes a carrier plane, a line candidate, and a filtered shadow, but not yet an exact identification of that external line candidate with the internal line `span(1,1,0)`, and not the nontrivial glue that makes the transport extension non-split.

### Head/tail polarized transport shadow

The current bridge now reaches a stronger split-shadow theorem than a bare ordered filtration.

- Internally, the transport `162` has a canonical head/middle/tail structure
  `81 -> 162 -> 81`.
- The internal square-zero rank-`81` glue points from tail to head.
- Externally, the current K3 bridge fixes a head-biased `U1` line and a tail-biased `U1` line.
- And it fixes the same ordered split dimension pattern
  `81 -> 162 -> 81`.

So the current bridge already reaches a canonical head/tail polarized split shadow, but still not the internal tail-to-head nilpotent glue itself.

### Transport Jordan shadow

The internal transport obstruction is now rigid enough to have an exact Jordan reading.

- Internally, the transport glue is a square-zero rank-`81` operator on dimension `162`.
- Therefore its Jordan type is forced exactly to `2^81`.
- So the internal associated graded is exactly `81(head) + 81(tail)`.
- Externally, the current bridge already fixes the polarized associated graded of that packet:
  head-biased `U1` line, tail-biased `U1` line, and the ordered split shadow
  `81 -> 162 -> 81`.

So the current bridge now reaches the polarized Jordan shadow of the internal transport packet, but not yet the nontrivial size-`2` Jordan blocks themselves.

### Single missing glue slot

The transport wall is now even narrower than that.

- The semisimplified shadow is fixed.
- The ordered filtered shadow is fixed.
- The head/tail polarization is fixed.
- The polarized Jordan shadow is fixed.

So the only missing datum for exact transport identity is one operator slot:

- a tail-to-head `81 x 81` glue map.

Internally that slot is occupied by the nonzero rank-`81` square-zero glue. Externally it is currently forced to be zero by splitness.

### Head-compatible external line candidate

The current exact bridge dictionary now does more than say there is some external
line candidate inside `U1`.

- Internally, the common family line `span(1,1,0)` is exact image-side data,
  because it is the image of the common square `2E13`.
- Internally, the current transport polarity is exact and tail-to-head.
- Externally, the bridge already fixes a head-biased `U1` line and a
  tail-biased `U1` line.
- And the sign-ordered rigid `U1` line selected by the current packet is exactly
  the head-biased one.

So the current external line ambiguity now collapses to one head-compatible
candidate: any bridge-compatible external realization of the internal common
line must use the head-biased `U1` line, not the tail-biased one.

What remains open is stronger than that:

- prove that this head-compatible external line is literally the same object as
  the internal line `span(1,1,0)`;
- and realize the missing non-split tail-to-head glue externally.

### External glue is structurally zero on the current bridge

The transport wall is now sharper than “we have not found the glue yet.”

- The current external transport `162` is exactly the split qutrit lift
  `81(+) ⊕ 81(-)` of the canonical mixed K3 plane.
- The current ordered external transport shadow therefore has zero extension
  class by construction.
- So the unique tail-to-head `81 x 81` glue slot is canonically zero on the
  present external bridge object.

That means any nonzero external glue operator would require genuinely new
external data beyond the current bridge package. The current wall is no longer
“locate the hidden external glue”; it is “decide what new external structure
could create one without breaking the already-locked split shadow.”

### Canonical rigid split transport avatar

The last two transport reductions now fit together into one sharper statement.

- The current bridge fixes one head-compatible external `U1` line.
- It also fixes the canonical tail-biased `U1` line.
- It fixes the ordered split dimensions `81 -> 162 -> 81`.
- And it forces the unique external tail-to-head glue slot to be zero.

So the current bridge does not merely see an undifferentiated transport shadow.
It fixes one canonical rigid split avatar of the internal packet:

- head line;
- split middle `162`;
- tail line;
- zero glue.

This is still not the internal non-split transport object, but it is now the
exact canonical split object that the present K3 bridge realizes.

### Transport deformation wall

That sharpens the remaining transport frontier one step further.

- The bridge no longer needs a new external transport object.
- It already fixes one canonical rigid split avatar.
- The only missing datum is a nonzero tail-to-head `81 x 81` square-zero glue
  block on that avatar.

So the remaining transport wall is now deformation-theoretic:

- preserve the fixed head line;
- preserve the fixed tail line;
- preserve the ordered dimensions `81 -> 162 -> 81`;
- replace zero glue by nonzero glue.

That is narrower than “search for the right external packet.” It is one exact
non-split deformation problem.

### Full-rank glue normal form

That deformation wall is now narrower than an arbitrary matrix problem.

- The fixed polarized shell is `81 -> 162 -> 81`.
- Exact completion requires a tail-to-head glue slot of shape `81 x 81`.
- The required rank is exactly `81`.

So any exact completion glue is automatically an isomorphism from tail to head.
Up to independent basis change on the fixed head and tail shells, every such
glue block is equivalent to `I_81`.

Equivalently, the completed polarized nilpotent has one canonical normal form:

- `J2^81`.

So the remaining transport wall is now existence of a non-split completion, not
glue shape.

### Internal operator normal-form match

That full-rank normal form now matches the internal transport operator exactly.

- The internal non-split ternary extension already has explicit fiber shift
  `[[0,1],[0,0]]`.
- Tensoring with the exact `81`-dimensional logical matter sector gives the
  operator model `I_81 ⊗ [[0,1],[0,0]]` on the `162`-sector.
- Any exact external completion now has the same polarized normal form
  `J2^81` up to the natural head/tail basis gauge.

So the remaining transport wall is no longer operator-shape mismatch. It is
realization of the nontrivial transport cocycle class on the external side.

### Unique nonzero ternary cocycle orbit

That cocycle-class wall is now narrower too.

- Over `F3` the fiber shift is `N = [[0,1],[0,0]]`.
- The only nonzero scalar multiples are `N` and `2N`.
- Those are gauge-equivalent by the adapted diagonal basis change
  `diag(1,2)`.

So up to the natural head/tail basis gauge there is only one nonzero ternary
glue orbit.

The remaining external wall is therefore existence of that unique nonzero orbit,
not selection among several different nonzero ternary types.

### Refined K3 zero-orbit theorem

The first external existence question is now answered negatively for the current
refined K3 bridge itself.

- The present refined K3 transport shadow is still split with zero extension
  class.
- That split shadow is already refinement-rigid at `sd^1`.

So the current refined K3 side still realizes only the zero ternary glue orbit.
Any realization of the unique nonzero ternary orbit would require genuinely new
external data beyond the current refined K3 bridge package.

### Exact image line in any completion

The line-level wall is now sharper too.

- Internally, `span(1,1,0)` is the exact image of the common square `2E13`.
- The internal transport operator image is the head/invariant line.
- Any exact external completion has the same operator normal form up to the
  natural head/tail basis gauge.

So in any exact completion of the current bridge shell, the bridge image of the
internal common line is forced to be the head-compatible `U1` line.

### Minimal external completion data

The next completion datum is now exact too.

- The shell `81 -> 162 -> 81` is already fixed.
- The head-compatible and tail lines are already fixed.
- The tail-to-head glue slot is already fixed.
- The only nonzero ternary glue orbit is already fixed up to the natural
  head/tail gauge.

So the minimal new external data is exactly one replacement:
the present zero slot must be replaced by the unique nonzero orbit in that
already-fixed `81x81` tail-to-head slot.

### Formal external completion avatar

That immediately gives a minimal formal completion object.

- It carries the forced head-compatible image line.
- It sits inside the canonical plane `U1`.
- It keeps the ordered shell `81 -> 162 -> 81`.
- And it uses the unique nonzero completion normal form `J2^81`.

So the missing piece is no longer common-object design. The missing piece is
realization of that formal completion by actual K3-side data.

### Central `2E13` visibility wall

The status of the internal central channel is now explicit.

- On the finite family side, the common square is exactly `2E13`.
- Its image is exactly the common internal line `span(1,1,0)`.
- The current external bridge fixes the canonical carrier plane `U1`.
- The full current external packet also picks a canonical dominant isotropic-line candidate inside `U1`, ordered by the positive/negative filtered-shadow basis.
- And on the transport side it now reaches the canonical polarized Jordan shadow
  of the transport packet.
- More sharply, the current external realization of that central channel now
  factors through the canonical rigid split transport avatar.
- And any exact completion would have to pass through the same unique full-rank
  glue normal form `J2^81`.
- And that normal form now matches the already-explicit internal transport
  operator model `I_81 ⊗ [[0,1],[0,0]]` up to basis gauge.
- And over `F3` that operator data itself now sits in one unique nonzero gauge
  orbit.
- In any exact completion, the image of the internal common line is therefore
  forced to be the head-compatible `U1` line.
- But the current split bridge still does not realize the nontrivial rank-`81`
  glue itself.

### `2E13 / A4` support stratification

The live family/transport bridge now has exact support layers.

- The central image-side `2E13` channel localizes to the head line in any exact
  completion.
- The first family-sensitive `A4` bridge packet has minimal canonical plane
  carrier `U1`.
- Exact transport completion uses the full rigid avatar shell
  `81 -> 162 -> 81`.

So the live bridge is no longer ambiguous between line, plane, and avatar
support. Those three roles are already stratified exactly.

### Yukawa / transport coupling hierarchy

The support story is now better than a static stratification.

- The central `2E13` image channel is line-level.
- The first family-sensitive `A4` bridge packet is plane-level on `U1`.
- The non-split transport identity is avatar-level on the formal completion
  `81 -> 162 -> 81`.
- The broader five-factor packet and the locally dominant `U3` piece remain
  real, but they are context rather than the minimal exact carrier.

So the unresolved family/transport closure is now best read as a support
filtration:

`head line  ⊂  U1  ⊂  formal completed avatar`.

So the conservative exact statement is now: the current bridge sees the carrier plane, a canonical line candidate, and the polarized Jordan shadow of the central `2E13` channel, but not yet the full central channel as an external extension object with its internal glue.

This is still not the final global theorem, but it is the sharpest exact local/global split so far on the unresolved external branch.

### Qiskit support-hierarchy search

The repo now has a first TOE-specific local Qiskit search workflow in
`tools/qiskit/toe_support_hierarchy_search.py`.

This is deliberately conservative. It does not guess new continuum physics. It
encodes the exact support hierarchy already proved in the bridge stack:

- `2E13` image channel on the head-compatible line
- first family-sensitive `A4` packet on minimal plane carrier `U1`
- transport completion on the full avatar shell

So the oracle marks exactly the support permutations whose first three slots are

- `head_line`
- `u1_plane`
- `transport_avatar`

with the local `U3` / `E8_2` order left free.

The first verified run on the explicit five-support search space had:

- permutation count `120`
- marked count `2`
- qubit count `7`
- Grover iterations `6`
- seeded target hit probability `255/256 = 0.99609375` at `256` shots

with the two exact marked permutations dominant, one residual non-target valid
permutation, and no invalid bitstrings.

A nearby iteration study over seeds `5, 6, 7` also peaks exactly at the
analytic Grover count:

- `5` iterations: mean target-hit probability `0.9609375`
- `6` iterations: mean target-hit probability `0.9973958333333334`
- `7` iterations: mean target-hit probability `0.8984375`

### Qiskit support-diagnostic search

The exact next refinement of that same support shell is now in
`tools/qiskit/toe_support_diagnostic_search.py`.

This does not enlarge the support space. It factorizes the same `120` support
states exactly as:

- `10` support interleavings choosing which `3` of `5` slots carry the bridge core
- `6` orders on `(head_line, u1_plane, transport_avatar)`
- `2` free local-context orders on `(u3_local, e8_2_local)`

So the exact identity is `5! = C(5,3) * 3! * 2! = 10 * 6 * 2`. The marked
sector keeps one support interleaving and one line/plane/avatar core order,
with the local tail order free.

A two-seed study over seeds `7,8` gave the cleanest operating point at
`6` iterations, with mean target-hit probability `0.99609375`.

### Qiskit support-diagnostic relaxation search

The next exact support-side refinement is now in
`tools/qiskit/toe_support_diagnostic_relaxation_search.py`.

This keeps the same factorized `120`-state support shell fixed and relaxes the
two exact support theorems one sector at a time:

- the support interleaving theorem
- the line/plane/avatar core-order theorem

The exact marked-count profile is:

- `exact`: `2`
- `interleaving-relaxed`: `20`
- `core-order-relaxed`: `12`
- `both-relaxed`: `120`

The two-seed study over seeds `7,8` gave the following clean operating points:

- `exact`: `6` iterations, mean target-hit probability `0.99609375`
- `interleaving-relaxed`: `1` iteration, mean target-hit probability `0.88671875`
- `core-order-relaxed`: `2` iterations, mean target-hit probability `1.0`
- `both-relaxed`: `0` iterations, mean target-hit probability `0.939453125`

So the relaxed support sectors expose a real padded-shell effect: once the
marked sector gets too large, Grover amplification stops helping and the best
point can collapse to the uniform state.

### Qiskit support-enhancement relaxation search

The next exact support-side refinement is now in
`tools/qiskit/toe_support_enhancement_relaxation_search.py`.

This tensors the same factorized support-relaxation shell with the exact
three-state external enhancement hierarchy:

- `current_k3_zero_orbit`
- `minimal_external_enhancement`
- `formal_completion_avatar`

So the exact discrete space is

`360 = 120 support states * 3 enhancement states`

padded to `9` qubits. More sharply, the marked sector factorizes exactly as

`Marked(relaxation, mode) = Marked_support(relaxation) * {enhancement(mode)}`

so the three enhancement modes are basis-conjugate to one another. The
support-side marked-count profile therefore stays exactly:

- `exact`: `2`
- `interleaving-relaxed`: `20`
- `core-order-relaxed`: `12`
- `both-relaxed`: `120`

A representative two-seed study over seeds `7,8` on the
`formal_completion_avatar` mode gives the clean operating points:

- `exact`: `12` iterations, mean target-hit probability `1.0`
- `interleaving-relaxed`: `3` iterations, mean target-hit probability `0.970703125`
- `core-order-relaxed`: `5` iterations, mean target-hit probability `0.982421875`
- `both-relaxed`: `1` iteration, mean target-hit probability `0.994140625`

So the enhancement hierarchy does not change the exact support-selectivity
geometry, but the larger `360 -> 512` padded shell does shift the optimal
Grover windows. Most sharply, the fully relaxed sector moves from a `0`-step
optimum on the bare-support `120`-state shell to a `1`-step optimum on the
enlarged shell.

### Qiskit double-interleaving shadow search

A bounded exact side result now sits between that support stack and the larger
bridge shell in `tools/qiskit/toe_double_interleaving_shadow_search.py`.

The support-core interleavings and the hyperbolic-factor interleavings are
isolated as a joint `100 = 10 * 10` shell of two canonical `J(5,3)` copies.
So the exact bridge now carries two separate `10`-state `3-of-5` Johnson
objects at once.

The current bridge is asymmetric there:

- the support theorem freezes one support interleaving
- the factor copy remains free

A two-seed study over seeds `7,8` shows the exact mode is cleanest at `2`
iterations, with mean target-hit probability `0.97265625`. If the support
interleaving theorem is relaxed too, the padded-shell optimum collapses to `0`
iterations.

### Qiskit bridge product-state search

The next exact search layer is now in
`tools/qiskit/toe_bridge_product_search.py`.

This combines three theorem-backed discrete sectors on one product space:

- strict support hierarchy on the bridge side
- five-factor ordering inside the selector-side packet
- glue state `{zero_split_shadow, unique_nonzero_orbit}`

So the current split-shadow theorem and the formal completion theorem are both
encoded on one search space of size `28800`, using `15` qubits after power-of-2
padding.

The seeded verification run (`seed = 7`, `256` shots) gave:

- `current-shadow`: marked count `20`, Grover iterations `32`, target-hit probability `1.0`
- `formal-completion`: marked count `20`, Grover iterations `32`, target-hit probability `1.0`

and in both modes the decoded outputs stayed entirely inside the exact marked
sector, with no non-target valid states and no invalid bitstrings in the kept
top counts.

The repo now also has a reusable iteration-study runner in
`tools/qiskit/toe_bridge_oracle_iteration_study.py`.

The first two-seed product study over seeds `7,8` shows that the `15`-qubit
product oracle is actually cleanest at `31` iterations:

- `31` iterations: mean target-hit probability `1.0`
- `32` iterations: mean target-hit probability `0.998046875`
- `33` iterations: mean target-hit probability `0.9921875`

### Qiskit bridge line-factor search

The next exact refinement is now in
`tools/qiskit/toe_bridge_line_factor_search.py`.

This adds the exact binary line-choice factor inside `U1`:

- `head_compatible_u1_line`
- `tail_biased_u1_line`

and the marked sector keeps only the theorem-compatible head line together with:

- strict support hierarchy
- five-factor packet ordering
- glue mode (`current-shadow` or `formal-completion`)

So the forced-image-line theorem is now encoded directly on one search space of
size `57600`, using `16` qubits after power-of-2 padding.

The seeded verification runs (`seed = 7`, `256` shots) gave:

- `current-shadow`: marked count `20`, Grover iterations `45`, target-hit probability `1.0`
- `formal-completion`: marked count `20`, Grover iterations `45`, target-hit probability `1.0`

and in both modes the decoded outputs stayed entirely inside the exact marked
sector, with no non-target valid states and no invalid bitstrings in the kept
top counts.

A two-seed study over seeds `7,8` shows that the `16`-qubit line-factor oracle
is actually cleanest at `44` iterations:

- `44` iterations: mean target-hit probability `1.0`
- `45` iterations: mean target-hit probability `0.998046875`
- `46` iterations: mean target-hit probability `0.998046875`

### Qiskit bridge weight-filter search

The next exact refinement is now in
`tools/qiskit/toe_bridge_weight_filter_search.py`.

This adds one theorem-backed concentration bit:

- `dominant_weight_filter_pass`
- `dominant_weight_filter_fail`

and the pass state means the exact current inequalities

- `U3` carries more than `4/5` of the hyperbolic selector packet
- `E8_2` carries more than `8/9` of the exceptional selector packet

So the current exact concentration hierarchy is now encoded directly on one
search space of size `115200`, using `17` qubits after power-of-2 padding.

The seeded verification runs (`seed = 7`, `256` shots) gave:

- `current-shadow`: marked count `20`, Grover iterations `64`, target-hit probability `1.0`
- `formal-completion`: marked count `20`, Grover iterations `64`, target-hit probability `1.0`

and in both modes the decoded outputs stayed entirely inside the exact marked
sector, with no non-target valid states and no invalid bitstrings in the kept
top counts.

A two-seed study over seeds `7,8` shows that the `17`-qubit weight-filter
oracle is actually cleanest at `63` iterations:

- `63` iterations: mean target-hit probability `1.0`
- `64` iterations: mean target-hit probability `0.998046875`
- `65` iterations: mean target-hit probability `0.998046875`

### Qiskit bridge split-weight-filter search

The next exact filter is now in
`tools/qiskit/toe_bridge_split_weight_filter_search.py`.

This splits the same concentration theorem into two independent exact binary
factors:

- `hyperbolic_dominance_pass` / `hyperbolic_dominance_fail`
- `exceptional_dominance_pass` / `exceptional_dominance_fail`

So the current bridge hierarchy now has an exact mixed-case search mode rather
than only the joint concentration bit. The marked sector keeps only the exact
`pass/pass` state, together with the already-forced support hierarchy,
five-factor ordering, head-compatible line, and chosen glue mode. The explicit
search space has size `230400`, using `18` qubits after padding.

The seeded verification runs (`seed = 7`, `256` shots) gave:

- `current-shadow`: marked count `20`, Grover iterations `90`, target-hit probability `1.0`
- `formal-completion`: marked count `20`, Grover iterations `90`, target-hit probability `1.0`

and in both modes the decoded outputs stayed inside the exact marked sector,
with no non-target valid states and no invalid bitstrings in the kept top
counts.

A local formal-completion probe at `89`, `90`, and `91` iterations also stayed
on the same `1.0` plateau for seed `7`, so the heavier `18`-qubit oracle looks
robust near the analytic Grover count even though a broader two-seed study is
more expensive in this environment.

### Qiskit bridge diagnostic-order search

The next exact diagnostic layer is now in
`tools/qiskit/toe_bridge_diagnostic_order_search.py`.

This does not enlarge the five-factor ordering sector. Instead, it factorizes
that same exact `120`-state space into three theorem-facing pieces:

- a hyperbolic order on `U1/U2/U3`
- an exceptional order on `E8_1/E8_2`
- an interleaving pattern choosing which `3` of the `5` slots carry the
  hyperbolic sector

The exact identity is

`5! = C(5,3) * 3! * 2! = 10 * 6 * 2`.

So the oracle becomes diagnostic by theorem sector rather than only by one
combined five-factor permutation. The full bridge product space remains
`230400`, using `18` qubits after padding.

The seeded verification runs (`seed = 7`, `256` shots) gave:

- `current-shadow`: marked count `20`, Grover iterations `90`, target-hit probability `1.0`
- `formal-completion`: marked count `20`, Grover iterations `90`, target-hit probability `1.0`

and in both modes the decoded outputs stayed inside the exact marked sector,
with no non-target valid states and no invalid bitstrings in the kept top
counts.

### Qiskit bridge diagnostic-relaxation search

The next exact diagnostic layer is now in
`tools/qiskit/toe_bridge_diagnostic_relaxation_search.py`.

This search does **not** reopen the whole split-weight state space. Instead, it
keeps the accepted pass/pass concentration channel fixed and relaxes the two
order theorems one sector at a time, while the interleaving sector stays free
just as it already does in the diagnostic-order oracle. The corrected exact
diagnostic state space has size `57600`, using `16` qubits after padding.

The marked counts are exact and theorem-facing:

- `exact`: `20`
- `exceptional-order-relaxed`: `40`
- `hyperbolic-order-relaxed`: `120`
- `both-orders-relaxed`: `240`

So the narrowing power of the two order theorems is now visible quantitatively,
not just structurally: the exceptional sector contributes the exact binary
factor, the hyperbolic sector contributes the exact 6-fold factor, and the
interleaving sector contributes no additional theorem restriction here.

Representative two-seed studies over seeds `7,8` on the
`formal-completion` mode give the clean operating points:

- `exact`: `45` iterations, mean target-hit probability `0.998046875`
- `exceptional-order-relaxed`: `32` iterations, mean target-hit probability `0.998046875`
- `hyperbolic-order-relaxed`: `18` iterations, mean target-hit probability `1.0`
- `both-orders-relaxed`: `13` iterations, mean target-hit probability `0.99609375`

In all four sectors the kept top decoded outputs stayed inside the marked
sector, with no non-target valid states and no invalid bitstrings.

### Qiskit bridge diagnostic-enhancement relaxation search

The next exact refinement is now in
`tools/qiskit/toe_bridge_diagnostic_enhancement_relaxation_search.py`.

This tensors the corrected diagnostic-relaxation shell with the exact
three-state enhancement hierarchy:

- `current_k3_zero_orbit`
- `minimal_external_enhancement`
- `formal_completion_avatar`

So the exact discrete space is

`86400 = 57600 * 3`

padded to `17` qubits. More sharply, the marked sector factorizes exactly as

`Marked(relaxation, mode) = Marked_diagnostic_relaxation(relaxation) * {enhancement(mode)}`

so the enhancement modes are basis-conjugate. The order-relaxation
marked-count profile therefore stays exactly:

- `exact`: `20`
- `exceptional-order-relaxed`: `40`
- `hyperbolic-order-relaxed`: `120`
- `both-orders-relaxed`: `240`

Representative two-seed studies over seeds `7,8` on the
`formal_completion_avatar` mode give the clean operating points:

- `exact`: `64` iterations, mean target-hit probability `0.998046875`
- `exceptional-order-relaxed`: `45` iterations, mean target-hit probability `0.998046875`
- `hyperbolic-order-relaxed`: `26` iterations, mean target-hit probability `0.998046875`
- `both-orders-relaxed`: `18` iterations, mean target-hit probability `1.0`

So the enhancement hierarchy now sits exactly above both lower discrete
geometries: it preserves the order-selectivity profile just as it preserved the
support-selectivity profile, while shifting the padded-shell Grover windows
from `57600 -> 65536` to `86400 -> 131072`.

### Qiskit bridge enhancement-factor search

The next exact bridge wall is now in
`tools/qiskit/toe_bridge_enhancement_factor_search.py`.

This does not just rephrase the old glue dichotomy. It refines that wall into
the exact three-state enhancement hierarchy already proved on the theory side:

- `current_k3_zero_orbit`
- `minimal_external_enhancement`
- `formal_completion_avatar`

So the local Qiskit search now distinguishes:

- the current refined K3 object, which still realizes only the zero orbit;
- the minimal exact new datum, which is just replacing that zero slot by the
  unique nonzero orbit in the already-fixed shell;
- the resulting formal completion avatar carrying the forced head line and the
  nonzero completion normal form.

The explicit search space has size `345600`, using `19` qubits after padding,
with marked count `20` in each mode.

The seeded verification runs (`seed = 7`, `256` shots) gave the same exact
operating point in all three modes:

- `current-k3-zero-orbit`: `127` iterations, target-hit probability `1.0`
- `minimal-external-enhancement`: `127` iterations, target-hit probability `1.0`
- `formal-completion-avatar`: `127` iterations, target-hit probability `1.0`

### Qiskit diagnostic-enhancement-slot search

The three-state enhancement hierarchy is now projected sharply onto the older
binary slot wall in
`exploration/w33_enhancement_slot_hierarchy_bridge.py` and
`tools/qiskit/toe_bridge_diagnostic_enhancement_slot_search.py`.

The exact law is:

- `current_k3_zero_orbit -> zero_by_splitness`
- `minimal_external_enhancement -> unique_nonzero_orbit_in_existing_slot`
- `formal_completion_avatar -> unique_nonzero_orbit_in_existing_slot`

So the enhancement hierarchy is not another copy of the binary slot wall. It
is a strict refinement of it: one zero-slot state and two distinct nonzero-slot
states. The diagnostic enhancement shell refined by slot status has exact size
`172800 = 86400·2`, padded to `18` qubits, and its marked-count profile stays
`20 / 40 / 120 / 240`. What changes is the exact marked pair projection: each
mode lands on one enhancement/slot singleton. Seeded exact checks at `256`
shots and `90` iterations returned target-hit probability `1.0` in all three
exact modes:

- `current-k3-zero-orbit -> (current_k3_zero_orbit, zero_by_splitness)`
- `minimal-external-enhancement -> (minimal_external_enhancement, unique_nonzero_orbit_in_existing_slot)`
- `formal-completion-avatar -> (formal_completion_avatar, unique_nonzero_orbit_in_existing_slot)`

### Qiskit cocycle-compatibility wall search

The stronger replacement for that free three-state axis is now in
`tools/qiskit/toe_bridge_cocycle_compatibility_search.py`.

Instead of a bare enhancement label, it uses the exact `6`-state wall factor

`wall_layer x orbit_state`

with wall layers

- `current_refined_k3_object`
- `slot_replacement_datum`
- `formal_completion_object`

and orbit states

- `zero_orbit`
- `unique_nonzero_orbit`

Only `3` wall states are admissible, and only `2` of those are nonzero:

- `current_refined_k3_object x zero_orbit`
- `slot_replacement_datum x unique_nonzero_orbit`
- `formal_completion_object x unique_nonzero_orbit`

So the wall is no longer just a relabeled enhancement family. It is an exact
compatibility theorem with forbidden corners. Tensoring that factor with the
corrected diagnostic shell again gives `345600` states on `19` qubits. Seeded
exact checks at `256` shots now give:

- `all-compatible`: `60` marked states, `74` iterations, target-hit `1.0`
- `nonzero-compatible`: `40` marked states, `90` iterations, target-hit `1.0`

In all three modes the kept top decoded outputs stayed inside the marked
sector, with no non-target valid states and no invalid bitstrings.

### Qiskit support-cocycle compatibility relaxation search

The sharper support-side projection of that same wall is now in
`tools/qiskit/toe_support_cocycle_compatibility_relaxation_search.py`.

It tensors the factorized `120`-state support-relaxation shell directly with
the exact `6`-state cocycle-compatibility wall, so the exact shell is
`720 = 120·6`, padded to `10` qubits. The factorization is still exact:

`Marked_support(relaxation) x Compatible_wall(focus)`.

On the live nonzero wall, the marked-count profile becomes:

- `exact`: `4`
- `interleaving-relaxed`: `40`
- `core-order-relaxed`: `24`
- `both-relaxed`: `240`

So the live nonzero wall multiplies the old support-relaxation profile by the
precise factor `2`. Seeded nonzero-wall checks at `256` shots give:

- `exact`: `13` iterations, target-hit `0.97265625`
- `interleaving-relaxed`: `4` iterations, target-hit `0.953125`
- `core-order-relaxed`: `5` iterations, target-hit `0.96875`
- `both-relaxed`: `1` iteration, target-hit `1.0`

### Qiskit diagnostic-cocycle compatibility relaxation search

The next exact lift is now in
`tools/qiskit/toe_bridge_cocycle_compatibility_relaxation_search.py`.

This tensors the corrected diagnostic-relaxation shell directly with the exact
`6`-state cocycle-compatibility wall, so the shell is again
`345600 = 57600·6`, padded to `19` qubits. The exact factorization is

`Marked_diagnostic_relaxation(relaxation) x Compatible_wall(focus)`.

On the live nonzero wall, the marked-count profile is now:

- `exact`: `40`
- `exceptional-order-relaxed`: `80`
- `hyperbolic-order-relaxed`: `240`
- `both-orders-relaxed`: `480`

So the cocycle wall is now resolved directly against the hyperbolic-order and
exceptional-order selectivity sectors rather than only the exact diagnostic
shell. Seeded nonzero-wall checks at `256` shots give:

- `exact`: `90` iterations, target-hit `1.0`
- `exceptional-order-relaxed`: `64` iterations, target-hit `1.0`
- `hyperbolic-order-relaxed`: `37` iterations, target-hit `1.0`
- `both-orders-relaxed`: `26` iterations, target-hit `1.0`

The promoted local bridge-oracle stack is now also recorded in
`tools/qiskit/bridge_oracle_ledger.json`.

### Enhancement-slot hierarchy bridge

The next exact refinement is now in
`exploration/w33_enhancement_slot_hierarchy_bridge.py` and
`tools/qiskit/toe_bridge_diagnostic_enhancement_slot_search.py`.

The exact compatibility law is:

- `current_k3_zero_orbit -> zero_by_splitness`
- `minimal_external_enhancement -> unique_nonzero_orbit_in_existing_slot`
- `formal_completion_avatar -> unique_nonzero_orbit_in_existing_slot`

So the three-state enhancement hierarchy strictly refines the older two-state
slot wall rather than duplicating it. The current K3 state is separated from
both completion-side states by slot status, while the minimal and formal
completion states share the same nonzero slot but not the same support role.

The Qiskit shell for that theorem is `172800 = 86400·2`, padded to `18`
qubits. The marked-count profile stays the same as the diagnostic-enhancement
family inside each mode, but the marked pair itself is now exact. Seeded
`both-orders-relaxed` checks at `256` shots came back exact at `26`
iterations:

- `current-k3-zero-orbit`: `1.0`, marked pair
  `['current_k3_zero_orbit', 'zero_by_splitness']`
- `minimal-external-enhancement`: `1.0`, marked pair
  `['minimal_external_enhancement', 'unique_nonzero_orbit_in_existing_slot']`
- `formal-completion-avatar`: `1.0`, marked pair
  `['formal_completion_avatar', 'unique_nonzero_orbit_in_existing_slot']`

### Carrier-preserving K3 enhancement theorem

The next exact refinement is now in
`exploration/w33_carrier_preserving_k3_enhancement_bridge.py`.

This sharpens the live external realization wall itself. The exact-completion
image line is already fixed to the head-compatible line in `U1`, the canonical
family carrier plane is already fixed to `U1`, the ordered transport shell is
already fixed as `81 -> 162 -> 81`, and the only missing operator datum is
still the existing tail-to-head `81x81` slot.

So any genuine K3-side enhancement that realizes the unique nonzero orbit must
be carrier-preserving rather than carrier-replacing: it can only replace the
current zero slot by the unique nonzero orbit in that already-fixed slot. The
open theorem is therefore realization of that already-fixed carrier package on
the K3 side, not discovery of a new line, plane, or shell.

### Completion datum-to-avatar lift

The next exact refinement is now in
`exploration/w33_completion_datum_avatar_lift_bridge.py` and
`tools/qiskit/toe_bridge_completion_datum_avatar_lift_search.py`.

This isolates the actual live distinction inside the shared nonzero slot. The
minimal and formal completion states already share the same nonzero orbit and
the same completion normal form, so the difference is role:

- `slot_replacement_datum`: only the required nonzero-orbit replacement in the fixed slot
- `formal_completion_object`: the unique minimal common external object carrying that datum together with the already-forced head line in `U1` and the ordered shell `81 -> 162 -> 81`

The matching shared-nonzero-wall oracle tensors that binary lift factor with
the corrected diagnostic-relaxation shell, so the exact state count is
`115200 = 57600·2`, padded to `17` qubits. The marked-count profile stays
`20 / 40 / 120 / 240`, with exact mode relation
`Marked_diagnostic_relaxation(relaxation) x {lift_state(mode)}`. Seeded exact
checks at `256` shots came back clean in both modes, and a two-seed
`63/64/65` probe on the formal completion side is now cleanest at `63`
iterations with mean target-hit probability `1.0`:

- `slot-replacement-datum`: target-hit `1.0` at `64` on seed `7`
- `formal-completion-object`: target-hit `1.0` at `64` on seed `7`
- `formal-completion-object`: mean target-hit `1.0` at `63` on seeds `7,8`

### Carrier-preserving transport-twisted K3 lift

The next exact geometric localization is now in
`exploration/w33_carrier_preserving_transport_twisted_k3_lift_bridge.py`.

This is the strongest honest step past the discrete wall. The external carrier
package is already fixed, the current external K3 shadow is still only the
split harmonic `81 + 81` package, and the missing internal datum is already
explicit as a nontrivial transport-twisted cocycle/operator package.

So the honest remaining wall is no longer a generic K3-enhancement problem. It
is a carrier-preserving transport-twisted nonzero-slot enhancement of the
current K3 shadow.

So any exact K3-side realization compatible with the current bridge must be a
carrier-preserving **transport-twisted lift** of that fixed external package.
The open wall is now existence of that lift on the K3 side, not the slot, the
line, the shell, or the internal operator shape.

### Transport-twisted target uniqueness

The next exact sharpening is now in
`exploration/w33_transport_twisted_k3_target_uniqueness_bridge.py`.

This tightens the post-`CCCLXXIII` wall from “some carrier-preserving
transport-twisted lift” to a unique target avatar statement. The forced head
line in `U1`, the ordered shell `81 -> 162 -> 81`, the unique nonzero orbit in
the existing tail-to-head slot, and the completion normal form `J2^81` are
already fixed.

So if a genuine K3-side transport-twisted realization exists at all, its
external completion target is already unique up to the natural head/tail basis
gauge. The live wall is therefore no longer classification of multiple
transport-twisted avatars. It is realization of **one** unique transport-
twisted avatar from actual K3-side data.

## Reproduce

### PMNS

```powershell
$env:PYTHONUTF8='1'
py -3 .\PMNS_CYCLOTOMIC.py
py -3 -m pytest tests\test_master_derivation.py -k "p20_pmns_theta12 or p21_pmns_theta23 or p22_pmns_theta13" -q
py -3 -m pytest tests\test_tower_generation_rules.py -k "pmns_theta12 or pmns_theta23 or pmns_theta13 or jarlskog_invariant" -q
```

### CE2 / L-infinity

```powershell
py -3 -m py_compile scripts\ce2_global_cocycle.py tests\test_ce2_explanations.py tests\test_ce2_global_predictor_integration.py
py -3 -m pytest tests\test_ce2_explanations.py -k "anchor_001_line_families or anchor_001_overlap_families or dual_" -q
py -3 -m pytest tests\test_ce2_global_predictor_integration.py -k "anchor_001_line_families or anchor_001_overlap_families" -q
```

Focused frontier checks used in this pass:

- `(20,0)`, `(20,1)`, `(20,2)` scan clean
- `(21,0)`, `(21,1)`, `(21,2)` scan clean
- `(22,0)`, `(22,1)`, `(22,2)` still have unresolved witnesses

## Conjectural physics reading

The exact CE2 data continues to look like staged closure:

1. matter transport on affine / Hessian lines
2. gauge compensation on the same orbit slice
3. diagonal or source coherence only after the transport branch is fixed

That is suggestive, but still interpretive. It is not yet a proof that the full physical theory closes in the same way.

Likewise, the SRG formulas for exceptional dimensions and electroweak quantities look real, but the strongest current reading is that they are shadows of a more fundamental Jordan / Freudenthal / TKK / projector mechanism, not standalone proofs by coincidence.

The local `w33_followup_deliverable_v19.zip` and `w33_followup_deliverable_v20.zip` bundles are structurally suggestive in this same direction. `v19` reproduces the diagonal `9 -> 10` bottleneck in a toy `CP^2`-wired `3x3` Hermitian model by appending a wedge scalar; `v20` sharpens that toy picture to a light-plane / heavy-line flag variable. That is closer to the repo's current exact finite story, because the reduced generation algebra itself now carries a common exact line-plane flag. But those bundle-level continuum interpretations are still not promoted here, because they have not yet been identified with the repo's exact `V4` / Kronecker / `240^2` Yukawa packet as a finished theorem.

## Not yet proved

- ~~A direct subgroup-chain or incidence-theorem derivation of the PMNS cyclotomic formulas from `W(3,3)` alone.~~
  **Resolved (Phase LVI, T801–T815, 62 tests).** The incidence-theorem derivation is the cyclotomic decomposition identity `Φ₃ = μ + Φ₆ + λ`, which partitions the 13 points of `PG(2,3)` into three natural sectors (collinear `μ=4`, transversal `Φ₆=7`, tangent `λ=2`). The PMNS mixing angles are sector-size ratios: `sin²θ₁₂ = μ/Φ₃ = 4/13`, `sin²θ₂₃ = Φ₆/Φ₃ = 7/13`, `sin²θ₁₃ = λ/(Φ₃·Φ₆) = 2/91`. The `θ₁₃` hierarchy arises from second-order `1/Φ₆` suppression. A three-flavor sum rule `s₁₂ + s₂₃ + s₁₃·Φ₆ = 1` holds for all `q`. Verified via explicit `W(3,3)` construction, spread overlap doubly stochastic matrices, and uniform line-adjacency `4(J₁₀ − I₁₀)`.
- A global closed-form transport law replacing every remaining dual CE2 anchor table.
- A finished theorem that turns the full historical TOE narrative into a single exact construction.
