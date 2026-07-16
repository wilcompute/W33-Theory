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
| inspect the newest exact breakthrough | [Passes 358–359: outer Weil envelope and exact `[[137,1,21]]` code](PASS358_359_GITHUB_BATCH_INTEGRITY_ALPHA_CODE_SYNTHESIS.md) |
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

## The current breakthrough: the selection layer

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

- an internally canonical selector-to-fermion chirality assignment (Passes 346 and 358 prove that the full
  controller exchanges the two choices, so any selection must import symmetry-breaking data);
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
