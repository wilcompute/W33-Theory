# Passes 2808–2812 — executable Holonet blueprint hardening

This packet is stacked on merged PR #207 / Passes 2803–2807. It upgrades `holonet_machine_blueprint.tex` to reflect the full logical-decoder M36 breakthrough and converts claim promotion into an executable CI contract.

## 2808 — minimal micro-ISA versus public ISA

The blueprint now distinguishes two interfaces:

- an internal four-operation, two-bit frame micro-engine using `F_p`, both controlled-add directions, and one translation;
- the public eight-opcode, three-bit Holonet ISA retained for scheduling, transport, and readable semantics.

The selected linear triple generates all `51,840` elements of `Sp(4,3)`. One translation spans all `81` affine translations, so the micro-engine generates `ASp(4,3)` of order `4,199,040`.

The existing `72 LC / 60.8 MHz` result belongs to the public convenience frame unit. The minimal unit has an independent simulation, synthesis, anti-fold, placement, and timing gate before any area number is promoted.

## 2809 — evidence-state and promotion-gate matrix

The document now separates:

1. exact proof;
2. RTL simulation;
3. synthesis;
4. placement and timing;
5. published component experiments;
6. modelled end-to-end scenarios;
7. a physically built Holonet.

Each transition has an explicit gate. A published qutrit `SUM` component at `0.92 ± 0.01` fidelity is not called a measured Holonet, and an exact repeater recurrence is not called a measured repeater.

## 2810 — deep M36 distillation and erratum

The full Pass-2804 search enumerates:

- the `11,520`-element projective two-qubit Clifford decoder group;
- all `5,355` binary rank-two isotropic `[[4,2]]` stabilizer projectors;
- all four syndromes.

The shallow grade and both middle Clifford orbits have no improving branch. The deep eight-ray grade has exactly `48` improving branches.

An explicit protocol uses input ray `5`, stabilizers `IYZY` and `YZXY`, syndrome `(-1,+1)`, and a Hadamard on the second logical qubit, producing ray `7`:

`P_success=(p^2-2p+2)/4`,

`F_out=(5p^2-12p+8)/(4(p^2-2p+2))`,

`F_out-F_in=p(p-1)(3p-2)/(4(p^2-2p+2))`.

It improves fidelity for every `0<p<2/3`, containing the entire deep magic-witness interval. The blueprint records the superseded fixed-gauge no-go as an erratum rather than deleting the failure history.

Boundary: this is a state-fidelity distillation theorem, not an asymptotic-yield theorem, fault-tolerant injection gadget, or logical threshold.

## 2811 — sensor, transpose, and mixer scope

For the standard finite qutrit Clifford lift, the scalar phase group is `mu_12` for every register width. Therefore the minimal phase-invariant sensor exponent is `3` for odd `n` and `9` for even `n`. Arbitrary `U(1)` representative phases still require exponent `3^n`.

At `q=5` and `q=7`, the transpose involution is checked objectwise for anti-symplecticity, controlled-add direction conjugacy, and the local-Fourier reverse-gate identity.

The dead `rtl/w33_spread_mixer36.sv` source is removed from the active tree. Verification and workflow triggers point to the exact packed-bus replacement. Its measured parallel area remains too large for the iCE40 target; the serial mixer is the deployable architecture.

## 2812 — executable migration, PDF, and drift closure

`analysis/bt2808_2812_blueprint_truth_gate.py` performs an idempotent migration and writes a source-hash certificate. The dedicated workflow:

- applies the migration;
- verifies a second application is a no-op;
- runs focused regressions;
- compiles the blueprint with Tectonic;
- rejects TeX errors and overfull boxes;
- commits the migrated source, PDF, and certificate;
- requires a second clean run with no generated drift.

## Boundary

This packet hardens the architecture document and promotes the exact PR #207 frontier. It does not claim remote hardware success before the dedicated runners return, infer asymptotic magic-state yield from one-round fidelity improvement, or claim a complete physical Holonet.
