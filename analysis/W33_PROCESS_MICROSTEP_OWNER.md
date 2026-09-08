# Reusable proofs, separately consumed process steps

`w33_process_microstep_owner.py` supplies the missing owner boundary between
the existing process kernel and interruptible counter arithmetic. A valid
arithmetic proof can be checked repeatedly; that alone does not establish that
one particular process should advance again. The owner retains an authoritative
microcursor and consumes each expected cursor at most once in serialized calls.

## What the parallel track already owns

The latest fetch found no commits beyond W33 `6f884f9d3` or Holotrade `a104478`.
The earlier parallel W33 batch includes `68f4f1e85`, which introduced
`w33_holovm_process_kernel.py`, and `b47805e57`, which introduced
`w33_steinberg_control_artifact_cache.py`. Their process/value separation and
artifact/authorization separation are prior work. The latter source was read
in full for this integration; the process kernel's fork and advance paths were
also reread. Its macro `advance` still executes a complete counter instruction.
The zipper packet `a459c0c92` supplies bounded bit-node microsteps. This owner
joins those existing objects; it claims no new universality or cache theorem.
Full historical and recursive manuscript intake remains incomplete.

## Execution architecture

1. Install an already trusted process and start an instruction. The owner stores
   its committed descriptor separately from its in-flight microcursor.
2. A worker returns a JSON envelope containing the expected cursor identity and
   an existing zipper receipt. The cursor identity commits the entire parent
   continuation, microstate, tick ordinal and history root.
3. The owner checks that envelope against its current head, invokes the existing
   store-free arithmetic verifier, materializes verified immutable writes, then
   replaces the head. A repeated envelope now has the wrong expected cursor.
4. On DONE, an explicit commit checks the current cursor and parent, publishes
   one child process and removes the in-flight entry. Guest registers remain
   at the old committed value until this action. The child keeps process ID,
   branch, passport and fibre; generation advances once per macro instruction.

The child history commits the parent and the complete microtrace hash chain.
Its `last_receipt` is a domain-separated microtrace digest, not a fabricated
macro receipt. Existing process archive/STRONG-retention/resume accepts this
descriptor, as tested with a discarded worker memory and a fresh restored store.
Consumers requiring a macro-receipt payload still need an explicit adapter.

## Concrete experiment

Eight forks start at the same counter value. Incrementing 255 to 256 takes
19 microticks. The executable constructs **19 inner proofs** and explicitly
binds each to all eight current cursors: **152 accepted outer submissions**.
All **152 immediate duplicate submissions are rejected**. The eight children
have one common value state, eight distinct histories and eight distinct
continuation identities; all match an independent macro execution.

The same inner receipt cannot be submitted under another fork's unchanged outer
envelope. Explicit rebinding is allowed when the other fork has the identical
microstate, and the arithmetic is verified again. This is proof-construction
reuse, not an eightfold runtime improvement or a transfer of authority.

Seven new tests cover fork confusion, corruption, duplicate delivery, pure
verification versus consumption, premature/stale commit, storage failure,
24 carrier/operation/value comparisons, proof fanout and STRONG recovery.
The existing seven process-kernel and nine zipper tests also pass: 23 tests.
The first run had an invalid HALT fixture (extraneous operands); correcting
the fixture required no owner change.

## Scope and literature connection

[Herlihy and Wing's linearizability paper](https://www.cs.cmu.edu/~wing/publications/HerlihyWing90.pdf)
provides the standard vocabulary for separating an operation's work from the
point where its effect becomes visible. Here that point is explicit owner
publication, but the implementation assumes serialized calls; this is not a
proof of a concurrent or distributed linearizable service.

The owner is trusted in-memory state. These hashes are not signatures or access
tokens. Workers must not mutate owner dictionaries or the authoritative store.
An interrupted write can leave unreachable immutable nodes but cannot advance
the head. Crash recovery of in-flight owner state, locking, durable commit,
external I/O exactly-once semantics, bounded metadata costs and microcheckpoint
retention admission remain separate work. The existing one-bit-node bounds
apply to inner arithmetic, not total envelope hashing or verification cost.

```sh
python analysis/w33_process_microstep_owner.py
python tests/test_w33_process_microstep_owner.py
python tests/test_w33_holovm_process_kernel.py
python tests/test_w33_counter_zipper_microcode.py
```

The executable writes `analysis/w33_process_microstep_owner_certificate.json`.
