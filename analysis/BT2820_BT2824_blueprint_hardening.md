# Passes 2820–2824 — executable Holonet blueprint hardening

Passes 2820–2824 were reserved directly on `master` after canonical Pass 2808 landed. This packet upgrades `holonet_machine_blueprint.tex` to incorporate the full logical-decoder M36 breakthrough, the exact PG(3,2) tetrahedral support lift, and explicit claim-promotion gates.

## 2820 — minimal micro-ISA versus public ISA

The blueprint distinguishes:

- the internal four-operation, two-bit frame micro-engine using `F_p`, both controlled-add directions, and one translation;
- the public eight-opcode, three-bit Holonet ISA retained for scheduling, transport, and readable semantics.

The selected linear triple generates all `51,840` elements of `Sp(4,3)`. One translation spans all `81` affine translations, so the micro-engine generates `ASp(4,3)` of order `4,199,040`.

The existing `72 LC / 60.8 MHz` result belongs to the public convenience frame unit. The minimal unit requires its own observed synthesis, anti-fold, placement, and timing evidence before an area figure is promoted.

## 2821 — deep M36 operating curve and erratum

The full Pass-2804 search enumerates the `11,520`-element projective two-qubit Clifford decoder group, all `5,355` binary rank-two isotropic `[[4,2]]` stabilizer projectors, and all four syndromes. The deep grade has exactly `48` improving branches.

For the explicit H-decoded branch,

`p_next=p(4-p)/(3(p^2-2p+2))`,

`P_success=(p^2-2p+2)/4`.

The fixed points are `0`, `2/3`, and `1`, with slopes `2/3`, `6/5`, and `2/3`. Accepted rounds purify exactly for `0<p<2/3`. The accepted-output yield per input for one round is `P_success/2`.

Boundary: this is an exact recurrence, not an optimized asymptotic-yield, preparation-cost, logical-noise, injection, or fault-tolerance theorem.

## 2822 — PG(3,2) tetrahedral support-first decoder

For a ternary projective point `[x] in PG(3,3)`, define its nonzero binary support mask `pi([x])` in `F_2^4\{0}`. Each support mask `S` has fiber size

`|pi^{-1}(S)|=2^(|S|-1)`.

The tetrahedral cell census `(4,6,4,1)` therefore lifts exactly to `(4,12,16,8)`. For each of the three perfect coordinate matchings, the 15 support fibers form an equitable W33 partition with quotient spectrum

`12^1 + 2^9 + (-4)^5`,

and residual phase spectrum

`2^15 + (-4)^10`.

The new decoder architecture is two-stage:

1. decode the 15-state binary support shell;
2. decode the 25-dimensional within-fiber ternary phase residual.

The selector factor `24=8*3` becomes intrinsic: `S_4` acts on the three coordinate matchings with `D_8` stabilizer, and the four Type-A masks are the four tetrahedral faces. Four faces times three matchings gives the 12 admissible face-pairing charts.

Boundary: the support map is combinatorial, not a field homomorphism. The exact `(4,12,16,8)` capacity theorem does not alone prove the quotient incidence object is the abstract tomotope, and the objectwise selector intertwiner remains open.

## 2823 — evidence and scope hardening

The document separates proof, simulation, synthesis, placement/timing, published components, modelled end-to-end systems, and a physically built Holonet.

It also records:

- the all-register finite-lift `mu_12` sensor law: exponent `3` for odd `n`, `9` for even `n`, while arbitrary `U(1)` representatives require `3^n`;
- objectwise transpose/CX direction closure at `q=5,7`;
- the removal of the rejected mixer source and migration to the exact packed-bus replacement, with the serial mixer retained as the deployable iCE40 architecture.

## 2824 — executable migration, PDF, and drift closure

`analysis/bt2820_2824_blueprint_truth_gate.py` performs an idempotent migration and writes a source-hash certificate. The dedicated workflow:

- rebuilds the exact M36 operating curve;
- reruns the canonical Pass-2808 support-lift verifier;
- applies the blueprint migration;
- verifies a second application is a no-op;
- runs focused regressions;
- compiles with Tectonic;
- rejects TeX errors and overfull boxes;
- commits the migrated source, PDF, and certificates;
- requires a second clean run with no generated drift.

## Boundary

This packet hardens the architecture document and turns it into a tested release artifact. It does not promote remote hardware before observed CI evidence, infer optimized magic-state yield from a one-branch recurrence, identify the support quotient with the abstract tomotope without an incidence intertwiner, or claim a complete physical Holonet.
