# Universal VM five-front closure — 3 September 2026

This pass executes the five non-sequential VM frontiers named after the finite-control / unbounded-guest architecture pass. The result is not a claim that the Holonet has been physically built. It is a sharper software/architecture boundary: the universal guest, memory authority, finite qutrit control, slow-path geometry and reversible storage policy now have explicit interfaces instead of being adjacent ideas.

## 1. Concrete 45-target slow-path control store

Holotrade commit `6b192207eb75e528653d838b675aa8d121729935` closes the explicit-bijection gap between the 45 real projective cost anomalies and the 45 points of an independently constructed `H(3,4)=GQ(4,2)`. The certificate carries all 45 target lifts, slots and Hermitian points and verifies bijectivity, edge preservation in both directions and equality of the transported line sets.

This pass then makes that table executable in Holotrade:

- `js/w33-slowpath-rom-decoder.js` (`aac3fbf4516aba9b657ed357dbda28d0ec717d6e`)
- `tests/w33-slowpath-rom-decoder.test.js` (`68f2daf93450b05708a93088cc002a34e31724fe`)

Boot admission reconstructs the 27 banks of five from the certificate and checks 45 unique projective targets, 45 unique slots, 135 incidences, three banks per target, 270 unique collinear pairs, SRG `(45,12,3,3)`, the GQ axiom, and exact equality between concrete anomaly lines transported by the table and the abstract `H(3,4)` banks. Runtime lookup normalizes `g ~ -g`; the two Sp lifts are one projective instruction.

The map is fixed and verified, not claimed canonical. That is the correct ROM contract: a hardware table needs a reproducible admitted labeling, not a uniqueness theorem for a labeling that the geometry does not supply.

## 2. Capability addresses are now machine words

`analysis/w33_capability_address_isa.py` (`bf77a2f373aa45688209fe00947225c15b1556c9`) turns the existing Merkle memory capability plus revocation epoch into a first-class virtual pointer.

A pointer commits:

`(Merkle root, fixed-depth base-40 address, bounds, cursor, rights, authority epoch, carrier, evidence floor, sealed state)`.

The reference ISA contains `CINC`, `CSETBOUNDS`, `CANDPERM`, `CREQUIRE`, `CSEAL`, `CLOAD` and `CSTORE`. Bounds, rights and evidence requirements are monotone: software can narrow authority but not widen it. Dereference checks the current Merkle snapshot root, carrier, current epoch/revocation authority, address prefix, requested right and backend evidence tier. A persistent store returns a new Merkle root and a pointer rebound to that snapshot; the previous pointer fails against the new snapshot rather than silently following mutable memory.

This is a software semantics model, not a claim that Python has CHERI-style hidden hardware tags. The hardware tag/forgery boundary remains open and explicit.

## 3. The 80 qutrit transvections now have phase-specified Clifford lifts

`analysis/w33_qutrit_clifford_phase_displacement_lift.py` (`7a559bb95ca425256c0ca0ec4b9d8c19b60d3e35`) closes the algebraic phase-bookkeeping boundary left by the exact Sp(4,3) transvection compiler.

With the odd-prime Weyl convention

`D(q,p) = omega^((q.p)/2) X^q Z^p`,

for the transvection `T(v,lambda): x -> x + lambda <x,v> v`, define

`U(v,lambda) = sum_k omega^(lambda k^2/2) P_k(D_v)`

with `P_k` the spectral projector of `D_v`. The quadratic phase cancellation gives the exact conjugation law

`U(v,lambda) D_x U(v,lambda)^† = D_{T(v,lambda)x}`.

The software verifier enumerates all 40 W33 projective axes and both nonzero `lambda`, giving all 80 primitive opcodes, and checks the 9x9 unitary and Weyl conjugation identities. A general affine frame `D_d U_F` carries the exact residual Pauli phase `-<d,Fx>`, and composition tracks the Weyl global-phase cocycle rather than dropping it.

The optical boundary remains fail closed. An accepted W33 device calibration packet is still insufficient unless it explicitly declares coverage for both `WEYL_DISPLACEMENT` and `TRANSVECTION_QUADRATIC_PHASE`. Prior-art measurements never become W33 device evidence by relabeling.

## 4. A universal structured bytecode now lowers to proof-carrying control packets

The repository already has a genuine WebAssembly binary frontend with block/loop/branch validation and a richer capability-backed Wasm runtime. The missing theorem was not “can we invent another Wasm subset?” It was a lossless bridge into the known universal two-counter semantic core.

`analysis/w33_structured_counter_bytecode_compiler.py` (`5c5b49b04a16ac8afd1e1f35812311d836f19167`) introduces a labelled validation-first counter IR:

- `block NAME inc r0|r1 NEXT`
- `block NAME decjz r0|r1 NONZERO ZERO`
- `block NAME halt`

Every finite existing `Program` has an exact labelled encoding, and compiling that encoding reproduces the original instruction tuple. Universality is inherited from the already-declared Minsky core; no new computability claim is smuggled through the frontend.

After validation, each *executed* guest transition is lowered to a `w33.universal-control-packet.v1`. The packet commits the semantic pre/post transition, canonical W33 route, an exact finite transvection control word, projective target, Sp central-lift bit, execution identity and the qutrit Clifford phase-frame digest. The packet is independently revalidated before it is admitted.

The canonical `add-r1-into-r0` example is the integration witness: with input counters `(7,11)`, the intended guest result is `(18,0)` after 24 transitions, hence 24 proof-carrying finite-control transactions. The dedicated closure test asserts this exact path.

This labelled counter language is the universal core IR *beneath* the existing real Wasm frontend. A complete arbitrary Wasm-to-counter compiler remains a distinct compiler theorem; this pass does not claim it prematurely.

## 5. Reversible memory now has an explicit time/space/GC policy surface

`analysis/w33_reversible_storage_economics.py` (`1303308f8b03f8323d5634853c91a460881a72dc`) connects the Bennett/Merkle undo runtime to the temporal Merkle collector.

For local journal segment length `B` and a workload padded to `B*2^L`, the defined recursive bridge uses

`C(0)=B`, `C(L)=3 C(L-1)`.

After copying the semantic output and reversing the bridge, the model's compute/copy/uncompute traversal upper bound is

`T = 2 B 3^L`.

Peak retained software state is modeled as

`B * token_bytes + (L+1) * checkpoint_bytes + output_bytes`,

where the byte coefficients are measured by serializing the committed 24-step reference VM, not invented hardware numbers. At `B=N`, this reduces to full-history compute/uncompute: `2N` elementary traversals and `N` local undo records. Smaller `B` reduces peak retained history while paying recomputation.

Temporary recursive checkpoints are STRONG Merkle roots while live and become GC-reclaimable after their reverse branch. HASH_ONLY audit roots do not pin bytes. A separate destructive periodic-discard control is intentionally excluded from the reversible Pareto frontier because it destroys inverse history.

No strategy emits a Joule estimate. Logical erasure counts and serialized Python bytes are not a physical Landauer measurement.

## The architecture after all five

The VM now has a clean transaction path:

`validated source -> authority-bearing address -> semantic transition -> W33 route -> exact Sp micro-word -> phase-specified qutrit Clifford -> GQ-checked exceptional control store -> reversible checkpoint/GC policy`.

This changes the interpretation of “the geometry is the machine.” The finite geometry is not asked to contain unbounded memory. It is the **certified control plane** that moves, types, authorizes and verifies transitions of extensible semantic state.

A useful definition of computation for this architecture is therefore:

> **Computation is an authorized state transition whose semantics, finite control realization, evidence level and retained causal history are independently committed and checkable.**

That is stronger than “execute an opcode” and narrower than a metaphysical claim. It is an implementable VM contract.

## Verification boundary

W33 commit `0c1268d86e8d236448ad2e2a98ce4e62ef98bf38` adds a dedicated Actions workflow, and `0069abffb688f10bec6a8d018d6d6cf3e67fb7be` adds cross-front executable assertions joining capability evidence tiers, bytecode packets, phase-frame digests and reversible-storage boundaries. At the time this note was written, GitHub's runners had queued the new jobs but had not yet produced a conclusion. The code is therefore **pushed and verification-gated**, not described here as CI-passed before the runner says so.

Holotrade's original explicit-bijection commit reports its exhaustive generator and 178 shape-catalogue tests with zero failures. The production decoder's new Node test is also runner-gated at this writing.
