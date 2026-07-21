# W(3,3): The Executable Atlas

## Finite geometry, exceptional symmetry, codes, lattices, selectors, and the Holonet

[![Pages](https://img.shields.io/badge/live_atlas-open-blue)](https://wilcompute.github.io/W33-Theory/)
[![Method](https://img.shields.io/badge/claims-evidence_tiered-6f42c1)](docs/index.html#reader-guide)
[![GAP](https://img.shields.io/badge/exact_group_witnesses-GAP-00a878)](analysis/w33_pass358_github_batch_integrity_audit.g)
[![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

> **One geometry. Thousands of witnesses. Every bridge has to name its map.**

This repository is a large executable research program centered on the symplectic generalized quadrangle
`W(3,3)`. Its exact core spans finite geometry, group actions, codes, lattices, representation theory,
cohomology, contextuality, and routing systems. It also contains an ambitious physics program and a runnable
Holonet architecture.

The distinction matters: the finite mathematics and software artifacts can be exact even when a proposed
physical interpretation is conditional. This repository does **not** currently establish a complete theory of
everything or a parameter-free derivation of the Standard Model. It does establish a deep, unusually
interconnected finite structure—and makes the remaining maps explicit.

## Start here

| If you want to... | Open this |
|---|---|
| understand the project in five minutes | [Live atlas](https://wilcompute.github.io/W33-Theory/) — use the Navigator and Reader Guide |
| see what the audit says is actually new | [The Selection Layer](analysis/THE_SELECTION_LAYER.md) |
| inspect the newest exact breakthrough | [Pass 540: symplectic separator and chain-ring Burnside witness](analysis/w33_pass540_symplectic_separator_chainring.g) |
| read the mathematical manuscript | [w33_paper.tex](w33_paper.tex) |
| run the finite-geometry machine | [HOLONET.md](HOLONET.md) |
| read the photonic program | [photonic_holonet.tex](photonic_holonet.tex) |
| understand practical implications and limits | [holonet_practical_implications.tex](holonet_practical_implications.tex) |
| reproduce the Clifford recovery protocol | [Recovery packet](docs/recovery_packet_landing.md) |
| find a result before re-deriving it | [RESULTS_INDEX.md](RESULTS_INDEX.md) |

The atlas is intentionally too large to read linearly. Navigate by question, then follow each promoted claim to
its witness, certificate, and test.

## The exact kernel

Let `V = F_3^4` carry a nondegenerate alternating form. The totally isotropic points and lines form `W(3,3)`.
Its collinearity graph has:

| Invariant | Exact value |
|---|---:|
| points / lines | `40 / 40` |
| points per line / lines per point | `4 / 4` |
| strongly regular parameters | `SRG(40,12,2,4)` |
| adjacency spectrum | `12^1, 2^24, (-4)^15` |
| edges | `240` |
| full graph-symmetry order | `51,840` |
| derived projective symmetry | `PSp(4,3)`, order `25,920` |
| clique-complex first homology | `H_1 ≅ Z^81` |

The same geometry is the projective commutation geometry of the `40` nonidentity two-qutrit Pauli classes.
Its full order-`51,840` symmetry is the exceptional Weyl-group-sized shell that drives much of the atlas. The
equality `240 = |E_8 roots|` is real and useful; an equivariant identification must still be constructed and
checked rather than inferred from the count alone.

## The newest exact frontier: chirality, spectral blindness, and chain rings

Pass 540 resolves the unexplained `q=3` full-support spectral merge. The `16` full-support sections are the
sign words of a four-cube. In a fixed oriented antipodal frame, coordinate product splits them into two
`8`-vertex demicubes; intrinsically the separator is the frame-corrected Moore–Dickson coefficient. These are
exactly the two `D_4` half-spin chiralities. Reorienting the frame may swap their labels, not the two-fiber split. Their common
block-difference polynomial `x^3 - 36x - 81` forgets that chirality, while a determinant-`-1` linear symmetry
exchanges it. This is an exact explanation of spectral blindness, not a selector for physical handedness.

The same GAP witness counts exactly `139,904` full-support `SL(2,5)` section orbits. In a deterministic sample of
`3,000` such orbits it finds a further affine-inequivalent, nonisomorphic cospectral Cayley pair outside the eight
explicit Pass-456/479/482 affine pairs and realizing Pass 481's sheet-coincidence mechanism. The two graphs also have the same exact critical group but different local profiles; the pair itself is checked exactly on both `125`-vertex graphs, but the sample does not enumerate
all `q=5` spectra. Over `Z/9`, exact signed-cycle Burnside averaging gives
`228100045392509153077600971330057241` section orbits and
`2051277771273019233341050472890368` full-support orbits. See the [GAP witness](analysis/w33_pass540_symplectic_separator_chainring.g)
and [machine-readable certificate](data/w33_pass540_symplectic_separator_chainring.json).

## Selection-layer foundation

The repository's whole rank/code arc was re-audited in Passes 322–329. Several headline results were already
published or already present elsewhere in this corpus. What survived the audit is sharper:

- a conditional but nontrivial argument selecting `q=3` through a matching `D_5` half-spin type;
- an explicit characteristic-changing integral module lift, rather than a dimension analogy;
- a curved selector bundle whose global obstruction can be computed;
- a reproducible method for separating exact objects, conditional identifications, and rediscoveries.

Passes 338–342 execute the finite boundaries left by that audit:

| Pass | Exact result | GAP witness | Certificate |
|---:|---|---|---|
| 338 | faithful principal `S_3` selector-frame cover of degree `240`; three `120` quotients and a new `80` refinement-parity quotient | [script](analysis/w33_pass338_selector_frame_240.g) | [JSON](data/w33_pass338_selector_frame_240.json) |
| 339 | extraspecial `2_+^(1+10)` group and its unique nonlinear degree-`32` Clifford carrier | [script](analysis/w33_pass339_extraspecial_clifford_spin_bridge.g) | [JSON](data/w33_pass339_extraspecial_clifford_spin_bridge.json) |
| 340 | characteristic-`3` discriminant modules `D_+ ≅ D_- ≅ 1 ⊕ 5 ⊕ 10` | [script](analysis/w33_pass340_halfspin_discriminant_module.g) | [JSON](data/w33_pass340_halfspin_discriminant_module.json) |
| 341 | the selector obstruction as a restriction-map failure in `H^2`; adjacent `H10` extensions have zero Yoneda product | [script](analysis/w33_pass341_selector_extension_cohomology.g) | [JSON](data/w33_pass341_selector_extension_cohomology.json) |
| 342 | exact global lattice reconciliation: the Eisenstein controller preserves two local spine lattices, not one forced class | [script](analysis/w33_pass342_global_lattice_reconciliation.g) | [JSON](data/w33_pass342_global_lattice_reconciliation.json) |

The central correction is structural: the selector `240`-cover and the signed-`E_8` `240`-action are not the
same object. They already lie over nonconjugate `40`-point actions. The selector-sign class exists locally but
does not globalize; its absence is a cohomological obstruction, not a missing numerical coincidence.

Passes 358–359 then use the newest GitHub batch as an adversarial audit. GAP separates the equal-order groups
`Sp(4,3)=2.U4(2)` and `W(E6)=PGSp(4,3)=U4(2).2`, replaces a contradictory `6+3` claim by the exact complex Weil
carrier `9=5+4`, and proves that the smallest outer-stable oscillator is the real envelope `18=10+8`. The same
packet identifies the length-137 cyclic construction as the binary quadratic-residue CSS code
**`[[137,1,21]]`**, using an exact GAP construction plus the published QR(137) minimum distance. That code theorem
does not derive the physical fine-structure constant.

Pass 360 determines what this corrected code can actually *do*.  Its residue-affine permutations form
`C137:C68` of order `9,316`; adjoining the nonresidue multiplier together with transversal Hadamard gives an
exact `AGL(1,137) = C137:C136` Clifford action of order `18,632`, whose nontrivial quotient acts as logical Hadamard
on the encoded qubit.  Extending by the parity coordinate produces explicit `PSL(2,137)` symmetry of
order `1,285,608`; the `PGL(2,137)` envelope of order `2,571,216` exchanges the two extended QR codes rather than
preserving either one separately.  All of this is code-theoretic and certificate-backed.

Pass 361 then proves the sharp boundary of that gate construction.  The QR/NQR checks give the orthogonal split
`F2^137 = 68 + 68 + 1`; four of the six one-qubit Clifford label maps are impossible because they would force a
nonzero support into the zero intersection of the two check spaces.  The only surviving uniform maps are identity
and `X/Z` swap, so the simple affine/fold-transversal logical image is exactly `<H> ≅ C2`.  Two independent
`4,692 × 137` phase-mask systems have full rank `137`, ruling out every nonzero subset-`S` mask in either
direction.  A logical phase gate therefore needs a genuinely different circuit resource, not a stronger reading
of the same symmetry.

Pass 362 takes the entangling route that Pass 361 intentionally left open.  Two QR-137 blocks form a
`[[274,2,21]]` code; the two encoded Hadamards and transversal CNOT preserve its rank-272 stabilizer and generate
the full real logical label group `O+(4,2) ≅ (S3 × S3):C2` of order `72`.  Keeping phases gives one real-Clifford
matrix group of order `2,304`.  It has two **different** order-`1,152` shadows: quotienting by global sign gives
the centerless `Aut(K4,4) = S4 wr C2`, while the kernel of total Hadamard parity is the central group `W(F4)`.
The common count `1,152 = 72 × 16` therefore hides a quotient/kernel distinction, not a group identity.  GAP also
locates `W(F4)/Z` as the twisted index-two subgroup of `Aut(K4,4)` cut out by equal permutation signs.

Pass 363 resolves the whole order-`1,152` neighborhood.  The order-`2,304` real Clifford group has three—and only
three—nonzero `C2` characters.  Their kernels are pairwise nonisomorphic: `W(F4)`, the central product `2O o 2O`,
and a mixed extraspecial kernel.  The apparent `Aut(C2^2)=S3` triality therefore does not lift.  Radial normalization
also separates two different actions on the same 48-point shell: `W(F4)` preserves the metric `24+24` root-length
split, while `2O o 2O` is transitive after the lengths are forgotten.  The same GAP witness corrects a legacy
shorthand: `GL(2,3)=SmallGroup(48,29)` is not binary octahedral `SmallGroup(48,28)`.

Passes 364–366 build the encoded exceptional tower.  Four QR blocks form `[[548,4,21]]`; all four encoded
Hadamards and twelve transversal CNOTs preserve the actual rank-544 stabilizer and generate `O+(8,2)`.  The explicit
interleaving `(x1,x2,x3,x4,z1,z2,z3,z4) -> (x1,z1,x2,z2,x3,z3,x4,z4)` identifies this phase space with the
Pass-124 `E8/2E8` graph split `255=135+120`.  At three blocks, the `[[411,3,21]]` code's minus refinement gives
`O-(6,2)=W(E6)` on the 36 W33 spreads, now with an explicit `PSp(4,3)`-equivariant bijection and a named
stabilizer-normalizing phase rotation.  Uniformly, the direct sum is `[[137m,m,21]]`, and
`[Sp(2m,2):O+(2m,2)]=2^(m-1)(2^m+1)` is exactly the number of plus quadratic refinements.

Pass 367 closes the exchange-to-gate question without over-unifying it.  W(E6) sign, outer-Weil parity, QR residue
character, and real-Clifford Hadamard parity synchronize in one `C2`-graded fiber product of order
`28,841,108,255,539,200`.  But the QR odd coset has
orders only `8` and `136`, hence no involution.  The common object is an exact grading, not one split `C2` action.

Pass 373 returns to the canonical W33 edge carrier and separates two objects that earlier summaries blurred.
The triangle-boundary image itself is the classical ternary code **`[240,120,3]_3`**.  GAP certifies its distance
from 240 nonzero, projectively distinct parity columns and an explicit triangle word, so all 480 nonzero
single-edge errors have distinct syndromes.  The complete radius-one maximum-likelihood lookup table therefore has
exactly **481 entries**.  This is not a new claim on the already-owned logical quotient: the canonical CSS code
remains **`[[240,81,3]]_3`** with `(d_X,d_Z)=(3,4)`.

Pass 374 then supplies the action-level theorem that the older BT571/BT637/BT644 scalar-cover lineage did not.
Those packets already own the four `F3* x F3*` lifts, their `25,920 + 25,920` phase split, and their sign-deck
maps.  On the 51,840 nonzero minimal X/Z vector pairings, the new GAP witness proves that both the connected and full geometric actions preserve four
separate 12,960-state sheets; the full `W(E6)` stabilizer is `C2 x C2`.  Thus the scalar lift is four copies of
`W(E6)/(C2 x C2)`, **not** a natural `W(E6)` torsor.  Any regular 51,840-state action would require additional
phase transport beyond W33 collineations and the signed-chain functor.

Pass 375 closes the two most obvious escape routes.  The scalar deck is `D=(F3*)^2 = V4`, but its owned phase
character `chi(a,b)=ab` selects one of the three binary characters.  Although `Aut(D)=S3`, the character
stabilizer is only `C2`; an order-three automorphism cycles the three kernels.  Accordingly the unrestricted
sheet normalizer is `S4`, while the exact phase-compatible normalizer is **`D8`**, with no element of order three.
The actual Pass-374 stabilizer independently satisfies `|N_W(E6)(K)|=32` and `N(K)/K=D8`, but the two `D8` objects
are not yet identified.  Finally, GAP proves that the split enlargement `W(E6) x V4` has no regular 51,840-state
complement: its projection kernel would have forbidden order 12,960 inside `W(E6)`.

Pass 376 makes the next comparison without turning it into a state-space claim.  The phase normalizer and
`N_W(E6)(K)/K` are isomorphic as marked `V4:C2` extensions: the phase deck maps to the canonical geometric
deck `C_N(K)/K`, their centers correspond, and both quotient actions have the `1+1+2` fingerprint.  There are
exactly **four** such marked isomorphisms, with residual ambiguity `C2 x C2`.  That identifies a central
two-element line, not a preferred scalar-sheet-to-state map or a restored Weyl torsor.

Pass 377 makes the Holonet oscillator language computationally precise.  BT828's `Q3 XOR` layer is a binary
three-coordinate switch bank, not ternary parity arithmetic.  Across the `360` one-axis events and three depth
residues, its exact header image is a `48`-flag plane with axis split `24+12+12`.  Depth acts on that plane by
the free `C3` shift `flag -> flag+64 (mod 192)`, giving `16` three-cycles.  This is a header-address theorem;
it does **not** yet identify a binary toggle with a Q6 edge traversal or a physical switch.

Pass 378 closes the tempting but invalid shortcut from that header clock to the 48-tick pulse schedule.  Both
objects have bare `16 x C3` set type, so abstract equivariant indexings exist, but there are exactly
`16! * 3^16 = 900657498850357248000` of them.  The scheduler repeats one `tomotope_flag` across each
`LOAD_FLAG / FLIP_Q6_AXIS / LATCH_VERTEX` triple while the header clock moves through three distinct flags.
GAP therefore proves that no C3-equivariant correspondence can factor through the actual scheduler flag label.
The common `16 x 3` shape is a noncanonical timing resemblance, not an edge, flag, or state intertwiner.

Pass 379 takes the remaining geometric shortcut off the table for the current address ABI. Transporting the
same header depth clock, flag to flag plus 64 modulo 192, through BT1371's pinned flag-to-Q6-edge table
preserves only 146 of the Q6 line graph's 960 adjacent edge pairs; 814 are lost and balanced by 814 false
positives. For example, adjacent flags 0 and 8 shift to nonadjacent Q6 edges at flags 64 and 72. The depth
clock is therefore a finite control-address transition, not a Q6 geometric operation, state traversal, or
physical oscillator through that table. A different explicitly built intertwiner remains an open construction,
not an implied one.

Pass 380 identifies the smallest real scheduler switch state: flag plus phase, a 48-state 16-by-3 register.
Pass 381 turns its remaining operational gap into a versioned, reviewed 16-row compiler ABI. Two rows preserve
the canonical anchors; the other fourteen are explicitly marked external bindings. GAP checks its full
48-pulse trace, bijectivity onto the header plane, inverse trace positions, and C3 phase steps. That produces
an executable crosswalk, not a newly forced Q6 geometry.

Pass 382 then isolates the computing content as a reversible 48-state `LOAD_FLAG -> FLIP_Q6_AXIS ->
LATCH_VERTEX` controller: the controller tick is one 48-cycle, whereas the phase clock disagrees with it at
the 16 latch steps. Pass 383 closes the branch/phase question at the correct typed level: an
orientation-preserving branch switch gives `C6`; `S3` requires an additional phase-reflecting involution that
the ABI does not supply.

Passes 384–385 close the remaining naturality shortcuts rather than hiding them. No strict Q6-to-binary-Q3
coordinate fold intertwines the current live table on all 48 header flags; the six profile-compatible folds
remain one symmetry orbit, and the header depth relation generates `S6` on directions. Independently, the
header quotient has two intrinsic eight-class orbits while the live stress path has trivial stabilizer even in
the full Q6 edge automorphism group. The two canonical anchors lie in the same header orbit but opposite
BT1371 colors, so no binding that preserves those inherited partitions retains both. The honest result is
therefore a reproducible compiler contract with stated external inputs—not an implied geometric or physical
identification.

## What the project contributes

The strongest current contribution is paper-sized and precise:

> If the shadow half-spinor is identified with a physical generation, the matching Dynkin type uniquely selects
> `q=3` among the odd rungs. The finite characteristic bridge and projective Clifford carrier now exist as
> explicit objects. A canonical refinement, chirality choice, physical field assignment, calibrated scale, and
> continuum dynamics do not yet follow.

The second selection route—requiring the magic resource to be an exceptional object of the same tower—selects
`q=3` as the uniquely self-contained rung, but that requirement is an elegance condition rather than a
computational necessity. [The Selection Layer](analysis/THE_SELECTION_LAYER.md) gives the full ownership audit,
citations, proof scope, and failure analysis.

## Paper as code

A promoted result should have the complete chain:

```text
claim → named construction/map → executable witness → machine-readable certificate → regression test → public surface
```

For the current packet:

```bash
# Run the five exact GAP witnesses
gap -q analysis/w33_pass338_selector_frame_240.g
gap -q analysis/w33_pass339_extraspecial_clifford_spin_bridge.g
gap -q analysis/w33_pass340_halfspin_discriminant_module.g
gap -q analysis/w33_pass341_selector_extension_cohomology.g
gap -q analysis/w33_pass342_global_lattice_reconciliation.g

# Rerun them through the focused regression harness
python3 -m pytest tests/test_pass338_342_gap_selector_clifford_cohomology.py -q

# Audit the newest GitHub batch and build the exact length-137 QR-CSS code
gap -q analysis/w33_pass358_github_batch_integrity_audit.g
gap -q analysis/w33_pass359_alpha_code_qr_css.g
python3 -m pytest tests/test_pass358_359_gap_github_integrity_alpha_code.py -q

# Rebuild the encoded Clifford/refinement capstone
gap -q analysis/w33_pass363_real_clifford_character_diamond.g
gap -q analysis/w33_pass364_qr548_e8_phase_space.g
gap -q analysis/w33_pass365_qr411_e6_minus_polar_lift.g
gap -q analysis/w33_pass366_qr137m_real_clifford_refinement_tower.g
gap -q analysis/w33_pass367_universal_c2_exchange_gate_pullback.g
python3 -m pytest tests/test_pass363_367_gap_qr_clifford_refinement.py -q

# Certify the W33 boundary decoder and classify the minimal-pair scalar sheets
gap -q analysis/w33_pass373_triangle_boundary_mlut.g
gap -q analysis/w33_pass374_minimal_pair_phase_sheet_obstruction.g
python3 -m pytest \
  tests/test_pass373_gap_triangle_boundary_mlut.py \
  tests/test_pass374_gap_minimal_pair_phase_sheet_obstruction.py -q

# Close the A4/S4 and split-deck escape routes
gap -q analysis/w33_pass375_phase_character_normalizer_obstruction.g
python3 -m pytest tests/test_pass375_gap_phase_character_normalizer_obstruction.py -q

# Compare the phase and geometric D8s as marked V4:C2 extensions
gap -q analysis/w33_pass376_marked_d8_bridge.g
python3 -m pytest tests/test_pass376_gap_marked_d8_bridge.py -q
```

Pass 341 can additionally use the optional GAP
[Cohomolo](https://gap-packages.github.io/cohomolo/README.html) package. The committed witness keeps a transparent
exact-value fallback for installations without it; all group and extension constructions still run in base GAP.

## The Holonet

The Holonet is the engineering face of the same geometry: a finite packet ABI, router, scheduler, correction
layer, contextuality testbed, and photonic design program. The software runs today:

```bash
python3 holonet_cmd.py info
python3 holonet_cmd.py route 0 39
python3 holonet_cmd.py verify
```

Use [HOLONET.md](HOLONET.md) for the full tour and [the public theorem ledger](docs/holonet_theorem_ledger.md)
for claim-to-artifact status. The exact routing and Clifford layers are classical executable artifacts; the error
correction, teleportation, and threshold surfaces include simulations; no physical photonic Holonet has been
built. The first proposed laboratory discriminator is the contextuality/control-arm experiment.

## Recovery Packet

The finite Clifford recovery protocol is packaged as a reproducible, indexed handoff:

```bash
python3 tools/bt1281_verify_recovery_certificate.py
```

Start with [the recovery guide](docs/recovery_packet_landing.md), use
[`data/bt1279_recovery_packet_index.json`](data/bt1279_recovery_packet_index.json) as the machine-readable manifest,
and inspect the strict
[`data/bt1275_strict_polar_path_recovery_certificate.json`](data/bt1275_strict_polar_path_recovery_certificate.json)
for the promoted finite-path result.

## Evidence levels

| Tier | Meaning |
|---|---|
| **E — Exact** | a named finite/algebraic object and map are checked by an executable witness |
| **S — Software / simulation** | behavior is demonstrated in code; hardware performance is not implied |
| **P — Proposed experiment** | a falsifiable implementation or measurement is specified; no result is claimed |
| **C — Conditional interpretation** | a conclusion depends on an explicit physical identification or modeling assumption |
| **F — Failed / superseded** | preserved for audit history, not promoted as current truth |

Numerical agreement, a repeated integer, or matching dimensions are search prompts—not derivations.

## Repository map

| Path | Role |
|---|---|
| `analysis/` | theorem witnesses, GAP programs, computational notebooks, and synthesis notes |
| `data/` | machine-readable certificates and generated result ledgers |
| `tests/` | focused regression tests and broader validation suites |
| `docs/index.html` | the living, searchable public atlas |
| `RESULTS_INDEX.md` | result-first inverted index used to prevent rediscovery |
| `w33_paper.tex` | mathematical manuscript |
| `photonic_holonet.tex` | photonic/Holonet manuscript |
| `holonet_practical_implications.tex` | practical architecture and scope boundaries |
| `HOLONET.md` | runnable machine quickstart |
| `archive/` and older pass files | development history; not automatically current status |

## The correction engine

This corpus is valuable partly because it records when its own ideas fail. The current workflow guards against
five recurring failure modes:

1. coordinate artifacts;
2. claims whose framing exceeds the witness;
3. named ideas with no constructed map;
4. sound calculations attached to one ungrounded physical sentence;
5. rediscovery of a result already in the repo or literature.

The newest example is Pass 343: CI forced a stale Pass 71 CSS claim to regenerate, and GAP proved the proposed
checks satisfy `H_X H_Z^T = A ≠ 0` over `F_2` (rank `16`, weight `480`). The advertised `[[360,9,≥9]]` code was
therefore withdrawn rather than patched around. The same audit then produced the opposite outcome in Pass 344:
Graph RH survived because GAP identified `u=1/11` as the second Perron-trivial pole and certified that all `78`
nontrivial roots have modulus squared `1/11`. The repository records both kinds of correction—retraction when a
claim fails, and preservation when only an implementation fails. Pass 345 then follows the correction backward:
the older `[[360,9,9]]` headline, `[[360,9,1]]` JSON, and literal ratio `ceil(360/250)=2` all collapse to one honest
statement—a 360-dimensional multiplicity ledger with no constructed stabilizers or distance.

Before claiming novelty, search for the **result itself**—the formula, integer sequence, group order, code
parameter, or orbit structure—not just the topic. Then check [RESULTS_INDEX.md](RESULTS_INDEX.md), the live atlas,
recent analysis files, and external primary sources. The pre-commit rediscovery check warns on likely duplicate
code parameters; it does not replace reading.

## Current Frontier

The exact finite atlas is mature; the continuum bridge and physical selection problem are not. The finite program
has not supplied:

- a controller-invariant selector-to-fermion chirality choice—Passes 346 and 358 prove that none exists without
  explicitly imported symmetry-breaking data;
- a dynamical action that turns dimensionless finite spectra into measured masses and couplings;
- a calibrated physical scale derived rather than inserted;
- a rigorous continuum/locality limit with the required spacetime dynamics;
- a uniqueness theorem showing that the full physical model, not merely a finite family, is forced.

Those are not cosmetic gaps. They are the precise frontier separating an exact finite atlas from a physical
theory.

## Citation, provenance, and license

Research led by **Wil Dahn**, developed with AI research agents including Claude, Codex, and Perplexity. The
commit history, witnesses, certificates, and correction records preserve result-level provenance.

- DOI: [10.5281/zenodo.18652825](https://doi.org/10.5281/zenodo.18652825)
- Citation metadata: [CITATION.cff](CITATION.cff)
- License: [MIT](LICENSE)

If you cite a specific theorem, cite its synthesis and executable artifact in addition to the repository-level
record.
