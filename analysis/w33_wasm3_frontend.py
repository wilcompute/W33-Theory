#!/usr/bin/env python3
"""Validated WebAssembly 3.0 binary frontend for the W33 virtual machine.

This is a real WebAssembly binary-format slice, not a W33-specific source
language.  It accepts the standard ``\0asm``/version-1 binary envelope used by
WebAssembly Core, decodes a deliberately small i32/control subset, validates
its stack/control discipline, executes it, and only *after validation* lowers
each instruction to a W33-routed Holonet packet slot.

Supported Core instructions:
    block, loop, br, br_if, return, end,
    local.get, local.set,
    i32.const, i32.eqz, i32.add, i32.sub.

Supported module shape:
    one defined function, no parameters, optional i32 locals, one i32 result,
    optional export of that function, no imports/tables/memories/globals.

The subset is intentionally smaller than the complete WebAssembly 3.0 Core
standard.  The theorem here is a frontend/refinement theorem: a genuine Wasm
binary can be decoded, type-validated, executed, and deterministically mapped
onto the W33 packet ABI without assigning any W33 transport metadata to invalid
code.  Unsupported valid WebAssembly constructs are rejected explicitly rather
than silently approximated.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from w33_typed_universal_microvm import GEOMETRY

MAGIC = b"\x00asm"
BINARY_VERSION = b"\x01\x00\x00\x00"
I32 = 0x7F
EMPTY_BLOCK = 0x40
BODY_OPS = ("LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX")

OPNAMES = {
    0x02: "block",
    0x03: "loop",
    0x0B: "end",
    0x0C: "br",
    0x0D: "br_if",
    0x0F: "return",
    0x20: "local.get",
    0x21: "local.set",
    0x41: "i32.const",
    0x45: "i32.eqz",
    0x6A: "i32.add",
    0x6B: "i32.sub",
}


def sha256(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def uleb(n: int) -> bytes:
    if n < 0:
        raise ValueError("uleb requires nonnegative integer")
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def sleb32(n: int) -> bytes:
    out = bytearray()
    more = True
    value = int(n)
    while more:
        b = value & 0x7F
        value >>= 7
        sign = b & 0x40
        more = not ((value == 0 and sign == 0) or (value == -1 and sign != 0))
        out.append(b | (0x80 if more else 0))
    return bytes(out)


class Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def take(self, n: int) -> bytes:
        if n < 0 or self.pos + n > len(self.data):
            raise ValueError("truncated Wasm binary")
        out = self.data[self.pos:self.pos+n]
        self.pos += n
        return out

    def byte(self) -> int:
        return self.take(1)[0]

    def u32(self) -> int:
        result = 0
        shift = 0
        for _ in range(5):
            b = self.byte()
            result |= (b & 0x7F) << shift
            if not (b & 0x80):
                return result
            shift += 7
        raise ValueError("u32 LEB too long")

    def s32(self) -> int:
        result = 0
        shift = 0
        b = 0
        for _ in range(5):
            b = self.byte()
            result |= (b & 0x7F) << shift
            shift += 7
            if not (b & 0x80):
                if shift < 32 and (b & 0x40):
                    result |= -(1 << shift)
                return int(result)
        raise ValueError("s32 LEB too long")

    def name(self) -> str:
        n = self.u32()
        return self.take(n).decode("utf-8")

    def done(self) -> bool:
        return self.pos == len(self.data)


@dataclass(frozen=True)
class WasmInstruction:
    op: str
    imm: int | None = None
    offset: int = 0


@dataclass(frozen=True)
class WasmFunction:
    locals_types: tuple[int, ...]
    instructions: tuple[WasmInstruction, ...]


@dataclass(frozen=True)
class WasmModule:
    result_type: int
    function: WasmFunction
    exports: tuple[tuple[str, int], ...]
    binary_digest: str


def _vec_types(r: Reader) -> tuple[int, ...]:
    return tuple(r.byte() for _ in range(r.u32()))


def _decode_instructions(body: bytes) -> tuple[tuple[int, ...], tuple[WasmInstruction, ...]]:
    r = Reader(body)
    local_groups = r.u32()
    locals_types: list[int] = []
    for _ in range(local_groups):
        count = r.u32()
        ty = r.byte()
        if ty != I32:
            raise ValueError("frontend supports i32 locals only")
        locals_types.extend([ty] * count)

    out: list[WasmInstruction] = []
    depth = 0
    saw_function_end = False
    while not r.done():
        offset = r.pos
        opcode = r.byte()
        if opcode not in OPNAMES:
            raise ValueError(f"unsupported Wasm opcode 0x{opcode:02x}")
        op = OPNAMES[opcode]
        imm: int | None = None
        if op in {"block", "loop"}:
            block_type = r.byte()
            if block_type != EMPTY_BLOCK:
                raise ValueError("frontend supports empty block signatures only")
            imm = block_type
            depth += 1
        elif op in {"br", "br_if", "local.get", "local.set"}:
            imm = r.u32()
        elif op == "i32.const":
            imm = r.s32()
        elif op == "end":
            if depth:
                depth -= 1
            else:
                saw_function_end = True
                out.append(WasmInstruction(op, imm, offset))
                if not r.done():
                    raise ValueError("bytes after function end")
                break
        out.append(WasmInstruction(op, imm, offset))
    if not saw_function_end or depth != 0:
        raise ValueError("unbalanced Wasm control structure")
    return tuple(locals_types), tuple(out)


def decode_module(data: bytes) -> WasmModule:
    r = Reader(data)
    if r.take(4) != MAGIC or r.take(4) != BINARY_VERSION:
        raise ValueError("not a supported WebAssembly core binary")

    func_types: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    function_type_indices: list[int] = []
    exports: list[tuple[str, int]] = []
    bodies: list[bytes] = []
    seen_sections: set[int] = set()

    while not r.done():
        section_id = r.byte()
        size = r.u32()
        payload = Reader(r.take(size))
        if section_id == 0:
            continue
        if section_id in seen_sections:
            raise ValueError("duplicate non-custom section")
        seen_sections.add(section_id)
        if section_id == 1:  # type
            for _ in range(payload.u32()):
                if payload.byte() != 0x60:
                    raise ValueError("only function types are supported")
                params = _vec_types(payload)
                results = _vec_types(payload)
                func_types.append((params, results))
        elif section_id == 3:  # function
            function_type_indices = [payload.u32() for _ in range(payload.u32())]
        elif section_id == 7:  # export
            for _ in range(payload.u32()):
                name = payload.name()
                kind = payload.byte()
                index = payload.u32()
                if kind == 0:
                    exports.append((name, index))
                else:
                    raise ValueError("frontend supports function exports only")
        elif section_id == 10:  # code
            for _ in range(payload.u32()):
                body_size = payload.u32()
                bodies.append(payload.take(body_size))
        else:
            raise ValueError(f"unsupported Wasm section {section_id}")
        if not payload.done():
            raise ValueError(f"section {section_id} has trailing bytes")

    if len(function_type_indices) != 1 or len(bodies) != 1:
        raise ValueError("frontend requires exactly one defined function")
    type_index = function_type_indices[0]
    if type_index >= len(func_types):
        raise ValueError("function type index out of range")
    params, results = func_types[type_index]
    if params != () or results != (I32,):
        raise ValueError("frontend requires () -> i32 function type")
    if any(index != 0 for _, index in exports):
        raise ValueError("exported function index out of range")
    locals_types, instructions = _decode_instructions(bodies[0])
    return WasmModule(I32, WasmFunction(locals_types, instructions), tuple(exports), sha256(data))


@dataclass
class ControlType:
    kind: str
    height: int


def validate(module: WasmModule) -> dict[str, Any]:
    stack: list[int] = []
    control: list[ControlType] = [ControlType("function", 0)]
    unreachable = False
    local_count = len(module.function.locals_types)

    def pop_i32() -> None:
        nonlocal unreachable
        if unreachable and len(stack) == control[-1].height:
            return
        if not stack or stack.pop() != I32:
            raise ValueError("Wasm validation stack type mismatch: expected i32")

    for ins in module.function.instructions:
        op = ins.op
        if op in {"block", "loop"}:
            control.append(ControlType(op, len(stack)))
            unreachable = False
        elif op == "end":
            if len(control) == 1:
                # Function end: an explicit return may have made the path unreachable.
                if not unreachable:
                    if stack != [I32]:
                        raise ValueError("function fallthrough must produce one i32")
                control.pop()
                continue
            frame = control.pop()
            if not unreachable and len(stack) != frame.height:
                raise ValueError("empty-signature block changes stack height")
            del stack[frame.height:]
            unreachable = False
        elif op in {"local.get", "local.set"}:
            if ins.imm is None or not 0 <= ins.imm < local_count:
                raise ValueError("local index out of range")
            if op == "local.get":
                stack.append(I32)
            else:
                pop_i32()
        elif op == "i32.const":
            stack.append(I32)
        elif op == "i32.eqz":
            pop_i32(); stack.append(I32)
        elif op in {"i32.add", "i32.sub"}:
            pop_i32(); pop_i32(); stack.append(I32)
        elif op in {"br", "br_if"}:
            if ins.imm is None or ins.imm >= len(control) - 1:
                raise ValueError("branch depth escapes function or control stack")
            if op == "br_if":
                pop_i32()
            else:
                unreachable = True
                del stack[control[-1].height:]
        elif op == "return":
            pop_i32()
            unreachable = True
            del stack[control[-1].height:]
        else:
            raise ValueError(op)

    if control:
        raise ValueError("function did not close its control frame")
    return {
        "valid": True,
        "locals": local_count,
        "instructions": len(module.function.instructions),
        "result": "i32",
    }


def _matching_ends(instructions: tuple[WasmInstruction, ...]) -> dict[int, int]:
    stack: list[int] = []
    match: dict[int, int] = {}
    for i, ins in enumerate(instructions):
        if ins.op in {"block", "loop"}:
            stack.append(i)
        elif ins.op == "end" and stack:
            start = stack.pop()
            match[start] = i
    if stack:
        raise ValueError("unclosed block")
    return match


def execute(module: WasmModule, fuel: int = 100000) -> int:
    validate(module)
    insns = module.function.instructions
    match = _matching_ends(insns)
    locals_ = [0] * len(module.function.locals_types)
    stack: list[int] = []
    control: list[dict[str, int | str]] = []
    pc = 0

    def i32(x: int) -> int:
        return x & 0xFFFFFFFF

    for _ in range(fuel):
        if not 0 <= pc < len(insns):
            raise RuntimeError("Wasm pc escaped function")
        ins = insns[pc]
        op = ins.op
        if op in {"block", "loop"}:
            control.append({"kind": op, "start": pc + 1, "end": match[pc]})
            pc += 1
        elif op == "end":
            if control and int(control[-1]["end"]) == pc:
                control.pop(); pc += 1
            else:
                if len(stack) != 1:
                    raise RuntimeError("function end result arity mismatch")
                return stack[-1]
        elif op == "local.get":
            stack.append(locals_[int(ins.imm)]); pc += 1
        elif op == "local.set":
            locals_[int(ins.imm)] = stack.pop(); pc += 1
        elif op == "i32.const":
            stack.append(i32(int(ins.imm))); pc += 1
        elif op == "i32.eqz":
            stack.append(1 if stack.pop() == 0 else 0); pc += 1
        elif op == "i32.add":
            b, a = stack.pop(), stack.pop(); stack.append(i32(a + b)); pc += 1
        elif op == "i32.sub":
            b, a = stack.pop(), stack.pop(); stack.append(i32(a - b)); pc += 1
        elif op in {"br", "br_if"}:
            take = True
            if op == "br_if":
                take = stack.pop() != 0
            if not take:
                pc += 1; continue
            depth = int(ins.imm)
            frame = control[-1-depth]
            del control[len(control)-depth:]
            if frame["kind"] == "loop":
                pc = int(frame["start"])
            else:
                control.pop()
                pc = int(frame["end"]) + 1
        elif op == "return":
            if len(stack) != 1:
                raise RuntimeError("return requires one i32 result")
            return stack.pop()
        else:
            raise RuntimeError(op)
    raise RuntimeError("Wasm execution fuel exhausted")


def lower_to_w33(module: WasmModule) -> list[dict[str, Any]]:
    """Validation is a hard precondition: invalid code gets no W33 address."""
    validation = validate(module)
    if not validation["valid"]:
        raise ValueError("module not valid")
    packets: list[dict[str, Any]] = []
    portal = 0
    for index, ins in enumerate(module.function.instructions):
        seed = f"{module.binary_digest}|{index}|{ins.op}|{ins.imm}".encode()
        target = int.from_bytes(hashlib.sha256(seed).digest()[:4], "big") % 40
        route = GEOMETRY.route(portal, target)
        buses = [GEOMETRY.line_by_pair[(a, b)] for a, b in zip(route, route[1:])]
        if len(route) - 1 > 2:
            raise AssertionError("W33 diameter-two refinement violated")
        frame = index // 16
        edge = index % 16
        tick = frame * 72 + edge * 3
        packets.append({
            "wasm_index": index,
            "wasm_offset": ins.offset,
            "op": ins.op,
            "imm": ins.imm,
            "source_portal": portal,
            "target_portal": target,
            "route": list(route),
            "line_buses": buses,
            "microframe": frame,
            "q6_body_edge": edge,
            "body_ticks": [tick, tick + 1, tick + 2],
            "body_ops": list(BODY_OPS),
        })
        portal = target
    return packets


def section(section_id: int, payload: bytes) -> bytes:
    return bytes([section_id]) + uleb(len(payload)) + payload


def vec(items: Iterable[bytes]) -> bytes:
    rows = list(items)
    return uleb(len(rows)) + b"".join(rows)


def sample_module_binary(n: int = 5) -> bytes:
    """Build genuine Wasm binary for sum 1..n using block/loop/br_if/br."""
    type_payload = vec([bytes([0x60, 0x00, 0x01, I32])])
    function_payload = vec([uleb(0)])
    name = b"main"
    export_payload = vec([uleb(len(name)) + name + bytes([0x00]) + uleb(0)])

    code = bytearray()
    code += uleb(1) + uleb(2) + bytes([I32])  # one local group: two i32 locals
    code += bytes([0x41]) + sleb32(n) + bytes([0x21]) + uleb(0)
    code += bytes([0x41]) + sleb32(0) + bytes([0x21]) + uleb(1)
    code += bytes([0x02, EMPTY_BLOCK])
    code += bytes([0x03, EMPTY_BLOCK])
    code += bytes([0x20]) + uleb(0) + bytes([0x45, 0x0D]) + uleb(1)
    code += bytes([0x20]) + uleb(1) + bytes([0x20]) + uleb(0) + bytes([0x6A, 0x21]) + uleb(1)
    code += bytes([0x20]) + uleb(0) + bytes([0x41]) + sleb32(1) + bytes([0x6B, 0x21]) + uleb(0)
    code += bytes([0x0C]) + uleb(0)
    code += bytes([0x0B, 0x0B])
    code += bytes([0x20]) + uleb(1) + bytes([0x0F, 0x0B])
    code_payload = vec([uleb(len(code)) + bytes(code)])
    return MAGIC + BINARY_VERSION + section(1, type_payload) + section(3, function_payload) + section(7, export_payload) + section(10, code_payload)


def verify() -> dict[str, Any]:
    raw = sample_module_binary(5)
    module = decode_module(raw)
    validation = validate(module)
    result = execute(module)
    packets = lower_to_w33(module)

    bad = bytearray(raw)
    # Replace the final local.get with local.set: validation must reject because
    # return then has no i32 operand. Search the final opcode pair robustly.
    needle = bytes([0x20, 0x01, 0x0F, 0x0B])
    at = raw.rfind(needle)
    if at < 0:
        raise AssertionError("sample mutation anchor missing")
    bad[at] = 0x21
    invalid_rejected = False
    invalid_lowering_blocked = False
    try:
        bad_module = decode_module(bytes(bad))
        validate(bad_module)
    except ValueError:
        invalid_rejected = True
    try:
        bad_module = decode_module(bytes(bad))
        lower_to_w33(bad_module)
    except ValueError:
        invalid_lowering_blocked = True

    checks = {
        "binary_magic_and_version": raw[:8] == MAGIC + BINARY_VERSION,
        "validation_passes_before_lowering": validation["valid"] is True,
        "structured_loop_result_is_15": result == 15,
        "export_main_present": ("main", 0) in module.exports,
        "all_instructions_lowered": len(packets) == len(module.function.instructions),
        "all_routes_diameter_two": all(len(row["route"]) - 1 <= 2 for row in packets),
        "all_packets_have_three_phases": all(tuple(row["body_ops"]) == BODY_OPS for row in packets),
        "invalid_program_rejected": invalid_rejected,
        "invalid_program_gets_no_transport": invalid_lowering_blocked,
    }
    return {
        "schema": "w33.wasm3-validated-frontend.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "wasm_profile": "WebAssembly Core 3.0 i32/control subset over the standard binary envelope",
        "module_digest": module.binary_digest,
        "sample_result": result,
        "instruction_count": len(module.function.instructions),
        "microframes": 1 + (len(packets) - 1) // 16,
        "max_w33_hops": max(len(row["route"]) - 1 for row in packets),
        "checks": checks,
        "packets": packets,
        "boundary": (
            "This is not a complete WebAssembly 3.0 implementation. Unsupported valid Core constructs are rejected. "
            "The useful theorem is ordering and refinement: decode -> validate -> execute/lower, with no W33 transport identity assigned to invalid code."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
