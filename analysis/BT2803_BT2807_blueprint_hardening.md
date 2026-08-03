# Passes 2803–2807 — executable Holonet blueprint hardening

This packet upgrades `holonet_machine_blueprint.tex` from a polished narrative into an executable evidence contract. It does not add a new physical claim. It prevents already-proved component results from being promoted beyond their actual scope.

## Pass 2803 — minimal core versus convenience ISA

The frame-control interface is split explicitly:

- the **minimal expressive core** has three Clifford generators plus one translation, four instructions total, so it fits in two opcode bits;
- the **convenience shell** retains eight three-bit opcodes for scheduling and readable semantics.

Both generate the same affine symplectic action. Resource numbers must state which interface was synthesized. The existing `72 LC / 60.8 MHz` result belongs to the full convenience frame unit, not automatically to every minimal four-instruction choice.

## Pass 2804 — evidence-state and promotion-gate matrix

The blueprint now separates:

1. proved mathematics;
2. simulated RTL;
3. synthesized netlists;
4. placed and timed hardware;
5. published laboratory components;
6. modelled end-to-end systems;
7. built end-to-end systems.

Each transition has an explicit promotion gate. In particular, a published `SUM` component at fidelity `0.92 ± 0.01` is not called a measured Holonet, and an exact repeater recurrence is not called a measured repeater.

## Pass 2805 — M36 logical-decoder gauge firewall

The clean GitHub runner exposed a real scope defect in the Pass-2784 two-copy census. Numerical eigenspace diagonalization allowed arbitrary column phases to alter the logical decoder while leaving the stabilizer projector unchanged. The repaired census constructs logical states from rank-one Pauli projectors and freezes a canonical phase convention.

The proved result is therefore:

> No improving branch occurs among all 5,355 binary rank-two isotropic `[[4,2]]` projectors and four syndromes in the frozen canonical logical Pauli decoder gauge, over the stated witness intervals.

The result does **not** yet cover arbitrary logical Clifford decoder gauges, nonidentical inputs, three-copy blocks, catalysts, adaptive protocols, or non-stabilizer assistance.

## Pass 2806 — sensor, transpose, and retired-mixer scope

The sensor section distinguishes exact evidence from extrapolation:

- `n=1`: scalar subgroup `μ12` and minimal exponent `3` are exact;
- `n=2`: the independent certificate gives minimal exponent `9`;
- the alternating all-register rule `3,9,3,9,…` remains conditional on an all-`n` proof that the scalar subgroup stays `μ12`.

The transpose construction is recorded at the eight checked primes `3,5,7,11,13,17,19,23`.

`rtl/w33_spread_mixer36.sv` is declared historical-only and forbidden in new build manifests. Builds must use the packed-port replacement or the serial mixer. The exact parallel replacement parses but does not fit the iCE40 target.

## Pass 2807 — executable migration and release closure

`analysis/bt2803_2807_blueprint_truth_gate.py` is an idempotent migration and verifier. It:

- repairs stale front-page claims;
- inserts the evidence-state matrix and scope firewalls;
- updates the ledger and reproduction commands;
- emits `data/PART_BT2803_BT2807_BLUEPRINT_HARDENING_results.json` with a source hash;
- fails if the migration is not applied or ceases to be idempotent.

The dedicated workflow applies the migration, runs focused regressions, compiles with Tectonic, rejects TeX errors and overfull boxes, and commits the generated source, PDF, and certificate back to the branch. A second clean run must then show no generated drift.

## Boundary

This packet improves the blueprint and its evidence discipline. It does not close the arbitrary-decoder M36 search, the all-register metaplectic scalar-group theorem, the noise-complete sensor model, or end-to-end physical validation.
