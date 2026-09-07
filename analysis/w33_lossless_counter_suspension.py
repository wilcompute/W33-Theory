#!/usr/bin/env python3
"""Lossless suspension of the authenticated counter guest, using existing GC.

The fibre quotient has six preimages per live projection: retain the missing
tag, not just its base. A root authenticates content but does not retain it:
pin a self-contained snapshot STRONG in w33_temporal_merkle_gc.RootRegistry.
This adapter assigns no physical points and makes no boundary-traffic claim.
The caller supplies a trusted expected root and controls handle consumption;
these functions do not provide authorization, distributed leases or consensus.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, fields

from w33_authenticated_counter_machine import Bit, BitStore, State, ZERO, is_root
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_merkle_capability_memory import ContentStore, digest
from w33_temporal_merkle_gc import RootRegistry

SCHEMA = "w33.lossless-counter-suspension.v1"
KIND = "SUSPENDED_COUNTER"


def _budget(limit: int) -> None:
    if type(limit) is not int or limit < 0:
        raise ValueError("node budget must be a natural number")


def reachable(store: BitStore, roots: tuple[str, str], limit: int) -> dict[str, Bit]:
    """Validate and collect the union of both lists without integer decoding."""
    _budget(limit)
    found: dict[str, Bit] = {}
    for root in roots:
        path: set[str] = set()
        while root != ZERO:
            if root in path:
                raise ValueError("cyclic counter memory")
            if root in found:
                break
            if len(found) >= limit:
                raise TimeoutError("snapshot node budget exhausted")
            path.add(root)
            node = store.get(root)
            found[root] = node
            root = node.tail
    return found


def _address(row: dict) -> FibreProductAddress:
    if (type(row) is not dict or set(row) != {f.name for f in fields(FibreProductAddress)}
            or any(type(v) is not int for v in row.values())):
        raise ValueError("invalid fibre address")
    return FibreProductAddress(**row)


def _state(row: dict) -> State:
    if (type(row) is not dict or set(row) != {f.name for f in fields(State)}
            or type(row["roots"]) not in (list, tuple) or len(row["roots"]) != 2):
        raise ValueError("invalid counter state")
    return State(**{**row, "roots": tuple(row["roots"])})


@dataclass(frozen=True)
class SuspensionHandle:
    reference_id: str
    root: str


def suspend(owner: str, state: State, address: FibreProductAddress,
            memory: BitStore, archive: ContentStore, registry: RootRegistry, *,
            max_nodes: int = 100_000) -> SuspensionHandle:
    """Validate first, then archive an immutable-by-digest snapshot and pin it.

    The single archive blob contains all reachable Bit nodes, so the existing
    collector can retain it atomically without interpreting a new node graph.
    This intentionally duplicates bytes across snapshots; cross-snapshot
    chunk sharing requires a separate collector adapter and cost model.
    """
    if type(owner) is not str or not owner:
        raise ValueError("an explicit owner is required")
    state = _state(asdict(state))
    address = _address(asdict(address))
    nodes = reachable(memory, state.roots, max_nodes)
    payload = {
        "schema": SCHEMA, "kind": "counter-suspension",
        "state": {**asdict(state), "roots": list(state.roots)}, "fibre": asdict(address),
        "nodes": [{"root": key, **asdict(nodes[key])} for key in sorted(nodes)],
    }
    root = digest(payload)
    if root in archive.blobs and archive.blobs[root] != payload:
        raise ValueError("archive content collision; previous bytes preserved")
    archive.put(payload)
    ref = registry.pin(KIND, owner, root, "STRONG")
    return SuspensionHandle(ref.reference_id, root)


def resume(handle: SuspensionHandle, expected_root: str, archive: ContentStore,
           registry: RootRegistry, *, max_nodes: int = 100_000
           ) -> tuple[State, FibreProductAddress, BitStore]:
    """Restore only a trusted, still-pinned snapshot; leave the pin intact.

    The owner releases the pin after transferring retention responsibility.
    Reusing a handle is allowed while it remains pinned; replay prevention is
    an owner commit/epoch policy, not a property of content-addressed storage.
    """
    _budget(max_nodes)
    if not is_root(expected_root) or handle.root != expected_root:
        raise ValueError("snapshot does not match the trusted expected root")
    ref = registry.references.get(handle.reference_id)
    if ref is None or (ref.root, ref.kind, ref.strength) != (expected_root, KIND, "STRONG"):
        raise PermissionError("resumption requires a live STRONG suspension pin")
    row = deepcopy(archive.get(expected_root))
    if digest(row) != expected_root:
        raise ValueError("corrupt suspension archive")
    if (type(row) is not dict or set(row) != {"schema", "kind", "state", "fibre", "nodes"}
            or row["schema"] != SCHEMA or row["kind"] != "counter-suspension"):
        raise ValueError("invalid suspension envelope")
    state, address = _state(row["state"]), _address(row["fibre"])
    entries = row["nodes"]
    if type(entries) is not list:
        raise ValueError("invalid snapshot node list")
    if len(entries) > max_nodes:
        raise TimeoutError("snapshot node budget exhausted")
    store = BitStore()
    previous = ""
    for entry in entries:
        if type(entry) is not dict or set(entry) != {"root", "bit", "tail"}:
            raise ValueError("invalid snapshot node")
        node = Bit(entry["bit"], entry["tail"])
        root = entry["root"]
        if not is_root(root) or root <= previous or node.root != root:
            raise ValueError("snapshot nodes must have unique sorted valid identities")
        store.put(node)
        previous = root
    found = reachable(store, state.roots, max_nodes)
    if set(found) != set(store.nodes):
        raise ValueError("snapshot has unreachable extra nodes")
    return state, address, store


def checkpoint_retention_audit(plan) -> dict:
    """Check the new ladder plan against its declared STRONG-root demand.

    This does not certify bytes, capacity, topology, or a reversible schedule.
    It detects the specific demand/strength mismatch before runtime admission.
    """
    required = plan.strong_checkpoints
    strong = sum(a.strength == "STRONG" for a in plan.assignments)
    audit_only = sum(a.strength == "HASH_ONLY" for a in plan.assignments)
    return {
        "required_strong_roots": required,
        "assigned_strong_roots": strong,
        "audit_only_roots": audit_only,
        "retention_demand_met": strong == required and audit_only == 0,
        "runtime_dispatch_certified": False,
    }


def verify() -> dict:
    """Replay a finite worker-loss witness and the complete fibre-tag census."""
    from collections import Counter
    from w33_authenticated_counter_machine import genesis, prove_step, verify_step
    from w33_adaptive_reversible_scheduler import AdaptiveReversibleScheduler
    from w33_ladder_checkpoint_placement import LadderCheckpointPlacer
    from w33_temporal_merkle_gc import TemporalMerkleGC
    from w33_typed_universal_microvm import add_r1_into_r0_program

    program, memory = add_r1_into_r0_program(), BitStore()
    state = genesis(program, memory, (7, 11), session="lossless-suspension-certificate")
    for _ in range(7):
        receipt = prove_step(program, state, memory)
        state, _ = verify_step(program, state, receipt)
    address = FibreProductAddress(17, 2, 5)
    archive, registry = ContentStore(), RootRegistry()
    handle = suspend("guest", state, address, memory, archive, registry)
    archived_nodes = len(archive.get(handle.root)["nodes"])
    memory.nodes.clear()
    TemporalMerkleGC(archive, registry).collect()
    restored, restored_address, fresh = resume(handle, handle.root, archive, registry)
    exact_resume = restored == state and restored_address == address
    for _ in range(100):
        if restored.halted:
            break
        receipt = prove_step(program, restored, fresh)
        restored, _ = verify_step(program, restored, receipt)
    output = [fresh.decode(root) for root in restored.roots]
    registry.pin("RECEIPT", "guest", handle.root, "HASH_ONLY")
    registry.release(handle.reference_id)
    TemporalMerkleGC(archive, registry).collect()
    buckets = Counter(FibreProductAddress.unpack(i).circuit216 for i in range(1296))
    placer = LadderCheckpointPlacer()
    strategy = max(AdaptiveReversibleScheduler(4096, address_depth=5).frontier,
                   key=lambda p: p.recursion_levels)
    overflow = checkpoint_retention_audit(placer.place(strategy))
    checks = {
        "worker_loss_preserves_exact_state_and_fibre_tags": exact_resume,
        "resumed_guest_halts_at_18_0": restored.halted and output == [18, 0],
        "each_live_projection_has_six_missing_tag_choices": len(buckets) == 216 and set(buckets.values()) == {6},
        "hash_only_receipt_does_not_retain_snapshot_bytes": handle.root in registry.audit_roots() and handle.root not in archive.blobs,
        "ladder_overflow_fails_strong_retention_demand": overflow["required_strong_roots"] == 13 and not overflow["retention_demand_met"],
    }
    return {
        "schema": "w33.lossless-counter-suspension-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks, "archived_counter_nodes": archived_nodes,
        "snapshot_step": state.steps, "final_step": restored.steps, "output": output,
        "projection_buckets": len(buckets), "choices_per_live_projection": 6,
        "overflow_plan": overflow,
        "scope": "Finite software recovery witness; no capacity, topology, network-traffic, authorization or quantum-resource certificate.",
    }


if __name__ == "__main__":
    import json
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
