"""Serialized owner for process-bound, reusable counter microproofs.

The trusted owner consumes each expected cursor once. It is not a signature,
durable transaction, thread-safe service, or exactly-once external-I/O protocol.
Forks may reuse an inner arithmetic proof but need different outer bindings.
"""
from dataclasses import asdict, dataclass, replace
import json

import w33_counter_zipper_microcode as micro
import w33_holovm_process_kernel as process
from w33_merkle_capability_memory import digest


@dataclass(frozen=True)
class Cursor:
    parent: process.ProcessContinuation
    control: micro.MicroState
    ticks: int
    history: str

    def __post_init__(self):
        if self.control.base != self.parent.state or self.control.fibre != self.parent.fibre:
            raise ValueError("microstate does not belong to parent process")
        if type(self.ticks) is not int or self.ticks < 0 or not process._is_digest(self.history):
            raise ValueError("invalid microstep ordinal or history")

    @property
    def identity(self):
        return digest({"schema": "w33.process-microcursor.v1",
                       "parent": self.parent.continuation_id,
                       "control": self.control.identity,
                       "ticks": self.ticks, "history": self.history})


@dataclass(frozen=True)
class Receipt:
    expected_cursor: str
    inner: micro.MicroReceipt

    def to_json(self):
        return json.dumps({"schema": "w33.process-microreceipt.v1",
                           "expected_cursor": self.expected_cursor,
                           "inner": json.loads(self.inner.to_json())},
                          sort_keys=True, separators=(",", ":"))

    @classmethod
    def from_json(cls, wire):
        row = json.loads(wire)
        if (type(row) is not dict or set(row) != {"schema", "expected_cursor", "inner"}
                or row["schema"] != "w33.process-microreceipt.v1"
                or not process._is_digest(row["expected_cursor"])):
            raise ValueError("invalid process microreceipt envelope")
        return cls(row["expected_cursor"], micro.MicroReceipt.from_json(json.dumps(row["inner"])))

    @property
    def identity(self):
        return digest(json.loads(self.to_json()))


def begin(program, parent, *, portals=None):
    control = micro.start(program, parent.state, parent.fibre, portals=portals)
    history = digest({"schema": "w33.process-microhistory.v1", "event": "begin",
                      "previous": parent.history_root, "parent": parent.continuation_id})
    return Cursor(parent, control, 0, history)


def prove(program, cursor, memory, *, portals=None):
    return Receipt(cursor.identity, micro.prove_tick(program, cursor.control, memory, portals=portals))


def verify(program, expected, receipt, *, portals=None):
    """Pure verification; the caller must separately consume its trusted head."""
    if type(receipt) is not Receipt or receipt.expected_cursor != expected.identity:
        raise ValueError("stale or foreign process cursor")
    control, writes = micro.verify_tick(program, expected.control, receipt.inner, portals=portals)
    history = digest({"schema": "w33.process-microhistory.v1", "event": "tick",
                      "previous": expected.history, "receipt": receipt.identity})
    return replace(expected, control=control, ticks=expected.ticks + 1, history=history), writes


def finish(program, cursor, *, portals=None):
    """Derive a child only from an owner-trusted, verified DONE cursor."""
    state = micro.committed(program, cursor.control, portals=portals)
    if cursor.ticks == 0:
        raise ValueError("no verified microsteps")
    parent = cursor.parent
    event = {"schema": "w33.process-microcommit.v1", "parent": parent.continuation_id,
             "cursor": cursor.identity, "state": asdict(state)}
    return replace(parent, state=state, generation=parent.generation + 1,
                   parent=parent.continuation_id, history_root=digest(event),
                   last_receipt=digest({"schema": "w33.process-microtrace.v1",
                                        "ticks": cursor.ticks, "history": cursor.history}))


class Owner:
    """Single serialized trusted owner; immutable data may be shared by workers.

    Rejection leaves the process/head unchanged. A storage exception can leave
    unreachable immutable bit nodes, but cannot publish a new execution head.
    Callers must serialize calls and protect these dictionaries from workers.
    """
    def __init__(self, program, memory, *, portals=None):
        self.program, self.memory, self.portals = program, memory, portals
        self.processes = {}
        self.inflight = {}

    def install(self, parent):
        if parent.process_id in self.processes:
            raise ValueError("process already installed")
        begin(self.program, parent, portals=self.portals)  # admission before publication
        self.processes[parent.process_id] = parent

    def start(self, process_id):
        if process_id in self.inflight:
            raise ValueError("instruction already in flight")
        cursor = begin(self.program, self.processes[process_id], portals=self.portals)
        self.inflight[process_id] = cursor
        return cursor

    def submit(self, process_id, receipt):
        expected = self.inflight[process_id]
        after, writes = verify(self.program, expected, receipt, portals=self.portals)
        for node in writes:
            self.memory.put(node)
        self.inflight[process_id] = after
        return after

    def commit(self, process_id, expected_cursor):
        cursor = self.inflight[process_id]
        if cursor.identity != expected_cursor:
            raise ValueError("stale process commit")
        if self.processes[process_id] != cursor.parent:
            raise ValueError("parent process changed during instruction")
        child = finish(self.program, cursor, portals=self.portals)
        self.processes[process_id] = child
        del self.inflight[process_id]
        return child


def experiment():
    """Fan out arithmetic proofs while independently checking the macro result."""
    from w33_authenticated_counter_machine import BitStore, genesis, prove_step, verify_step
    from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
    from w33_typed_universal_microvm import Instruction, Program
    program = Program((Instruction("INC", 0, 1), Instruction("HALT")), name="micro-fanout")
    memory = BitStore()
    state = genesis(program, memory, (255, 0), session="micro-fanout")
    oracle = BitStore(memory.nodes.values())
    expected, _ = verify_step(program, state, prove_step(program, state, oracle))
    parent = process.spawn(state, FibreProductAddress(7, 2, 5), digest("demo-passport"))
    forks = [process.fork(parent, f"fork-{i}") for i in range(8)]
    owner = Owner(program, memory)
    for child in forks:
        owner.install(child)
        owner.start(child.process_id)
    proofs, submissions, duplicate_rejections = 0, 0, 0
    while owner.inflight[forks[0].process_id].control.phase != "DONE":
        first = owner.inflight[forks[0].process_id]
        inner = prove(program, first, memory).inner
        proofs += 1
        for child in forks:
            cursor = owner.inflight[child.process_id]
            envelope = Receipt.from_json(Receipt(cursor.identity, inner).to_json())
            owner.submit(child.process_id, envelope)
            submissions += 1
            try:
                owner.submit(child.process_id, envelope)
            except ValueError:
                duplicate_rejections += 1
    children = [owner.commit(p.process_id, owner.inflight[p.process_id].identity) for p in forks]
    checks = {
        "all_children_match_independent_macro_oracle": all(x.state == expected for x in children),
        "all_histories_distinct": len({x.history_root for x in children}) == len(forks),
        "all_continuations_distinct": len({x.continuation_id for x in children}) == len(forks),
        "all_duplicate_submissions_rejected": duplicate_rejections == submissions,
        "one_proof_per_tick_serves_every_fork": submissions == proofs * len(forks),
        "all_microheads_consumed": not owner.inflight,
    }
    return {"schema": "w33.process-microstep-owner-experiment.v1",
            "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
            "forks": len(forks), "inner_proofs": proofs, "outer_submissions": submissions,
            "duplicate_rejections": duplicate_rejections,
            "result": memory.decode(expected.roots[0]),
            "boundary": "Serialized in-memory owner; no durable or external-I/O exactly-once claim."}


if __name__ == "__main__":
    from pathlib import Path
    result = experiment()
    wire = json.dumps(result, indent=2, sort_keys=True) + "\n"
    Path(__file__).with_name("w33_process_microstep_owner_certificate.json").write_text(wire)
    print(wire, end="")
    raise SystemExit(result["status"] != "PASS")
