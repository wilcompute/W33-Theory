# Recovery and useful output after the September 6 VM updates

The new authenticated-counter guest can now survive loss of its worker memory.
`w33_lossless_counter_suspension.py` exports the exact control state, both fibre
tags and the union of reachable binary-counter nodes into a content-addressed
archive blob. The existing `RootRegistry` pins it STRONG; the existing
`TemporalMerkleGC` retains it. Resume checks the owner's trusted expected root,
the live pin, the content hashes and complete reachability before returning a
fresh `BitStore`. After suspension at step 7, destroying worker memory and
collecting the archive, the resumed guest finishes `(7,11) -> (18,0)` at step 24.
Both immutable carrier types pass the recovery test. All 1296 fibre addresses
round-trip distinctly in the regression suite.

This is a concrete extension of `w33_authenticated_counter_machine.py`,
`w33_finite_control_unbounded_guest_hypervisor.py` and
`w33_temporal_merkle_gc.py`. It supplies recoverable software state; it does not
infer physical storage or quantum hardware from the finite geometry.

## What the new commits establish, and what execution additionally needs

W33 `270a9a3fb` and `c2df9ac5f`, and Holotrade `27e2fb5`, introduce spread-ladder
checkpoint accounting (`w33_spread_ladder_reversible_gc.py`,
`w33_ladder_checkpoint_placement.py`, and Holotrade
`scheduler/w33-reversible-checkpoint-ladder.js`). Their geometric result is the cut bound
`|boundary S| >= |S|(40-|S|)/4`, attained by unions of spread lines. The table
`36,64,84,96,100,96,84,64,36,0` and the sum 660 remain valid geometry.
Equating twice that sum with executed network traffic additionally requires a
protocol that traverses each counted boundary edge once in each direction.
Local pin/release and GC do not themselves implement such a protocol. A stored
root, its byte length, the number of possible values and a set of occupied
network points are different quantities.

| New proposal | Executable requirement exposed by the audit |
| --- | --- |
| Retain the shared base while suspending a fibre leg | A fixed live projection has six possible missing tags. Preserve that tag or a replay source that determines it. |
| A base with 36 possible values occupies rung 9 | Provide an explicit placement and capacity contract; cardinality alone does not allocate 36 points. |
| Overflow checkpoints become HASH_ONLY | Such roots preserve identity but need not preserve resumability. Supply retained bytes or a verified recomputation schedule. |
| Boundary-optimal checkpoint regions | Specify message generation and routing before reporting executed hop counts. |

The real space-favoured adaptive strategy requests 13 STRONG checkpoints. Its
ladder plan supplies 10 STRONG and 3 HASH_ONLY references.
`checkpoint_retention_audit` therefore reports `retention_demand_met=false`.
This does not disprove the cut theorem or rule out recomputation: it prevents
the current descriptor from being mistaken for a demonstrated reversible
runtime. Even plans without overflow still require capacity, byte availability
and a runtime schedule; the adapter never marks them dispatchable.

The missing-information observation is already in the earlier fibre certificate:
both projections are six-to-one. The retention distinction is already in the
temporal-GC module, whose existing witness explicitly sweeps HASH_ONLY bytes.
The new contribution is wiring these obligations into a working counter-guest
snapshot and an admission audit. Reversible checkpointing and its storage/time
trade-offs are prior art: [Bennett](https://doi.org/10.1137/0218053) and
[Li, Tromp and Vitanyi](https://arxiv.org/abs/quant-ph/9703009).

## The magic update needed reconciliation with the same blueprint

Continuity decision `eb975fb4-592b-4403-80c1-87ecc0af8da5`, accompanying
`c2df9ac5f`, narrowed the remaining work to decoder and yield after finding 104
acceptance witnesses. However, the blueprint's existing three-copy section and
`w33_pass2990_2995_overhaul_and_rank2.md` already explain why rank-one
stabilizer acceptance witnesses carry no magic. That prior finding belongs to
Passes 2933 and 2977; this audit does not claim it as new.

`w33_three_copy_output_rank_audit.py` replays every one of the source search's
27,391 projectors for each of 36 rays. It checks that the eight-witness storage
cap is never reached, computes binary rank and commutation independently from
the returned labels, and dense-verifies every hit (the original certificate
checked at most four per ray). All 104 hits have six independent generators on
six qubits. Hence `k=6-6=0`, and the projector range has dimension `2^k=1`.
The accepted output is a stabilizer state. Stabilizer decoding cannot turn it
into a distilled magic state. The rank formula is standard
[stabilizer-code theory](https://arxiv.org/abs/quant-ph/9705052).

With the user's explicit approval, the new shared insert and blueprint update
now preserve the acceptance result while keeping useful super-linear
distillation open. The original search and certificate remain available;
the audit has its own frozen certificate. This is not a no-go for asymmetric
protocols, more copies, or different correction conditions.

## Replay and limits

```sh
python tests/test_w33_lossless_counter_suspension.py
OPENBLAS_NUM_THREADS=1 python tests/test_w33_three_copy_output_rank_audit.py
PYTHONPATH=analysis python analysis/w33_lossless_counter_suspension.py
PYTHONPATH=analysis OPENBLAS_NUM_THREADS=1 python analysis/w33_three_copy_output_rank_audit.py
```

The eight recovery tests cover worker loss, all fibre coordinates, actual GC,
malformed archives, corrupt content, budgets, serialized archive reload and real scheduler overflow.
The two output-rank tests include full family replay and rejection of dependent
or noncommuting generator lists. Frozen results are
`w33_lossless_counter_suspension_certificate.json` and
`w33_three_copy_output_rank_audit_certificate.json` in this directory.

Snapshots are self-contained archive blobs: bytes are shared within each
counter snapshot but duplicated across snapshots. Hash identifiers assume
collision resistance for finite runs. Callers own authorization, epoch/replay
policy and pin handoff; a trusted expected root is not obtained from an
untrusted sender. Resume is repeatable while a pin remains live. This is not a
distributed lease, consensus or durability guarantee for an external service.

## Reading coverage

This continuation refreshed both remotes and inspected the new VM diffs and
their certificates, then followed the rank-one result back into the blueprint
and earlier analysis. Holotrade's new blocker-selector correction and the
bounded-search updates were also inspected. Full semantic reading of the
original three-day history and all recursive paper inputs remains incomplete.
Captured diffs are not counted as read. The durable intake ledger is maintained
under `C:/Repos/W33-VM-20260905-reading` and must be continued before any claim of
complete corpus coverage.
