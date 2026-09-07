# W33 HoloVM Content-Addressed Process Kernel

## Result

This pass closes a systems gap above the existing W33 universal guest, authenticated
counter memory, capability ISA, execution passport, checkpoint migration, shared
snapshot archive, temporal GC, and joint snapshot admission scheduler.

The new executable object is a **process continuation**.

\[
\boxed{
\text{process continuation}
=
(\text{process id},\text{semantic state},\text{placement},
\text{passport},\text{causal lineage})
}
\]

The continuation itself is immutable and content addressed. Its Merkle node has one
strong child: the already-existing recoverable shared snapshot root.

This gives an exact distinction that the prior stack did not encode:

\[
\boxed{\text{value identity} \neq \text{process identity}.}
\]

Two forks may contain byte-for-byte identical guest state, and therefore intentionally
deduplicate to the same shared snapshot root, while still being distinct runnable
processes with distinct continuation roots.

The verifier is:

```sh
python analysis/w33_holovm_process_kernel.py
python tests/test_w33_holovm_process_kernel.py
```

## Why this was the missing layer

The repository already had all of the pieces needed to execute a VM, but they lived at
different identity levels.

| Existing object | What it identifies |
|---|---|
| authenticated `State` | guest/control state |
| shared snapshot root | recoverable value state |
| execution passport | admitted control/evidence context |
| fibre-product address | finite machine placement |
| root-registry reference | retention authority |
| authenticated receipt | one verified state transition |

None of these is a process identifier. In particular, the current shared archive
correctly collapses identical snapshots. That is ideal for storage and insufficient
for process semantics: two forks can have the same state without being the same
process.

The new process node sits above—not instead of—those objects.

## Process / value separation theorem

Let \(S\) be a recoverable shared snapshot and let \(P_a,P_b\) be two forks of one
continuation with identical semantic state and placement.

The implementation verifies:

\[
\operatorname{root}(S_a)=\operatorname{root}(S_b),
\]

but

\[
\operatorname{pid}(P_a)\neq\operatorname{pid}(P_b),
\qquad
\operatorname{root}(P_a)\neq\operatorname{root}(P_b).
\]

The process roots each have the same snapshot root as their sole Merkle child.
Therefore the union of two same-state process snapshots contains one shared value
closure and two process descriptors. In the executable witness, the exact marginal
payload of the second fork is exactly the canonical JSON size of its one outer process
descriptor. No counter node is copied.

This is copy-on-write at the **process-state** level, not just at the memory-page level.

## State transition law

Execution is now expressed as a transition between immutable continuations:

\[
C_n
\;\xrightarrow{\;\rho_n\;}\;
C_{n+1},
\]

where \(\rho_n\) is the existing authenticated-counter receipt.

`advance()` does not trust the prover's proposed post-state. It calls the existing
store-free `verify_step`, reconstructs the opened carry/borrow prefix, checks the W33
route, and only then creates the child continuation. The logical process id is stable
across the step while the continuation id changes.

Thus:

\[
\boxed{
\text{process identity is stable; state identity is persistent; execution creates a child.}
}
\]

A deterministic replay of the same parent with the same program produces the same
receipt and child continuation.

## Fork law

`fork(parent, branch)` creates a new process id from

\[
(\text{parent process id},\text{parent continuation id},\text{explicit branch label})
\]

without modifying the authenticated counter store.

A fork is therefore not "copy an emulated computer." It is:

\[
\boxed{
\text{allocate one lineage descriptor over an immutable shared state closure}.
}
\]

This is the strongest computing consequence of the new shared-archive work. The
machine becomes closer to a persistent functional value graph than to a mutable box
full of RAM.

## Retention, causality, and forgetting

The process root is a normal strong root in the existing `RootRegistry`. The temporal
collector follows its one Merkle child and therefore retains the complete shared
snapshot closure.

The causal `parent` and `history_root` hashes are descriptor values, deliberately not
Merkle-child edges. This is crucial. A descendant can remember the identity of an
ancestor without forcing the runtime to keep the ancestor's executable bytes forever.

The verifier demonstrates:

1. pin parent, sibling, and descendant process roots;
2. retain the parent continuation hash as `HASH_ONLY`;
3. release the parent's `STRONG` reference;
4. collect;
5. the parent's executable process blob is gone;
6. its causal hash remains;
7. sibling and descendant still resume exactly.

So at the software level:

\[
\boxed{
\text{retained memory}
=
\text{transitive closure of STRONG continuation roots},
}
\]

while

\[
\boxed{
\text{causal history}
=
\text{hash chain/DAG that may outlive the bytes}.
}
\]

This makes a precise version of the project's "time as memory" intuition: execution
time is represented by the partial order of authenticated continuation events, while
memory cost is the subset of that causal history still held strongly enough to
reconstruct. **This is a software semantics statement, not a physical identity between
time and thermodynamic memory.**

## The virtual hardware

The current W33 VM stack can now be read as one machine.

| Virtual hardware | Current executable realization |
|---|---|
| vCPU | authenticated `prove_step` + independent store-free `verify_step` |
| integer ALU | persistent binary carry/borrow prefix rewrite |
| register file | pc, portal, two counter roots, generation, history root |
| MMU | bounded base-40 capability-address ISA |
| process descriptor | content-addressed `ProcessContinuation` |
| process table | strong process roots in `RootRegistry` |
| interconnect | W(3,3) route, diameter at most two |
| placement coordinate | \(36\times6\times6=1296\) fibre-product hypervisor address |
| checkpoint / swap | shared immutable snapshot DAG |
| fork | one process node above an already shared value closure |
| replay log | authenticated receipts + causal history root |
| scheduler input | process/snapshot roots and exact retained-union payload |
| syscall migration | existing neutral continuation at explicit safe point |
| irreversible forget | release strong root, then temporal GC |
| physical backend gate | existing evidence-tier-gated qutrit/photonic lowering |

This architecture sharpens the current manuscript equation

\[
\text{computation}
=
\text{authorized state transition}
+
\text{certified finite control}
+
\text{retained causal provenance}.
\]

A more operational form is now:

\[
\boxed{
\text{computer}
=
\text{transition verifier}
+
\text{content-addressed continuation graph}
+
\text{authority to retain/advance roots}.
}
\]

The "CPU" is no longer where the enduring machine state lives. A worker is a replay
engine that temporarily materializes an admitted continuation, verifies a transition,
and emits the next continuation root.

## Relation to the external literature

This construction is deliberately a synthesis, not a claim that content addressing,
capabilities, or reversible checkpointing were invented here.

* **Venti** uses content hashes as block identifiers and coalesces duplicate blocks;
  the W33 shared archive uses the same broad content-addressed-storage idea, while the
  new contribution here is the explicit process/value identity split above that
  shared closure.
* **CHERI** is the relevant capability discipline: authority-carrying pointers have
  bounds/permissions/provenance and derived authority is monotone. The W33
  capability-address ISA adopts that software-level discipline but does **not** claim
  CHERI's hardware tags or unforgeability.
* **WebAssembly** specifies execution through abstract-machine reduction rules over
  program state. The W33 stack already refines a Wasm path into the universal
  counter IR; the process kernel supplies a persistent continuation identity below
  that language boundary.
* **Bennett reversible simulation** establishes explicit time/space tradeoffs by
  retaining and uncomputing intermediate states. The W33 ladder/checkpoint work is a
  concrete finite-control policy in that tradition. This process kernel does not
  alter Bennett's theorem; it makes retained checkpoints first-class process roots.

References:

- C. H. Bennett, *Time/Space Trade-Offs for Reversible Computation*, SIAM J.
  Computing 18(4), 1989.
- S. Quinlan and S. Dorward, *Venti: A New Approach to Archival Data Storage*,
  FAST 2002.
- CHERI architecture documentation, University of Cambridge CTSRD.
- WebAssembly Core Specification 3.0, 2026.

## What this says about the Holonet

The Holonet's strongest computing interpretation is not "forty nodes somehow contain
an infinite computer." The finite geometry is the **control fabric**. Universal
semantics live in an extensible family of authenticated immutable state objects.

That division is now explicit:

\[
\boxed{
\underbrace{W(3,3)}_{\text{finite control/routing}}
\quad+\quad
\underbrace{\text{inductively extensible Merkle state}}_{\text{guest memory}}
\quad+\quad
\underbrace{\text{continuation roots}}_{\text{process/time}}
}
\]

The physical photonic proposal can implement more or less of the finite-control side
depending on calibration evidence. The software theorem does not require a claim
that a single photon carries an actually unbounded tape.

## Boundaries

The verifier does **not** prove:

- a hardware process implementation;
- hardware-unforgeable capabilities;
- persistent storage durability under power loss;
- distributed ownership/consensus for root mutation;
- physical energy per GC event;
- a physical equivalence of time and memory;
- that an optical Holonet has been fabricated;
- quantum universality of the finite Clifford plane by itself.

It proves a narrower and useful thing: the repository's existing executable VM pieces
admit one coherent immutable process semantics, with exact fork, step, retention,
resume, and forgetting rules.

## Architectural consequence

The next natural kernel ABI is no longer "save/restore a VM object." It is:

```text
ADMIT(passport, continuation_root)
RUN(continuation_root, fuel/evidence)
EMIT(receipt, child_continuation_root)
FORK(continuation_root, branch_label)
PIN(continuation_root)
RELEASE(continuation_root)
RESUME(continuation_root)
```

That is small enough to lower onto a classical host, a capability machine, a
distributed replay worker, or—after calibration—the finite photonic control plane,
without changing guest semantics.
