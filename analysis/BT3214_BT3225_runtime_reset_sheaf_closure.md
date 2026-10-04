# Passes 3214–3225 — runtime, reset and sheaf closure

## Executive result

This packet executes the five outstanding machine fronts and two independent outside-box
constructions without importing unmerged claims as evidence.

The principal source-level results are:

1. The complete **194-design** affine-runtime engine is now plan-bound, resumable in 32
   shards and cryptographically self-identifying. A global runtime/information optimum is
   emitted only if all 194 records reach the exact affine order `4,199,040`.
2. The physical tri-ISA promotion path is fail-closed. Exact source runtime never promotes
   `low4` or `fast6` without observed placement and calibration evidence for every compared
   mode.
3. The **876-state** curvature-aware Moore quotient is compiled into a deterministic
   102-bit-word ROM with a canonical semantic hash and recursive bisimulation certificate.
4. Runtime and M36 shards are accumulated as domain-separated Merkle leaves carrying plan,
   engine, source, result and candidate identities. Missing, duplicate, stale or malformed
   shards cannot yield a complete root.
5. The active evidence stack is converted into a dependency certificate. Its frozen snapshot
   has **zero merge-ready PRs** and grants no merge authority.
6. The finite-port factorisation produces a 2-complex with
   `(V,E,F)=(45,720,240)` and Betti numbers
   \[
      (b_0,b_1,b_2)=(1,436,0)
   \]
   over `F2`, `F3` and `F5`. Its binary CSS chain complex is exactly
   `[[720,436,2]]`, with `d_X=2` and `d_Z=3`.
7. Phase synchronization and epistemic reset are formally distinct. On the
   `876 x 12 = 10,512` product state space, every phase-only word has rank at least 876;
   the optimal phase marker attains rank 876, not rank one.

The packet deliberately stops at source and finite-theorem claims until the focused RTL,
placement, exhaustive-shard and PDF lanes terminate successfully.

## 3214 — all-194 full-affine runtime closure

The frozen library consists of six zero-translation symplectic generators

`F_p, F_f, S_p, S_f, CX_pf, CX_fp`

and four translations `Z0..Z3`. Exact universality requires both linear order `51,840` and
translation-orbit span rank four. This gives 80 universal five-opcode and 114 universal
six-opcode subsets.

The new plan contains every design's exact frame metrics and control-channel information:
collision count, frame diameter and mean distance, translation rank, decoder-operation cost,
and average/minimum/maximum destination entropy. Its semantic digest binds every shard.

Each shard performs directed BFS on all `51,840 x 81 = 4,199,040` affine elements and records:

- exact reached order;
- directed diameter;
- exact mean distance;
- complete growth series;
- growth-series digest;
- record digest and enclosing shard digest.

Aggregation refuses:

- fewer or more than 32 shard files;
- duplicate or missing shard indices;
- cross-plan records;
- a stale plan digest;
- duplicate global design indices;
- any order other than `4,199,040`;
- any growth series whose entries do not sum to `4,199,040`.

Only a complete aggregate computes the six-objective runtime/information Pareto frontier.
At source publication time the engine and plan are present; the 32 exhaustive BFS shards are
not yet observed.

## 3215 — physical promotion is evidence-gated

The frozen source values remain:

| mode | full-group mean | collision probability | source operation units |
|---|---:|---:|---:|
| current4 | 14.1755851337 | 45/324 | 4 |
| low4 | 15.2163239693 | 36/324 | 5 |
| fast6 | 13.7293695702 | 63/486 | 8 |

These values do not determine a hardware winner. The promotion record must contain one device,
one toolchain, one commit, and observed `placed`, `logic_cells` and `fmax_mhz` fields for all
three modes. Without that record the result is `FAIL_CLOSED_SOURCE_ONLY` and `current4` remains
the fallback.

The RTL enforces the same rule independently: `low4` and `fast6` require both placement and
calibration bits. A requested but unverified mode falls back to `current4` and raises the
fallback output.

## 3216 — canonical 876-state quotient ROM

The compiler independently reconstructs:

- 48,826 zero-, one- and two-fault D4 hypotheses;
- all 120 triangle syndromes;
- the frozen 23-test signatures;
- 46,284 base signatures and 1,436 collision classes;
- the exact `none/flat/curved` curvature labels;
- the recursively minimized Moore signatures.

The resulting controller has 770 distinct initial classes and 876 recursive states. State IDs
are assigned by sorting complete recursive signatures rather than by traversal order, making the
ROM invariant under incidental dictionary or queue ordering.

Each 102-bit word contains:

- eight 10-bit child-state IDs;
- an eight-bit valid-outcome mask;
- three two-bit curvature counts;
- a seven-bit next triangle action;
- one terminal bit.

The generated JSON carries the full transition table and semantic SHA-256; the generated MEMH is
consumed by synthesizable RTL. Equality of complete recursive output/action/child signatures is
the machine-checkable bisimulation certificate. No ROM area or timing is claimed before Yosys
and HX8K placement complete.

## 3217 and 3222 — proof-carrying distributed evidence

Every runtime or M36 shard becomes a domain-separated leaf that binds:

- evidence kind and schema;
- shard index and total count;
- plan digest;
- engine digest;
- source identity;
- result-file digest;
- record and candidate counts;
- completion status;
- candidate subtree root when applicable.

The accumulator constructs separate runtime and M36 roots and one two-leaf umbrella root. It
also derives deterministic audit indices from the committed root and exports inclusion proofs.
Positive inclusion controls, a one-field tamper control, and a duplicate-index control are frozen.

A naysayer record is actionable when it supplies a committed inclusion path plus a deterministic
violation such as wrong affine order, stale plan hash, malformed candidate, duplicate index,
digest mismatch or independent-certificate rejection.

This architecture was informed by proof-carrying-data and distributed-proof work, including
Chiesa--Tromer--Virza's distributed PCD construction (IACR ePrint 2015/377) and the BOIL
accumulation construction (IACR ePrint 2024/1993). The committed implementation is intentionally
weaker: SHA-256/Merkle integrity does **not** prove honest computation, zero knowledge, consensus,
or cryptographic soundness. Full recomputation and independent certification remain decisive.

## 3218 — executable evidence-stack preconditions

The frozen live snapshot records:

- `#242`: open, non-mergeable against advanced master, focused rerun queued;
- `#243`: open, stacked on `#242`, workflow action required;
- `#244`: open, stacked on `#243`, focused evidence unobserved;
- `#246`: open and independently mergeable, focused lane pending;
- `#247`: merged source, with PDF and physical boundaries retained.

The exact dependency sequence is:

1. observe `#242`; if its run is green, reconcile newest master and require another green run;
2. only after `#242` merges, reconcile/retarget `#243`, approve its bootstrap and inspect the
   materialized source before its focused gate;
3. only after `#243` merges, reconcile and run `#244`;
4. independently observe and reconcile `#246`;
5. preserve `#247`'s terminal source artifact and unobserved evidence boundaries.

No row is currently ready for human merge review. The scheduler never mutates GitHub and never
grants merge authority.

## 3219 and 3221 — bonkers bridge becomes a port-nerve cohomology problem

The merged finite-port factorisation supplies 45 canonical blocks and 240 support ports. Every
port belongs to exactly three blocks, and its three block pairs are unique to that port. Hence the
block graph's 720 edges are partitioned into 240 triangular faces.

Let

\[
 C_2 \xrightarrow{\partial_2} C_1 \xrightarrow{\partial_1} C_0
\]

be the resulting cellular chain complex. The block graph is connected, so
`rank(partial_1)=44`. Because the 240 face boundaries have disjoint edge supports,
`rank(partial_2)=240` over every field. Therefore

\[
 b_0=1,\qquad b_1=720-44-240=436,\qquad b_2=0.
\]

This immediately changes the bridge question. A phase-decorated edge assignment `a` has port
flux

\[
 \delta_1 a = \partial_2^T a.
\]

A nonzero flux obstructs a flat lift. But zero flux does not choose a unique bridge: over
`F_p`, there are `p^436` gauge-inequivalent constant-coefficient flat classes. The failed direct
45-object crosswalk is therefore replaced by a huge moduli problem, not rescued by adding an
unconstrained phase bit.

The distinction is consistent with the sheaf-theoretic contextuality literature. Abramsky,
Barbosa, Kishida, Lal and Mansfield (arXiv:1502.03097) show cohomological obstructions can witness
important contextuality arguments. Carù (arXiv:1701.00656) proves the obstruction is not a
complete invariant in general. Accordingly this packet claims only cellular flatness obstruction
and ambiguity on the explicit finite-port nerve.

### The induced CSS code

Take `H_X=partial_1` and `H_Z=partial_2^T` over `F2`. Orthogonality follows from
`partial_1 partial_2=0`, and

\[
 k=720-44-240=436.
\]

The block SRG contains

\[
 45\cdot32\cdot22/6=5,280
\]

triangles; only 240 are filled port faces. Any of the remaining 5,040 triangles is a
weight-three non-boundary cycle, so `d_Z=3`. Two edges in one filled face form a dual cocycle;
no weight-one cocycle exists and no two-edge cut can exist in the degree-32 graph, so `d_X=2`.
Thus the exact code is

\[
 [[720,436,2]].
\]

It is useful as a high-rate provenance/checksum fabric, but distance two rules out calling it a
fault-tolerant quantum memory.

## 3220 — bonkers synchronization theorem and reset thermodynamics

Cross the curvature controller with twelve phase states. The product has

\[
 876\cdot12=10,512
\]

states. Every phase-only symbol acts as identity on the belief coordinate. Consequently every
phase-only word has product-map rank at least 876. The optimal phase marker collapses all twelve
phase states and attains rank exactly 876, proving:

> Epoch synchronization is not epistemic reset.

A rank-one reset requires a distinct, authorized, logically irreversible belief operation. The
RTL therefore lets a marker set `phase_locked` but requires both reset authorization and a valid
proof root before emitting a one-cycle belief-reset pulse.

Berlinkov and Szykula's algebraic synchronization work (arXiv:1412.8363) motivates treating reset
through image rank rather than through a verbal synchronization analogy. A rank-one reset removes
the full finite-state capacity

\[
 \log_2 876 = 9.7747870596\ \text{bits}.
\]

The Shannon entropy actually erased depends on the input belief distribution. For the explicit
uniform or maximally mixed 876-state ensemble at 300 K, the Landauer floor is

\[
 k_B T\ln 876 = 2.8063207254\times10^{-20}\ \mathrm{J}
              = 0.1751567627\ \mathrm{eV}.
\]

This is neither a distribution-independent per-event reset charge nor a CMOS or optical energy
forecast. The phase marker itself leaves all 876 belief states distinguishable and therefore
removes no belief-state capacity.

## 3223–3225 — hardware and evidence surface

The unified RTL contains:

- the generated 876-entry quotient ROM;
- a phase-versus-belief reset supervisor;
- a supplied-root comparator for runtime/M36 authorization;
- an evidence-gated tri-ISA selector;
- low-pin HX8K wrappers;
- a combined adversarial testbench.

The testbench checks ROM initialization and out-of-range fail-closure, phase lock without belief
reset, denial of unauthorized reset, proof-root authorization, digest mismatch rejection, and
unplaced/uncalibrated ISA fallback.

The focused workflow must regenerate every fast source artifact, run pytest and Icarus, synthesize
and place the ROM/control wrappers, integrate all four front doors twice, compile all three PDFs,
and freeze observed evidence. Separate matrix workflows execute the 32 full-BFS shards and the
256 logical M36 shards. No exhaustive aggregate or digital/physical result is claimed before
those workflows terminate and their artifacts are inspected.

## Publication boundary

Source, finite constructions, exact rank arguments, fail-closed protocols, RTL and workflows are
committed. The following remain unobserved or incomplete at source publication:

- all 32 affine BFS shards and the complete 194-record aggregate;
- all 256 M36 shards and any accepted candidate;
- observed tri-ISA area, Fmax, power or calibration;
- quotient-ROM Icarus/Yosys/HX8K results;
- materialized canonical manuscript changes and three successful PDF builds;
- laboratory optical, detector, thermal, coherence or fabrication behavior.
