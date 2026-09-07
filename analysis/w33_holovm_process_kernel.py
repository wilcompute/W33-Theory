#!/usr/bin/env python3
"""Content-addressed process/continuation kernel for the W33 HoloVM stack.

The repository already has five independently useful identities:

* an authenticated guest State (semantic/control state),
* a shared snapshot root (recoverable value state),
* an ExecutionPassport root (admitted control/evidence context),
* a fibre-product address (finite machine placement), and
* a RootRegistry reference (retention authority).

This module adds the missing *process* identity without weakening any of them.

A process continuation is an immutable descriptor above a shared snapshot.  Its
content root commits lineage, process id, generation, passport id, semantic
state and fibre placement, while a single Merkle child points at the existing
shared counter snapshot.  Consequently two forks can share every state byte and
still have distinct continuation identities.  Stepping creates a new
continuation from an independently verified authenticated-counter receipt.
Strong roots retain executable bytes; HASH_ONLY roots retain causal identity
without pinning those bytes.

This is software process semantics.  It is not a physical photon lifetime, a
thermodynamic time law, a hardware capability tag, or a claim that finite W33
control contains unbounded storage.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Any

from w33_authenticated_counter_machine import (
    BitStore,
    Receipt,
    State,
    genesis,
    prove_step,
    verify_step,
)
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_merkle_capability_memory import ContentStore, canonical_json, digest
from w33_shared_counter_archive import prepare, _restore
from w33_temporal_merkle_gc import RootRegistry, TemporalMerkleGC
from w33_typed_universal_microvm import Carrier, Program, add_r1_into_r0_program

PROCESS_SCHEMA = "w33.holovm-process-continuation.v1"
PROCESS_KIND = "HOLOVM_PROCESS"
PROCESS_BLOB_SCHEMA = "w33.holovm-process-blob.v1"


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(c in "0123456789abcdef" for c in value[7:])
    )


@dataclass(frozen=True)
class ProcessContinuation:
    """One immutable runnable continuation.

    ``process_id`` is stable across steps of one logical process.
    ``continuation_id`` changes at every fork/step because it hashes the complete
    descriptor. ``parent`` is a causal hash, deliberately *not* a Merkle child:
    retaining a child continuation does not force retention of all ancestor
    bytes.  The history hash preserves ancestry after GC.
    """

    process_id: str
    branch: str
    generation: int
    parent: str | None
    passport_id: str
    state: State
    fibre: FibreProductAddress
    history_root: str
    last_receipt: str | None = None

    def __post_init__(self) -> None:
        if not _is_digest(self.process_id):
            raise ValueError("process id must be content addressed")
        if not isinstance(self.branch, str) or not self.branch:
            raise ValueError("branch label must be nonempty")
        if type(self.generation) is not int or self.generation < 0:
            raise ValueError("generation must be a natural number")
        if self.parent is not None and not _is_digest(self.parent):
            raise ValueError("parent continuation id must be a digest")
        if not _is_digest(self.passport_id) or not _is_digest(self.history_root):
            raise ValueError("passport and history roots must be digests")
        if self.last_receipt is not None and not _is_digest(self.last_receipt):
            raise ValueError("receipt id must be a digest")

    def descriptor(self) -> dict[str, Any]:
        return {
            "schema": PROCESS_SCHEMA,
            "process_id": self.process_id,
            "branch": self.branch,
            "generation": self.generation,
            "parent": self.parent,
            "passport_id": self.passport_id,
            "state": {**asdict(self.state), "roots": list(self.state.roots)},
            "fibre": asdict(self.fibre),
            "history_root": self.history_root,
            "last_receipt": self.last_receipt,
        }

    @property
    def continuation_id(self) -> str:
        return digest(self.descriptor())


@dataclass(frozen=True)
class PreparedProcess:
    root: str
    snapshot_root: str
    blobs: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ProcessHandle:
    reference_id: str
    root: str


def _state(row: object) -> State:
    if type(row) is not dict:
        raise ValueError("invalid process state")
    row = dict(row)
    if type(row.get("roots")) is not list or len(row["roots"]) != 2:
        raise ValueError("process state must contain two counter roots")
    row["roots"] = tuple(row["roots"])
    return State(**row)


def _fibre(row: object) -> FibreProductAddress:
    if type(row) is not dict:
        raise ValueError("invalid process fibre")
    return FibreProductAddress(**row)


def _process(row: object) -> ProcessContinuation:
    if type(row) is not dict or row.get("schema") != PROCESS_SCHEMA:
        raise ValueError("invalid process descriptor")
    expected = {
        "schema", "process_id", "branch", "generation", "parent", "passport_id",
        "state", "fibre", "history_root", "last_receipt",
    }
    if set(row) != expected:
        raise ValueError("unexpected process descriptor fields")
    return ProcessContinuation(
        process_id=row["process_id"],
        branch=row["branch"],
        generation=row["generation"],
        parent=row["parent"],
        passport_id=row["passport_id"],
        state=_state(row["state"]),
        fibre=_fibre(row["fibre"]),
        history_root=row["history_root"],
        last_receipt=row["last_receipt"],
    )


def spawn(state: State, fibre: FibreProductAddress, passport_id: str, *,
          branch: str = "main") -> ProcessContinuation:
    """Create a process identity around an admitted state/passport."""
    if not _is_digest(passport_id):
        raise ValueError("spawn requires the exact validated passport digest")
    process_id = digest({
        "schema": "w33.holovm-process-id.v1",
        "image": state.image,
        "session": state.session,
        "passport_id": passport_id,
        "branch": branch,
    })
    history = digest({
        "schema": "w33.holovm-history-genesis.v1",
        "process_id": process_id,
        "state": {**asdict(state), "roots": list(state.roots)},
        "fibre": asdict(fibre),
        "passport_id": passport_id,
    })
    return ProcessContinuation(
        process_id, branch, 0, None, passport_id, state, fibre, history
    )


def fork(parent: ProcessContinuation, branch: str) -> ProcessContinuation:
    """Fork process identity without copying immutable guest state."""
    if not isinstance(branch, str) or not branch:
        raise ValueError("fork branch must be nonempty")
    process_id = digest({
        "schema": "w33.holovm-fork-id.v1",
        "parent_process": parent.process_id,
        "parent_continuation": parent.continuation_id,
        "branch": branch,
    })
    history = digest({
        "schema": "w33.holovm-history-event.v1",
        "previous": parent.history_root,
        "event": "fork",
        "parent_continuation": parent.continuation_id,
        "child_process": process_id,
        "branch": branch,
    })
    return ProcessContinuation(
        process_id=process_id,
        branch=branch,
        generation=parent.generation + 1,
        parent=parent.continuation_id,
        passport_id=parent.passport_id,
        state=parent.state,
        fibre=parent.fibre,
        history_root=history,
    )


def advance(program: Program, process: ProcessContinuation, memory: BitStore,
            *, max_openings: int = 100_000
            ) -> tuple[ProcessContinuation, Receipt]:
    """Execute one authenticated guest transition and return a new continuation."""
    if process.state.image != program.image_id:
        raise ValueError("process image does not match executable program")
    receipt = prove_step(
        program, process.state, memory, max_openings=max_openings
    )
    after, writes = verify_step(program, process.state, receipt)
    # The prover materialized its proposed writes in ``memory``. Independently
    # reconstructed verifier writes must resolve to the same roots.
    for node in writes:
        memory.put(node)
    history = digest({
        "schema": "w33.holovm-history-event.v1",
        "previous": process.history_root,
        "event": "guest-step",
        "parent_continuation": process.continuation_id,
        "receipt": receipt.receipt_id,
        "post_state": {**asdict(after), "roots": list(after.roots)},
    })
    child = ProcessContinuation(
        process_id=process.process_id,
        branch=process.branch,
        generation=process.generation + 1,
        parent=process.continuation_id,
        passport_id=process.passport_id,
        state=after,
        fibre=process.fibre,
        history_root=history,
        last_receipt=receipt.receipt_id,
    )
    return child, receipt


def prepare_process(process: ProcessContinuation, memory: BitStore,
                    *, max_nodes: int = 100_000) -> PreparedProcess:
    """Wrap one shared value snapshot in one process-specific Merkle node."""
    snapshot = prepare(process.state, process.fibre, memory, max_nodes=max_nodes)
    blobs: dict[str, dict[str, Any]] = {}
    for key, wire in snapshot.blobs:
        row = json.loads(wire)
        if digest(row) != key:
            raise ValueError("corrupt shared snapshot proposal")
        blobs[key] = row
    outer = {
        "kind": "node",
        "value": {
            "schema": PROCESS_BLOB_SCHEMA,
            "process": process.descriptor(),
            "snapshot_root": snapshot.root,
        },
        "children": [[0, snapshot.root]],
    }
    root = digest(outer)
    blobs[root] = outer
    return PreparedProcess(
        root=root,
        snapshot_root=snapshot.root,
        blobs=tuple(
            (key, canonical_json(row).decode())
            for key, row in sorted(blobs.items())
        ),
    )


def _overlay(proposal: PreparedProcess, archive: ContentStore,
             *, max_nodes: int) -> tuple[ContentStore, ProcessContinuation]:
    if not isinstance(proposal, PreparedProcess):
        raise ValueError("invalid process proposal")
    view = ContentStore()
    view.blobs = dict(archive.blobs)
    keys: set[str] = set()
    for key, wire in proposal.blobs:
        row = json.loads(wire)
        if key in keys or digest(row) != key:
            raise ValueError("duplicate or corrupt proposed process blob")
        if key in view.blobs and view.blobs[key] != row:
            raise ValueError("content collision with process archive")
        keys.add(key)
        view.blobs[key] = row

    outer = view.get(proposal.root)
    if (
        type(outer) is not dict
        or set(outer) != {"kind", "value", "children"}
        or outer["kind"] != "node"
        or outer["children"] != [[0, proposal.snapshot_root]]
    ):
        raise ValueError("invalid process root")
    value = outer["value"]
    if (
        type(value) is not dict
        or set(value) != {"schema", "process", "snapshot_root"}
        or value["schema"] != PROCESS_BLOB_SCHEMA
        or value["snapshot_root"] != proposal.snapshot_root
    ):
        raise ValueError("invalid process root value")
    process = _process(value["process"])
    state, fibre, _, _ = _restore(proposal.snapshot_root, view, max_nodes)
    if state != process.state or fibre != process.fibre:
        raise ValueError("process descriptor disagrees with recoverable snapshot")

    # A proposal is self-contained: exactly the closure of its process root.
    temporary = RootRegistry()
    temporary.pin(PROCESS_KIND, "proposal-validation", proposal.root, "STRONG")
    closure = set(TemporalMerkleGC(view, temporary).plan()["marked"])
    if closure != keys:
        raise ValueError("process proposal must contain exactly its reachable closure")
    return view, process


def retained_payload_bytes(store: ContentStore, keys: set[str]) -> int:
    return sum(len(canonical_json(store.blobs[key])) for key in keys)


def install(owner: str, proposal: PreparedProcess, archive: ContentStore,
            registry: RootRegistry, *, max_payload_bytes: int,
            max_nodes: int = 100_000) -> ProcessHandle:
    """Atomically admit one process root against the complete strong-root union."""
    if not isinstance(owner, str) or not owner:
        raise ValueError("process owner must be nonempty")
    if type(max_payload_bytes) is not int or max_payload_bytes < 0:
        raise ValueError("invalid process payload budget")
    view, _ = _overlay(proposal, archive, max_nodes=max_nodes)

    future = RootRegistry()
    future.references = dict(registry.references)
    ref = future.pin(PROCESS_KIND, owner, proposal.root, "STRONG")
    plan = TemporalMerkleGC(view, future).plan()
    marked = set(plan["marked"])
    if retained_payload_bytes(view, marked) > max_payload_bytes:
        raise MemoryError("retained process union exceeds payload budget")

    retained = {key: view.blobs[key] for key in marked}
    archive.blobs.clear()
    archive.blobs.update(retained)
    registry.references[ref.reference_id] = ref
    return ProcessHandle(ref.reference_id, proposal.root)


def resume_process(handle: ProcessHandle, expected_root: str,
                   archive: ContentStore, registry: RootRegistry,
                   *, max_nodes: int = 100_000
                   ) -> tuple[ProcessContinuation, BitStore]:
    if handle.root != expected_root:
        raise ValueError("wrong trusted process root")
    ref = registry.references.get(handle.reference_id)
    if ref is None or (
        ref.root, ref.kind, ref.strength
    ) != (expected_root, PROCESS_KIND, "STRONG"):
        raise PermissionError("live strong process authority required")
    outer = archive.get(expected_root)
    value = outer.get("value")
    if (
        outer.get("kind") != "node"
        or type(value) is not dict
        or value.get("schema") != PROCESS_BLOB_SCHEMA
        or value.get("snapshot_root") is None
    ):
        raise ValueError("corrupt process root")
    process = _process(value["process"])
    state, fibre, memory, _ = _restore(
        value["snapshot_root"], archive, max_nodes
    )
    if state != process.state or fibre != process.fibre:
        raise ValueError("process root no longer matches recoverable state")
    return process, memory


def verify() -> dict[str, Any]:
    """Executable witness for process/value separation and causal GC semantics."""
    program = add_r1_into_r0_program()
    memory = BitStore()
    state = genesis(
        program, memory, (255, 0), session="holovm-process-kernel"
    )
    fibre = FibreProductAddress(7, 2, 5)
    passport = digest({
        "schema": "w33.process-kernel-demo-passport.v1",
        "image": program.image_id,
        "carrier": Carrier.CIRCUIT_ST81.value,
    })
    root = spawn(state, fibre, passport)
    left = fork(root, "left")
    right = fork(root, "right")

    value_left = prepare(left.state, left.fibre, memory)
    value_right = prepare(right.state, right.fibre, memory)
    proc_left = prepare_process(left, memory)
    proc_right = prepare_process(right, memory)

    left_map = dict(proc_left.blobs)
    right_map = dict(proc_right.blobs)
    union = {**left_map, **right_map}
    left_bytes = sum(len(w.encode()) for w in left_map.values())
    union_bytes = sum(len(w.encode()) for w in union.values())
    fork_marginal = union_bytes - left_bytes
    right_outer_bytes = len(right_map[proc_right.root].encode())

    archive, registry = ContentStore(), RootRegistry()
    h_left = install(
        "left", proc_left, archive, registry, max_payload_bytes=10**9
    )
    h_right = install(
        "right", proc_right, archive, registry, max_payload_bytes=10**9
    )
    live_left, mem_left = resume_process(
        h_left, h_left.root, archive, registry
    )
    live_right, _ = resume_process(
        h_right, h_right.root, archive, registry
    )

    stepped, receipt = advance(program, live_left, mem_left)
    stepped_again, receipt_again = advance(
        program, live_left, BitStore(mem_left.nodes.values())
    )
    deterministic_step = (
        stepped == stepped_again
        and receipt.receipt_id == receipt_again.receipt_id
    )
    proc_stepped = prepare_process(stepped, mem_left)
    h_stepped = install(
        "left-next", proc_stepped, archive, registry, max_payload_bytes=10**9
    )

    # Retain only the causal hash of the old continuation, not its executable
    # bytes. The child descriptor stores parent/history as values, not Merkle
    # child edges, so releasing the old strong root makes those bytes collectible.
    audit = registry.pin("HOLOVM_AUDIT", "left-old", h_left.root, "HASH_ONLY")
    registry.release(h_left.reference_id)
    gc = TemporalMerkleGC(archive, registry).collect()
    right_after_gc, right_mem_after_gc = resume_process(
        h_right, h_right.root, archive, registry
    )
    next_after_gc, next_mem_after_gc = resume_process(
        h_stepped, h_stepped.root, archive, registry
    )

    checks = {
        "forks_share_exact_semantic_state": (
            left.state == right.state == root.state
            and left.state.roots == right.state.roots
        ),
        "forks_have_distinct_process_and_continuation_ids": (
            left.process_id != right.process_id
            and left.continuation_id != right.continuation_id
        ),
        "value_snapshot_intentionally_deduplicates_forks": (
            value_left.root == value_right.root
        ),
        "process_snapshot_keeps_forks_distinct": (
            proc_left.root != proc_right.root
        ),
        "fork_marginal_is_exactly_one_process_descriptor": (
            fork_marginal == right_outer_bytes
            and fork_marginal < left_bytes
        ),
        "two_process_roots_share_one_value_closure": (
            proc_left.snapshot_root == proc_right.snapshot_root
        ),
        "strong_process_roots_resume_exactly": (
            live_left == left and live_right == right
        ),
        "authenticated_step_is_deterministic": deterministic_step,
        "step_preserves_process_id_but_changes_continuation": (
            stepped.process_id == left.process_id
            and stepped.continuation_id != left.continuation_id
            and stepped.parent == left.continuation_id
            and stepped.last_receipt == receipt.receipt_id
        ),
        "guest_step_uses_w33_route_of_at_most_two_hops": (
            len(receipt.route) - 1 <= 2
        ),
        "released_ancestor_bytes_are_collectible": (
            h_left.root not in archive.blobs
            and audit.root in registry.audit_roots()
            and gc["collected"] >= 1
        ),
        "sibling_survives_ancestor_collection": (
            right_after_gc == right
            and right_mem_after_gc.decode(right.state.roots[0]) == 255
        ),
        "descendant_survives_ancestor_collection": (
            next_after_gc == stepped
            and next_mem_after_gc.decode(stepped.state.roots[0]) == 255
        ),
    }
    return {
        "schema": "w33.holovm-process-kernel-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "process_model": {
            "value_snapshot_root": value_left.root,
            "left_process_root": proc_left.root,
            "right_process_root": proc_right.root,
            "stepped_process_root": proc_stepped.root,
            "left_process_id": left.process_id,
            "right_process_id": right.process_id,
            "stable_left_process_id_after_step": stepped.process_id,
            "receipt_id": receipt.receipt_id,
        },
        "payload": {
            "one_fork_bytes": left_bytes,
            "two_forks_union_bytes": union_bytes,
            "second_fork_marginal_bytes": fork_marginal,
            "second_fork_outer_descriptor_bytes": right_outer_bytes,
        },
        "causality": {
            "root_generation": root.generation,
            "fork_generation": left.generation,
            "stepped_generation": stepped.generation,
            "ancestor_hash_retained_as_audit": audit.root,
            "ancestor_executable_blob_retained": h_left.root in archive.blobs,
        },
        "virtual_hardware": {
            "vcpu": "prove_step + store-free verify_step authenticated transition engine",
            "register_file": "pc, portal, two authenticated roots, generation, history root",
            "mmu": "base-40 W33 Merkle capability ISA (existing module)",
            "interconnect": "W(3,3) diameter-two route certificate",
            "placement": "36 x 6 x 6 finite fibre-product coordinate",
            "process_table": "STRONG content roots in RootRegistry",
            "swap_checkpoint": "shared immutable snapshot DAG",
            "fork": "one new process descriptor over shared value closure",
            "forget": "release STRONG root; keep optional HASH_ONLY causal identity",
        },
        "interpretation": (
            "The runnable VM is naturally an immutable continuation graph: "
            "execution allocates a child state, fork allocates a process descriptor, "
            "and GC is the explicit operation that forgets executable history."
        ),
        "honesty_boundary": (
            "Payload byte counts cover canonical JSON blobs only. This is software "
            "process semantics, not a hardware process implementation, physical "
            "thermodynamic law, or proof that one finite device has unbounded memory."
        ),
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2, sort_keys=True))
    raise SystemExit(payload["status"] != "PASS")
