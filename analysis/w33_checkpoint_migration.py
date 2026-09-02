#!/usr/bin/env python3
"""Typed checkpoint/migration semantics for the two inequivalent W33 carriers.

There are deliberately two different operations:

1. FULL CHECKPOINT / RESTORE is same-carrier only.  It preserves the complete
   VM state, private six-state fibre coordinate, and memory root.
2. NEUTRAL CONTINUATION is an application-level handoff at an explicit syscall
   safe point.  It may cross the ST81/ST64 fork, but carries only classical guest
   state plus the common base36 address and immutable shared-object identities.
   The target gets a fresh carrier-local fibre tag and a new trace lineage.

Thus cross-carrier continuation is not a gauge transform and not quantum-state
migration between the inequivalent 81- and 64-dimensional modules.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any

from w33_heterogeneous_36_ipc import FiberEndpoint
from w33_merkle_capability_memory import PersistentMemory
from w33_typed_universal_microvm import (
    Capability,
    Carrier,
    Program,
    TypedUniversalMicroVM,
    digest as vm_digest,
)


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def logical_dim(carrier: Carrier) -> int:
    return 81 if carrier == Carrier.CIRCUIT_ST81 else 64


@dataclass(frozen=True)
class FullCheckpoint:
    image_id: str
    carrier: str
    logical_dimension: int
    pc: int
    counters: tuple[int, int]
    portal: int
    halted: bool
    steps: int
    trace_root: str
    memory_root: str
    endpoint_state216: int

    @property
    def checkpoint_id(self) -> str:
        return digest(asdict(self))


@dataclass(frozen=True)
class NeutralContinuation:
    image_id: str
    source_carrier: str
    base36: int
    pc: int
    counters: tuple[int, int]
    guest_steps: int
    shared_roots: tuple[str, ...]
    safe_point: str = "SYSCALL_BOUNDARY"

    @property
    def continuation_id(self) -> str:
        return digest(asdict(self))


def full_checkpoint(vm: TypedUniversalMicroVM, memory: PersistentMemory,
                    endpoint: FiberEndpoint) -> FullCheckpoint:
    if vm.state.capability.carrier != memory.machine_type or endpoint.carrier != memory.machine_type:
        raise ValueError("VM, memory and endpoint carrier must agree")
    return FullCheckpoint(
        image_id=vm.program.image_id,
        carrier=vm.state.capability.carrier.value,
        logical_dimension=vm.state.capability.logical_dimension,
        pc=vm.state.pc,
        counters=tuple(vm.state.counters()),
        portal=vm.state.portal,
        halted=vm.state.halted,
        steps=vm.state.steps,
        trace_root=vm.state.trace_root,
        memory_root=memory.root,
        endpoint_state216=endpoint.state216,
    )


def restore_full(checkpoint: FullCheckpoint, program: Program, memory: PersistentMemory,
                 target_carrier: Carrier) -> tuple[TypedUniversalMicroVM, FiberEndpoint]:
    if checkpoint.image_id != program.image_id:
        raise ValueError("checkpoint program image mismatch")
    if checkpoint.carrier != target_carrier.value:
        raise PermissionError("full checkpoint cannot cross the inequivalent 216-carrier fork")
    if memory.machine_type != target_carrier or memory.root != checkpoint.memory_root:
        raise ValueError("memory snapshot does not match full checkpoint")
    vm = TypedUniversalMicroVM(program, Capability(target_carrier, logical_dim(target_carrier)))
    vm.state.pc = checkpoint.pc
    vm.state.set_counters(checkpoint.counters)
    vm.state.portal = checkpoint.portal
    vm.state.halted = checkpoint.halted
    vm.state.steps = checkpoint.steps
    vm.state.trace_root = checkpoint.trace_root
    return vm, FiberEndpoint(target_carrier, checkpoint.endpoint_state216)


def export_neutral(vm: TypedUniversalMicroVM, endpoint: FiberEndpoint,
                   shared_roots: tuple[str, ...], safe_point: str = "SYSCALL_BOUNDARY") -> NeutralContinuation:
    if endpoint.carrier != vm.state.capability.carrier:
        raise ValueError("endpoint and VM carrier mismatch")
    if safe_point != "SYSCALL_BOUNDARY":
        raise PermissionError("cross-carrier continuation is allowed only at an explicit neutral syscall boundary")
    return NeutralContinuation(
        image_id=vm.program.image_id,
        source_carrier=vm.state.capability.carrier.value,
        base36=endpoint.base36,
        pc=vm.state.pc,
        counters=tuple(vm.state.counters()),
        guest_steps=vm.state.steps,
        shared_roots=tuple(shared_roots),
    )


def resume_neutral(cont: NeutralContinuation, program: Program, target_carrier: Carrier,
                   fresh_private_tag6: int) -> tuple[TypedUniversalMicroVM, FiberEndpoint, str]:
    if cont.image_id != program.image_id:
        raise ValueError("continuation program image mismatch")
    if cont.safe_point != "SYSCALL_BOUNDARY":
        raise PermissionError("continuation is not at a neutral safe point")
    if not 0 <= fresh_private_tag6 < 6:
        raise ValueError("fresh private tag must lie in 0..5")
    vm = TypedUniversalMicroVM(program, Capability(target_carrier, logical_dim(target_carrier)))
    vm.state.pc = cont.pc
    vm.state.set_counters(cont.counters)
    vm.state.steps = cont.guest_steps
    vm.state.portal = cont.base36
    lineage = digest({
        "resume_from": cont.continuation_id,
        "target_carrier": target_carrier.value,
        "target_logical_dimension": logical_dim(target_carrier),
    })
    vm.state.trace_root = lineage
    endpoint = FiberEndpoint(target_carrier, 6 * cont.base36 + fresh_private_tag6)
    return vm, endpoint, lineage


def verify() -> dict[str, Any]:
    from w33_typed_universal_microvm import add_r1_into_r0_program
    from w33_merkle_capability_memory import ContentStore, MemoryCapability

    program = add_r1_into_r0_program()
    vm81 = TypedUniversalMicroVM(program, Capability(Carrier.CIRCUIT_ST81, 81))
    vm81.state.counter0, vm81.state.counter1 = 7, 3
    vm81.step(); vm81.step()
    endpoint81 = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 7 + 2)
    store = ContentStore()
    cap81 = MemoryCapability(Carrier.CIRCUIT_ST81)
    mem81 = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81).write(cap81, (7, 1), {"shared": "checkpoint"})

    cp = full_checkpoint(vm81, mem81, endpoint81)
    restored, restored_endpoint = restore_full(cp, program, mem81, Carrier.CIRCUIT_ST81)

    cross_full_blocked = False
    try:
        restore_full(cp, program, mem81, Carrier.PAIR_ST64)
    except PermissionError:
        cross_full_blocked = True

    cont = export_neutral(vm81, endpoint81, (store.subtree(mem81.root, (7,)) or "",))
    vm64, endpoint64, lineage = resume_neutral(cont, program, Carrier.PAIR_ST64, fresh_private_tag6=5)

    descriptor = json.dumps(asdict(cont), sort_keys=True)
    checks = {
        "same_carrier_full_restore_exact_guest": restored.state.pc == vm81.state.pc and restored.state.counters() == vm81.state.counters(),
        "same_carrier_private_fibre_restored": restored_endpoint.state216 == endpoint81.state216,
        "same_carrier_trace_preserved": restored.state.trace_root == vm81.state.trace_root,
        "cross_carrier_full_restore_rejected": cross_full_blocked,
        "neutral_continuation_preserves_classical_guest": vm64.state.pc == vm81.state.pc and vm64.state.counters() == vm81.state.counters(),
        "neutral_continuation_preserves_common_base": endpoint64.base36 == endpoint81.base36 == 7,
        "target_private_fibre_is_fresh": endpoint64.private_tag6 == 5 and endpoint64.private_tag6 != endpoint81.private_tag6,
        "target_has_new_carrier_identity": vm64.state.capability.carrier == Carrier.PAIR_ST64 and vm64.state.capability.logical_dimension == 64,
        "trace_lineage_restarts": lineage == vm64.state.trace_root and lineage != vm81.state.trace_root,
        "neutral_descriptor_has_no_private_fibre": "private_tag6" not in descriptor and "state216" not in descriptor,
    }
    return {
        "schema": "w33.checkpoint-migration.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "full_checkpoint": cp.checkpoint_id,
        "neutral_continuation": cont.continuation_id,
        "checks": checks,
        "interpretation": "Full machine migration is same-carrier only. Cross-carrier handoff is a new machine instance rehydrated from carrier-neutral classical state at a typed safe point.",
        "quantum_boundary": "No ST81 quantum state is converted into an ST64 quantum state or vice versa.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
