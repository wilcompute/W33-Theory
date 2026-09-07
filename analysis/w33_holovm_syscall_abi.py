#!/usr/bin/env python3
"""Executable syscall ABI for the content-addressed W33 HoloVM.

This module turns the process-continuation kernel into a small host interface:

  ADMIT   validate/register one program and retain a genesis continuation
  RUN     resume a trusted continuation and execute finite fuel
  EMIT    commit a receipt chain and child continuation identity
  FORK    allocate a new process lineage above shared immutable state
  PIN     add retention or hash-only authority
  RELEASE remove one authority reference
  RESUME  materialize an exact retained continuation
  YIELD   export carrier-neutral classical continuation state at a safe point

The ABI intentionally does not make the worker itself the VM.  A worker is a
replay engine over immutable continuation roots.  Process state survives worker
replacement because it is content addressed and independently verifiable.

`YIELD` is not quantum-state migration.  It exports only the classical guest
state, common base-36 placement coordinate and immutable identities.  Rehydrating
that yield on another carrier creates a new carrier-local process identity.

The Wasm certificate at the bottom uses the repository's existing validated,
invocation-specialising Wasm trace compiler.  It therefore proves an end-to-end
path for those completed validated invocations; it is not a static all-input
compiler for arbitrary WebAssembly.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import json
from typing import Any

from w33_authenticated_counter_machine import BitStore, State, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_process_kernel import (
    PROCESS_KIND,
    ProcessContinuation,
    ProcessHandle,
    advance,
    fork as fork_process,
    install,
    prepare_process,
    resume_process,
    spawn,
)
from w33_merkle_capability_memory import ContentStore, digest
from w33_temporal_merkle_gc import RootRegistry, TemporalMerkleGC
from w33_typed_universal_microvm import Carrier, Program

ABI_SCHEMA = "w33.holovm-syscall-abi.v1"
YIELD_SCHEMA = "w33.holovm-neutral-yield.v1"
EMISSION_SCHEMA = "w33.holovm-emission.v1"


def _is_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 71
        and value.startswith("sha256:")
        and all(c in "0123456789abcdef" for c in value[7:])
    )


@dataclass(frozen=True)
class Emission:
    parent_root: str
    child_root: str
    process_id: str
    generation: int
    receipt_ids: tuple[str, ...]
    halted: bool
    stop_reason: str

    @property
    def emission_id(self) -> str:
        return digest({"schema": EMISSION_SCHEMA, **asdict(self)})


@dataclass(frozen=True)
class RunResult:
    handle: ProcessHandle
    process: ProcessContinuation
    emission: Emission


@dataclass(frozen=True)
class NeutralYield:
    source_process_id: str
    source_continuation: str
    source_carrier: str
    passport_id: str
    image: str
    layout: str
    session: str
    roots: tuple[str, str]
    pc: int
    steps: int
    portal: int
    halted: bool
    base36: int
    generation: int
    history_root: str
    safe_point: str = "SYSCALL_BOUNDARY"

    @property
    def yield_id(self) -> str:
        return digest({"schema": YIELD_SCHEMA, **asdict(self)})


class HoloVMKernel:
    """Owner-serialized reference host for immutable HoloVM continuations."""

    def __init__(self) -> None:
        self.archive = ContentStore()
        self.registry = RootRegistry()
        self.programs: dict[str, Program] = {}
        self.events: list[dict[str, Any]] = []

    def _event(self, op: str, payload: dict[str, Any]) -> str:
        body = {
            "schema": "w33.holovm-kernel-event.v1",
            "sequence": len(self.events),
            "op": op,
            "payload": payload,
        }
        body["event_id"] = digest(body)
        self.events.append(body)
        return body["event_id"]

    def register_program(self, program: Program) -> None:
        previous = self.programs.get(program.image_id)
        if previous is not None and previous != program:
            raise ValueError("image id collision in program registry")
        self.programs[program.image_id] = program

    def ADMIT(
        self,
        owner: str,
        program: Program,
        state: State,
        memory: BitStore,
        fibre: FibreProductAddress,
        passport_id: str,
        *,
        max_payload_bytes: int = 10**9,
    ) -> ProcessHandle:
        """Admit a concrete genesis state under an exact passport identity."""
        if state.image != program.image_id:
            raise ValueError("ADMIT program/state image mismatch")
        if not _is_digest(passport_id):
            raise ValueError("ADMIT requires a canonical passport digest")
        self.register_program(program)
        process = spawn(state, fibre, passport_id)
        proposal = prepare_process(process, memory)
        handle = install(
            owner,
            proposal,
            self.archive,
            self.registry,
            max_payload_bytes=max_payload_bytes,
        )
        self._event("ADMIT", {
            "owner": owner,
            "root": handle.root,
            "process_id": process.process_id,
            "generation": process.generation,
            "passport_id": passport_id,
        })
        return handle

    def RESUME(self, handle: ProcessHandle) -> tuple[ProcessContinuation, BitStore]:
        process, memory = resume_process(
            handle, handle.root, self.archive, self.registry
        )
        self._event("RESUME", {
            "root": handle.root,
            "process_id": process.process_id,
            "generation": process.generation,
        })
        return process, memory

    def RUN(
        self,
        handle: ProcessHandle,
        *,
        fuel: int,
        owner: str | None = None,
        max_openings: int = 100_000,
        max_payload_bytes: int = 10**9,
    ) -> RunResult:
        """Execute at most ``fuel`` verified guest transitions from one root."""
        if type(fuel) is not int or fuel < 0:
            raise ValueError("RUN fuel must be a natural number")
        process, memory = self.RESUME(handle)
        program = self.programs.get(process.state.image)
        if program is None:
            raise KeyError("RUN has no registered program for continuation image")
        parent_root = handle.root
        receipts = []
        current = process
        for _ in range(fuel):
            if current.state.halted:
                break
            current, receipt = advance(
                program, current, memory, max_openings=max_openings
            )
            receipts.append(receipt)

        proposal = prepare_process(current, memory)
        child = install(
            owner or f"run:{current.process_id}:{current.generation}",
            proposal,
            self.archive,
            self.registry,
            max_payload_bytes=max_payload_bytes,
        )
        stop_reason = "halted" if current.state.halted else "fuel-exhausted"
        emission = Emission(
            parent_root=parent_root,
            child_root=child.root,
            process_id=current.process_id,
            generation=current.generation,
            receipt_ids=tuple(r.receipt_id for r in receipts),
            halted=current.state.halted,
            stop_reason=stop_reason,
        )
        self._event("RUN", {
            "parent_root": parent_root,
            "child_root": child.root,
            "fuel": fuel,
            "executed": len(receipts),
            "emission_id": emission.emission_id,
            "stop_reason": stop_reason,
        })
        return RunResult(child, current, emission)

    def EMIT(self, result: RunResult) -> Emission:
        """Return a content-addressed transition-chain commitment."""
        if result.handle.root != result.emission.child_root:
            raise ValueError("EMIT child handle/root mismatch")
        if result.process.process_id != result.emission.process_id:
            raise ValueError("EMIT process identity mismatch")
        self._event("EMIT", {
            "emission_id": result.emission.emission_id,
            "child_root": result.emission.child_root,
            "receipt_count": len(result.emission.receipt_ids),
        })
        return result.emission

    def FORK(
        self,
        handle: ProcessHandle,
        branch: str,
        *,
        owner: str | None = None,
        max_payload_bytes: int = 10**9,
    ) -> ProcessHandle:
        process, memory = self.RESUME(handle)
        child = fork_process(process, branch)
        proposal = prepare_process(child, memory)
        out = install(
            owner or f"fork:{branch}:{child.process_id}",
            proposal,
            self.archive,
            self.registry,
            max_payload_bytes=max_payload_bytes,
        )
        self._event("FORK", {
            "parent_root": handle.root,
            "child_root": out.root,
            "parent_process": process.process_id,
            "child_process": child.process_id,
            "branch": branch,
        })
        return out

    def PIN(self, handle: ProcessHandle, owner: str, strength: str = "STRONG") -> str:
        ref = self.registry.pin(PROCESS_KIND, owner, handle.root, strength)
        self._event("PIN", {
            "root": handle.root,
            "owner": owner,
            "strength": strength,
            "reference_id": ref.reference_id,
        })
        return ref.reference_id

    def RELEASE(self, reference_id: str, *, collect: bool = False) -> dict[str, Any]:
        released = self.registry.release(reference_id)
        collection = TemporalMerkleGC(self.archive, self.registry).collect() if collect else None
        payload = {
            "reference_id": reference_id,
            "root": released.root,
            "strength": released.strength,
            "collected": 0 if collection is None else collection["collected"],
        }
        self._event("RELEASE", payload)
        return payload

    def YIELD(self, handle: ProcessHandle) -> NeutralYield:
        """Export only carrier-neutral classical process state at a safe point."""
        process, _ = self.RESUME(handle)
        state = process.state
        out = NeutralYield(
            source_process_id=process.process_id,
            source_continuation=process.continuation_id,
            source_carrier=state.carrier,
            passport_id=process.passport_id,
            image=state.image,
            layout=state.layout,
            session=state.session,
            roots=state.roots,
            pc=state.pc,
            steps=state.steps,
            portal=state.portal,
            halted=state.halted,
            base36=process.fibre.base,
            generation=process.generation,
            history_root=process.history_root,
        )
        self._event("YIELD", {
            "source_root": handle.root,
            "yield_id": out.yield_id,
            "base36": out.base36,
            "source_carrier": out.source_carrier,
        })
        return out

    def rehydrate_yield(
        self,
        owner: str,
        yielded: NeutralYield,
        memory: BitStore,
        target_carrier: Carrier,
        *,
        circuit_tag: int,
        pair_tag: int,
        max_payload_bytes: int = 10**9,
    ) -> ProcessHandle:
        """Create a fresh carrier-local process from a neutral safe-point yield."""
        if yielded.safe_point != "SYSCALL_BOUNDARY":
            raise PermissionError("yield is not carrier-neutral")
        program = self.programs.get(yielded.image)
        if program is None:
            raise KeyError("rehydration requires the image to be registered")
        state = State(
            image=yielded.image,
            layout=yielded.layout,
            session=yielded.session,
            carrier=target_carrier.value,
            roots=yielded.roots,
            pc=yielded.pc,
            steps=yielded.steps,
            portal=yielded.portal,
            halted=yielded.halted,
        )
        fibre = FibreProductAddress(yielded.base36, circuit_tag, pair_tag)
        new_process_id = digest({
            "schema": "w33.holovm-rehydrated-process-id.v1",
            "yield_id": yielded.yield_id,
            "source_process": yielded.source_process_id,
            "target_carrier": target_carrier.value,
            "fibre": asdict(fibre),
        })
        history = digest({
            "schema": "w33.holovm-history-event.v1",
            "previous": yielded.history_root,
            "event": "carrier-neutral-rehydrate",
            "yield_id": yielded.yield_id,
            "target_carrier": target_carrier.value,
            "child_process": new_process_id,
        })
        process = ProcessContinuation(
            process_id=new_process_id,
            branch="rehydrated",
            generation=yielded.generation + 1,
            parent=yielded.source_continuation,
            passport_id=yielded.passport_id,
            state=state,
            fibre=fibre,
            history_root=history,
        )
        proposal = prepare_process(process, memory)
        handle = install(
            owner,
            proposal,
            self.archive,
            self.registry,
            max_payload_bytes=max_payload_bytes,
        )
        self._event("REHYDRATE", {
            "yield_id": yielded.yield_id,
            "root": handle.root,
            "process_id": new_process_id,
            "target_carrier": target_carrier.value,
        })
        return handle


def verify() -> dict[str, Any]:
    """Certificate including an end-to-end validated Wasm -> HoloVM execution."""
    from w33_wasm_trace_counter_refinement import control_invocation, trace_program

    wasm_result, wasm_events, wasm_binary = control_invocation()
    program = trace_program(wasm_events, "holovm-wasm-control-trace")
    memory = BitStore()
    state = genesis(
        program,
        memory,
        (0, 0),
        session="holovm-syscall-wasm",
        carrier=Carrier.CIRCUIT_ST81,
    )
    passport = digest({
        "schema": "w33.holovm-syscall-demo-passport.v1",
        "wasm_binary": wasm_binary,
        "program": program.image_id,
    })
    kernel = HoloVMKernel()
    admitted = kernel.ADMIT(
        "wasm",
        program,
        state,
        memory,
        FibreProductAddress(0, 1, 2),
        passport,
    )
    run = kernel.RUN(admitted, fuel=len(wasm_events) + 1, owner="wasm-complete")
    emission = kernel.EMIT(run)
    final, final_memory = kernel.RESUME(run.handle)

    forked = kernel.FORK(run.handle, "audit-branch")
    fork_process_state, _ = kernel.RESUME(forked)
    yield_record = kernel.YIELD(run.handle)
    rehydrated = kernel.rehydrate_yield(
        "cross-carrier",
        yield_record,
        final_memory,
        Carrier.PAIR_ST64,
        circuit_tag=4,
        pair_tag=5,
    )
    rehydrated_process, _ = kernel.RESUME(rehydrated)

    # Add an audit pin, release only that pin, and prove executable authority remains.
    audit_pin = kernel.PIN(run.handle, "audit", "HASH_ONLY")
    kernel.RELEASE(audit_pin, collect=True)
    still_live, _ = kernel.RESUME(run.handle)

    event_digests = tuple(
        digest(event) for event in wasm_events
    )
    joins = tuple(
        {
            "sequence": i + 1,
            "wasm_event_digest": event_digests[i],
            "receipt_id": emission.receipt_ids[i],
        }
        for i in range(len(wasm_events))
    )
    checks = {
        "wasm_source_execution_result_is_28": wasm_result == 28,
        "validated_wasm_trace_reaches_halted_holovm": final.state.halted,
        "one_native_wasm_event_maps_to_one_authenticated_holovm_step": (
            len(wasm_events) >= 1
            and len(emission.receipt_ids) == len(wasm_events) + 1
            and len(joins) == len(wasm_events)
        ),
        "trace_counter_matches_native_event_count": (
            final_memory.decode(final.state.roots[0]) == len(wasm_events)
            and final_memory.decode(final.state.roots[1]) == 0
        ),
        "process_id_stays_stable_across_run": final.process_id == run.process.process_id,
        "fork_allocates_new_process_without_changing_state": (
            fork_process_state.process_id != final.process_id
            and fork_process_state.state == final.state
        ),
        "yield_contains_no_private_fibre_tags": (
            "circuit_tag" not in asdict(yield_record)
            and "pair_tag" not in asdict(yield_record)
        ),
        "cross_carrier_rehydration_is_new_process": (
            rehydrated_process.process_id != final.process_id
            and rehydrated_process.state.carrier == Carrier.PAIR_ST64.value
            and rehydrated_process.fibre.base == final.fibre.base
            and rehydrated_process.state.roots == final.state.roots
        ),
        "hash_only_release_does_not_kill_live_process": still_live == final,
        "kernel_event_log_is_content_addressed": all(
            _is_digest(e["event_id"]) for e in kernel.events
        ),
        "emission_is_content_addressed": _is_digest(emission.emission_id),
    }
    return {
        "schema": ABI_SCHEMA,
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "wasm": {
            "binary_digest": wasm_binary,
            "native_result": wasm_result,
            "native_events": len(wasm_events),
            "holovm_receipts_including_halt": len(emission.receipt_ids),
            "join_digest": digest(joins),
        },
        "abi": ["ADMIT", "RUN", "EMIT", "FORK", "PIN", "RELEASE", "RESUME", "YIELD"],
        "roots": {
            "admitted": admitted.root,
            "completed": run.handle.root,
            "forked": forked.root,
            "rehydrated": rehydrated.root,
            "emission": emission.emission_id,
            "yield": yield_record.yield_id,
        },
        "boundary": (
            "The Wasm path is exact for the repository's validated completed invocation and its invocation-specialised trace program. "
            "It is not a static all-input Wasm compiler. YIELD transfers only classical safe-point state; it does not migrate ST81 quantum state into ST64."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
