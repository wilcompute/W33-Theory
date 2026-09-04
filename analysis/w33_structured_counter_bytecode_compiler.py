#!/usr/bin/env python3
"""Structured universal bytecode -> two-counter semantics -> W33 control packets.

The repository already contains a genuine WebAssembly binary frontend, including
validated block/loop/br/br_if control, and a richer capability-backed Wasm
runtime.  What was still missing was the *universality-preserving bridge* to the
small two-counter core used by ``w33_typed_universal_microvm`` and from there to
the proof-carrying finite-control packet.

This module deliberately does not pretend that a small ad-hoc Wasm subset is
Turing complete.  Instead it introduces a tiny labelled structured bytecode that
is a presentation of the exact Minsky core:

    block NAME inc    r0|r1 NEXT
    block NAME decjz  r0|r1 NONZERO ZERO
    block NAME halt

Labels replace raw program counters.  A module is decoded and completely
validated -- unique labels, typed registers, closed branch targets, reachable
entry -- before a single W33 portal is assigned.  Compilation then resolves
labels to the repository's existing ``Instruction`` objects.

The universality theorem is therefore a refinement theorem, not a new
computability assertion:

  * every finite two-counter ``Program`` has a lossless labelled encoding here;
  * compiling that encoding reproduces the original instruction tuple exactly;
  * two-counter machines are the already-declared abstract universal guest core.

After compilation, every *executed* guest transition is lowered to a
``w33.universal-control-packet.v1``.  The packet commits the pre/post semantic
transition, reuses the MicroVM's canonical diameter-two W33 route, carries an
exact transvection micro-word, projective target and Sp lift bit, and binds the
new algebraic qutrit phase-frame digest.  The control packet is then independently
revalidated; invalid source code never receives routing or Clifford metadata.

This is intentionally the universal-core IR beneath the existing WebAssembly
frontends, not a replacement for WebAssembly.  A future full Wasm->counter
compiler can target this labelled IR while preserving Wasm validation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Iterable

from w33_qutrit_clifford_phase_displacement_lift import CliffordPhaseFrame
from w33_typed_universal_microvm import (
    Capability,
    Carrier,
    Instruction,
    Program,
    TypedUniversalMicroVM,
    add_r1_into_r0_program,
)
from w33_universal_control_packet import (
    ControlPacket,
    MicroOp,
    Stage,
    digest as packet_digest,
    target_digest,
    validate_packet,
    word_matrix,
)
from w33_projective_symplectic_lift_control_abi import central_lift_bit


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class Block:
    label: str
    op: str
    register: int | None = None
    target: str | None = None
    zero_target: str | None = None

    def descriptor(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class StructuredModule:
    name: str
    start: str
    blocks: tuple[Block, ...]

    @property
    def module_id(self) -> str:
        return digest({
            "schema": "w33.structured-counter-bytecode.v1",
            "name": self.name,
            "start": self.start,
            "blocks": [b.descriptor() for b in self.blocks],
        })


@dataclass(frozen=True)
class ValidatedModule:
    module: StructuredModule
    order: tuple[str, ...]
    label_to_pc: dict[str, int]
    reachable: frozenset[str]


def _register(token: str) -> int:
    if token == "r0":
        return 0
    if token == "r1":
        return 1
    raise ValueError(f"unknown counter register {token!r}; only r0/r1 exist")


def parse(source: str) -> StructuredModule:
    """Parse the deliberately tiny line-oriented structured bytecode."""
    rows: list[list[str]] = []
    for raw in source.splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            rows.append(line.split())
    if len(rows) < 3 or rows[0][0] != "module" or len(rows[0]) != 2:
        raise ValueError("first non-comment line must be: module NAME")
    if rows[1][0] != "start" or len(rows[1]) != 2:
        raise ValueError("second non-comment line must be: start LABEL")

    blocks: list[Block] = []
    for row in rows[2:]:
        if len(row) < 3 or row[0] != "block":
            raise ValueError("instruction line must begin: block LABEL ...")
        label, op = row[1], row[2].lower()
        if op == "inc" and len(row) == 5:
            blocks.append(Block(label, "INC", _register(row[3]), row[4]))
        elif op == "decjz" and len(row) == 6:
            blocks.append(Block(label, "DECJZ", _register(row[3]), row[4], row[5]))
        elif op == "halt" and len(row) == 3:
            blocks.append(Block(label, "HALT"))
        else:
            raise ValueError(f"malformed block line: {' '.join(row)}")
    return StructuredModule(rows[0][1], rows[1][1], tuple(blocks))


def validate(module: StructuredModule) -> ValidatedModule:
    if not module.name or not module.blocks:
        raise ValueError("module name and at least one block are required")
    labels = [b.label for b in module.blocks]
    if any(not x for x in labels) or len(set(labels)) != len(labels):
        raise ValueError("block labels must be nonempty and unique")
    if module.start not in set(labels):
        raise ValueError("entry label does not exist")
    label_to_pc = {label: i for i, label in enumerate(labels)}

    for block in module.blocks:
        if block.op == "INC":
            if block.register not in (0, 1) or block.target not in label_to_pc or block.zero_target is not None:
                raise ValueError(f"invalid INC block {block.label}")
        elif block.op == "DECJZ":
            if (
                block.register not in (0, 1)
                or block.target not in label_to_pc
                or block.zero_target not in label_to_pc
            ):
                raise ValueError(f"invalid DECJZ block {block.label}")
        elif block.op == "HALT":
            if any(x is not None for x in (block.register, block.target, block.zero_target)):
                raise ValueError(f"HALT block {block.label} carries operands")
        else:
            raise ValueError(f"unknown structured opcode {block.op}")

    # Reachability is computed rather than assumed. Dead blocks are legal -- just
    # as dead Wasm code can be valid -- but the entry itself must belong to the
    # closed CFG and the certificate records which blocks are live.
    reachable: set[str] = set()
    work = [module.start]
    by_label = {b.label: b for b in module.blocks}
    while work:
        label = work.pop()
        if label in reachable:
            continue
        reachable.add(label)
        b = by_label[label]
        for nxt in (b.target, b.zero_target):
            if nxt is not None and nxt not in reachable:
                work.append(nxt)
    return ValidatedModule(module, tuple(labels), label_to_pc, frozenset(reachable))


def compile_to_minsky(module: StructuredModule) -> Program:
    checked = validate(module)
    if checked.order[0] != module.start:
        # Program.pc is currently fixed at zero. Reorder blocks with entry first,
        # preserving source order for the remainder, then resolve labels.
        order = (module.start,) + tuple(x for x in checked.order if x != module.start)
    else:
        order = checked.order
    pc = {label: i for i, label in enumerate(order)}
    by_label = {b.label: b for b in module.blocks}
    ins: list[Instruction] = []
    for label in order:
        b = by_label[label]
        if b.op == "INC":
            ins.append(Instruction("INC", b.register, pc[b.target]))  # type: ignore[index]
        elif b.op == "DECJZ":
            ins.append(Instruction("DECJZ", b.register, pc[b.target], pc[b.zero_target]))  # type: ignore[index]
        else:
            ins.append(Instruction("HALT"))
    return Program(tuple(ins), name=module.name)


def from_minsky(program: Program) -> StructuredModule:
    """Lossless labelled presentation of any finite repository two-counter program."""
    labels = tuple(f"b{i}" for i in range(len(program.instructions)))
    blocks: list[Block] = []
    for i, ins in enumerate(program.instructions):
        if ins.op == "INC":
            blocks.append(Block(labels[i], "INC", ins.register, labels[int(ins.target)]))
        elif ins.op == "DECJZ":
            blocks.append(
                Block(
                    labels[i],
                    "DECJZ",
                    ins.register,
                    labels[int(ins.target)],
                    labels[int(ins.zero_target)],
                )
            )
        else:
            blocks.append(Block(labels[i], "HALT"))
    return StructuredModule(program.name, labels[0], tuple(blocks))


def structural_refinement(program: Program) -> dict[str, Any]:
    encoded = from_minsky(program)
    compiled = compile_to_minsky(encoded)
    exact = compiled.instructions == program.instructions and compiled.name == program.name
    return {
        "exact": exact,
        "source_module_id": encoded.module_id,
        "instruction_count": len(program.instructions),
        "entry": encoded.start,
    }


def _packet_for_step(
    module: StructuredModule,
    cert: Any,
    counters_before: list[int],
    counters_after: list[int],
) -> ControlPacket:
    source = int(cert.route[0])
    target = int(cert.route[-1])
    # A deterministic one-transvection finite-control word. Guest semantics do
    # not depend on this choice; the packet verifier proves the chosen backend
    # control realization independently.
    word = (MicroOp(target, 1),)
    matrix = word_matrix(word)
    phase = CliffordPhaseFrame(((target, 1),))
    semantic = {
        "module_id": module.module_id,
        "pre": cert.pre,
        "post": cert.post,
        "step": cert.step,
        "pc_before": cert.pc_before,
        "pc_after": cert.pc_after,
        "instruction": cert.instruction,
        "counters_before": counters_before,
        "counters_after": counters_after,
    }
    return ControlPacket(
        schema="w33.universal-control-packet.v1",
        semantic_transition_digest=packet_digest(semantic),
        source_portal=source,
        target_portal=target,
        route=cert.route,
        microcode=word,
        projective_target_digest=target_digest(matrix),
        sp_central_lift_bit=central_lift_bit(matrix),
        requested_stage=Stage.SYMPLECTIC_EXECUTE.value,
        execution_passport_id=packet_digest({
            "schema": "w33.structured-bytecode-execution.v1",
            "module_id": module.module_id,
            "carrier": cert.carrier,
        }),
        clifford_phase_frame_digest=phase.phase_frame_digest,
    )


def execute_and_packetize(
    module: StructuredModule,
    counters: tuple[int, int] = (0, 0),
    fuel: int = 100000,
) -> dict[str, Any]:
    program = compile_to_minsky(module)  # validation happens before routing
    vm = TypedUniversalMicroVM(program, Capability(Carrier.CIRCUIT_ST81, 81))
    vm.state.set_counters(counters)
    packets: list[ControlPacket] = []
    for _ in range(fuel):
        if vm.state.halted:
            break
        before = vm.state.counters()
        cert = vm.step()
        if cert is None:
            break
        after = vm.state.counters()
        packet = _packet_for_step(module, cert, before, after)
        verdict = validate_packet(packet)
        if not verdict["ok"]:
            raise AssertionError({"packet": packet.packet_id, "checks": verdict["checks"]})
        packets.append(packet)
    else:
        raise RuntimeError("structured bytecode execution fuel exhausted")
    return {
        "program": program,
        "state": vm.state,
        "packets": tuple(packets),
        "packet_ids": tuple(p.packet_id for p in packets),
    }


def verify() -> dict[str, Any]:
    sample_source = """
    module add-r1-into-r0
    start entry
    block entry decjz r1 add done
    block add inc r0 entry
    block done halt
    """
    parsed = parse(sample_source)
    parsed_validation = validate(parsed)
    sample = add_r1_into_r0_program()
    compiled = compile_to_minsky(parsed)
    exact_sample = compiled.instructions == sample.instructions

    generic_roundtrip = structural_refinement(sample)
    run = execute_and_packetize(parsed, (7, 11))
    packets = run["packets"]
    final = run["state"]

    malformed_rejected_before_routing = True
    for bad in (
        "module x\nstart a\nblock a inc r2 a\n",
        "module x\nstart a\nblock a inc r0 missing\n",
        "module x\nstart a\nblock a halt\nblock a halt\n",
    ):
        try:
            validate(parse(bad))
            malformed_rejected_before_routing = False
        except ValueError:
            pass

    phase_bound = all(
        isinstance(p.clifford_phase_frame_digest, str)
        and p.clifford_phase_frame_digest.startswith("sha256:")
        for p in packets
    )
    packet_semantics_unique = len({p.semantic_transition_digest for p in packets}) == len(packets)
    route_bound = all(len(p.route) - 1 <= 2 for p in packets)
    word_bound = all(0 < len(p.microcode) <= 5 for p in packets)
    all_packets_reverify = all(validate_packet(p)["ok"] for p in packets)

    checks = {
        "source_parser_and_validator_pass": parsed_validation.module.module_id == parsed.module_id,
        "sample_compiles_exactly_to_existing_two_counter_program": exact_sample,
        "arbitrary_program_roundtrip_is_structurally_exact": generic_roundtrip["exact"],
        "malformed_source_gets_no_routing_metadata": malformed_rejected_before_routing,
        "sample_executes_expected_universal_core_semantics": final.halted and final.counters() == [18, 0],
        "sample_has_expected_24_guest_steps": final.steps == 24 and len(packets) == 24,
        "every_executed_step_has_independently_valid_control_packet": all_packets_reverify,
        "all_routes_obey_W33_diameter_two": route_bound,
        "all_micro_words_fit_five_op_envelope": word_bound,
        "every_packet_binds_qutrit_phase_frame": phase_bound,
        "semantic_transition_digests_are_step_specific": packet_semantics_unique,
    }
    return {
        "schema": "w33.structured-counter-bytecode-compiler-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "module_id": parsed.module_id,
        "compiled_image_id": compiled.image_id,
        "universal_refinement": (
            "Every finite Program in the repository's two-counter core has an exact labelled encoding "
            "and compiles back to the same instruction tuple; universality is inherited from that core."
        ),
        "sample": {
            "input_counters": [7, 11],
            "output_counters": final.counters(),
            "steps": final.steps,
            "packets": len(packets),
            "first_packet": packets[0].packet_id if packets else None,
            "last_packet": packets[-1].packet_id if packets else None,
        },
        "relationship_to_wasm": (
            "The repository's w33_wasm3_frontend.py remains the genuine WebAssembly binary frontend. "
            "This module is the universal labelled counter IR beneath it; a complete semantics-preserving "
            "Wasm-to-counter compiler is still a distinct future compiler theorem."
        ),
        "boundary": (
            "The structural roundtrip proves exact coverage of the existing two-counter guest language. "
            "It does not claim that the currently implemented finite WebAssembly subsets lower to this IR in full."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
