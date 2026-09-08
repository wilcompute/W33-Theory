# Receipt consumption survives owner restart

The previous owner (`5e478c7b0`, `w33_process_microstep_owner.py`) consumes
process-bound receipts in memory. Restarting it loses that authoritative head.
The new `w33_durable_microstep_owner.py` stores each head **together with every
bit needed to resume it** in one SQLite transaction. Persisting only an identity
would preserve neither the bytes nor the consumed-receipt boundary.

Fresh GitKraken fetches found no parallel commits beyond W33 `5e478c7b0` or
Holotrade `a104478`. Corpus searches found no earlier analysis implementation
using `BEGIN IMMEDIATE` or `sqlite3.connect`. This is an integration of existing
VM objects and standard database transactions, not a new persistence theorem.
Full historical and recursive manuscript reading remains incomplete.

## Storage and execution contract

The database binds the program image and portal layout. Each process row holds
a content digest and canonical JSON containing its parent descriptor, tick
ordinal, microhistory, existing zipper checkpoint and optional committed child.
The zipper checkpoint retains the complete live bit closure, including stack
and partial result. Reads check the envelope digest, process identity, exact
closure and parent/control relationship; a committed child must equal the
existing micro-owner's derived result.

`submit` starts `BEGIN IMMEDIATE`, reads the authoritative row after acquiring
the writer lock, checks the process-bound receipt with the existing verifier,
and updates the complete snapshot before committing. It never relies on a
cached head from a previous read. `commit` publishes the final child in the same
way. `start` requires that child's exact continuation identity before starting
the next instruction. Independent connections therefore cannot both consume
the same expected cursor. The connection itself is not shared across threads.

The reference uses SQLite rollback-journal mode (`DELETE`) and `synchronous=FULL`.
SQLite supplies the atomicity and recovery mechanism; the VM supplies the
record, exact closure, semantic checks and receipt-consumption rule. See
[SQLite transactions](https://www.sqlite.org/lang_transaction.html) and
[SQLite atomic commit and its filesystem assumptions](https://www.sqlite.org/atomiccommit.html).

## Process-death experiment

Pause DEC on `2^16` after eight ticks, then submit the next receipt from a
separate Python process that terminates with `os._exit(73)` at a test hook:

| Termination point | Recovered tick | Retrying that receipt | Completion |
| --- | ---: | --- | --- |
| Updated SQL row, before COMMIT | 8 | Accepted once | 35 ticks, value 65535 |
| After COMMIT, before returning | 9 | Rejected | 35 ticks, value 65535 |

Both scenarios then terminate another worker after the final macro COMMIT but
before its reply. The recovered child is intact, and a second macro commit is
rejected. The old microreceipt also rejects after starting the next instruction.
These are four actual subprocess exits, not exceptions standing in for death.

Five new tests pass. Besides the exit cases, they cover 18 independent
carrier/operation/value macro comparisons with a reopen after every microtick;
a synchronized two-connection race with one accepted and one rejected submit;
wrong program/layout and record corruption; and an injected exception that
rolls back the whole snapshot. Seven existing in-memory owner tests also pass.
`w33_durable_microstep_owner_certificate.json` records the observed exit-case
values and the test result, without timing-dependent fields.

## Limits that remain explicit

The database is trusted authority. Restoring an old valid database can replay
old work; resisting that requires an independently trusted monotonic anchor.
An attacker who rewrites both a record and its digest is outside this model.
No external I/O is committed here, so this is not an exactly-once payment,
message-delivery or hardware-action protocol.

Each tick serializes a full closure. This is deliberately expensive: the inner
arithmetic still opens at most one bit, but database reads/writes, hash work,
checkpoint size and transaction duration are not constant. Stored snapshots
have a 32 MB envelope limit and inherit the checkpoint's 100,000-node limit.
This adapter does not yet share snapshots through the existing STRONG registry
or budget them through joint admission. Those policies need an explicit bridge.

The tests terminate processes at transaction boundaries. They do not test a
physical power cut, a torn disk sector, a network filesystem or faulty fsync.
Durability relies on SQLite and the platform meeting their documented contract.

```sh
python tests/test_w33_durable_microstep_owner.py --certificate
python tests/test_w33_process_microstep_owner.py
```
