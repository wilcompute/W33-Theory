# Shared counter archives and exact storage admission

The authenticated counter VM can now retain multiple independently resumable
guests in one collector-visible archive. Binary tails are shared by content;
each snapshot keeps its own full control state and both fibre tags. Admission
counts the actual union of retained payloads, including unrelated strong roots.
This is an executable storage component for the existing universal guest, not
a physical computer or a claim that finite storage supports unbounded runs.

## Ownership and external checks

The universal instruction semantics and arithmetic receipts belong to
`w33_authenticated_counter_machine.py`. Full-state recovery and fibre retention
belong to `w33_lossless_counter_suspension.py`; this module reuses its validators.
The strong-root contract belongs to `w33_temporal_merkle_gc.py`, and cross-carrier
content sharing already exists in `w33_zero_copy_merkle36.py`.
`w33_adaptive_reversible_scheduler.py` already estimates checkpoint/history
storage using a deduplication ratio. This packet supplies a concrete archive
and exact payload quote; it does not replace that scheduler or prove its
optimality. All paths in this paragraph are under `analysis/`.

Content-addressed archival deduplication is established prior art:
[Quinlan and Dorward, Venti, FAST 2002](https://www.usenix.org/legacy/events/fast02/quinlan/quinlan_html/).
Authenticated data structures likewise have an established foundation:
[Miller et al., Authenticated Data Structures, POPL 2014](https://www.cs.umd.edu/~jkatz/papers/ADS.pdf).
The contribution here is integration with this repository's counter state,
fibre metadata, retention registry and collector, with executable admission
and independent recovery tests. Weighted coverage below is standard set algebra.

## Virtual storage process

1. `prepare(state, fibre, memory)` validates the guest and builds immutable
   serialized descriptors. Each archived bit names its original counter digest
   and one collector-visible tail edge. A metadata node names both counter roots.
2. `quote(proposal, archive, registry)` validates the proposal and calculates
   current, prospective and marginal canonical JSON payload bytes.
3. `publish(..., max_payload_bytes=budget)` recomputes the current strong-root
   union, validates content, and rejects an excessive budget before changing
   archive or registry. A successful call installs that union, drops unretained
   blobs and pins the new snapshot. A stale quote grants no admission right.
4. The worker can discard its counter store. `resume(handle, trusted_root, ...)`
   checks a live strong reference and all reachable content, rebuilds the
   counter store and returns the complete state and fibre address. Execution
   continues through the existing arithmetic receipt verifier.
5. Releasing one guest allows collection of its metadata. Shared tails survive
   while another strong root reaches them; an audit hash alone retains no bytes.

For candidate snapshots S, let C(s) be a snapshot's reachable blob keys, B the
closure of other strong roots plus the empty sentinel, and w(b) the length of
the canonical JSON payload. Then

    F(S) = sum(w(b) for b in B union union(C(s) for s in S))
    marginal(x | S) = sum(w(b) for b in C(x) minus retained(S))

Thus adding retained snapshots can only reduce another snapshot's marginal
cost. This explains why a per-guest size or uniform deduplication factor can
misprice a particular admission. It does not establish an optimal scheduling
policy: future access patterns, priorities and execution costs remain separate.

## Measured witnesses

The frozen `w33_shared_counter_archive_certificate.json` is reproduced by
`w33_shared_counter_archive.verify()`:

| Workload | Canonical payload bytes |
| --- | ---: |
| Retain counters (n,0), n = 0 through 255, shared archive | 263216 |
| Same 256 states, existing monolithic archive | 469207 |
| One zero-counter snapshot, shared archive | 821 |
| Same single snapshot, monolithic archive | 671 |
| Add counter 254 with counter 255 already retained | 1029 additional |
| Add counter 128 with counter 255 already retained | 2529 additional |

Every population snapshot restores. The population contains 256 metadata
nodes, 255 shared binary nodes and one empty sentinel. Both final candidates
have eight-bit counters, but their overlap differs. Sharing has overhead:
the lone zero snapshot is larger. All 1458 comparisons of A subset B and
x outside B on six actual snapshot closures satisfy diminishing marginal cost.

The experiment also exposed an implementation limit: the old recursive mark
walk raised `RecursionError` on a 1500-node generic chain. The collector now
uses an explicit stack. A regression retains, collects and restores a 4096-bit
counter, and checks that a missing child fails before any sweep.

Run from the repository root:

```sh
python tests/test_w33_shared_counter_archive.py
python tests/test_w33_lossless_counter_suspension.py
python tests/test_w33_temporal_gc_replay.py
```

Tests additionally cover exact budget boundaries, stale quotes, cross-carrier
forks, release and collection, corruption, malformed proposals, JSON transport,
unrelated strong-root charges, and execution after worker memory is discarded.

## Boundaries and independent research directions

The budget covers canonical blob payloads only. It excludes registry records,
hash-index keys, Python objects, peak scratch memory, I/O and CPU. Preparation
and admission materialize temporary copies: this is not a bounded-RAM service.
Owner operations must be serialized; there is no concurrent transaction,
authorization service, lease protocol or durable crash recovery. Validation
rejection leaves archive and registry unchanged; process failure or allocation
failure during installation is outside this in-memory model. SHA-256 names
support finite collision-free executions, not an infinite injective namespace.

The wider requested three-day history and recursive paper reading remain in
progress. This packet does not certify that the entire corpus has been read.

Five independent directions:

- Connect exact marginal storage quotes to the existing scheduler and measure
  workloads where shared suffixes change the preferred placement.
- Bound arithmetic receipt work with incremental carry/borrow execution while
  preserving the existing instruction semantics.
- Build crash-safe archive publication with an explicit durable root protocol.
- Separate reusable arithmetic proofs from guest authority and session binding.
- Compile retention lifetimes so temporary guest roots can be released safely.
